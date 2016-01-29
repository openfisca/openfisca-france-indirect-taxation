# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:41:21 2015

@author: thomas.douenne
"""

# L'objectif est d'exprimer pour chaque décile de revenu la part que représente les dépenses en TICPE sur l'ensemble
# du revenu. Ce revenu prend trois définitions : le revenu total, le revenu disponible, ou l'ensemble des dépenses du
# ménage. Ces calculs sont réalisés pour 2000, 2005 et 2011, et les parts spécifiques à l'essence et au diesel sont
# spécifiées.

# Import de modules généraux
from __future__ import division

from pandas import concat

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import simulate_df_calee_by_grosposte, \
    df_weighted_average_grouped, graph_builder_line_percent, save_dataframe_to_graph


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    simulated_variables = [
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

    # Formation des bases de données, dépenses moyennes en TICPE par décile de revenu, que l'on divise ensuite par le
    # revenu. Calcul effectué pour 2000, 2005 et 2011 pour l'ensemble des carburants, puis chacun séparément
    for element in ['ticpe_totale', 'diesel_ticpe', 'essence_ticpe']:
        part_ticpe_revtot = None
        part_ticpe_rev_disp_loyerimput = None
        part_ticpe_depenses_totales = None
        for year in [2000, 2005, 2011]:
            data_simulation = simulate_df_calee_by_grosposte(simulated_variables = simulated_variables, year = year)
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

            # Aggrégation des trois années pour chaque type de calcul
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

        # Réalisation des gréphiques
        graph_builder_line_percent(part_ticpe_revtot, 1, 0.35)
        graph_builder_line_percent(part_ticpe_rev_disp_loyerimput, 1, 0.35)
        graph_builder_line_percent(part_ticpe_depenses_totales, 1, 0.35)

        # Enregistrement des dataframe en fichiers csv
        save_dataframe_to_graph(
            part_ticpe_rev_disp_loyerimput, 'part_{}_sur_rev_disployerimput.csv'.format(element))
