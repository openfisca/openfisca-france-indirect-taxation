# -*- coding: utf-8 -*-

# This script depicts households' net fiscal transfers from the reform.
# It is equal to the transfers received from the reform, minus the additional
# taxes paid. A positive value means the household received higher transfers than
# the increase in taxes he faced. These amounts do not take into account VAT.


from openfisca_france_indirect_taxation.examples.utils_example import (
    dataframe_by_group,
    graph_builder_bar,
    )
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.reforms.reforme_tva_2019 import reforme_tva_2019


inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'poste_11_1_1_1_1',
    'poste_11_1_1_1_2',
    'poste_11_1_2_1_1',
    'poste_11_1_3_1',
    'poste_11_1_3_2',
    # 'poste_11_2_1_1_1',
    'poste_agrege_11',
    'rev_disp_loyerimput',
    'depenses_tot',
    'ocde10',
    ]

survey_scenario = SurveyScenario.create(
    inflation_kwargs = inflation_kwargs,
    reform = reforme_tva_2019,
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

for category in ['niveau_vie_decile']:  # ['niveau_vie_decile', 'age_group_pr', 'strate']:
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
        ['poste_agrege_restauration', 'part_restauration_rev_disp_loyerimput']
        + ['part_restauration_depenses_tot']
        ]
    graph_builder_bar(df_to_plot['part_restauration_rev_disp_loyerimput'], False)
    graph_builder_bar(df_to_plot['part_restauration_depenses_tot'], False)
    # save_dataframe_to_graph(df_to_plot, 'Monetary/transfers_by_{}.csv'.format(category))
