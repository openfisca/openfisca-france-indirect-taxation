# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, \
    save_dataframe_to_graph
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group

# Simulate contribution to fuel tax reform by categories
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])


for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']:

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = '{}'.format(reforme),
        year = year,
        data_year = data_year
        )

    simulated_variables = [
        'total_taxes_energies',
        'rev_disp_loyerimput',
        'pondmen',
        'ocde10',
        ]

    indiv_df_reform = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
    indiv_df_use_baseline =survey_scenario.create_data_frame_by_entity(simulated_variables,
        use_baseline =True, period = year)

    menages_reform = indiv_df_reform['menage']
    menages_use_baseline =indiv_df_reference['menage']

    unite_conso = (menages_reform['ocde10'] * menages_reform['pondmen']).sum()
    contribution = (
        (menages_reform['total_taxes_energies'] - menages_reference['total_taxes_energies']) *
        menages_reference['pondmen']
        ).sum()
    contribution_unite_conso = contribution / unite_conso

    for category in ['niveau_vie_decile', 'age_group_pr', 'strate']:
        df_reform = \
            dataframe_by_group(survey_scenario, category, simulated_variables, use_baseline =False)
        df_use_baseline =\
            dataframe_by_group(survey_scenario, category, simulated_variables, use_baseline =True)

        df_reform[u'Cost of the reform after green cheques'] = (
            ((contribution_unite_conso) * df_reform['ocde10'] -
            (df_reform['total_taxes_energies'] - df_reference['total_taxes_energies']))
            )

        # Réalisation de graphiques
        graph_builder_bar(df_reform[u'Cost of the reform after green cheques'])

        #save_dataframe_to_graph(
        #    df_reform[u'Cost of the reform after green cheques'],
        #    'Contributions_reforme/Green_cheques/contribution_{0}_apres_cheques_verts_by_{1}.csv'.format(reforme,
        #    category)
        #    )
