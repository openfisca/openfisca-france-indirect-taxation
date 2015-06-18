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
        'decile',
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

    df1995 = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 1995)
    annee = df1995.apply(lambda row: 1995, axis = 1)
    df1995["year"] = annee

    df2000 = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2000)
    annee = df2000.apply(lambda row: 2000, axis = 1)
    df2000["year"] = annee

    df2005 = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2005)
    annee = df2005.apply(lambda row: 2005, axis = 1)
    df2005["year"] = annee

    df2011 = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2011)
    if year == 2011:
        df2011.decile[df2011.decuc == 10] = 10
    annee = df2011.apply(lambda row: 2011, axis = 1)
    df2011["year"] = annee

    var_to_concat = var_to_be_simulated

    Wconcat1995 = df_weighted_average_grouped(dataframe = df1995, groupe = 'year', varlist = var_to_concat)
    Wconcat2000 = df_weighted_average_grouped(dataframe = df2000, groupe = 'year', varlist = var_to_concat)
    Wconcat2005 = df_weighted_average_grouped(dataframe = df2005, groupe = 'year', varlist = var_to_concat)
    Wconcat2011 = df_weighted_average_grouped(dataframe = df2011, groupe = 'year', varlist = var_to_concat)

    Wconcat1995['taxe_{}'.format(1)] = Wconcat1995['montant_droit_d_accise_vin']
    Wconcat1995['taxe_{}'.format(2)] = Wconcat1995['montant_droit_d_accise_biere']
    Wconcat1995['taxe_{}'.format(3)] = Wconcat1995['montant_droit_d_accise_alcools_forts']
    Wconcat1995['taxe_{}'.format(4)] = Wconcat1995['montant_droit_d_accise_cigarette']
    Wconcat1995['taxe_{}'.format(5)] = Wconcat1995['montant_droit_d_accise_cigares']
    Wconcat1995['taxe_{}'.format(6)] = Wconcat1995['montant_droit_d_accise_tabac_a_rouler']
    Wconcat1995['taxe_{}'.format(7)] = Wconcat1995['montant_taxe_assurance_transport']
    Wconcat1995['taxe_{}'.format(8)] = Wconcat1995['montant_taxe_assurance_sante']
    Wconcat1995['taxe_{}'.format(9)] = Wconcat1995['montant_taxe_autres_assurances']
    Wconcat1995['taxe_{}'.format(10)] = Wconcat1995['montant_tipp']
    Wconcat1995['taxe_{}'.format(11)] = Wconcat1995['montant_tva_total']

    Wconcat2000['taxe_{}'.format(1)] = Wconcat2000['montant_droit_d_accise_vin']
    Wconcat2000['taxe_{}'.format(2)] = Wconcat2000['montant_droit_d_accise_biere']
    Wconcat2000['taxe_{}'.format(3)] = Wconcat2000['montant_droit_d_accise_alcools_forts']
    Wconcat2000['taxe_{}'.format(4)] = Wconcat2000['montant_droit_d_accise_cigarette']
    Wconcat2000['taxe_{}'.format(5)] = Wconcat2000['montant_droit_d_accise_cigares']
    Wconcat2000['taxe_{}'.format(6)] = Wconcat2000['montant_droit_d_accise_tabac_a_rouler']
    Wconcat2000['taxe_{}'.format(7)] = Wconcat2000['montant_taxe_assurance_transport']
    Wconcat2000['taxe_{}'.format(8)] = Wconcat2000['montant_taxe_assurance_sante']
    Wconcat2000['taxe_{}'.format(9)] = Wconcat2000['montant_taxe_autres_assurances']
    Wconcat2000['taxe_{}'.format(10)] = Wconcat2000['montant_tipp']
    Wconcat2000['taxe_{}'.format(11)] = Wconcat2000['montant_tva_total']

    Wconcat2005['taxe_{}'.format(1)] = Wconcat1995['montant_droit_d_accise_vin']
    Wconcat2005['taxe_{}'.format(2)] = Wconcat2005['montant_droit_d_accise_biere']
    Wconcat2005['taxe_{}'.format(3)] = Wconcat2005['montant_droit_d_accise_alcools_forts']
    Wconcat2005['taxe_{}'.format(4)] = Wconcat2005['montant_droit_d_accise_cigarette']
    Wconcat2005['taxe_{}'.format(5)] = Wconcat2005['montant_droit_d_accise_cigares']
    Wconcat2005['taxe_{}'.format(6)] = Wconcat2005['montant_droit_d_accise_tabac_a_rouler']
    Wconcat2005['taxe_{}'.format(7)] = Wconcat2005['montant_taxe_assurance_transport']
    Wconcat2005['taxe_{}'.format(8)] = Wconcat2005['montant_taxe_assurance_sante']
    Wconcat2005['taxe_{}'.format(9)] = Wconcat2005['montant_taxe_autres_assurances']
    Wconcat2005['taxe_{}'.format(10)] = Wconcat2005['montant_tipp']
    Wconcat2005['taxe_{}'.format(11)] = Wconcat2005['montant_tva_total']

    Wconcat2011['taxe_{}'.format(1)] = Wconcat2011['montant_droit_d_accise_vin']
    Wconcat2011['taxe_{}'.format(2)] = Wconcat2011['montant_droit_d_accise_biere']
    Wconcat2011['taxe_{}'.format(3)] = Wconcat2011['montant_droit_d_accise_alcools_forts']
    Wconcat2011['taxe_{}'.format(4)] = Wconcat2011['montant_droit_d_accise_cigarette']
    Wconcat2011['taxe_{}'.format(5)] = Wconcat2011['montant_droit_d_accise_cigares']
    Wconcat2011['taxe_{}'.format(6)] = Wconcat2011['montant_droit_d_accise_tabac_a_rouler']
    Wconcat2011['taxe_{}'.format(7)] = Wconcat2011['montant_taxe_assurance_transport']
    Wconcat2011['taxe_{}'.format(8)] = Wconcat2011['montant_taxe_assurance_sante']
    Wconcat2011['taxe_{}'.format(9)] = Wconcat2011['montant_taxe_autres_assurances']
    Wconcat2011['taxe_{}'.format(10)] = Wconcat2011['montant_tipp']
    Wconcat2011['taxe_{}'.format(11)] = Wconcat2011['montant_tva_total']

    list_taxes_1995 = []
    for i in range(1, 12):
        Wconcat1995['part_{}'.format(i)] = Wconcat1995['taxe_{}'.format(i)] / Wconcat1995['montant_total_taxes_indirectes']
        'list_taxes_{}_1995'.format(i)
        list_taxes_1995.append('part_{}'.format(i))

    list_taxes_2000 = []
    for i in range(1, 12):
        Wconcat2000['part_{}'.format(i)] = Wconcat2000['taxe_{}'.format(i)] / Wconcat2000['montant_total_taxes_indirectes']
        'list_taxes_{}_2000'.format(i)
        list_taxes_2000.append('part_{}'.format(i))

    list_taxes_2005 = []
    for i in range(1, 12):
        Wconcat2005['part_{}'.format(i)] = Wconcat2005['taxe_{}'.format(i)] / Wconcat2005['montant_total_taxes_indirectes']
        'list_taxes_{}_2005'.format(i)
        list_taxes_2005.append('part_{}'.format(i))

    list_taxes_2011 = []
    for i in range(1, 12):
        Wconcat2011['part_{}'.format(i)] = Wconcat2011['taxe_{}'.format(i)] / Wconcat2011['montant_total_taxes_indirectes']
        'list_taxes_{}_2011'.format(i)
        list_taxes_2011.append('part_{}'.format(i))

    df_to_graph = concat([Wconcat1995[list_taxes_1995], Wconcat2000[list_taxes_2000], Wconcat2005[list_taxes_2005], Wconcat2011[list_taxes_2011]])

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
    axes.set_xticklabels(['1995', '2000', '2005', '2011'], rotation=0);

    axes.legend(
        bbox_to_anchor = (1.5, 1),
        )

    plt.show()
    plt.savefig('C:\Users\hadrien\Desktop\Travail\ENSAE\Statapp\graphe_taxes_indirectes.eps', format='eps', dpi=1000)
