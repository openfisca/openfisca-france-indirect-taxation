# -*- coding: utf-8 -*-

# This script depicts households' net fiscal transfers from the reform.
# It is equal to the transfers received from the reform, minus the additional
# taxes paid. A positive value means the household received higher transfers than
# the increase in taxes he faced. These amounts do not take into account VAT.

# Import general modules
from __future__ import division


# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
#elasticities = get_elasticities(data_year)
#elasticities = get_elasticities_aidsills(data_year, True)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'poste_11_1_1_1_1',
    'poste_11_1_1_1_2',
    'poste_11_1_2_1_1',
    'poste_11_1_3_1',
    'poste_11_1_3_2',
    #'poste_11_2_1_1_1',
    'poste_agrege_11',
    'rev_disp_loyerimput',
    'depenses_tot',
    'ocde10',
    ]

survey_scenario = SurveyScenario.create(
    #elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'reforme_tva_2019',
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

for category in ['niveau_vie_decile']: #['niveau_vie_decile', 'age_group_pr', 'strate']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables)

    df['poste_agrege_restauration'] = (
        df['poste_11_1_1_1_1']
        + df['poste_11_1_1_1_2']
        + df['poste_11_1_2_1_1']
        + df['poste_11_1_3_1']
        + df['poste_11_1_3_2']
        )

    df['part_restauration_rev_disp_loyerimput'] = df['poste_agrege_restauration'] / df['rev_disp_loyerimput']
    df['part_restauration_depenses_tot'] = df['poste_agrege_restauration'] / df['depenses_tot']

    # Réalisation de graphiques
    df_to_plot = df[
        ['poste_agrege_restauration'] + ['part_restauration_rev_disp_loyerimput']
        + ['part_restauration_depenses_tot']
        ]
    graph_builder_bar(df_to_plot['part_restauration_rev_disp_loyerimput'], False)
    graph_builder_bar(df_to_plot['part_restauration_depenses_tot'], False)
    #save_dataframe_to_graph(df_to_plot, 'Monetary/transfers_by_{}.csv'.format(category))
