# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:48:09 2015

@author: germainmarchand
"""

from __future__ import division

from openfisca_france_indirect_taxation.example.utils_example import simulate, df_weighted_average_grouped, \
    graph_builder_bar


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Exemple: graphe par décile de revenu par uc de la ventilation de la consommation
    # selon les postes agrégés de la CN

    list_coicop12 = []
    for coicop12_index in range(1, 9):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))

    simulated_variables = [
        'pondmen',
        'decuc',
        'niveau_vie_decile',
        'tva_taux_plein',
        'tva_taux_intermediaire',
        'tva_taux_reduit',
        'tva_taux_super_reduit',
        'tva_total',
        'revtot',
        'somme_coicop12_conso',
        'ocde10',
        ]

    simulated_variables += list_coicop12

    # Constition d'une base de données agrégée par décile (= collapse en stata)
    for year in [2000, 2005, 2011]:
        df = simulate(simulated_variables = simulated_variables, year = year)
        var_to_concat = ['tva_taux_plein', 'tva_taux_intermediaire', 'tva_taux_reduit',
                         'tva_taux_super_reduit', 'tva_total']
        aggregates_data_frame = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile',
            varlist = var_to_concat)

        list_part_TVA = []
        aggregates_data_frame['part_tva_taux_plein'] = \
            aggregates_data_frame['tva_taux_plein'] / aggregates_data_frame['tva_total']
        list_part_TVA.append('part_tva_taux_plein')
        aggregates_data_frame['part_tva_taux_intermediaire'] = \
            aggregates_data_frame['tva_taux_intermediaire'] / aggregates_data_frame['tva_total']
        list_part_TVA.append('part_tva_taux_intermediaire')
        aggregates_data_frame['part_tva_taux_reduit'] = \
            aggregates_data_frame['tva_taux_reduit'] / aggregates_data_frame['tva_total']
        list_part_TVA.append('part_tva_taux_reduit')
        aggregates_data_frame['part_tva_taux_super_reduit'] = \
            aggregates_data_frame['tva_taux_super_reduit'] / aggregates_data_frame['tva_total']
        list_part_TVA.append('part_tva_taux_super_reduit')

        df_to_graph = aggregates_data_frame[list_part_TVA].copy()

        graph_builder_bar(df_to_graph)
