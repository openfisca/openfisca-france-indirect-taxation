# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:19:14 2015

@author: thomas.douenne
"""

from __future__ import division

from pandas import DataFrame
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


def percent_formatter(x, pos = 0):
    return '%1.0f%%' % (100 * x)


def graph_builder_bar(graph):
    axes = graph.plot(
        kind = 'bar',
        stacked = True,
        color = ['#FF0000', '#0000FF', '#006600', '#660066', '#FFFF00', '#999966', '#FF6699', '#00FFFF',
                 '#CC3300', '#990033', '#3366CC', '#000000']
        )
    plt.axhline(0, color = 'k')
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
    axes.legend(
        bbox_to_anchor = (1.5, 1.05),
        )
    return plt.show()


def graph_builder_bar_list(graph):
    axes = graph.plot(
        kind = 'bar',
        stacked = True,
        color = ['#FF0000']
        )
    plt.axhline(0, color = 'k')
    axes.legend(
        bbox_to_anchor = (1.5, 1.05),
        )
    return plt.show()


def graph_builder_line(graph):
    axes = graph.plot(
        )
    plt.axhline(0, color = 'k')
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
    axes.legend(
        bbox_to_anchor = (1, 1),
        )
    return plt.show()


def graph_builder_carburants(data_frame, name, legend1, legend2, color1, color2, color3, color4):
    axes = data_frame.plot(
        color = [color1, color2, color3, color4])
    fig = axes.get_figure()
    plt.axhline(0, color = 'k')
    # axes.xaxis(data_frame['annee'])
    axes.legend(
        bbox_to_anchor = (legend1, legend2),
        )
    return plt.show(), fig.savefig('C:/Users/thomas.douenne/Documents/data/graphs_transports/{}.png'.format(name))


def graph_builder_carburants_no_color(data_frame, name, legend1, legend2):
    axes = data_frame.plot()
    fig = axes.get_figure()
    plt.axhline(0, color = 'k')
    # axes.xaxis(data_frame['annee'])
    axes.legend(
        bbox_to_anchor = (legend1, legend2),
        )
    return plt.show(), fig.savefig('C:/Users/thomas.douenne/Documents/data/graphs_transports/{}.png'.format(name))
