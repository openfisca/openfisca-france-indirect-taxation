# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

# Simulate contribution to fuel tax reform by categories
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
del inflation_kwargs['inflator_by_variable']['somme_coicop12']

variations_emissions = dict()
for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']:
    simulated_variables = [
        'emissions_CO2_energies',
        'emissions_CO2_carburants',
        'emissions_CO2_electricite',
        'emissions_CO2_gaz',
        'emissions_CO2_fioul_domestique',
        'pondmen',
        ]

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = '{}'.format(reforme),
        year = year,
        data_year = data_year
        )

    indiv_df_reform = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
    indiv_df_reference = survey_scenario.create_data_frame_by_entity(simulated_variables,
        reference = True, period = year)

    menages_reform = indiv_df_reform['menages']
    menages_reference = indiv_df_reference['menages']

    variations_emissions['carburants_{}'.format(reforme)] = (
        (menages_reform['emissions_CO2_carburants'] - menages_reference['emissions_CO2_carburants']) *
        menages_reform['pondmen']
        ).sum() / 1e06

    if reforme != 'rattrapage_diesel':
        variations_emissions['gaz_{}'.format(reforme)] = (
            (menages_reform['emissions_CO2_gaz'] - menages_reference['emissions_CO2_gaz']) *
            menages_reform['pondmen']
            ).sum() / 1e06
        variations_emissions['fioul_domestique_{}'.format(reforme)] = (
            (menages_reform['emissions_CO2_fioul_domestique'] -
            menages_reference['emissions_CO2_fioul_domestique']) *
            menages_reform['pondmen']
            ).sum() / 1e06

        if reforme == 'taxe_carbone':
            variations_emissions['electricite_{}'.format(reforme)] = (
                (menages_reform['emissions_CO2_electricite'] -
                menages_reference['emissions_CO2_electricite']) *
                menages_reform['pondmen']
                ).sum() / 1e06

            variations_emissions['total_logement_{}'.format(reforme)] = (
                variations_emissions['gaz_{}'.format(reforme)] +
                variations_emissions['fioul_domestique_{}'.format(reforme)] +
                variations_emissions['electricite_{}'.format(reforme)]
                ).sum()
        else:
            variations_emissions['total_logement_{}'.format(reforme)] = (
                variations_emissions['gaz_{}'.format(reforme)] +
                variations_emissions['fioul_domestique_{}'.format(reforme)]
                ).sum()

    variations_emissions['total_{}'.format(reforme)] = (
        (menages_reform['emissions_CO2_energies'] - menages_reference['emissions_CO2_energies']) *
        menages_reform['pondmen']
        ).sum() / 1e06
