# -*- coding: utf-8 -*-


import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter
import os
import pkg_resources
import numpy as np


from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.surveys import get_input_data_frame, SurveyScenario
from openfisca_survey_manager.survey_collections import SurveyCollection


from openfisca_france_indirect_taxation.examples.calage_bdf_cn import \
    build_df_calee_on_grospostes, build_df_calee_on_ticpe


def age_group(data):
    data['age_group'] = 6
    data.loc[data['agepr'] < 70, 'age_group'] = 5
    data.loc[data['agepr'] < 60, 'age_group'] = 4
    data.loc[data['agepr'] < 50, 'age_group'] = 3
    data.loc[data['agepr'] < 40, 'age_group'] = 2
    data.loc[data['agepr'] < 30, 'age_group'] = 1

    return data


def energy_modes(data):
    data['energy_mode'] = (
        2 * data['combustibles_liquides']
        + 1 * data['gaz_ville']
        - 1 * (data['combustibles_liquides'] * data['gaz_ville'])
        )
    data['energy_mode'] = data['energy_mode'].astype(int)

    return data


def simulate(simulated_variables, year):
    '''
    Construction de la DataFrame à partir de laquelle sera faite l'analyse des données
    '''
    input_data_frame = get_input_data_frame(year)
    data_year = year
    # input_data_frame = get_input_data_frame(year)
    survey_scenario = SurveyScenario().create(year = year, data_year = data_year)
    simulation = survey_scenario.new_simulation()
    return DataFrame(
        dict([
            (name, simulation.calculate(name, period = year)) for name in simulated_variables

            ])
        )


def simulate_df_calee_by_grosposte(simulated_variables, year):
    '''
    Construction de la DataFrame à partir de laquelle sera faite l'analyse des données
    '''
    input_data_frame = get_input_data_frame(year)
    input_data_frame_calee = build_df_calee_on_grospostes(input_data_frame, year, year)
    # TODO calage non inclus !!!
    data_year = year
    # input_data_frame = get_input_data_frame(year)
    survey_scenario = SurveyScenario().create(year = year, data_year = data_year)

    simulation = survey_scenario.new_simulation()
    return DataFrame(
        dict([
            (name, simulation.calculate(name, period = year)) for name in simulated_variables

            ])
        )


def simulate_df_calee_on_ticpe(simulated_variables, year):
    '''
    Construction de la DataFrame à partir de laquelle sera faite l'analyse des données
    '''
    input_data_frame = get_input_data_frame(year)
    input_data_frame_calee = build_df_calee_on_ticpe(input_data_frame, year, year)
    # TODO calage non inclus !!!
    data_year = year
    # input_data_frame = get_input_data_frame(year)
    survey_scenario = SurveyScenario().create(year = year, data_year = data_year)
    simulation = survey_scenario.new_simulation()
    return DataFrame(
        dict([
            (name, simulation.calculate(name, period = year)) for name in simulated_variables

            ])
        )


def wavg(groupe, var):
    '''
    Fonction qui calcule la moyenne pondérée par groupe d'une variable
    '''
    d = groupe[var]
    w = groupe['pondmen']
    return (d * w).sum() / w.sum()


def brde(data, depenses, revenu, logement):
    mediane_revenu_uc = np.median(
        data[revenu] / data['ocde10']
        )
    data['bas_revenu'] = (
        1 * (
            (data[revenu] / data['ocde10'])
            < (0.6 * mediane_revenu_uc))
        )
    if logement == 'logement':
        data['depenses_bis'] = data[depenses] / data['surfhab_d']
    else:
        data['depenses_bis'] = data[depenses].copy()
    mediane_depenses = np.median(data['depenses_bis'])
    data['depenses_elevees'] = 1 * (data['depenses_bis'] > mediane_depenses)
    data['brde_m2_{0}_{1}'.format(logement, revenu)] = (
        data['bas_revenu'] * data['depenses_elevees']
        )
    del data['depenses_bis']

    return data


def cheque_energie_logement_transport(data, depenses_logement, depenses_transport, cheque):
    data['part_cheque_logement'] = (
        data[depenses_logement] / (data[depenses_logement] + data[depenses_transport])
        )
    data['part_cheque_logement'] = data['part_cheque_logement'].fillna(0)
    data['cheque_logement'] = data['part_cheque_logement'] * data[cheque]
    data['cheque_transport'] = data[cheque] - data['cheque_logement']
    del data['part_cheque_logement']

    return data


def cheque_par_energie(data, depenses_combustibles_liquides, depenses_electricite, depenses_gaz, cheque):
    data['part_cheque_combustibles_liquides'] = (
        data[depenses_combustibles_liquides] / (data[depenses_combustibles_liquides] + data[depenses_electricite] + data[depenses_gaz])
        )
    data['part_cheque_electricite'] = (
        data[depenses_electricite] / (data[depenses_combustibles_liquides] + data[depenses_electricite] + data[depenses_gaz])
        )
    data['part_cheque_combustibles_liquides'] = data['part_cheque_combustibles_liquides'].fillna(0)
    data['part_cheque_electricite'] = data['part_cheque_electricite'].fillna(0)
    data['cheque_combustibles_liquides'] = data['part_cheque_combustibles_liquides'] * data[cheque]
    data['cheque_electricite'] = data['part_cheque_electricite'] * data[cheque]
    data['cheque_gaz_ville'] = data[cheque] - data['cheque_combustibles_liquides'] - data['cheque_electricite']
    del data['part_cheque_combustibles_liquides'], data['part_cheque_electricite']

    return data


def cheque_vert(data_reference, data_reforme, reforme):
    unite_conso = (data_reforme['ocde10'] * data_reforme['pondmen']).sum()
    contribution = (
        (data_reforme['total_taxes_energies'] - data_reference['total_taxes_energies'])
        * data_reference['pondmen']
        ).sum()
    contribution_unite_conso = contribution / unite_conso

    if reforme != 'rattrapage_diesel':
        data_reforme['part_cheque_logement'] = (
            (data_reforme['depenses_energies_logement_ajustees_{}'.format(reforme)] - data_reforme['depenses_energies_logement'])
            / ((data_reforme['depenses_energies_logement_ajustees_{}'.format(reforme)] - data_reforme['depenses_energies_logement'])
+ (data_reforme['depenses_carburants_corrigees_ajustees_{}'.format(reforme)] - data_reforme['depenses_carburants_corrigees']))
            )
        data_reforme['part_cheque_logement'] = data_reforme['part_cheque_logement'].fillna(1)
        data_reforme['part_cheque_logement'] = (
            (data_reforme['part_cheque_logement'] < 1) * data_reforme['part_cheque_logement']
            + (data_reforme['part_cheque_logement'] > 1) * 1
            )
        data_reforme['part_cheque_logement'] = (data_reforme['part_cheque_logement'] > 0) * data_reforme['part_cheque_logement']
        data_reforme['cheque_vert_logement'] = data_reforme['part_cheque_logement'] * contribution_unite_conso * data_reforme['ocde10']
        data_reforme['cheque_vert_transport'] = (1 - data_reforme['part_cheque_logement']) * contribution_unite_conso * data_reforme['ocde10']
    else:
        data_reforme['cheque_vert_transport'] = contribution_unite_conso * data_reforme['ocde10']

    return data_reforme


def collapse(dataframe, groupe, var):
    '''
    Pour une variable, fonction qui calcule la moyenne pondérée au sein de chaque groupe.
    '''
    grouped = dataframe.groupby([groupe])
    var_weighted_grouped = grouped.apply(lambda x: wavg(groupe = x, var = var))
    return var_weighted_grouped


def dataframe_by_group(survey_scenario, category, variables, use_baseline =False):
    pivot_table = pandas.DataFrame()
    period = survey_scenario.year
    if reference is not False:
        for values_reference in variables:
            pivot_table = pandas.concat([
                pivot_table,
                survey_scenario.compute_pivot_table(values = [values_reference], columns = [category],
                    use_baseline =True, period = period)])
    else:
        for values_reform in variables:
            pivot_table = pandas.concat([
                pivot_table,
                survey_scenario.compute_pivot_table(values = [values_reform], columns = [category], period = period)
                ])

    df_reform = pivot_table.T

    return df_reform


def df_weighted_average_grouped(dataframe, groupe, varlist):
    '''
    Agrège les résultats de weighted_average_grouped() en une unique dataframe pour la liste de variable 'varlist'.
    '''
    return DataFrame(
        dict([
            (var, collapse(dataframe, groupe, var)) for var in varlist
            ])
        )


# To choose color when doing graph, could put a list of colors in argument
def graph_builder_bar(graph, stacked):
    axes = graph.plot(
        kind = 'bar',
        stacked = stacked,
        )
    plt.axhline(0, color = 'k')
    axes.legend(
        bbox_to_anchor = (1.5, 1.05),
        )
    return plt.show()


def graph_builder_bar_percent(graph):
    axes = graph.plot(
        kind = 'bar',
        stacked = False,
        )
    plt.axhline(0, color = 'k')
    axes.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    # .1% means that we want one decimal
    axes.legend(
        bbox_to_anchor = (1.5, 1.05),
        )
    return plt.show()


def graph_builder_bar_list(graph, a, b):
    axes = graph.plot(
        kind = 'bar',
        stacked = True,
        color = ['#FF0000']
        )
    plt.axhline(0, color = 'k')
    axes.legend(
        bbox_to_anchor = (a, b),
        )
    return plt.show()


def graph_builder_line_percent(graph):
    axes = graph.plot(
        )
    plt.axhline(0, color = 'k')
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
    return plt.show()


def graph_builder_line(graph):
    axes = graph.plot(
        )
    plt.axhline(0, color = 'k')
    axes.legend(
        bbox_to_anchor = (1, 0.25),
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


def percent_formatter(x, pos = 0):
    return '%1.0f%%' % (100 * x)


def precarite(data, brde, tee, logement):
    if logement == 'logement':
        data['precarite_{}'.format(logement)] = (
            data[brde] + data[tee] + data['froid_4_criteres_3_deciles']
            - (data[brde] * data[tee]) - (data[brde] * data['froid_4_criteres_3_deciles'])
            - (data[tee] * data['froid_4_criteres_3_deciles']) + (data[brde] * data[tee] * data['froid_4_criteres_3_deciles'])
            )
    else:
        data['precarite_{}'.format(logement)] = (
            data[brde] + data[tee] - (data[brde] * data[tee])
            )

    return data


def save_dataframe_to_graph(dataframe, file_name):
    assets_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
        )
    return dataframe.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets', 'to_graph',
        file_name), sep = ';')


def tee_10_3(data, depenses, revenu, logement):
    data['tee_10_3_{0}_{1}'.format(revenu, logement)] = \
        1 * ((data[depenses] / data[revenu]) > 0.1) * (data['niveau_vie_decile'] < 4)

    return data
