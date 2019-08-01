# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_line, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

#
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
# del inflation_kwargs['inflator_by_variable']['somme_coicop12']

simulated_variables = ['emissions_CO2_carburants', 'emissions_CO2_energies_logement', 'emissions_CO2_energies_totales']

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    # inflation_kwargs = inflation_kwargs,
    year = year,
    data_year = data_year
    )
for category in ['niveau_vie_decile', 'age_group_pr', 'strate']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables, use_baseline =True)

    # Réalisation de graphiques
    graph_builder_line(df)
    # save_dataframe_to_graph(df, 'Emissions/emissions_by_{}.csv'.format(category))
