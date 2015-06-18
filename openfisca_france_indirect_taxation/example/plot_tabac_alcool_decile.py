# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 15:43:49 2015

@author: hadrien
"""

# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division

from pandas import DataFrame, concat
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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
    # Liste des coicop agrégées en 12 postes
    list_coicop12 = ['coicop12_2']
#    for coicop12_index in range(1, 13):
#        list_coicop12.append('coicop12_{}'.format(coicop12_index))
    # Liste des variables que l'on veut simuler
    var_to_be_simulated = [
        'ident_men',
        'pondmen',
        'decuc',
        'age',
        'niveau_vie_decile',
        'revtot',
        'ocde10',
        'niveau_de_vie',
        'rev_disponible',
        'consommation_cigarette',
        'consommation_cigares',
        'consommation_tabac_a_rouler',
        'consommation_alcools_forts',
        'consommation_vin',
        'consommation_biere'
        ]
    # Merge des deux listes
    var_to_be_simulated += list_coicop12

    for year in [2000, 2005, 2011]:
        # Constition d'une base de données agrégée par décile (= collapse en stata)
        df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        if year == 2011:
            df.niveau_vie_decile[df.decuc == 10] = 10

        var_to_concat = list_coicop12 + ['rev_disponible']
        Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = var_to_be_simulated)

        list_alcool_tabac = []
        Wconcat['part_alcool'] = (Wconcat['consommation_alcools_forts'] + Wconcat['consommation_vin'] + Wconcat['consommation_biere']) / Wconcat['rev_disponible']
        list_alcool_tabac.append('part_alcool')
        Wconcat['part_tabac'] = (Wconcat['consommation_cigarette'] + Wconcat['consommation_cigares'] + Wconcat['consommation_tabac_a_rouler']) / Wconcat['rev_disponible']
        list_alcool_tabac.append('part_tabac')

        df_to_graph = Wconcat[list_alcool_tabac].copy()
        df_to_graph.columns = [
            'Alcool',
            'Tabac'
            ]

        axes = df_to_graph.plot(
            kind = 'bar',
            stacked = True,
            color = ['#006600', '#FF0000']

            )
        plt.axhline(0, color = 'k')

            # TODO utiliser format et corriger également ici
            # https://github.com/openfisca/openfisca-matplotlib/blob/master/openfisca_matplotlib/graphs.py#L123
        axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
        axes.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], rotation=0)

        # Supprimer la légende du graphique
        axes.legend(
            bbox_to_anchor = (1.5, 1.0),
            ) # TODO: supprimer la légende pour les lignes pointillées et continues
    plt.show()

