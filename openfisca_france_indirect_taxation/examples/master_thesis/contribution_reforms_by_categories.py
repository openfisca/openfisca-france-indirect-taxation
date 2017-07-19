# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_line_percent, graph_builder_bar, \
    save_dataframe_to_graph, dataframe_by_group
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
    simulated_variables = [
        'total_taxes_energies',
        'depenses_energies',
        'rev_disp_loyerimput',
        'somme_coicop12'
        ]

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = reforme,
        year = year,
        data_year = data_year
        )

    for category in ['niveau_vie_decile', 'age_group_pr', 'strate_agrege']:
        df_reform = \
            dataframe_by_group(survey_scenario, category, simulated_variables, reference = False)
        df_reference = \
            dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)

        df_reform['Additional effort rate on TICPE reform - expenditures'] = (
            ((df_reform['total_taxes_energies']) - (df_reference['total_taxes_energies'])) / df_reform['somme_coicop12']
            )
        df_reform['Additional effort rate on TICPE reform - income'] = (
            ((df_reform['total_taxes_energies']) - (df_reference['total_taxes_energies'])) /
            df_reform['rev_disp_loyerimput']
            )

        # Réalisation de graphiques
        # graph_builder_bar(df_reform['total_taxes_energies']) - (df_reference['total_taxes_energies'])
        graph_builder_line_percent(
            df_reform[['Additional effort rate on TICPE reform - expenditures',
            'Additional effort rate on TICPE reform - income']]
            )

        save_dataframe_to_graph(
            df_reform,
            'Contributions_reforme/Before_redistribution/contribution_additionnelles_reforme_{0}_{1}.csv'.format(reforme, category)
            )
