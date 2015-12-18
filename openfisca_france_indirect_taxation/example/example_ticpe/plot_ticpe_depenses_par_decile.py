# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 10:37:09 2015

@author: thomas.douenne
"""

from __future__ import division

from pandas import concat

from openfisca_france_indirect_taxation.example.utils_example import simulate_df_calee_by_grosposte, \
    df_weighted_average_grouped, graph_builder_line, save_dataframe_to_graph


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    simulated_variables = [
        'pondmen',
        'decuc',
        'niveau_vie_decile',
        'ticpe_totale',
        'diesel_ticpe',
        'essence_ticpe',
        'consommation_ticpe',
        'diesel_depenses',
        'essence_depenses'
        ]

    depenses_ticpe_carburants = None
    depenses_ticpe_diesel = None
    depenses_ticpe_essence = None
    depenses_carburants = None
    depenses_diesel = None
    depenses_essence = None

    for year in [2000, 2005, 2011]:
        data_simulation = simulate_df_calee_by_grosposte(simulated_variables = simulated_variables, year = year)
        if year == 2011:
            data_simulation.niveau_vie_decile[data_simulation.decuc == 10] = 10
        varlist = ['ticpe_totale', 'diesel_ticpe', 'essence_ticpe', 'consommation_ticpe', 'diesel_depenses',
                   'essence_depenses']
        depenses = df_weighted_average_grouped(dataframe = data_simulation, groupe = 'niveau_vie_decile',
            varlist = varlist)
        depenses.rename(columns = {'ticpe_totale': 'ticpe totale {}'.format(year),
            'diesel_ticpe': 'ticpe diesel {}'.format(year),
            'essence_ticpe': 'ticpe essence {}'.format(year),
            'consommation_ticpe': 'depenses carburants {}'.format(year),
            'diesel_depenses': 'depenses diesel {}'.format(year),
            'essence_depenses': 'depenses essence {}'.format(year)},
            inplace = True)

        # Contributions à la TICPE
        if depenses_ticpe_carburants is not None:
            depenses_ticpe_carburants = concat(
                [depenses_ticpe_carburants, depenses['ticpe totale {}'.format(year)]], axis = 1)
        else:
            depenses_ticpe_carburants = depenses['ticpe totale {}'.format(year)]

        if depenses_ticpe_diesel is not None:
            depenses_ticpe_diesel = concat(
                [depenses_ticpe_diesel, depenses['ticpe diesel {}'.format(year)]], axis = 1)
        else:
            depenses_ticpe_diesel = depenses['ticpe diesel {}'.format(year)]

        if depenses_ticpe_essence is not None:
            depenses_ticpe_essence = concat(
                [depenses_ticpe_essence, depenses['ticpe essence {}'.format(year)]], axis = 1)
        else:
            depenses_ticpe_essence = depenses['ticpe essence {}'.format(year)]

        # Dépenses en carburants
        if depenses_carburants is not None:
            depenses_carburants = concat(
                [depenses_carburants, depenses['depenses carburants {}'.format(year)]], axis = 1)
        else:
            depenses_carburants = depenses['depenses carburants {}'.format(year)]

        if depenses_diesel is not None:
            depenses_diesel = concat(
                [depenses_diesel, depenses['depenses diesel {}'.format(year)]], axis = 1)
        else:
            depenses_diesel = depenses['depenses diesel {}'.format(year)]

        if depenses_essence is not None:
            depenses_essence = concat(
                [depenses_essence, depenses['depenses essence {}'.format(year)]], axis = 1)
        else:
            depenses_essence = depenses['depenses essence {}'.format(year)]

    graph_builder_line(depenses_ticpe_carburants)
    graph_builder_line(depenses_ticpe_diesel)
    graph_builder_line(depenses_ticpe_essence)

    graph_builder_line(depenses_carburants)
    graph_builder_line(depenses_diesel)
    graph_builder_line(depenses_essence)

    save_dataframe_to_graph(depenses_carburants, 'depenses_carburants_par_decile.csv')
    save_dataframe_to_graph(depenses_diesel, 'depenses_diesel_par_decile.csv')
    save_dataframe_to_graph(depenses_essence, 'depenses_essence_par_decile.csv')
