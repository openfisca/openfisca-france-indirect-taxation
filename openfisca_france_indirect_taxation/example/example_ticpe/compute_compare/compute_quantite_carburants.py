# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 14:32:30 2015

@author: thomas.douenne
"""

# Import de modules généraux
from __future__ import division

import numpy as np
import csv
import pkg_resources
import os

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.example.utils_example import simulate_df_calee_on_ticpe
from openfisca_france_indirect_taxation.example.dataframes_from_legislation.get_accises import \
    get_accise_ticpe_majoree


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Liste des variables que l'on veut simuler
    simulated_variables_with_e10 = [
        'pondmen',
        'sp_e10_ticpe',
        'sp95_ticpe',
        'sp98_ticpe',
        'super_plombe_ticpe',
        'diesel_ticpe'
        ]

    simulated_variables_without_e10 = [
        'pondmen',
        'sp95_ticpe',
        'sp98_ticpe',
        'super_plombe_ticpe',
        'diesel_ticpe'
        ]

    # Calcul des montants agrégés des quantités de carburants consommées par les ménages, dont essence et diesel
    quantites_carburants_consommees = dict()
    quantites_diesel_consommees = dict()
    quantites_essence_consommees = dict()
    for year in [2000, 2005, 2011]:
        try:
            data_simulation = \
                simulate_df_calee_on_ticpe(simulated_variables = simulated_variables_with_e10, year = year)
            diesel_ticpe_ponderee = (data_simulation['diesel_ticpe'] * data_simulation['pondmen']).sum()
            sp95_ticpe_ponderee = (data_simulation['sp95_ticpe'] * data_simulation['pondmen']).sum()
            sp98_ticpe_ponderee = (data_simulation['sp98_ticpe'] * data_simulation['pondmen']).sum()
            super_plombe_ticpe_ponderee = (data_simulation['super_plombe_ticpe'] * data_simulation['pondmen']).sum()
            sp_e10_ticpe_ponderee = (data_simulation['sp_e10_ticpe'] * data_simulation['pondmen']).sum()
        except:
            data_simulation = \
                simulate_df_calee_on_ticpe(simulated_variables = simulated_variables_without_e10, year = year)
            diesel_ticpe_ponderee = (data_simulation['diesel_ticpe'] * data_simulation['pondmen']).sum()
            sp95_ticpe_ponderee = (data_simulation['sp95_ticpe'] * data_simulation['pondmen']).sum()
            sp98_ticpe_ponderee = (data_simulation['sp98_ticpe'] * data_simulation['pondmen']).sum()
            super_plombe_ticpe_ponderee = (data_simulation['super_plombe_ticpe'] * data_simulation['pondmen']).sum()
            sp_e10_ticpe_ponderee = 0

        liste_carburants_accise = get_accise_ticpe_majoree()
        value_accise_diesel = liste_carburants_accise['accise majoree diesel'].loc[u'{}'.format(year)] / 100
        value_accise_sp = liste_carburants_accise['accise majoree sans plomb'].loc[u'{}'.format(year)] / 100
        value_accise_super_plombe = \
            liste_carburants_accise['accise majoree super plombe'].loc[u'{}'.format(year)] / 100

        quantite_diesel = diesel_ticpe_ponderee / (value_accise_diesel)
        quantite_sans_plomb = (sp95_ticpe_ponderee + sp98_ticpe_ponderee + sp_e10_ticpe_ponderee) / (value_accise_sp)
        quantite_super_plombe = super_plombe_ticpe_ponderee / (value_accise_super_plombe)

        if quantite_super_plombe == np.nan:
            quantite_essence = quantite_sans_plomb + quantite_super_plombe
        else:
            quantite_essence = quantite_sans_plomb

        quantite_carburants = quantite_diesel + quantite_essence
        quantites_carburants_consommees['en milliers de m3 en {}'.format(year)] = quantite_carburants / 1000000
        quantites_diesel_consommees['en milliers de m3 en {}'.format(year)] = quantite_diesel / 1000000
        quantites_essence_consommees['en milliers de m3 en {}'.format(year)] = quantite_essence / 1000000

    # Enregistrement des montants agrégées dans des fichiers csv
    assets_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
        )

    writer_carburants = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'quantites', 'quantites_carburants_consommees_bdf.csv'), 'wb'))
    for key, value in quantites_carburants_consommees.items():
        writer_carburants.writerow([key, value])

    writer_diesel = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'quantites', 'quantites_diesel_consommees_bdf.csv'), 'wb'))
    for key, value in quantites_diesel_consommees.items():
        writer_diesel.writerow([key, value])

    writer_essence = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'quantites', 'quantites_essence_consommees_bdf.csv'), 'wb'))
    for key, value in quantites_essence_consommees.items():
        writer_essence.writerow([key, value])
