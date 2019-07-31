# -*- coding: utf-8 -*-

# This script computes the reduction in CO2 emissions from the reform.
# The results are given per energy, and in total.


# Import general modules


# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

# Simulate contribution to fuel tax reform by categories
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
#elasticities = get_elasticities(data_year)
elasticities = get_elasticities_aidsills(data_year, False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

emissions_cce_seulement = dict()
emissions_officielle = dict()
emissions_officielle_plus_cspe = dict()
emissions_rattrapage_integral = dict()

simulated_variables = [
    'emissions_CO2_carburants',
    'emissions_CO2_carburants_cce_seulement',
    'emissions_CO2_carburants_officielle_2018_in_2016',
    'emissions_CO2_carburants_rattrapage_integral',
    'emissions_CO2_combustibles_liquides',
    'emissions_CO2_combustibles_liquides_officielle_2018_in_2016',
    'emissions_CO2_diesel',
    'emissions_CO2_diesel_officielle_2018_in_2016',
    'emissions_CO2_electricite_cspe',
    'emissions_CO2_electricite',
    'emissions_CO2_energies_totales',
    'emissions_CO2_energies_totales_officielle_2018_in_2016',
    'emissions_CO2_energies_totales_officielle_2018_in_2016_plus_cspe',
    'emissions_CO2_essence',
    'emissions_CO2_essence_officielle_2018_in_2016',
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

# Carburants
emissions_cce_seulement['carburants'] = (
    (df_reforme['emissions_CO2_carburants'] - df_reforme['emissions_CO2_carburants_cce_seulement'])
    * df_reforme['pondmen']
    ).sum() / 1e06
emissions_officielle['carburants'] = (
    (df_reforme['emissions_CO2_carburants'] - df_reforme['emissions_CO2_carburants_officielle_2018_in_2016'])
    * df_reforme['pondmen']
    ).sum() / 1e06
emissions_officielle_plus_cspe['carburants'] = emissions_officielle['carburants']
emissions_rattrapage_integral['carburants'] = (
    (df_reforme['emissions_CO2_carburants'] - df_reforme['emissions_CO2_carburants_rattrapage_integral'])
    * df_reforme['pondmen']
    ).sum() / 1e06

# Combustibles liquides
emissions_cce_seulement['combustibles_liquides'] = (
    (df_reforme['emissions_CO2_combustibles_liquides']
- df_reforme['emissions_CO2_combustibles_liquides_officielle_2018_in_2016'])
    * df_reforme['pondmen']
    ).sum() / 1e06
emissions_officielle['combustibles_liquides'] = emissions_cce_seulement['combustibles_liquides']
emissions_officielle_plus_cspe['combustibles_liquides'] = emissions_cce_seulement['combustibles_liquides']
emissions_rattrapage_integral['combustibles_liquides'] = 0

# Diesel
emissions_officielle['diesel'] = (
    (df_reforme['emissions_CO2_diesel'] - df_reforme['emissions_CO2_diesel_officielle_2018_in_2016'])
    * df_reforme['pondmen']
    ).sum() / 1e06

# Electricité
emissions_cce_seulement['electricite'] = 0
emissions_officielle['electricite'] = 0
emissions_officielle_plus_cspe['electricite'] = (
    (df_reforme['emissions_CO2_electricite']
- df_reforme['emissions_CO2_electricite_cspe'])
    * df_reforme['pondmen']
    ).sum() / 1e06
emissions_rattrapage_integral['electricite'] = 0

# Essence
emissions_officielle['essence'] = (
    (df_reforme['emissions_CO2_essence'] - df_reforme['emissions_CO2_essence_officielle_2018_in_2016'])
    * df_reforme['pondmen']
    ).sum() / 1e06

# Gaz de ville
emissions_cce_seulement['gaz_ville'] = (
    (df_reforme['emissions_CO2_gaz_ville'] - df_reforme['emissions_CO2_gaz_ville_officielle_2018_in_2016'])
    * df_reforme['pondmen']
    ).sum() / 1e06
emissions_officielle['gaz_ville'] = emissions_cce_seulement['gaz_ville']
emissions_officielle_plus_cspe['gaz_ville'] = emissions_cce_seulement['gaz_ville']
emissions_rattrapage_integral['gaz_ville'] = 0

# Total logement
emissions_cce_seulement['total_logement'] = (
    emissions_cce_seulement['gaz_ville']
    + emissions_cce_seulement['combustibles_liquides']
    + emissions_cce_seulement['electricite']
    )
emissions_officielle['total_logement'] = (
    emissions_officielle['gaz_ville']
    + emissions_officielle['combustibles_liquides']
    + emissions_officielle['electricite']
    )
emissions_officielle_plus_cspe['total_logement'] = (
    emissions_officielle_plus_cspe['gaz_ville']
    + emissions_officielle_plus_cspe['combustibles_liquides']
    + emissions_officielle_plus_cspe['electricite']
    )
emissions_rattrapage_integral['total_logement'] = (
    emissions_rattrapage_integral['gaz_ville']
    + emissions_rattrapage_integral['combustibles_liquides']
    + emissions_rattrapage_integral['electricite']
    )

# Total
emissions_cce_seulement['total'] = (
    emissions_cce_seulement['total_logement']
    + emissions_cce_seulement['carburants']
    )
emissions_officielle['total'] = (
    emissions_officielle['total_logement']
    + emissions_officielle['carburants']
    )
emissions_officielle_plus_cspe['total'] = (
    emissions_officielle_plus_cspe['total_logement']
    + emissions_officielle_plus_cspe['carburants']
    )
emissions_rattrapage_integral['total'] = (
    emissions_rattrapage_integral['total_logement']
    + emissions_rattrapage_integral['carburants']
    )
