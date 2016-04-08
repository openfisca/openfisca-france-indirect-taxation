# -*- coding: utf-8 -*-

from __future__ import division

import pandas as pd
import numpy as np
from pandas import concat

from openfisca_france_indirect_taxation.utils import get_input_data_frame
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_price_index_builder import \
    df_indice_prix_produit


# Now that we have our price indexes, we construct a dataframe with the rest of the information

data_frame_for_reg = None
for year in [2000, 2005, 2011]:
    aggregates_data_frame = get_input_data_frame(2011)
    aggregates_data_frame['depenses_tot'] = 0
    for i in range(1, 13):
        aggregates_data_frame['depenses_tot'] += aggregates_data_frame['coicop12_{}'.format(i)]

    produits = [column for column in aggregates_data_frame.columns if column.isdigit()]

    data = aggregates_data_frame[produits + ['vag']].copy()

    data.index.name = 'ident_men'
    data.reset_index(inplace = True)
    df = pd.melt(data, id_vars = ['vag', 'ident_men'], value_vars=produits,
        value_name = 'depense_bien', var_name = 'bien')

    df_indice_prix_produit = df_indice_prix_produit[['indice_prix_produit'] + ['prix'] + ['temps'] + ['mois']]

    df['vag'] = df['vag'].astype(str)
    df['indice_prix_produit'] = df['vag'] + '_' + df['bien']
    df['indice_prix_produit'] = df['indice_prix_produit'].str.replace('_0', '')
    df['indice_prix_produit'] = df['indice_prix_produit'].str.replace('_', '')
    df['coicop_12_numero'] = df['bien'].str[:2]
    df = df[['ident_men'] + ['coicop_12_numero'] + ['indice_prix_produit'] + ['depense_bien'] + ['vag']]

    df = pd.merge(df, df_indice_prix_produit, on = 'indice_prix_produit')
    df_temps = df[['vag'] + ['temps'] + ['mois']]
    df_temps['mois'] = df_temps['mois'].astype(float)
    df_temps['mois2'] = df_temps['mois'] ** 2
    df_temps = df_temps.drop_duplicates(cols='vag', take_last=True)
    df_temps = df_temps.astype(float)

    # Construct the price index by coicop:

    df['coicop_12_numero'] = df['coicop_12_numero'].astype(int)  # Goal : transform 1.0 into 1 to merge with same id.
    df = df.astype(str)
    df['id'] = df['coicop_12_numero'] + '_' + df['ident_men']

    df_depense_coicop = None
    for i in range(1, 13):
        if df_depense_coicop is not None:
            df_depense_coicop = concat([df_depense_coicop, aggregates_data_frame['coicop12_{}'.format(i)]], axis = 1)
        else:
            df_depense_coicop = aggregates_data_frame['coicop12_{}'.format(i)]

    list_coicop12 = [column for column in df_depense_coicop.columns]
    df_depense_coicop.index.name = 'ident_men'
    df_depense_coicop.reset_index(inplace = True)
    df_depense_coicop = pd.melt(df_depense_coicop, id_vars = ['ident_men'], value_vars = list_coicop12)
    df_depense_coicop.rename(columns = {'value': 'depense_par_coicop'}, inplace = True)
    df_depense_coicop.rename(columns = {'variable': 'numero_coicop'}, inplace = True)
    df_depense_coicop['numero_coicop'] = df_depense_coicop['numero_coicop'].str.split('coicop12_').str[1]

    df_depense_coicop = df_depense_coicop.astype(str)
    df_depense_coicop['id'] = df_depense_coicop['numero_coicop'] + '_' + df_depense_coicop['ident_men']
    df_to_merge = df_depense_coicop[['id'] + ['depense_par_coicop']]

    df = pd.merge(df, df_to_merge, on = 'id')

    df[['prix'] + ['depense_bien'] + ['depense_par_coicop']] = (
        df[['prix'] + ['depense_bien'] + ['depense_par_coicop']].astype(float)
        )

    df['part_bien_coicop'] = df['depense_bien'] / df['depense_par_coicop']
    df.fillna(0, inplace=True)
    df['indice_prix_pondere'] = df['part_bien_coicop'] * df['prix']

    df.sort(['id'])
    grouped = df['indice_prix_pondere'].groupby(df['id'])
    grouped = grouped.aggregate(np.sum)
    grouped.index.name = 'id'
    grouped = grouped.reset_index()

    # Import information about households, including niveau_vie_decile
    # (To do: Obviously there are mistakes in its computation, check why).

    df_info_menage = aggregates_data_frame[['ocde10'] + ['depenses_tot'] + ['vag'] + ['typmen'] + ['revtot'] +
        ['poste_coicop_2201'] + ['poste_coicop_2202'] + ['poste_coicop_2203']]
    df_info_menage['fumeur'] = 0
    df_info_menage[['poste_coicop_2201'] + ['poste_coicop_2202'] + ['poste_coicop_2203']] = \
        df_info_menage[['poste_coicop_2201'] + ['poste_coicop_2202'] + ['poste_coicop_2203']].astype(float)
    df_info_menage['consommation_tabac'] = (
        df_info_menage['poste_coicop_2201'] + df_info_menage['poste_coicop_2202'] + df_info_menage['poste_coicop_2203']
        )
    df_info_menage['fumeur'] = 1 * (df_info_menage['consommation_tabac'] > 0)
    df_info_menage.drop(['consommation_tabac', 'poste_coicop_2201', 'poste_coicop_2202', 'poste_coicop_2203'],
        inplace = True, axis = 1)
    df_info_menage.index.name = 'ident_men'
    df_info_menage.reset_index(inplace = True)
    df_info_menage['ident_men'] = df_info_menage['ident_men'].astype(str)

    data_frame = pd.merge(df_depense_coicop, df_info_menage, on = 'ident_men')

    data_frame = pd.merge(data_frame, grouped, on = 'id')
    data_frame[['depenses_tot'] + ['depense_par_coicop']] = (
        data_frame[['depenses_tot'] + ['depense_par_coicop']].astype(float)
        )
    data_frame['wi'] = data_frame['depense_par_coicop'] / data_frame['depenses_tot']
    data_frame = data_frame.astype(str)

    # By construction, those who don't consume in coicop_i have a price index of 0 for this coicop.
    # We replace it with the price index of the whole coicop at the same vag.

    data_frame['indice_prix_produit'] = data_frame['vag'] + data_frame['numero_coicop'] + '000'

    df_indice_prix_produit['prix'] = df_indice_prix_produit['prix'].astype(float)
    df_indice_prix_produit['prix_coicop'] = df_indice_prix_produit['prix']
    df_indice_prix_produit_to_merge = df_indice_prix_produit[['indice_prix_produit'] + ['prix_coicop']]

    data_frame = pd.merge(data_frame, df_indice_prix_produit_to_merge, on = 'indice_prix_produit')

    data_frame['indice_prix_pondere'] = data_frame['indice_prix_pondere'].astype(float)
    data_frame.loc[data_frame['indice_prix_pondere'] == 0, 'indice_prix_pondere'] = \
        data_frame.loc[data_frame['indice_prix_pondere'] == 0, 'prix_coicop']
    data_frame = data_frame.drop(['prix_coicop', 'indice_prix_produit'], axis = 1)

    # Reshape the dataframe to have the price index of each coicop as a variable

    data_frame_prix = data_frame[['numero_coicop'] + ['ident_men'] + ['indice_prix_pondere']]
    data_frame_prix.index.name = 'ident_men'
    data_frame_prix = pd.pivot_table(data_frame_prix, index='ident_men', columns='numero_coicop',
        values='indice_prix_pondere')
    data_frame_prix.reset_index(inplace = True)
    data_frame = pd.merge(data_frame, data_frame_prix, on = 'ident_men')
    for i in range(1, 13):
        data_frame.rename(columns = {'{}'.format(i): 'p{}'.format(i)}, inplace = True)

    del data_frame['id']
    data_frame = data_frame.astype(float)

    data_frame['depenses_par_uc'] = data_frame['depenses_tot'] / data_frame['ocde10']

    data_frame = pd.merge(data_frame, df_temps, on = 'vag')

    data_frame['numero_coicop'] = data_frame['numero_coicop'].astype(int)
    data_frame['numero_coicop'] = data_frame['numero_coicop'].astype(str)
    data_frame2 = pd.pivot_table(data_frame, index = 'ident_men', columns = 'numero_coicop',
        values = 'wi')
    for i in range(1, 13):
        data_frame2.rename(columns = {'{}'.format(i): 'w{}'.format(i)}, inplace = True)
    data_frame2.index.name = 'ident_men'
    data_frame2 = data_frame2.reset_index()
    data_frame = pd.merge(data_frame, data_frame2, on = 'ident_men')
    data_frame = data_frame.drop_duplicates(cols = 'ident_men', take_last = True)
    data_frame.drop(
        ['depense_par_coicop', 'depenses_tot', 'indice_prix_pondere', 'wi', 'numero_coicop'],
        inplace = True, axis = 1
        )

    data_frame.to_csv('data_frame_r_{}_by_coicop.csv'.format(year), sep = ',')

    if data_frame_for_reg is not None:
        data_frame_for_reg = pd.concat([data_frame_for_reg, data_frame])
    else:
        data_frame_for_reg = data_frame

data_frame_for_reg.to_csv('data_frame_for_stata_by_coicop.csv', sep = ',')
data_frame_for_reg['somme_wi'] = 0
for i in range(1, 13):
    data_frame_for_reg['somme_wi'] += data_frame_for_reg['w{}'.format(i)]
assert (data_frame_for_reg['somme_wi'] == 1).any(), 'The expenditure shares do not sum to 1'
