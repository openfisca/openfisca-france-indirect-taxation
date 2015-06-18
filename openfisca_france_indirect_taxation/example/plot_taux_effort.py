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
import matplotlib.ticker as ticker

import openfisca_france_indirect_taxation
from openfisca_survey_manager.survey_collections import SurveyCollection

from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, percent_formatter



# On va dans ce fichier créer les graphiques permettant de voir les taux d'effort selon trois définition du revenu:
# - revenu total
# - revenu disponible
# - revenu disponible et loyer imputé

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)


    # Liste des variables que l'on veut simuler
    var_to_be_simulated = [
        'ident_men',
        'pondmen',
        'decuc',
        'niveau_vie_decile',
        'revtot',
        'somme_coicop12_conso',
        'ocde10',
        'niveau_de_vie',
        'revtot' ,
        'rev_disponible',
        'rev_disp_loyerimput',
        'montant_total_taxes_indirectes' # ,
        ]

# 1 calcul taux d'effort sur le revenu total
    # Constition d'une base de données agrégée par décile (= collapse en stata)
    for year in [2000, 2005, 2011]:
        df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        if year == 2011:
            df.niveau_vie_decile[df.decuc == 10] = 10
        varlist = ['revtot', 'montant_total_taxes_indirectes', 'rev_disponible', 'rev_disp_loyerimput']
        Wconcat1 = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = varlist)
        Wconcat1['taux_d_effort_revtot_{}'.format(year)] = Wconcat1['montant_total_taxes_indirectes'] / Wconcat1['revtot']
        df_to_graph1 = Wconcat1['taux_d_effort_revtot_{}'.format(year)]

        df.rev_disponible = df.rev_disponible * 1.33
        Wconcat2 = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = varlist)
        Wconcat2['taux_d_effort_rev_disponible_{}'.format(year)] = Wconcat2['montant_total_taxes_indirectes'] / Wconcat2['rev_disponible']
        df_to_graph2 = Wconcat2['taux_d_effort_rev_disponible_{}'.format(year)]

        Wconcat3 = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = varlist)
        Wconcat3['taux_d_effort_rev_disp_loyerimput_{}'.format(year)] = Wconcat3['montant_total_taxes_indirectes'] / Wconcat3['rev_disp_loyerimput']
        df_to_graph3 = Wconcat3['taux_d_effort_rev_disp_loyerimput_{}'.format(year)]

        axes1 = df_to_graph1.plot(stacked = True)
        plt.axhline(0, color = 'k')

        axes2 = df_to_graph2.plot(stacked = True)
        plt.axhline(0, color = 'k')

        axes3 = df_to_graph3.plot(stacked = True)
        plt.axhline(0, color = 'k')

        axes1.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))

        axes1.legend(
            bbox_to_anchor = (1.80, 0.95),
            )

    plt.show()
