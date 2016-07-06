# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

import pandas

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_line_percent, graph_builder_bar, \
    save_dataframe_to_graph
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

for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2014_2015', 'cce_2014_2016']:
    simulated_variables = [
        'difference_contribution_energie_{}'.format(reforme),
        'depenses_energies',
        'rev_disp_loyerimput',
        'somme_coicop12'
        ]

    if reforme[:3] != 'cce':
        survey_scenario = SurveyScenario.create(
            elasticities = elasticities,
            inflation_kwargs = inflation_kwargs,
            reform_key = '{}'.format(reforme),
            year = year,
            data_year = data_year
            )
    else:
        survey_scenario = SurveyScenario.create(
            elasticities = elasticities,
            inflation_kwargs = inflation_kwargs,
            reform_key = 'contribution_climat_energie_reforme',
            year = year,
            data_year = data_year
            )

    for category in ['niveau_vie_decile', 'age_group_pr', 'strate_agrege']:
        pivot_table = pandas.DataFrame()
        for values in simulated_variables:
            pivot_table = pandas.concat([
                pivot_table,
                survey_scenario.compute_pivot_table(values = [values], columns = ['{}'.format(category)])
                ])
        df = pivot_table.T
        df['Additional effort rate on TICPE reform - expenditures'] = \
            df['difference_contribution_energie_{}'.format(reforme)] / df['somme_coicop12']
        df['Additional effort rate on TICPE reform - income'] = \
            df['difference_contribution_energie_{}'.format(reforme)] / df['rev_disp_loyerimput']
        save_dataframe_to_graph(
            df, 'Contributions_reforme/Before_redistribution/contribution_additionnelles_reforme_{0}_{1}.csv'.format(reforme, category)
            )

        # Réalisation de graphiques
        graph_builder_bar(df['difference_contribution_energie_{}'.format(reforme)])
        graph_builder_line_percent(
            df[['Additional effort rate on TICPE reform - expenditures',
            'Additional effort rate on TICPE reform - income']]
            )
