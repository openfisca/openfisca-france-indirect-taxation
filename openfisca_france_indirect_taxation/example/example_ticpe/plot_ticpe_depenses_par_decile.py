# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 10:37:09 2015

@author: thomas.douenne
"""

from __future__ import division

from pandas import concat

from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, \
    graph_builder_line


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    var_to_be_simulated = [
        'pondmen',
        'decuc',
        'niveau_vie_decile',
        'ticpe_totale',
        'diesel_ticpe',
        'essence_ticpe'
        ]

    depenses_ticpe_totale = None
    depenses_ticpe_diesel = None
    depenses_ticpe_essence = None
    for year in [2000, 2005, 2011]:
        data_simulation = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        if year == 2011:
            data_simulation.niveau_vie_decile[data_simulation.decuc == 10] = 10
        varlist = ['ticpe_totale', 'diesel_ticpe', 'essence_ticpe']
        depenses_ticpe = df_weighted_average_grouped(dataframe = data_simulation, groupe = 'niveau_vie_decile',
            varlist = varlist)
        depenses_ticpe.rename(columns = {'ticpe_totale': 'ticpe totale {}'.format(year),
            'diesel_ticpe': 'ticpe diesel {}'.format(year),
            'essence_ticpe': 'ticpe essence {}'.format(year)},
            inplace = True)

        if depenses_ticpe_totale is not None:
            depenses_ticpe_totale = concat(
                [depenses_ticpe_totale, depenses_ticpe['ticpe totale {}'.format(year)]], axis = 1)
        else:
            depenses_ticpe_totale = depenses_ticpe['ticpe totale {}'.format(year)]
        if depenses_ticpe_diesel is not None:
            depenses_ticpe_diesel = concat(
                [depenses_ticpe_diesel, depenses_ticpe['ticpe diesel {}'.format(year)]], axis = 1)
        else:
            depenses_ticpe_diesel = depenses_ticpe['ticpe diesel {}'.format(year)]
        if depenses_ticpe_essence is not None:
            depenses_ticpe_essence = concat(
                [depenses_ticpe_essence, depenses_ticpe['ticpe essence {}'.format(year)]], axis = 1)
        else:
            depenses_ticpe_essence = depenses_ticpe['ticpe essence {}'.format(year)]

    graph_builder_line(depenses_ticpe_totale)
    graph_builder_line(depenses_ticpe_diesel)
    graph_builder_line(depenses_ticpe_essence)
