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

from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.example.utils_example import simulate, df_weighted_average_grouped


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    simulated_variables = [
        'tva_taux_plein',
        'consommation_tva_taux_plein',
        'categorie_fiscale_11',
        'tva_taux_intermediaire',
        'consommation_tva_taux_intermediaire',
        'tva_taux_reduit',
        'tva_taux_super_reduit',
        'tva_total',
        'ident_men',
        'pondmen',
        'decuc',
        'age',
        'revtot',
        'rev_disponible',
        'ocde10',
        'niveau_de_vie',
        #'depenses_by_grosposte',
        #'cs8pr'
        ]

    # Exemple : graphe par décile de revenu par uc de la ventilation de la consommation selon les postes agrégés de la CN
    for year in [2000, 2005, 2011]:
        # Constition d'une base de données agrégée par décile (= collapse en stata)
        df = simulate(simulated_variables = simulated_variables, year = year)
        Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'cs8pr', varlist = ['tva_total', 'revtot'])
        df_to_plot = Wconcat['tva_total'] / Wconcat['revtot']

        # Plot du graphe avec matplotlib
        plt.figure();
        df_to_plot.plot(kind='bar', stacked=True); plt.axhline(0, color='k')
        Wconcat.plot(kind='bar', stacked=True); plt.axhline(0, color='k')
