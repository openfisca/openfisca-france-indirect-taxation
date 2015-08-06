# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:16:54 2015

@author: thomas.douenne
"""

from __future__ import division

import pandas as pd

from openfisca_france_indirect_taxation.model.base import tax_from_expense_including_tax, taux_implicite
from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame
from ipp_macro_series_parser.agregats_transports.transports_cleaner import g2_1, g_3a
from ipp_macro_series_parser.agregats_transports.parser_cleaner_prix_carburants import prix_mensuel_carburants_90_15
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_price_index_builder import date_to_vag

# Match prices with vag :

prix_mensuel_carburants_90_15[['annee'] + ['mois']] = prix_mensuel_carburants_90_15[['annee'] + ['mois']].astype(str)
prix_mensuel_carburants_90_15['date'] = \
    prix_mensuel_carburants_90_15['annee'] + '_' + prix_mensuel_carburants_90_15['mois']

prix_mensuel_carburants_90_15['vag'] = prix_mensuel_carburants_90_15['date'].map(date_to_vag)
del prix_mensuel_carburants_90_15['date']

# pourcentage_parc_i: g2_1
# pourcentage_conso_i: g_3a

for year in [2000]:
    aggregates_data_frame = get_input_data_frame(year)

    # Get scalar values from aggregates:

    g2_1.columns = g2_1.columns.astype(str)
    g_3a.columns = g_3a.columns.astype(str)

    conso_totale_vp_diesel = g_3a.at[12, '{}'.format(year)]
    conso_totale_vp_super = g_3a.at[2, '{}'.format(year)]
    taille_parc_diesel = g2_1.at[2, '{}'.format(year)]
    taille_parc_super = g2_1.at[1, '{}'.format(year)]

    conso_moyenne_vp_diesel = conso_totale_vp_diesel / taille_parc_diesel
    conso_moyenne_vp_super = conso_totale_vp_super / taille_parc_super

    # Get the dataframe:

    data = aggregates_data_frame[['ident_men'] + ['pondmen'] + ['07220'] + ['vag'] + ['veh_diesel'] +
        ['veh_essence'] + ['veh_tot']]
    data = data.astype(float)
    data.rename(columns = {'07220': 'depenses_carburants'}, inplace = True)

    data['part_conso_diesel'] = (data['veh_diesel'] * conso_moyenne_vp_diesel) / \
        ((data['veh_essence'] * conso_moyenne_vp_super) + (data['veh_diesel'] * conso_moyenne_vp_diesel))
    data['part_conso_super'] = (data['veh_essence'] * conso_moyenne_vp_super) / \
        ((data['veh_essence'] * conso_moyenne_vp_super) + (data['veh_diesel'] * conso_moyenne_vp_diesel))

    data['depenses_diesel'] = data['depenses_carburants'] * data['part_conso_diesel']
    data['depenses_super'] = data['depenses_carburants'] * data['part_conso_super']

    # For those for whom the type of the car is not filled: use the average consumption at the agregate level:

    data['depenses_diesel'].fillna(0, inplace = True)
    data['depenses_super'].fillna(0, inplace = True)
    data['diff'] = data['depenses_carburants'] - (data['depenses_diesel'] + data['depenses_super'])
    data.loc[data['diff'] > 1, 'depenses_diesel'] = \
        data['depenses_carburants'] * (conso_totale_vp_diesel / (conso_totale_vp_diesel + conso_totale_vp_super))
    data.loc[data['diff'] > 1, 'depenses_super'] = \
        data['depenses_carburants'] * (conso_totale_vp_super / (conso_totale_vp_diesel + conso_totale_vp_super))
    del data['diff']

    # Match expenses with prices to compute quantities:

    prix_mensuel_carburants_90_15_small = prix_mensuel_carburants_90_15[['vag'] + ['diesel_ttc'] + ['super_95_ttc']]
    prix_mensuel_carburants_90_15_small = \
        prix_mensuel_carburants_90_15_small[prix_mensuel_carburants_90_15_small['vag'] > 0]
    prix_mensuel_carburants_90_15_small = \
        prix_mensuel_carburants_90_15_small.drop_duplicates(cols = 'vag', take_last = True)
    data = pd.merge(data, prix_mensuel_carburants_90_15_small, on = 'vag')

    # Compute quantities and expenses in ticpe:

    data['taux_implicite_ticpe_diesel'] = taux_implicite(0.4284, 0.196, data['diesel_ttc'])
    data['taux_implicite_ticpe_super'] = taux_implicite(0.6069, 0.196, data['super_95_ttc'])

    data['depenses_ticpe_diesel'] = tax_from_expense_including_tax(data['depenses_diesel'],
        data['taux_implicite_ticpe_diesel'])
    data['depenses_ticpe_super'] = tax_from_expense_including_tax(data['depenses_super'],
        data['taux_implicite_ticpe_super'])
    data['depenses_ticpe'] = data['depenses_ticpe_diesel'] + data['depenses_ticpe_super']

    data['quantite_diesel'] = data['depenses_diesel'] / data['diesel_ttc']
    data['quantite_super'] = data['depenses_super'] / data['super_95_ttc']
    data['quantite_carburants'] = data['quantite_diesel'] + data['quantite_super']

    # Asserts:

    data['check_depenses_carbu'] = (data['depenses_diesel'] + data['depenses_super']) - data['depenses_carburants']
    assert data['check_depenses_carbu'].max() < 0.0001, 'The sum of diesel and super is higher than the total'
    assert data['check_depenses_carbu'].min() > -0.0001, 'The sum of diesel and super is lower than the total'
    del data['check_depenses_carbu']

    small_df = data[data['depenses_carburants'] > 0]
    small_df['quantite_carburants'] = small_df['quantite_carburants'].fillna(0)
    small_df = small_df[small_df['quantite_carburants'] == 0]
    assert len(small_df) == 0, 'Some people consume fuel but are missing in quantite_carburants_inflate'
    del small_df

    # Summarize the results:

    agregats = dict()
    agregats['quantite_carburants_totale'] = (data['quantite_carburants'] * data['pondmen']).sum()
    agregats['quantite_diesel_totale'] = (data['quantite_diesel'] * data['pondmen']).sum()
    agregats['quantite_super_totale'] = (data['quantite_super'] * data['pondmen']).sum()
    agregats['depenses_carburants_totale'] = (data['depenses_carburants'] * data['pondmen']).sum()
    agregats['depenses_diesel_totale'] = (data['depenses_diesel'] * data['pondmen']).sum()
    agregats['depenses_super_totale'] = (data['depenses_super'] * data['pondmen']).sum()
    agregats['depenses_ticpe_totale'] = (data['depenses_ticpe'] * data['pondmen']).sum()
    agregats['depenses_ticpe_diesel'] = (data['depenses_ticpe_diesel'] * data['pondmen']).sum()
    agregats['depenses_ticpe_super'] = (data['depenses_ticpe_super'] * data['pondmen']).sum()

    # NB: il faut aussi pondérer selon la consommation de 95, 98, d'E85, d'E10 et de super plombe (important en 2000).
    # NB: l'accise est la même pour 95, 98 et E10, beaucoup plus basse pour E85, mais < 1% de la conso de super.
