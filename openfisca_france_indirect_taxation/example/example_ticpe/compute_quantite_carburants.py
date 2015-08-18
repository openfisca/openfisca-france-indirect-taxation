# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 14:32:30 2015

@author: thomas.douenne
"""

from __future__ import division

import numpy as np

from openfisca_france_indirect_taxation.example.utils_example import simulate_df
from openfisca_france_indirect_taxation.model.get_dataframe_from_legislation.get_accises import \
    get_accise_ticpe_majoree


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Liste des variables que l'on veut simuler
    var_to_be_simulated_with_e10 = [
        'pondmen',
        'revtot',
        'somme_coicop12_conso',
        'rev_disp_loyerimput',
        'ticpe_totale',
        'sp_e10_ticpe',
        'sp95_ticpe',
        'sp98_ticpe',
        'super_plombe_ticpe',
        'diesel_ticpe',
        'paysnai'
        ]

    var_to_be_simulated_without_e10 = [
        'pondmen',
        'revtot',
        'somme_coicop12_conso',
        'rev_disp_loyerimput',
        'ticpe_totale',
        'sp95_ticpe',
        'sp98_ticpe',
        'super_plombe_ticpe',
        'diesel_ticpe',
        'paysnai'
        ]

    quantites_carburants_consommees = dict()
    for year in [2000, 2005, 2011]:
        try:
            data_simulation = simulate_df(var_to_be_simulated = var_to_be_simulated_with_e10, year = year)
            data_simulation['diesel_ticpe_ponderee'] = data_simulation['diesel_ticpe'] * data_simulation['pondmen']
            data_simulation['sp95_ticpe_ponderee'] = data_simulation['sp95_ticpe'] * data_simulation['pondmen']
            data_simulation['sp98_ticpe_ponderee'] = data_simulation['sp98_ticpe'] * data_simulation['pondmen']
            data_simulation['sp_e10_ticpe_ponderee'] = data_simulation['sp_e10_ticpe'] * data_simulation['pondmen']
            data_simulation['super_plombe_ticpe_ponderee'] = \
                data_simulation['super_plombe_ticpe'] * data_simulation['pondmen']
        except:
            data_simulation = simulate_df(var_to_be_simulated = var_to_be_simulated_without_e10, year = year)
            data_simulation['diesel_ticpe_ponderee'] = data_simulation['diesel_ticpe'] * data_simulation['pondmen']
            data_simulation['sp95_ticpe_ponderee'] = data_simulation['sp95_ticpe'] * data_simulation['pondmen']
            data_simulation['sp98_ticpe_ponderee'] = data_simulation['sp98_ticpe'] * data_simulation['pondmen']
            data_simulation['sp_e10_ticpe_ponderee'] = 0
            data_simulation['super_plombe_ticpe_ponderee'] = \
                data_simulation['super_plombe_ticpe'] * data_simulation['pondmen']

        liste_carburants_accise = get_accise_ticpe_majoree()
        value_accise_diesel = liste_carburants_accise['accise majoree diesel'].loc[u'{}'.format(year)] / 100
        value_accise_sp = liste_carburants_accise['accise majoree sans plomb'].loc[u'{}'.format(year)] / 100
        value_accise_super_plombe = \
            liste_carburants_accise['accise majoree super plombe'].loc[u'{}'.format(year)] / 100

        quantite_diesel = data_simulation['diesel_ticpe_ponderee'].sum() / (value_accise_diesel)
        quantite_sans_plomb = (
            data_simulation['sp95_ticpe_ponderee'].sum() + data_simulation['sp98_ticpe_ponderee'].sum() +
            data_simulation['sp_e10_ticpe_ponderee'].sum()) / (value_accise_sp)
        quantite_super_plombe = data_simulation['super_plombe_ticpe_ponderee'].sum() / (value_accise_super_plombe)

        if quantite_super_plombe == np.nan:
            quantite_essence = quantite_sans_plomb + quantite_super_plombe
        else:
            quantite_essence = quantite_sans_plomb

        quantite_carburants = quantite_diesel + quantite_essence
        quantites_carburants_consommees['en milliers de m3 en {}'.format(year)] = quantite_carburants / 1000000
