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
from pandas import DataFrame
import matplotlib.pyplot as plt

import openfisca_france_indirect_taxation
from openfisca_survey_manager.survey_collections import SurveyCollection


from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame, simulate_df, wavg, collapse, df_weighted_average_grouped


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)


# Exemple: graphe par décile de revenu par uc de la ventilation de la consommation selon les postes agrégés de la CN
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
        'consommation_totale',
        'ocde10',
        'niveau_de_vie',
        ]
    # Merge des deux listes
    var_to_be_simulated += list_coicop12

    # Constition d'une base de données agrégée par décile (= collapse en stata)
    for year in [2000, 2005, 2011]:
        df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        var_to_concat = list_coicop12 + ['consommation_totale']
        Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = var_to_concat)

        # Construction des parts
        list_part_coicop12 = []
        for i in range(1, 13):
            Wconcat['part_coicop12_{}'.format(i)] = Wconcat['coicop12_{}'.format(i)] / Wconcat['consommation_totale']
            'list_part_coicop12_{}'.format(i)
            list_part_coicop12.append('part_coicop12_{}'.format(i))

        df_to_graph = Wconcat[list_part_coicop12]

        axes = df_to_graph.plot(kind = 'bar', stacked = True)
        plt.axhline(0, color = 'k')

        axes.legend(
            bbox_to_anchor = (1.5, 1),
            )

    plt.show()

    #TODO: analyser, changer les déciles de revenus en déciles de consommation
    # faire un truc plus joli, mettres labels...
