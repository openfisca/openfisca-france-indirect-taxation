# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 15:20:51 2015

@author: thomas.douenne
"""

from __future__ import division

import pandas as pd
import numpy as np
from pandas import concat

from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame
from openfisca_france_indirect_taxation.aids_price_index_builder import indice_prix_mensuel_98_2015, df2, date_to_vag

# Now that we have our price indexes, we construct a dataframe with the rest of the information

data_frame_for_reg = None
for year in [2005]:
    aggregates_data_frame = get_input_data_frame(year)
    aggregates_data_frame['depenses_tot'] = 0
    produits = [column for column in aggregates_data_frame.columns if column.isdigit()]
    aggregates_data_frame['depenses_tot'] = aggregates_data_frame[produits].sum(axis=1)

    data = aggregates_data_frame[produits + ['vag'] + ['depenses_tot']].copy()

    data.index.name = 'ident_men'
    data.reset_index(inplace = True)
    df = pd.melt(data, id_vars = ['ident_men', 'vag', 'depenses_tot'], value_vars = produits,
        value_name = 'depense_bien', var_name = 'bien')

    df3 = df2[['indice_prix_produit'] + ['prix'] + ['temps'] + ['mois']]

    df['vag'] = df['vag'].astype(str)
    df['indice_prix_produit'] = df['vag'] + '_' + df['bien']
    df['indice_prix_produit'] = df['indice_prix_produit'].str.replace('_0', '')
    df['indice_prix_produit'] = df['indice_prix_produit'].str.replace('_', '')
    df['coicop_12_numero'] = df['bien'].str[:2]

# categ_1: alimentation (coicop_1)
# categ_2: tabac et alcool (coicop_2)
# categ_3: habillement et ameublement (coicop_3 et 5)
# categ_4: logement (coicop_4)
# categ_5: sante et education (coicop_6 et 10)
# categ_6: transports (coicop_7)
# categ_7: loisirs (coicop_9)
# categ_8: restauration et hotellerie (coicop_11)
# categ_9: communication et divers (coicop_8 et 12)

    df['coicop_12_numero'] = df['coicop_12_numero'].astype(float)
    df['numero_categ'] = df['coicop_12_numero']
    df['numero_categ'] = df['numero_categ'].replace(5, 3)
    df['numero_categ'] = df['numero_categ'].replace(6, 5)
    df['numero_categ'] = df['numero_categ'].replace(10, 5)
    df['numero_categ'] = df['numero_categ'].replace(7, 6)
    df['numero_categ'] = df['numero_categ'].replace(9, 7)
    df['numero_categ'] = df['numero_categ'].replace(8, 9)
    df['numero_categ'] = df['numero_categ'].replace(11, 8)
    df['numero_categ'] = df['numero_categ'].replace(12, 9)

    df = df[['ident_men'] + ['numero_categ'] + ['indice_prix_produit'] + ['depense_bien'] + ['vag']]

    df = pd.merge(df, df3, on = 'indice_prix_produit')
    df_temps = df[['vag'] + ['temps'] + ['mois']]
    df_temps['mois'] = df_temps['mois'].astype(float)
    df_temps['mois2'] = df_temps['mois'] ** 2
    df_temps['temps2'] = df_temps['temps'] ** 2
    df_temps = df_temps.drop_duplicates(cols='vag', take_last=True)
    df_temps = df_temps.astype(float)

    # Construct the price index by category:

    df['numero_categ'] = df['numero_categ'].astype(int)  # Goal : transform 1.0 into 1 to merge with same id.
    df = df.astype(str)
    df['id'] = df['numero_categ'] + '_' + df['ident_men']

    df_depense_categ = None
    for i in range(1, 13):
        if df_depense_categ is not None:
            df_depense_categ = concat([df_depense_categ, aggregates_data_frame['coicop12_{}'.format(i)]], axis = 1)
        else:
            df_depense_categ = aggregates_data_frame['coicop12_{}'.format(i)]
    df_depense_categ['categ_1'] = df_depense_categ['coicop12_1'].copy()
    df_depense_categ['categ_2'] = df_depense_categ['coicop12_2'].copy()
    df_depense_categ['categ_3'] = df_depense_categ['coicop12_3'] + df_depense_categ['coicop12_5']
    df_depense_categ['categ_4'] = df_depense_categ['coicop12_4'].copy()
    df_depense_categ['categ_5'] = df_depense_categ['coicop12_6'] + df_depense_categ['coicop12_10']
    df_depense_categ['categ_6'] = df_depense_categ['coicop12_7'].copy()
    df_depense_categ['categ_7'] = df_depense_categ['coicop12_9'].copy()
    df_depense_categ['categ_8'] = df_depense_categ['coicop12_11'].copy()
    df_depense_categ['categ_9'] = df_depense_categ['coicop12_8'] + df_depense_categ['coicop12_12']
    for i in range(1, 13):
        df_depense_categ = df_depense_categ.drop(['coicop12_{}'.format(i)], axis = 1)

    list_categ = [column for column in df_depense_categ.columns]
    df_depense_categ.index.name = 'ident_men'
    df_depense_categ.reset_index(inplace = True)
    df_depense_categ = pd.melt(df_depense_categ, id_vars = ['ident_men'], value_vars = list_categ)
    df_depense_categ.rename(columns = {'value': 'depense_par_categ'}, inplace = True)
    df_depense_categ.rename(columns = {'variable': 'numero_categ'}, inplace = True)
    df_depense_categ['numero_categ'] = df_depense_categ['numero_categ'].str.split('categ_').str[1]

    df_depense_categ = df_depense_categ.astype(str)
    df_depense_categ['id'] = df_depense_categ['numero_categ'] + '_' + df_depense_categ['ident_men']
    df_to_merge = df_depense_categ[['id'] + ['depense_par_categ']]

    df = pd.merge(df, df_to_merge, on = 'id')

    df[['prix'] + ['depense_bien'] + ['depense_par_categ']] = (
        df[['prix'] + ['depense_bien'] + ['depense_par_categ']].astype(float)
        )

    df['part_bien_categ'] = df['depense_bien'] / df['depense_par_categ']
    df.fillna(0, inplace=True)
    df['indice_prix_pondere'] = df['part_bien_categ'] * df['prix']

    df.sort(['id'])
    grouped = df['indice_prix_pondere'].groupby(df['id'])
    grouped = grouped.aggregate(np.sum)
    grouped.index.name = 'id'
    grouped = grouped.reset_index()
    # Import information about households

    df_info_menage = aggregates_data_frame[['ocde10'] + ['depenses_tot'] + ['vag'] + ['typmen'] + ['revtot'] +
        ['02201'] + ['02202'] + ['02203']]
    df_info_menage['fumeur'] = 0
    df_info_menage[['02201'] + ['02202'] + ['02203']] = df_info_menage[['02201'] + ['02202'] + ['02203']].astype(float)
    df_info_menage['consommation_tabac'] = df_info_menage['02201'] + df_info_menage['02202'] + df_info_menage['02203']
    df_info_menage['fumeur'] = 1 * (df_info_menage['consommation_tabac'] > 0)
    df_info_menage.drop(['consommation_tabac', '02201', '02202', '02203'], inplace = True, axis = 1)
    df_info_menage.index.name = 'ident_men'
    df_info_menage.reset_index(inplace = True)
    df_info_menage['ident_men'] = df_info_menage['ident_men'].astype(str)

    data_frame = pd.merge(df_depense_categ, df_info_menage, on = 'ident_men')

    data_frame = pd.merge(data_frame, grouped, on = 'id')
    data_frame[['depenses_tot'] + ['depense_par_categ']] = (
        data_frame[['depenses_tot'] + ['depense_par_categ']].astype(float)
        )
    data_frame['wi'] = data_frame['depense_par_categ'] / data_frame['depenses_tot']
    data_frame[['vag'] + ['numero_categ']] = data_frame[['vag'] + ['numero_categ']].astype(str)

    # By construction, those who don't consume in coicop_i have a price index of 0 for this coicop.
    # We replace it with the price index of the whole coicop at the same vag.

    df_prix_categ = indice_prix_mensuel_98_2015[['_1000'] + ['_2000'] + ['_3000'] + ['_4000'] + ['_5000'] + ['_6000'] +
        ['_7000'] + ['_8000'] + ['_9000'] + ['_10000'] + ['_11000'] + ['_12000'] + ['temps'] + ['date']]
    df_prix_categ
    df_prix_categ['vag'] = df_prix_categ['date'].map(date_to_vag)
    df_prix_categ.dropna(inplace = True)
    del df_prix_categ['date']
    df_prix_categ = df_prix_categ.astype(float)
    df_prix_categ['1'] = df_prix_categ['_1000']
    df_prix_categ['2'] = df_prix_categ['_2000']
    df_prix_categ['3'] = (df_prix_categ['_3000'] + df_prix_categ['_5000']) / 2
    df_prix_categ['4'] = df_prix_categ['_4000']
    df_prix_categ['5'] = (df_prix_categ['_6000'] + df_prix_categ['_10000']) / 2
    df_prix_categ['6'] = df_prix_categ['_7000']
    df_prix_categ['7'] = df_prix_categ['_9000']
    df_prix_categ['8'] = df_prix_categ['_11000']
    df_prix_categ['9'] = (df_prix_categ['_8000'] + df_prix_categ['_12000']) / 2
    df_prix_categ = df_prix_categ[['1'] + ['2'] + ['3'] + ['4'] + ['5'] + ['6'] + ['7'] + ['8'] + ['9'] + ['vag']]
    df_prix_categ = pd.melt(df_prix_categ, id_vars = ['vag'], value_name = 'prix_categ')
    df_prix_categ['vag'] = df_prix_categ['vag'].astype(int)
    df_prix_categ['vag'] = df_prix_categ['vag'].astype(str)
    df_prix_categ['indice_prix_produit'] = df_prix_categ['vag'] + '_' + df_prix_categ['variable']
    df_prix_categ = df_prix_categ[['indice_prix_produit'] + ['prix_categ']]
    df_prix_categ = df_prix_categ.drop_duplicates(cols = 'indice_prix_produit', take_last = True)

    data_frame['indice_prix_produit'] = data_frame['vag'] + '_' + data_frame['numero_categ']

    data_frame = pd.merge(data_frame, df_prix_categ, on = 'indice_prix_produit')

    data_frame['indice_prix_pondere'] = data_frame['indice_prix_pondere'].astype(float)
    data_frame.loc[data_frame['indice_prix_pondere'] == 0, 'indice_prix_pondere'] = \
        data_frame.loc[data_frame['indice_prix_pondere'] == 0, 'prix_categ']
    data_frame = data_frame.drop(['prix_categ', 'indice_prix_produit'], axis = 1)

    # Reshape the dataframe to have the price index of each coicop as a variable

    data_frame_prix = data_frame[['numero_categ'] + ['ident_men'] + ['indice_prix_pondere']]
    data_frame_prix.index.name = 'ident_men'
    data_frame_prix = pd.pivot_table(data_frame_prix, index='ident_men', columns='numero_categ',
        values='indice_prix_pondere')
    data_frame_prix.reset_index(inplace = True)
    data_frame = pd.merge(data_frame, data_frame_prix, on = 'ident_men')
    for i in range(1, 10):
        data_frame.rename(columns = {'{}'.format(i): 'p{}'.format(i)}, inplace = True)

    del data_frame['id']
    data_frame = data_frame.astype(float)

    data_frame['depenses_reelles'] = data_frame['depenses_tot'] / data_frame['ocde10']

    data_frame = pd.merge(data_frame, df_temps, on = 'vag')

    data_frame['decile'] = pd.qcut(data_frame['depenses_reelles'], 10, labels = False)
    data_frame['decile'] += 1

    # Pivot the table to get one row per person.

    data_frame['numero_categ'] = data_frame['numero_categ'].astype(int)
    data_frame2 = pd.pivot_table(data_frame, index = 'ident_men', columns = 'numero_categ',
        values = 'wi')
    for i in range(1, 10):
        data_frame2.rename(columns = {'{}'.format(i): 'w{}'.format(i)}, inplace = True)
    data_frame2.index.name = 'ident_men'
    data_frame2 = data_frame2.reset_index()
    data_frame = pd.merge(data_frame, data_frame2, on = 'ident_men')
    data_frame = data_frame.drop_duplicates(cols = 'ident_men', take_last = True)
    data_frame.drop(['depense_par_categ', 'depenses_tot', 'indice_prix_pondere', 'wi'], inplace = True, axis = 1)

    if data_frame_for_reg is not None:
        data_frame_for_reg = pd.concat([data_frame_for_reg, data_frame])
    else:
        data_frame_for_reg = data_frame

data_frame_for_reg.to_csv('data_frame_for_r.csv', sep = ',')
