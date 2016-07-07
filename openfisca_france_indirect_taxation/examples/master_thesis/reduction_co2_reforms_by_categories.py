# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

import pandas

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph
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

for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']:
    simulated_variables = ['emissions_CO2_energies']

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = '{}'.format(reforme),
        year = year,
        data_year = data_year
        )

    for category in ['niveau_vie_decile', 'age_group_pr', 'strate_agrege']:
        pivot_table = pandas.DataFrame()
        pivot_table_reference = pandas.DataFrame()
        for values in simulated_variables:
            pivot_table = pandas.concat([
                pivot_table,
                survey_scenario.compute_pivot_table(values = [values], columns = [category])
                ])
            pivot_table_reference = pandas.concat([
                pivot_table_reference,
                survey_scenario.compute_pivot_table(values = [values], columns = ['{}'.format(category)],
                    reference = True)])

        df_reform = pivot_table.T
        df_reference = pivot_table_reference.T

        df_reform[u'Reduction in carbon emissions from reform'] = \
            df_reform['emissions_CO2_energies'] - df_reference['emissions_CO2_energies']

        # Réalisation de graphiques
        graph_builder_bar(df_reform[u'Reduction in carbon emissions from reform'])

        save_dataframe_to_graph(
            df_reform, 'Emissions_reforme/reduction_emissions_reforme_{0}_by_{1}.csv'.format(reforme, category)
            )
