# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

# Simulate contribution to fuel tax reform by categories
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

variations_revenue = dict()
for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']:
    simulated_variables = [
        'total_taxes_energies',
        'pondmen',
        ]

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = reforme,
        year = year,
        data_year = data_year
        )

    indiv_df_reform = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
    indiv_df_use_baseline = survey_scenario.create_data_frame_by_entity(simulated_variables,
        use_baseline =True, period = year)

    menages_reform = indiv_df_reform['menage']
    menages_use_baseline = indiv_df_reference['menage']

    variations_revenue['total_{}'.format(reforme)] = (
        (menages_reform['total_taxes_energies'] - menages_reference['total_taxes_energies'])
        * menages_reform['pondmen']
        ).sum() / 1e06
