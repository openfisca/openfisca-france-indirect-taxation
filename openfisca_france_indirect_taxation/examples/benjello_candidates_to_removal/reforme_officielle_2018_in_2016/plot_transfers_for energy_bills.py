# -*- coding: utf-8 -*-

# This script ...







from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'tarifs_sociaux_electricite',
    'tarifs_sociaux_gaz',
    'cheques_energie_officielle_2018_in_2016',
    #'cheques_energie_integral_inconditionnel_officielle_2018_in_2016',
    ]

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'officielle_2018_in_2016',
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
for category in ['niveau_vie_decile']: #['niveau_vie_decile', 'age_group_pr', 'strate']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables)
    graph_builder_bar(df, False)
