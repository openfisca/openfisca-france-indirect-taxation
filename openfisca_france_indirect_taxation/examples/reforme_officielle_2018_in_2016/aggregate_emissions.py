# -*- coding: utf-8 -*-

# This script computes the reduction in CO2 emissions from the reform.
# The results are given per energy, and in total.


# Import general modules
from __future__ import division

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

# Simulate contribution to fuel tax reform by categories
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

variations_emissions = dict()
simulated_variables = [
    'emissions_CO2_carburants',
    'emissions_CO2_carburants_officielle_2018_in_2016',
    'emissions_CO2_combustibles_liquides',
    'emissions_CO2_combustibles_liquides_officielle_2018_in_2016',
    'emissions_CO2_energies_totales',
    'emissions_CO2_energies_totales_officielle_2018_in_2016',
    'emissions_CO2_gaz_ville',
    'emissions_CO2_gaz_ville_officielle_2018_in_2016',
    'pondmen',
    ]

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'officielle_2018_in_2016',
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

variations_emissions['carburants'] = (
    (df_reforme['emissions_CO2_carburants'] - df_reforme['emissions_CO2_carburants_officielle_2018_in_2016']) *
    df_reforme['pondmen']
    ).sum() / 1e06

variations_emissions['gaz_ville'] = (
    (df_reforme['emissions_CO2_gaz_ville'] - df_reforme['emissions_CO2_gaz_ville_officielle_2018_in_2016']) *
    df_reforme['pondmen']
    ).sum() / 1e06
variations_emissions['combustibles_liquides'] = (
    (df_reforme['emissions_CO2_combustibles_liquides'] -
    df_reforme['emissions_CO2_combustibles_liquides_officielle_2018_in_2016']) *
    df_reforme['pondmen']
    ).sum() / 1e06

variations_emissions['total_logement'] = (
    variations_emissions['gaz_ville'] +
    variations_emissions['combustibles_liquides']
    ).sum()

variations_emissions['total'] = (
    (df_reforme['emissions_CO2_energies_totales'] - df_reforme['emissions_CO2_energies_totales_officielle_2018_in_2016']) *
    df_reforme['pondmen']
    ).sum() / 1e06
