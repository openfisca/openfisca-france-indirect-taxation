# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:25:34 2015

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
        'montant_droit_d_accise_vin',
        'montant_droit_d_accise_biere',
        'montant_droit_d_accise_alcools_forts',
        'montant_droit_d_accise_cigarette',
        'montant_droit_d_accise_cigares',
        'montant_droit_d_accise_tabac_a_rouler',
        'montant_taxe_assurance_transport',
        'montant_taxe_assurance_sante',
        'montant_taxe_autres_assurances',
        'montant_tipp',
        'montant_tva_total',
        'montant_total_taxes_indirectes',
        'montant_total_taxes_indirectes_sans_tva'
        ]


    p = dict()
    for year in [2000, 2005, 2011]:
        simulation_data_frame = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        annee = simulation_data_frame.apply(lambda row: year, axis = 1)
        simulation_data_frame["year"] = annee
        if year == 2011:
            simulation_data_frame.niveau_vie_decile[simulation_data_frame.decuc == 10] = 10

        var_to_concat = var_to_be_simulated
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame, groupe = 'year', varlist = var_to_concat)

        aggregates_data_frame['taxe_1'] = aggregates_data_frame['montant_droit_d_accise_vin']
        aggregates_data_frame['taxe_2'] = aggregates_data_frame['montant_droit_d_accise_biere']
        aggregates_data_frame['taxe_3'] = aggregates_data_frame['montant_droit_d_accise_alcools_forts']
        aggregates_data_frame['taxe_4'] = aggregates_data_frame['montant_droit_d_accise_cigarette']
        aggregates_data_frame['taxe_5'] = aggregates_data_frame['montant_droit_d_accise_cigares']
        aggregates_data_frame['taxe_6'] = aggregates_data_frame['montant_droit_d_accise_tabac_a_rouler']
        aggregates_data_frame['taxe_7'] = aggregates_data_frame['montant_taxe_assurance_transport']
        aggregates_data_frame['taxe_8'] = aggregates_data_frame['montant_taxe_assurance_sante']
        aggregates_data_frame['taxe_9'] = aggregates_data_frame['montant_taxe_autres_assurances']
        aggregates_data_frame['taxe_10'] = aggregates_data_frame['montant_tipp']
        aggregates_data_frame['taxe_11'] = aggregates_data_frame['montant_tva_total']

        list_taxes = []
        for i in range(1, 12):
            aggregates_data_frame['part_{}'.format(i).format(year)] = aggregates_data_frame['taxe_{}'.format(i)] / aggregates_data_frame['montant_total_taxes_indirectes']
            'list_taxes_{}'.format(i)
            list_taxes.append('part_{}'.format(i))

        df_to_graph = concat([aggregates_data_frame[list_taxes]])

        df_to_graph.columns = ['Vin', u'Bière', 'Alcools forts', 'Cigarettes', 'Cigares', u'Tabac à rouler',
            'Assurance transport', u'Assurance santé', 'Autres assurances', 'TIPP', 'TVA']

        axes = df_to_graph.plot(
            kind = 'bar',
            stacked = True,
            color = ['#FF0000', '#006600', '#000000', '#0000FF', '#FFFF00', '#999966', '#FF6699', '#00FFFF', '#CC3300',
                     '#990033', '#3366CC']
            )
        plt.axhline(0, color = 'k')

        axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
        axes.set_xticklabels(['2000', '2005', '2011'], rotation=0);

        axes.legend(
            bbox_to_anchor = (1.5, 1),
            )

    plt.show()
