# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 11:11:34 2015

@author: thomas.douenne
"""


from __future__ import division

from pandas import concat

from openfisca_france_indirect_taxation.example.utils_example import simulate_df_calee_by_grosposte, \
    df_weighted_average_grouped, graph_builder_bar


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    var_to_be_simulated = [
        'pondmen',
        'revtot',
        'consommation_ticpe',
        'essence_depenses',
        'diesel_depenses',
        'strate'
        ]

    for element in ['consommation_ticpe', 'diesel_depenses', 'essence_depenses']:
        part_ticpe_revtot_strate = None
        for year in [2005]:
            data_simulation = simulate_df_calee_by_grosposte(var_to_be_simulated = var_to_be_simulated, year = year)
            varlist = [element, 'revtot']
            part_ticpe_revtot_wip = df_weighted_average_grouped(
                dataframe = data_simulation, groupe = 'strate', varlist = varlist
                )
            part_ticpe_revtot_wip['part ' + element.replace('_', ' ') + ' revtot {} par strate'.format(year)] = \
                part_ticpe_revtot_wip[element] / part_ticpe_revtot_wip['revtot']
            data_to_append_revtot = \
                part_ticpe_revtot_wip['part ' + element.replace('_', ' ') + ' revtot {} par strate'.format(year)]

            if part_ticpe_revtot_strate is not None:
                part_ticpe_revtot_strate = concat([part_ticpe_revtot_strate, data_to_append_revtot], axis = 1)
            else:
                part_ticpe_revtot_strate = data_to_append_revtot

        graph_builder_bar(part_ticpe_revtot_strate)
