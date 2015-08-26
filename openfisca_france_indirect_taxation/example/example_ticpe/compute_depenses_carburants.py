# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 18:33:36 2015

@author: thomas.douenne
"""

from __future__ import division
import csv
import pkg_resources
import os

from openfisca_france_indirect_taxation.example.utils_example import simulate_df_calee_on_ticpe


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Liste des variables que l'on veut simuler
    var_to_be_simulated = [
        'pondmen',
        'diesel_depenses',
        'essence_depenses',
        'coicop12_7'
        ]

    depenses_transports_totales = dict()
    depenses_carburants_totales = dict()
    depenses_diesel_totales = dict()
    depenses_essence_totales = dict()
    for year in [2000, 2005, 2011]:
        data_simulation = simulate_df_calee_on_ticpe(var_to_be_simulated = var_to_be_simulated, year = year)
        depenses_diesel = (data_simulation['diesel_depenses'] * data_simulation['pondmen']).sum()
        depenses_essence = (data_simulation['essence_depenses'] * data_simulation['pondmen']).sum()
        depenses_carburants = depenses_diesel + depenses_essence
        depenses_transports = (data_simulation['coicop12_7'] * data_simulation['pondmen']).sum()

        depenses_transports_totales['en {}'.format(year)] = depenses_transports / 1000000
        depenses_carburants_totales['en {}'.format(year)] = depenses_carburants / 1000000
        depenses_diesel_totales['en {}'.format(year)] = depenses_diesel / 1000000
        depenses_essence_totales['en {}'.format(year)] = depenses_essence / 1000000

    assets_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
        )

    writer_transports = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'depenses_transports_totales_bdf.csv'), 'wb'))
    for key, value in depenses_transports_totales.items():
        writer_transports.writerow([key, value])

    writer_carburants = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'depenses_carburants_totales_bdf.csv'), 'wb'))
    for key, value in depenses_carburants_totales.items():
        writer_carburants.writerow([key, value])

    writer_diesel = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'depenses_diesel_totales_bdf.csv'), 'wb'))
    for key, value in depenses_diesel_totales.items():
        writer_diesel.writerow([key, value])

    writer_essence = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'depenses_essence_totales_bdf.csv'), 'wb'))
    for key, value in depenses_essence_totales.items():
        writer_essence.writerow([key, value])
