# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 17:36:56 2015

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


def get_input_data_frame(year):
    openfisca_survey_collection = SurveyCollection.load(
        collection = "openfisca_indirect_taxation", config_files_directory = config_files_directory)
    openfisca_survey = openfisca_survey_collection.get_survey("openfisca_indirect_taxation_data_{}".format(year))
    input_data_frame = openfisca_survey.get_values(table = "input")
    input_data_frame.reset_index(inplace = True)
    return input_data_frame


def simulate_df(var_to_be_simulated, year):
    '''
    Construction de la DataFrame à partir de laquelle sera faite l'analyse des données
    '''
    input_data_frame = get_input_data_frame(year)
    TaxBenefitSystem = openfisca_france_indirect_taxation.init_country()

    tax_benefit_system = TaxBenefitSystem()
    survey_scenario = SurveyScenario().init_from_data_frame(
        input_data_frame = input_data_frame,
        tax_benefit_system = tax_benefit_system,
        year = year,
        )
    simulation = survey_scenario.new_simulation()
    return DataFrame(
        dict([
            (name, simulation.calculate(name)) for name in var_to_be_simulated

            ])
        )


def wavg(groupe, var):
    '''
    Fonction qui calcule la moyenne pondérée par groupe d'une variable
    '''
    d = groupe[var]
    w = groupe['pondmen']
    return (d * w).sum() / w.sum()


def collapse(dataframe, groupe, var):
    '''
    Pour une variable, fonction qui calcule la moyenne pondérée au sein de chaque groupe.
    '''
    grouped = dataframe.groupby([groupe])
    var_weighted_grouped = grouped.apply(lambda x: wavg(groupe = x, var = var))
    return var_weighted_grouped


def df_weighted_average_grouped(dataframe, groupe, varlist):
    '''
    Agrège les résultats de weighted_average_grouped() en une unique dataframe pour la liste de variable 'varlist'.
    '''
    return DataFrame(
        dict([
            (var, collapse(dataframe, groupe, var)) for var in varlist
            ])
        )


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)


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
        'decile',
        'revtot',
        'rev_disponible',
        'ident_men',
        'pondmen',
        ]

    varlist = ['rev_disponible',
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
               'montant_taxe_autres_assurances'
              ]


    df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2000)
    Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'decile', varlist = varlist)

    Wconcat['montant_taxe_{}'.format(1)] = Wconcat['montant_tva_total']
    Wconcat['montant_taxe_{}'.format(2)] = Wconcat['montant_tipp']
    Wconcat['montant_taxe_{}'.format(3)] = Wconcat['montant_taxe_assurance_sante'] + Wconcat['montant_taxe_assurance_transport'] + Wconcat['montant_taxe_autres_assurances']
    Wconcat['montant_taxe_{}'.format(4)] = Wconcat['montant_droit_d_accise_vin'] + Wconcat['montant_droit_d_accise_biere']  +Wconcat['montant_droit_d_accise_alcools_forts']
    Wconcat['montant_taxe_{}'.format(5)] = Wconcat['montant_droit_d_accise_cigares'] + Wconcat['montant_droit_d_accise_cigarette'] + Wconcat['montant_droit_d_accise_tabac_a_rouler']


    list_part_taxes = []
    for i in range(1, 6):
        Wconcat['part_taxe_{}'.format(i)] = Wconcat['montant_taxe_{}'.format(i)] / Wconcat['rev_disponible']
        'list_part_taxes_{}'.format(i)
        list_part_taxes.append('part_taxe_{}'.format(i))

    df_to_graph = Wconcat[list_part_taxes]

    df_to_graph.columns = [
        'TVA', 'TIPP','Assurances','Alcools','Tabac'
        ]


    axes = df_to_graph.plot(
        kind = 'bar',
        stacked = True,
        color = ['#0000FF','#FF0000','#006600','#CC3300','#3366CC']
        )

    plt.axhline(0, color = 'k')


    def percent_formatter(x, pos = 0):
        return '%1.0f%%' % (100 * x)

    axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
    axes.set_xticklabels( ['1','2','3','4','5','6','7','8','9','10'], rotation=0 )


    axes.legend(
        bbox_to_anchor = (1.3, 1),
        )

    plt.show()
    plt.savefig('C:/Users/Etienne/Documents/data/graphe4.eps', format='eps', dpi=1000)
