# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:24:45 2015

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
from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame, simulate_df, wavg, collapse, df_weighted_average_grouped, percent_formatter

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    list_coicop12 = []
    for coicop12_index in range(1, 13):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))

    var_to_be_simulated = [
        'decuc',
        'age',
        'montant_tva_total',
        'montant_tipp',
        'montant_droit_d_accise_vin',
        'montant_droit_d_accise_biere',
        'montant_droit_d_accise_alcools_forts',
        'montant_droit_d_accise_cigarette',
        'montant_droit_d_accise_cigares',
        'montant_droit_d_accise_tabac_a_rouler',
        'montant_taxe_assurance_transport',
        'montant_taxe_assurance_sante',
        'montant_taxe_autres_assurances',
        'niveau_vie_decile',
        'revtot',
        'rev_disponible',
        'ident_men',
        'pondmen',
        'somme_coicop12'
        ]

    var_to_be_simulated += list_coicop12

    for year in [2000, 2005, 2011]:
        df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        if year == 2011:
            df.niveau_vie_decile[df.decuc == 10] = 10
        Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = var_to_be_simulated)

        Wconcat['montant_taxe_1'] = Wconcat['montant_tva_total']
        Wconcat['montant_taxe_2'] = Wconcat['montant_tipp']
        Wconcat['montant_taxe_3'] = Wconcat['montant_taxe_assurance_sante'] + Wconcat['montant_taxe_assurance_transport'] + Wconcat['montant_taxe_autres_assurances']
        Wconcat['montant_taxe_4'] = Wconcat['montant_droit_d_accise_vin'] + Wconcat['montant_droit_d_accise_biere'] + Wconcat['montant_droit_d_accise_alcools_forts']
        Wconcat['montant_taxe_5'] = Wconcat['montant_droit_d_accise_cigares'] + Wconcat['montant_droit_d_accise_cigarette'] + Wconcat['montant_droit_d_accise_tabac_a_rouler']

        Wconcat['montant_total'] = (Wconcat['montant_taxe_{}'.format(1)] + Wconcat['montant_taxe_{}'.format(2)] + Wconcat['montant_taxe_{}'.format(3)] + Wconcat['montant_taxe_{}'.format(4)] + Wconcat['montant_taxe_{}'.format(5)])

        Wconcat['sur_rev_disponible'] = Wconcat['montant_total'] / Wconcat['rev_disponible']
        #TODO: la conso hors loyer ne se calcule pas en enlevant le poste coicop logement mais en enlevant les loyers réellement payés
        Wconcat['sur_conso_hors_loyer'] = Wconcat['montant_total'] / (Wconcat['somme_coicop12'] - Wconcat['coicop12_{}'.format(4)])

        df_to_graph = Wconcat['sur_rev_disponible']
        df_to_graph_2 = Wconcat['sur_conso_hors_loyer']

        axes = df_to_graph.plot(
            stacked = True
            )
        axes = df_to_graph_2.plot(
            stacked = True
            )
        plt.axhline(0, color = 'k')

        axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))

        axes.legend(
            bbox_to_anchor = (1.55, 1),
            )

    plt.show()
