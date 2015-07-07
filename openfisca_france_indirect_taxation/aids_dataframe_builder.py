# -*- coding: utf-8 -*-
"""
Created on Wed Jul 01 17:25:21 2015

@author: thomas.douenne
"""

from __future__ import division

import pandas as pd
import numpy as np
from pandas import concat

from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame, simulate_df
from openfisca_france_indirect_taxation.aids_price_index_builder import indice_prix_mensuel_98_2015, df2


# Now that we have our price indexes, we construct a dataframe with the rest of the information

data_frame_for_reg = None
for year in [2011]:
    aggregates_data_frame = get_input_data_frame(year)
    aggregates_data_frame['depenses_tot'] = 0
    for i in range(1, 13):
        aggregates_data_frame['depenses_tot'] += aggregates_data_frame['coicop12_{}'.format(i)]

    produits = [column for column in aggregates_data_frame.columns if column.isdigit()]

    data = aggregates_data_frame[produits + ['vag']].copy()

    data.index.name = 'ident_men'
    data.reset_index(inplace = True)
    df = pd.melt(data, id_vars = ['vag', 'ident_men'], value_vars=produits,
        value_name = 'depense_bien', var_name = 'bien')

    df2 = df2[['indice_prix_produit'] + ['prix'] + ['temps'] + ['mois']]

    df['vag'] = df['vag'].astype(str)
    df['indice_prix_produit'] = df['vag'] + '_' + df['bien']
    df['indice_prix_produit'] = df['indice_prix_produit'].str.replace('_0', '')
    df['indice_prix_produit'] = df['indice_prix_produit'].str.replace('_', '')
    df['coicop_12_numero'] = df['bien'].str[:2]
    df = df[['ident_men'] + ['coicop_12_numero'] + ['indice_prix_produit'] + ['depense_bien'] + ['vag']]

    df = pd.merge(df, df2, on = 'indice_prix_produit')
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
    df['ln_prix'] = np.log(df['prix'])
    del df['prix']

    df['part_bien_coicop'] = df['depense_bien'] / df['depense_par_coicop']
    df.fillna(0, inplace=True)
    df['indice_prix_pondere'] = df['part_bien_coicop'] * df['ln_prix']

    df.sort(['id'])
    grouped = df['indice_prix_pondere'].groupby(df['id'])
    grouped = grouped.aggregate(np.sum)
    grouped.index.name = 'id'
    grouped = grouped.reset_index()

    # Import information about households, including niveau_vie_decile
    # (To do: Obviously there are mistakes in its computation, check why).

    var_to_be_simulated = ['niveau_vie_decile']
    simulation_data_frame = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
    simulation_data_frame.index.name = 'ident_men'
    simulation_data_frame.reset_index(inplace = True)
    simulation_data_frame['ident_men'] = simulation_data_frame['ident_men'].astype(str)

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
    df_info_menage = pd.merge(df_info_menage, simulation_data_frame, on = 'ident_men')

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

    df2['prix'] = df2['prix'].astype(float)
    df2['ln_prix_coicop'] = np.log(df2['prix'])
    df3 = df2[['indice_prix_produit'] + ['ln_prix_coicop']]

    data_frame = pd.merge(data_frame, df3, on = 'indice_prix_produit')

    data_frame['indice_prix_pondere'] = data_frame['indice_prix_pondere'].astype(float)
    data_frame['ln_prix_coicop'] = data_frame['ln_prix_coicop'].astype(float)
    data_frame.loc[data_frame['indice_prix_pondere'] == 0, 'indice_prix_pondere'] = \
        data_frame.loc[data_frame['indice_prix_pondere'] == 0, 'ln_prix_coicop']
    data_frame = data_frame.drop(['ln_prix_coicop', 'indice_prix_produit'], axis = 1)

    # Reshape the dataframe to have the price index of each coicop as a variable

    data_frame_prix = data_frame[['numero_coicop'] + ['ident_men'] + ['indice_prix_pondere']]
    data_frame_prix.index.name = 'ident_men'
    data_frame_prix = pd.pivot_table(data_frame_prix, index='ident_men', columns='numero_coicop',
        values='indice_prix_pondere')
    data_frame_prix.reset_index(inplace = True)
    data_frame = pd.merge(data_frame, data_frame_prix, on = 'ident_men')
    for i in range(1, 13):
        data_frame.rename(columns = {'{}'.format(i): 'ln_p{}'.format(i)}, inplace = True)

    # Construct a linear approximation of the global price index ln_P (hence LA-AIDS) :

    df_indice_prix_global = data_frame[['ident_men'] + ['wi'] + ['indice_prix_pondere']]
    df_indice_prix_global = df_indice_prix_global.astype(float)
    df_indice_prix_global['ln_P'] = \
        df_indice_prix_global['wi'] * df_indice_prix_global['indice_prix_pondere']
    df_indice_prix_global = df_indice_prix_global['ln_P'].groupby(df_indice_prix_global['ident_men'])
    df_indice_prix_global = df_indice_prix_global.aggregate(np.sum)
    df_indice_prix_global.index.name = 'ident_men'
    df_indice_prix_global = df_indice_prix_global.reset_index()
    del data_frame['id']
    data_frame = data_frame.astype(float)

    data_frame = pd.merge(data_frame, df_indice_prix_global, on = 'ident_men')
    data_frame['depenses_reelles'] = data_frame['depenses_tot'] / data_frame['ocde10']
    data_frame['ln_depenses_reelles'] = np.log(data_frame['depenses_reelles'])
    del data_frame['depenses_reelles']
    data_frame['ln_depenses_reelles'] = data_frame['ln_depenses_reelles'] - data_frame['ln_P']

    data_frame = pd.merge(data_frame, df_temps, on = 'vag')

    if data_frame_for_reg is not None:
        data_frame_for_reg = pd.concat([data_frame_for_reg, data_frame])
    else:
        data_frame_for_reg = data_frame
