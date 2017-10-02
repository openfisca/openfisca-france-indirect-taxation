# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


simulated_variables = [
    'depenses_diesel',
    'depenses_diesel_ajustees_rattrapage_diesel',
    'pondmen',
    #'depenses_combustibles_liquides',
    #'depenses_gaz_ville',
    #'rev_disponible',
    #'loyer_impute',
    #'depenses_electricite',
    ]

year = 2014
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
elasticities = get_elasticities(data_year)

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'rattrapage_diesel',
    year = year,
    data_year = data_year
    )


indiv_df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

print sum(indiv_df['pondmen'] * indiv_df['depenses_diesel']) / indiv_df['pondmen'].sum()
print sum(indiv_df['pondmen'] * indiv_df['depenses_diesel_ajustees_rattrapage_diesel']) / indiv_df['pondmen'].sum()

#for var in simulated_variables:
#    print var
#    print indiv_df[var].mean()

#for category in ['niveau_vie_decile']:
#    df = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)
