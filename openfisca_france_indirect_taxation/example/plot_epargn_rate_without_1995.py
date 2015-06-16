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
        dict(
            (name, simulation.calculate(name)) for name in var_to_be_simulated

            )
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
        'decile',
        'rev_disponible',
        'ident_men',
        'pondmen',
        'somme_coicop12',
        'montant_tva_total',
        'montant_tipp',
        'montant_taxe_assurance_sante',
        'montant_droit_d_accise_vin',
        'montant_droit_d_accise_cigares',
        'montant_taxe_assurance_transport',
        'montant_taxe_autres_assurances',
        'montant_droit_d_accise_biere',
        'montant_droit_d_accise_alcools_forts',
        'montant_droit_d_accise_cigarette',
        'montant_droit_d_accise_tabac_a_rouler',
        ]

    var_to_be_simulated += list_coicop12

#    df1995 = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 1995)
#    Wconcat1995 = df_weighted_average_grouped(dataframe = df1995, groupe = 'decile', varlist = varlist)
#    Wconcat1995['épargne'] = Wconcat1995['rev_disponible'] - Wconcat1995['somme_coicop12']
#
#    Wconcat1995['montant_taxe_{}'.format(1)] = Wconcat1995['montant_tva_total']
#    Wconcat1995['montant_taxe_{}'.format(2)] = Wconcat1995['montant_tipp']
#    Wconcat1995['montant_taxe_{}'.format(3)] = Wconcat1995['montant_taxe_assurance_sante'] + Wconcat1995['montant_taxe_assurance_transport'] + Wconcat1995['montant_taxe_autres_assurances']
#    Wconcat1995['montant_taxe_{}'.format(4)] = Wconcat1995['montant_droit_d_accise_vin'] + Wconcat1995['montant_droit_d_accise_biere'] + Wconcat1995['montant_droit_d_accise_alcools_forts']
#    Wconcat1995['montant_taxe_{}'.format(5)] = Wconcat1995['montant_droit_d_accise_cigares'] + Wconcat1995['montant_droit_d_accise_cigarette'] + Wconcat1995['montant_droit_d_accise_tabac_a_rouler']
#
#    Wconcat1995['montant_total'] = (Wconcat1995['montant_taxe_{}'.format(1)] + Wconcat1995['montant_taxe_{}'.format(2)] + Wconcat1995['montant_taxe_{}'.format(3)] + Wconcat1995['montant_taxe_{}'.format(4)] + Wconcat1995['montant_taxe_{}'.format(5)])
#    Wconcat1995['1995'] = Wconcat1995['montant_total'] / Wconcat1995['rev_disponible']
#    df_to_graph_1995 = Wconcat1995['1995']

    df2000 = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2000)
    Wconcat2000 = df_weighted_average_grouped(dataframe = df2000, groupe = 'decile', varlist = var_to_be_simulated)

    Wconcat2000['montant_taxe_{}'.format(1)] = Wconcat2000['montant_tva_total']
    Wconcat2000['montant_taxe_{}'.format(2)] = Wconcat2000['montant_tipp']
    Wconcat2000['montant_taxe_{}'.format(3)] = Wconcat2000['montant_taxe_assurance_sante'] + Wconcat2000['montant_taxe_assurance_transport'] + Wconcat2000['montant_taxe_autres_assurances']
    Wconcat2000['montant_taxe_{}'.format(4)] = Wconcat2000['montant_droit_d_accise_vin'] + Wconcat2000['montant_droit_d_accise_biere'] + Wconcat2000['montant_droit_d_accise_alcools_forts']
    Wconcat2000['montant_taxe_{}'.format(5)] = Wconcat2000['montant_droit_d_accise_cigares'] + Wconcat2000['montant_droit_d_accise_cigarette'] + Wconcat2000['montant_droit_d_accise_tabac_a_rouler']

    Wconcat2000['montant_total'] = (Wconcat2000['montant_taxe_{}'.format(1)] + Wconcat2000['montant_taxe_{}'.format(2)] + Wconcat2000['montant_taxe_{}'.format(3)] + Wconcat2000['montant_taxe_{}'.format(4)] + Wconcat2000['montant_taxe_{}'.format(5)])
    Wconcat2000['2000'] = Wconcat2000['montant_total'] / Wconcat2000['rev_disponible']
    df_to_graph_2000 = Wconcat2000['2000']

    df2005 = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2005)
    Wconcat2005 = df_weighted_average_grouped(dataframe = df2005, groupe = 'decile', varlist = var_to_be_simulated)

    Wconcat2005['montant_taxe_{}'.format(1)] = Wconcat2005['montant_tva_total']
    Wconcat2005['montant_taxe_{}'.format(2)] = Wconcat2005['montant_tipp']
    Wconcat2005['montant_taxe_{}'.format(3)] = Wconcat2005['montant_taxe_assurance_sante'] + Wconcat2005['montant_taxe_assurance_transport'] + Wconcat2005['montant_taxe_autres_assurances']
    Wconcat2005['montant_taxe_{}'.format(4)] = Wconcat2005['montant_droit_d_accise_vin'] + Wconcat2005['montant_droit_d_accise_biere'] + Wconcat2005['montant_droit_d_accise_alcools_forts']
    Wconcat2005['montant_taxe_{}'.format(5)] = Wconcat2005['montant_droit_d_accise_cigares'] + Wconcat2005['montant_droit_d_accise_cigarette'] + Wconcat2005['montant_droit_d_accise_tabac_a_rouler']

    Wconcat2005['montant_total'] = (Wconcat2005['montant_taxe_{}'.format(1)] + Wconcat2005['montant_taxe_{}'.format(2)] + Wconcat2005['montant_taxe_{}'.format(3)] + Wconcat2005['montant_taxe_{}'.format(4)] + Wconcat2005['montant_taxe_{}'.format(5)])
    Wconcat2005['2005'] = Wconcat2005['montant_total'] / Wconcat2005['rev_disponible']
    df_to_graph_2005 = Wconcat2005['2005']

    df2011 = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2011)
    Wconcat2011 = df_weighted_average_grouped(dataframe = df2011, groupe = 'decile', varlist = var_to_be_simulated)

    Wconcat2011['montant_taxe_{}'.format(1)] = Wconcat2011['montant_tva_total']
    Wconcat2011['montant_taxe_{}'.format(2)] = Wconcat2011['montant_tipp']
    Wconcat2011['montant_taxe_{}'.format(3)] = Wconcat2011['montant_taxe_assurance_sante'] + Wconcat2011['montant_taxe_assurance_transport'] + Wconcat2011['montant_taxe_autres_assurances']
    Wconcat2011['montant_taxe_{}'.format(4)] = Wconcat2011['montant_droit_d_accise_vin'] + Wconcat2011['montant_droit_d_accise_biere'] + Wconcat2011['montant_droit_d_accise_alcools_forts']
    Wconcat2011['montant_taxe_{}'.format(5)] = Wconcat2011['montant_droit_d_accise_cigares'] + Wconcat2011['montant_droit_d_accise_cigarette'] + Wconcat2011['montant_droit_d_accise_tabac_a_rouler']

    Wconcat2011['montant_total'] = (Wconcat2011['montant_taxe_{}'.format(1)] + Wconcat2011['montant_taxe_{}'.format(2)] + Wconcat2011['montant_taxe_{}'.format(3)] + Wconcat2011['montant_taxe_{}'.format(4)] + Wconcat2011['montant_taxe_{}'.format(5)])
    Wconcat2011['2011'] = Wconcat2011['montant_total'] / Wconcat2011['rev_disponible']
    df_to_graph_2011 = Wconcat2011['2011']

#    axes = df_to_graph_1995.plot(
#        stacked = True
#        )
    axes = df_to_graph_2000.plot(
        stacked = True
        )
    axes = df_to_graph_2005.plot(
        stacked = True
        )
    axes = df_to_graph_2011.plot(
        stacked = True
        )

    plt.axhline(0, color = 'k')

    def percent_formatter(x, pos = 0):
        return '%1.0f%%' % (100 * x)

    axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
    axes.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], rotation=0)

    axes.legend(
        bbox_to_anchor = (1, 1),
        )

    plt.show()
    print df2000.decile
    print df2005.decile
    print df2011.decile
