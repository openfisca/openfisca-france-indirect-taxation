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
        'decile',
        'revtot',
        'rev_disponible',
        'ident_men',
        'pondmen',
        'somme_coicop12'
        ]

    var_to_be_simulated += list_coicop12


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
               'montant_taxe_autres_assurances',
               'somme_coicop12'
              ]


    varlist += list_coicop12


    df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2005)
    if year == 2011:
        df.decile[df.decuc == 10 ] = 10
    Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'decile', varlist = varlist)

    Wconcat['montant_taxe_{}'.format(1)] = Wconcat['montant_tva_total']
    Wconcat['montant_taxe_{}'.format(2)] = Wconcat['montant_tipp']
    Wconcat['montant_taxe_{}'.format(3)] = Wconcat['montant_taxe_assurance_sante'] + Wconcat['montant_taxe_assurance_transport'] + Wconcat['montant_taxe_autres_assurances']
    Wconcat['montant_taxe_{}'.format(4)] = Wconcat['montant_droit_d_accise_vin'] + Wconcat['montant_droit_d_accise_biere']  +Wconcat['montant_droit_d_accise_alcools_forts']
    Wconcat['montant_taxe_{}'.format(5)] = Wconcat['montant_droit_d_accise_cigares'] + Wconcat['montant_droit_d_accise_cigarette'] + Wconcat['montant_droit_d_accise_tabac_a_rouler']

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


    def percent_formatter(x, pos = 0):
        return '%1.0f%%' % (100 * x)

    axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
    axes.set_xticklabels( ['1','2','3','4','5','6','7','8','9','10'], rotation=0 )


    axes.legend(
        labels = ['sur revenu disponible', 'sur consommation hors loyer'],
        bbox_to_anchor = (1, 1),
        )

    plt.show()
    plt.savefig('C:\Users\hadrien\Desktop\Travail\ENSAE\Statapp\graphe_taxes_indirectes_total.eps', format='eps', dpi=1000)
