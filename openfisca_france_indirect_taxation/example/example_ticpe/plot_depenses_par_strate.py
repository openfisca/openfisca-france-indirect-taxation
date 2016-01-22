# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 11:11:34 2015

@author: thomas.douenne
"""

# L'objectif est de calculer, pour chaque zone de résidence "strate", les dépenses moyennes en carburants.
# L'analyse peut être affinée afin de comparer les dépenses en diesel et en essence.
# On constate que pour les deux carburants les ménages ruraux consomment davantage que les urbains.

# Import de modules généraux
from __future__ import division

from pandas import concat

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.example.utils_example import simulate_df_calee_by_grosposte, \
    df_weighted_average_grouped, graph_builder_bar, save_dataframe_to_graph


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    simulated_variables = [
        'pondmen',
        'revtot',
        'consommation_ticpe',
        'essence_depenses',
        'diesel_depenses',
        'strate'
        ]

    # Calcul des dépenses moyennes en carburants des ménages selon leur zone de résidence
    depenses_par_residence = None
    for element in ['consommation_ticpe', 'diesel_depenses', 'essence_depenses']:
        part_ticpe_revtot_strate = None
        for year in [2005]:
            data_simulation = simulate_df_calee_by_grosposte(simulated_variables = simulated_variables, year = year)
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

        # Réalisation de graphiques représentant les dépenses moyennes en carburants par zone de résidence des ménages
        graph_builder_bar(part_ticpe_revtot_strate)

        # Sauvegarde de la dataframe en fichier csv
        if depenses_par_residence is not None:
            depenses_par_residence = concat([depenses_par_residence, part_ticpe_revtot_strate], axis = 1)
        else:
            depenses_par_residence = part_ticpe_revtot_strate

    save_dataframe_to_graph(depenses_par_residence, 'part_depenses_residence.csv')
