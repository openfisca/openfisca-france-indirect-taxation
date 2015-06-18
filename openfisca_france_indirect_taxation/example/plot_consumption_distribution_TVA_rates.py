# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:48:09 2015

@author: germainmarchand
"""

from __future__ import division

from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker #TODO: axes en pourcentage
import numpy as np

import openfisca_france_indirect_taxation
from openfisca_survey_manager.survey_collections import SurveyCollection


from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, percent_formatter


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

    var_to_be_simulated = [
        'ident_men',
        'pondmen',
        'decuc',
        'age',
        'decile',
        'montant_tva_taux_plein',
        'montant_tva_taux_intermediaire',
        'montant_tva_taux_reduit',
        'montant_tva_taux_super_reduit',
        'montant_tva_total',
        'revtot',
        'somme_coicop12_conso',
        'ocde10',
        'niveau_de_vie',
        ]

    var_to_be_simulated += list_coicop12

    # Constition d'une base de données agrégée par décile (= collapse en stata)
    for year in [2000]:
        df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        var_to_concat = ['montant_tva_taux_plein', 'montant_tva_taux_intermediaire', 'montant_tva_taux_reduit',
                         'montant_tva_taux_super_reduit', 'montant_tva_total']
        aggregates_data_frame = df_weighted_average_grouped(dataframe = df, groupe = 'decuc', varlist = var_to_concat)

        list_part_TVA = []
        aggregates_data_frame['part_tva_taux_plein'] = aggregates_data_frame['montant_tva_taux_plein'] / aggregates_data_frame['montant_tva_total']
        list_part_TVA.append('part_tva_taux_plein')
        aggregates_data_frame['part_tva_taux_intermediaire'] = aggregates_data_frame['montant_tva_taux_intermediaire'] / aggregates_data_frame['montant_tva_total']
        list_part_TVA.append('part_tva_taux_intermediaire')
        aggregates_data_frame['part_tva_taux_reduit'] = aggregates_data_frame['montant_tva_taux_reduit'] / aggregates_data_frame['montant_tva_total']
        list_part_TVA.append('part_tva_taux_reduit')
        aggregates_data_frame['part_tva_taux_super_reduit'] = aggregates_data_frame['montant_tva_taux_super_reduit'] / aggregates_data_frame['montant_tva_total']
        list_part_TVA.append('part_tva_taux_super_reduit')

        df_to_graph = aggregates_data_frame[list_part_TVA].copy()
        print len(df_to_graph.columns)
        df_to_graph.columns = ['tva_taux_plein', 'tva_taux_intermediaire', 'tva_taux_reduit', 'tva_taux_super_reduit']

        axes = df_to_graph.plot(
            kind = 'bar',
            stacked = True,
            )
        plt.axhline(0, color = 'k')

            # TODO utiliser format et corriger également ici
            # https://github.com/openfisca/openfisca-matplotlib/blob/master/openfisca_matplotlib/graphs.py#L123
        axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))

        # Supprimer la légende du graphique
    #    axes.legend(
    #        bbox_to_anchor = (1.4, 1.0),
    #        ) # TODO: supprimer la légende pour les lignes pointillées et continues
    #    plt.show()
        # TODO: analyser, changer les déciles de revenus en déciles de consommation
        # faire un truc plus joli, mettres labels...
