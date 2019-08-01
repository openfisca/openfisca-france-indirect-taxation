# -*- coding: utf-8 -*-

# This script computes the share of households that financial lose from the reform,
# after transfers. This share is given by category (in particular by income deciles).
# Losses are computed on the basis of total financial gains and losses : a person
# loses from the reform if the transfer is lower than the additional spending induced
# by the reform.


import pandas as pd

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.utils_example import (
    graph_builder_bar, age_group, energy_modes)
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


year = 2016
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
elasticities = get_elasticities(data_year)

reforme = 'officielle_2018_in_2016'

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = reforme,
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'emissions_CO2_energies_totales',
    'combustibles_liquides',
    'gaz_ville',
    'niveau_vie_decile',
    'pondmen',
    'strate',
    'agepr',
    'ocde10'
    ]

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df_reforme = age_group(df_reforme)
df_reforme = energy_modes(df_reforme)


def emissions_by_categ(data, categ):

    min_categ = data[categ].min()
    max_categ = data[categ].max()
    elements_categ = list(range(min_categ, max_categ + 1))
    df_to_plot = pd.DataFrame(index = elements_categ, columns = ['emissions_CO2'])

    for element in range(min_categ, max_categ + 1):
        df = data.query('{0} == {1}'.format(categ, element))
        df_to_plot['emissions_CO2'][element] = \
            (df['emissions_CO2_energies_totales'] / df['ocde10'] * df['pondmen']).sum() / df['pondmen'].sum()

    graph_builder_bar(df_to_plot, False)
    save_dataframe_to_graph(df_to_plot, 'Emissions/co2_emissions_by_{}.csv'.format(categ))

    return df_to_plot


df_to_plot = emissions_by_categ(df_reforme, 'niveau_vie_decile')
df_to_plot = emissions_by_categ(df_reforme, 'strate')
df_to_plot = emissions_by_categ(df_reforme, 'age_group')
df_to_plot = emissions_by_categ(df_reforme, 'energy_mode')
