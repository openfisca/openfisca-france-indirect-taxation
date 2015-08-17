# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 12:27:47 2015

@author: thomas.douenne
"""

from __future__ import division

from openfisca_france_indirect_taxation.model.base import tax_from_expense_including_tax, taux_implicite
from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame
from ipp_macro_series_parser.agregats_transports.transports_cleaner import *
from ipp_macro_series_parser.agregats_transports.parser_cleaner_prix_carburants import prix_carburants_90_14


# Quotient: how much more diesel car owners consume compare to super car owners.
# pourcentage_parc_i: g2_1
# pourcentage_conso_i: g_3a

for year in [2011]:
    aggregates_data_frame = get_input_data_frame(year)

    g2_1.columns = g2_1.columns.astype(str)
    g_3a.columns = g_3a.columns.astype(str)

    conso_totale_vp_diesel = g_3a.at[12, '{}'.format(year)]
    conso_totale_vp_super = g_3a.at[2, '{}'.format(year)]
    taille_parc_diesel = g2_1.at[2, '{}'.format(year)]
    taille_parc_super = g2_1.at[1, '{}'.format(year)]

    conso_moyenne_vp_diesel = conso_totale_vp_diesel / taille_parc_diesel
    conso_moyenne_vp_super = conso_totale_vp_super / taille_parc_super

    data = aggregates_data_frame[['ident_men'] + ['pondmen'] + ['07220'] + ['vag'] + ['veh_diesel'] +
        ['veh_essence'] + ['veh_tot']]
    data = data.astype(float)
    data.rename(columns = {'07220': 'depenses_carburants'}, inplace = True)

    data['part_conso_diesel'] = (data['veh_diesel'] * conso_moyenne_vp_diesel) / \
        ((data['veh_essence'] * conso_moyenne_vp_super) + (data['veh_diesel'] * conso_moyenne_vp_diesel))
    data['part_conso_super'] = (data['veh_essence'] * conso_moyenne_vp_super) / \
        ((data['veh_essence'] * conso_moyenne_vp_super) + (data['veh_diesel'] * conso_moyenne_vp_diesel))

    data['diesel_depenses'] = data['depenses_carburants'] * data['part_conso_diesel']
    data['depenses_super'] = data['depenses_carburants'] * data['part_conso_super']

    # Some checks :

    data['check_depenses_carbu'] = (data['diesel_depenses'] + data['depenses_super']) - data['depenses_carburants']
    assert data['check_depenses_carbu'].max() < 0.0001, 'The sum of diesel and super is higher than the total'
    assert data['check_depenses_carbu'].min() > -0.0001, 'The sum of diesel and super is lower than the total'
    del data['check_depenses_carbu']

    small_data = data[data['veh_tot'] > 0]
    small_data = small_data[small_data['veh_essence'] == 0]
    small_data = small_data[small_data['veh_diesel'] == 0]
    print small_data.shape
    del small_data

    prix_carburants = prix_carburants_90_14[prix_carburants_90_14.index == year]
    prix_diesel_ttc = prix_carburants[prix_carburants['carburant'] == 'diesel_ttc']
    prix_diesel_ttc = prix_diesel_ttc.iat[0, 1]
    prix_super_95_ttc = prix_carburants[prix_carburants['carburant'] == 'super_95_ttc']
    prix_super_95_ttc = prix_super_95_ttc.iat[0, 1]
    prix_super_98_ttc = prix_carburants[prix_carburants['carburant'] == 'super_98_ttc']
    prix_super_98_ttc = prix_super_98_ttc.iat[0, 1]
    prix_super_95_e10_ttc = prix_carburants[prix_carburants['carburant'] == 'super_95_e10_ttc']
    prix_super_95_e10_ttc = prix_super_95_e10_ttc.iat[0, 1]
    prix_super_plombe_ttc = prix_carburants[prix_carburants['carburant'] == 'super_plombe_ttc']
    prix_super_plombe_ttc = prix_super_plombe_ttc.iat[0, 1]
    prix_gplc_ttc = prix_carburants[prix_carburants['carburant'] == 'gplc_ttc']
    prix_gplc_ttc = prix_gplc_ttc.iat[0, 1]

    taux_implicite_diesel_ticpe = taux_implicite(0.4284, 0.196, prix_diesel_ttc)
    taux_implicite_ticpe_super = taux_implicite(0.6069, 0.196, prix_super_95_ttc)

    data['depenses_diesel_ticpe'] = tax_from_expense_including_tax(data['diesel_depenses'], taux_implicite_diesel_ticpe)
    data['depenses_ticpe_super'] = tax_from_expense_including_tax(data['depenses_super'], taux_implicite_ticpe_super)
    data['depenses_ticpe'] = data['depenses_diesel_ticpe'] + data['depenses_ticpe_super']
    data['part_ticpe_depenses'] = data['depenses_ticpe'] / data['depenses_carburants']

    data['quantite_diesel'] = data['diesel_depenses'] / prix_diesel_ttc
    data['quantite_super'] = data['depenses_super'] / prix_super_95_ttc
    data['quantite_carburants'] = data['quantite_diesel'] + data['quantite_super']
    data['quantite_carburants_inflate'] = data['quantite_carburants'] * data['pondmen']
    print data['quantite_carburants_inflate'].sum()

    # NB: il faut aussi pondérer selon la consommation de 95, 98, d'E85 et d'E10.
    # NB: l'accise est la même pour 95, 98 et E10, beaucoup plus basse pour E85, mais < 1% de la conso de super.

    data['depenses_ticpe_inflate'] = data['depenses_ticpe'] * data['pondmen']
    print data['depenses_ticpe_inflate'].sum()
    data['depenses_carburants_inflate'] = data['depenses_carburants'] * data['pondmen']
    print data['depenses_carburants_inflate'].sum()

    data['check'] = 0
    data.loc[data['depenses_ticpe'] > 0, 'check'] = 1
    print data['check'].mean()
