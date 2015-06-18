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
        'decile',
        'revtot',
        'somme_coicop12_conso',
        'somme_coicop12',
        'ocde10',
        'niveau_de_vie',
        'revtot',
        'rev_disponible',
        'rev_disp_loyerimput',
        'montant_tva_total',
        'montant_droit_d_accise_alcool',
        'montant_droit_d_accise_tabac',
        'montant_taxe_assurance',
        'montant_tipp'
        ]

    for year in [2000, 2005, 2011]:
        df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)

        if year == 2011:
            df.decile[df.decuc == 10] = 10

        varlist = ['somme_coicop12', 'rev_disp_loyerimput', 'rev_disponible', 'montant_tva_total', 'montant_droit_d_accise_alcool', 'montant_droit_d_accise_tabac',
                   'montant_taxe_assurance', 'montant_tipp']
        Wconcat_rev_disp = df_weighted_average_grouped(dataframe = df, groupe = 'decile', varlist = varlist)
        Wconcat_conso = df_weighted_average_grouped(dataframe = df, groupe = 'decile', varlist = varlist)
        Wconcat_rev_disp_loyerimput = df_weighted_average_grouped(dataframe = df, groupe = 'decile', varlist = varlist)

        list_taux_d_effort_rev_disp = []

        Wconcat_rev_disp['taux_d_effort_tva'] = Wconcat_rev_disp['montant_tva_total'] / Wconcat_rev_disp['rev_disponible']
        list_taux_d_effort_rev_disp.append('taux_d_effort_tva')
        Wconcat_rev_disp['taux_d_effort_alcool'] = Wconcat_rev_disp['montant_droit_d_accise_alcool'] / Wconcat_rev_disp['rev_disponible']
        list_taux_d_effort_rev_disp.append('taux_d_effort_alcool')
        Wconcat_rev_disp['taux_d_effort_tabac'] = Wconcat_rev_disp['montant_droit_d_accise_tabac'] / Wconcat_rev_disp['rev_disponible']
        list_taux_d_effort_rev_disp.append('taux_d_effort_tabac')
        Wconcat_rev_disp['taux_d_effort_assurance'] = Wconcat_rev_disp['montant_taxe_assurance'] / Wconcat_rev_disp['rev_disponible']
        list_taux_d_effort_rev_disp.append('taux_d_effort_assurance')
        Wconcat_rev_disp['taux_d_effort_tipp'] = Wconcat_rev_disp['montant_tipp'] / Wconcat_rev_disp['rev_disponible']
        list_taux_d_effort_rev_disp.append('taux_d_effort_tipp')

        list_taux_d_effort_conso = []

        Wconcat_conso['taux_d_effort_tva'] = Wconcat_conso['montant_tva_total'] / Wconcat_conso['somme_coicop12']
        list_taux_d_effort_conso.append('taux_d_effort_tva')
        Wconcat_conso['taux_d_effort_alcool'] = Wconcat_conso['montant_droit_d_accise_alcool'] / Wconcat_conso['somme_coicop12']
        list_taux_d_effort_conso.append('taux_d_effort_alcool')
        Wconcat_conso['taux_d_effort_tabac'] = Wconcat_conso['montant_droit_d_accise_tabac'] / Wconcat_conso['somme_coicop12']
        list_taux_d_effort_conso.append('taux_d_effort_tabac')
        Wconcat_conso['taux_d_effort_assurance'] = Wconcat_conso['montant_taxe_assurance'] / Wconcat_conso['somme_coicop12']
        list_taux_d_effort_conso.append('taux_d_effort_assurance')
        Wconcat_conso['taux_d_effort_tipp'] = Wconcat_conso['montant_tipp'] / Wconcat_conso['somme_coicop12']
        list_taux_d_effort_conso.append('taux_d_effort_tipp')

        list_taux_d_effort_rev_disp_loyerimput = []

        Wconcat_rev_disp_loyerimput['taux_d_effort_tva'] = Wconcat_rev_disp_loyerimput['montant_tva_total'] / Wconcat_rev_disp_loyerimput['rev_disp_loyerimput']
        list_taux_d_effort_rev_disp_loyerimput.append('taux_d_effort_tva')
        Wconcat_rev_disp_loyerimput['taux_d_effort_alcool'] = Wconcat_rev_disp_loyerimput['montant_droit_d_accise_alcool'] / Wconcat_rev_disp_loyerimput['rev_disp_loyerimput']
        list_taux_d_effort_rev_disp_loyerimput.append('taux_d_effort_alcool')
        Wconcat_rev_disp_loyerimput['taux_d_effort_tabac'] = Wconcat_rev_disp_loyerimput['montant_droit_d_accise_tabac'] / Wconcat_rev_disp_loyerimput['rev_disp_loyerimput']
        list_taux_d_effort_rev_disp_loyerimput.append('taux_d_effort_tabac')
        Wconcat_rev_disp_loyerimput['taux_d_effort_assurance'] = Wconcat_rev_disp_loyerimput['montant_taxe_assurance'] / Wconcat_rev_disp_loyerimput['rev_disp_loyerimput']
        list_taux_d_effort_rev_disp_loyerimput.append('taux_d_effort_assurance')
        Wconcat_rev_disp_loyerimput['taux_d_effort_tipp'] = Wconcat_rev_disp_loyerimput['montant_tipp'] / Wconcat_rev_disp_loyerimput['rev_disp_loyerimput']
        list_taux_d_effort_rev_disp_loyerimput.append('taux_d_effort_tipp')

        df_to_graph_rev_disp = Wconcat_rev_disp[list_taux_d_effort_rev_disp].copy()
        df_to_graph_rev_disp.columns = ['TVA', 'Taxes sur les Alcools', 'Taxes sur le tabac', 'Taxes sur les assurances', 'TICPE']

        axes = df_to_graph_rev_disp.plot(
            kind = 'bar',
            stacked = True,
            )
        plt.axhline(0, color = 'k')

        axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
        axes.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], rotation=0)

        axes.legend(
            bbox_to_anchor = (1.6, 1.0),
            )

        df_to_graph_conso = Wconcat_conso[list_taux_d_effort_rev_disp].copy()
        df_to_graph_conso.columns = ['TVA', 'Taxes sur les Alcools', 'Taxes sur le tabac', 'Taxes sur les assurances', 'TICPE']


        axes = df_to_graph_conso.plot(
            kind = 'bar',
            stacked = True,
            )
        plt.axhline(0, color = 'k')

        axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
        axes.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], rotation=0)

        axes.legend(
            bbox_to_anchor = (1.6, 1.0),
            )


        df_to_graph_rev_disp_loyerimput = Wconcat_rev_disp_loyerimput[list_taux_d_effort_rev_disp_loyerimput].copy()
        df_to_graph_rev_disp_loyerimput.columns = ['TVA', 'Taxes sur les Alcools', 'Taxes sur le tabac', 'Taxes sur les assurances', 'TICPE']

        axes = df_to_graph_rev_disp_loyerimput.plot(
            kind = 'bar',
            stacked = True,
            )
        plt.axhline(0, color = 'k')

        axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
        axes.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], rotation=0)

        axes.legend(
            bbox_to_anchor = (1.6, 1.0),
            )
