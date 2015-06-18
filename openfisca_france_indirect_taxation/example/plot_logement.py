# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 15:42:16 2015

@author: Etienne
"""

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

    # Lite des coicop agrégées en 12 postes
    list_coicop12 = []
    for coicop12_index in range(1, 13):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))
    # Liste des variables que l'on veut simuler
    var_to_be_simulated = [
        'ident_men',
        'pondmen',
        'decuc',
        'age',
        'niveau_vie_decile',
        'revtot',
        'somme_coicop12',
        'ocde10',
        'niveau_de_vie',
        'rev_disponible'
        ]
    # Merge des deux listes
    var_to_be_simulated += list_coicop12

    p = dict()
    for year in [2000, 2005, 2011]:
        simulation_data_frame = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        annee = simulation_data_frame.apply(lambda row: year, axis = 1)
        simulation_data_frame["year"] = annee
        if year == 2011:
            simulation_data_frame.niveau_vie_decile[simulation_data_frame.decuc == 10] = 10

        var_to_concat = list_coicop12 + ['rev_disponible', 'somme_coicop12']
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame, groupe = 'year', varlist = var_to_concat)

        list_part_coicop12 = []
        aggregates_data_frame['part_coicop12_4'] = aggregates_data_frame['coicop12_4'] / aggregates_data_frame['rev_disponible']
        'list_part_coicop12_4'
        list_part_coicop12.append('part_coicop12_4')
        df_to_graph = concat([aggregates_data_frame[list_part_coicop12]])

        df_to_graph.columns = [
            u'Logement, eau, gaz et électricté'
            ]

        axes = df_to_graph.plot(
            kind = 'bar',
            stacked = True,
            color = ['#0000FF']
            )
        plt.axhline(0, color = 'k')

        axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
        axes.set_xticklabels(['2000', '2005', '2011'], rotation=0);

        axes.legend(
            bbox_to_anchor = (0.85, 1.15),
            )

    plt.show()
