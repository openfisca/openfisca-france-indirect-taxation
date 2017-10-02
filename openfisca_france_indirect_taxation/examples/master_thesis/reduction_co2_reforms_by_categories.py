# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

# Simulate contribution to fuel tax reform by categories
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']:
    simulated_variables = ['emissions_CO2_energies_totales']

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = '{}'.format(reforme),
        year = year,
        data_year = data_year
        )

    for category in ['niveau_vie_decile', 'age_group_pr', 'strate']:
        df_reform = \
            dataframe_by_group(survey_scenario, category, simulated_variables, reference = False)
        df_reference = \
            dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)

        df_reform[u'Reduction in carbon emissions from reform'] = \
            df_reform['emissions_CO2_energies_totales'] - df_reference['emissions_CO2_energies_totales']

        # Réalisation de graphiques
        graph_builder_bar(df_reform[u'Reduction in carbon emissions from reform'])

        #save_dataframe_to_graph(
        #    df_reform, 'Emissions_reforme/reduction_emissions_reforme_{0}_by_{1}.csv'.format(reforme, category)
        #    )
