# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:41:21 2015

@author: thomas.douenne
"""

from __future__ import division

from pandas import concat

from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, \
    graph_builder_line_percent


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    var_to_be_simulated = [
        'pondmen',
        'decuc',
        'niveau_vie_decile',
        'revtot',
        'somme_coicop12_conso',
        'rev_disp_loyerimput',
        'ticpe_totale',
        'diesel_ticpe',
        'essence_ticpe'
        ]

    for element in ['ticpe_totale', 'diesel_ticpe', 'essence_ticpe']:
        part_ticpe_revtot = None
        part_ticpe_rev_disp_loyerimput = None
        part_ticpe_depenses_totales = None
        for year in [2000, 2005, 2011]:
            data_simulation = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
            if year == 2011:
                data_simulation.niveau_vie_decile[data_simulation.decuc == 10] = 10
            varlist = [element, 'revtot', 'somme_coicop12_conso', 'rev_disp_loyerimput']
            part_ticpe_revtot_wip = df_weighted_average_grouped(
                dataframe = data_simulation, groupe = 'niveau_vie_decile', varlist = varlist
                )
            part_ticpe_revtot_wip['part ' + element.replace('_', ' ') + ' revtot {}'.format(year)] = \
                part_ticpe_revtot_wip[element] / part_ticpe_revtot_wip['revtot']
            data_to_append_revtot = \
                part_ticpe_revtot_wip['part ' + element.replace('_', ' ') + ' revtot {}'.format(year)]

            part_ticpe_rev_loyerimput_wip = df_weighted_average_grouped(
                dataframe = data_simulation, groupe = 'niveau_vie_decile', varlist = varlist
                )
            part_ticpe_rev_loyerimput_wip[
                'part ' + element.replace('_', ' ') + ' rev disp loyerimput {}'.format(year)] = (
                part_ticpe_rev_loyerimput_wip[element] /
                part_ticpe_rev_loyerimput_wip['rev_disp_loyerimput']
                )
            data_to_append_rev_loyerimput = \
                part_ticpe_rev_loyerimput_wip[
                    'part ' + element.replace('_', ' ') + ' rev disp loyerimput {}'.format(year)]

            part_ticpe_depenses_totales_wip = df_weighted_average_grouped(
                dataframe = data_simulation, groupe = 'niveau_vie_decile', varlist = varlist
                )
            part_ticpe_depenses_totales_wip['part ' + element.replace('_', ' ') + ' depenses {}'.format(year)] = (
                part_ticpe_depenses_totales_wip[element] /
                part_ticpe_depenses_totales_wip['somme_coicop12_conso']
                )
            data_to_append_depenses_totales = \
                part_ticpe_depenses_totales_wip['part ' + element.replace('_', ' ') + ' depenses {}'.format(year)]

            if part_ticpe_revtot is not None:
                part_ticpe_revtot = concat([part_ticpe_revtot, data_to_append_revtot], axis = 1)
            else:
                part_ticpe_revtot = data_to_append_revtot

            if part_ticpe_rev_disp_loyerimput is not None:
                part_ticpe_rev_disp_loyerimput = \
                    concat([part_ticpe_rev_disp_loyerimput, data_to_append_rev_loyerimput], axis = 1)
            else:
                part_ticpe_rev_disp_loyerimput = data_to_append_rev_loyerimput

            if part_ticpe_depenses_totales is not None:
                part_ticpe_depenses_totales = \
                    concat([part_ticpe_depenses_totales, data_to_append_depenses_totales], axis = 1)
            else:
                part_ticpe_depenses_totales = data_to_append_depenses_totales

        graph_builder_line_percent(part_ticpe_revtot)
        graph_builder_line_percent(part_ticpe_rev_disp_loyerimput)
        graph_builder_line_percent(part_ticpe_depenses_totales)
