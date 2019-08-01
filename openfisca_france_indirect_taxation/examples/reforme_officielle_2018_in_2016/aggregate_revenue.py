# -*- coding: utf-8 -*-

# This script compares the revenue raised by various scenarios of reform.
# This revenue only includes energy taxes and neglect the effect on VAT.


from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.reforms.officielle_2018_in_2016 import reforme_officielle_2018_in_2016

# Simulate contribution to fuel tax reform by categories
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

variations_revenue = dict()
simulated_variables = [
    'total_taxes_energies',
    'total_taxes_energies_cce_seulement',
    'total_taxes_energies_officielle_2018_in_2016',
    'total_taxes_energies_officielle_2018_in_2016_plus_cspe',
    'total_taxes_energies_rattrapage_integral',
    'pondmen',
    ]

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform = reforme_officielle_2018_in_2016,
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

# Here I should include VAT gains
variations_revenue['revenue_cce_seulement'] = (
    (df_reforme['total_taxes_energies_cce_seulement'] - df_reforme['total_taxes_energies'])
    * df_reforme['pondmen']
    ).sum() / 1e06
variations_revenue['revenue_officielle_2018_in_2016'] = (
    (df_reforme['total_taxes_energies_officielle_2018_in_2016'] - df_reforme['total_taxes_energies'])
    * df_reforme['pondmen']
    ).sum() / 1e06
variations_revenue['revenue_officielle_2018_in_2016_plus_cspe'] = (
    (df_reforme['total_taxes_energies_officielle_2018_in_2016_plus_cspe'] - df_reforme['total_taxes_energies'])
    * df_reforme['pondmen']
    ).sum() / 1e06
variations_revenue['revenue_rattrapage_integral'] = (
    (df_reforme['total_taxes_energies_rattrapage_integral'] - df_reforme['total_taxes_energies'])
    * df_reforme['pondmen']
    ).sum() / 1e06
