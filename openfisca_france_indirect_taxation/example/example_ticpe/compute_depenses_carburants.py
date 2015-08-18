# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 18:33:36 2015

@author: thomas.douenne
"""

from __future__ import division

from openfisca_france_indirect_taxation.example.utils_example import simulate_df


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Liste des variables que l'on veut simuler
    var_to_be_simulated = [
        'pondmen',
        'diesel_depenses',
        'essence_depenses'
        ]

    depenses_carburants_totales = dict()
    depenses_diesel_totales = dict()
    depenses_essence_totales = dict()
    for year in [2000, 2005, 2011]:
        data_simulation = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        data_simulation['depenses diesel ponderees'] = \
            data_simulation['diesel_depenses'] * data_simulation['pondmen']
        data_simulation['depenses essence ponderees'] = \
            data_simulation['essence_depenses'] * data_simulation['pondmen']
        depenses_diesel = data_simulation['depenses diesel ponderees'].sum()
        depenses_essence = data_simulation['depenses essence ponderees'].sum()
        depenses_carburants = depenses_diesel + depenses_essence

        depenses_carburants_totales['en {}'.format(year)] = depenses_carburants / 1000000
        depenses_diesel_totales['en {}'.format(year)] = depenses_diesel / 1000000
        depenses_essence_totales['en {}'.format(year)] = depenses_essence / 1000000
