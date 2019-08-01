# -*- coding: utf-8 -*-

# This script depicts households' net fiscal transfers from the reform.
# It is equal to the transfers received from the reform, minus the additional
# taxes paid. A positive value means the household received higher transfers than
# the increase in taxes he faced. These amounts do not take into account VAT.


from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
# from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
# from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
# elasticities = get_elasticities(data_year)
# elasticities = get_elasticities_aidsills(data_year, True)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'poste_11_1_1_1_1',  # repas pris dans un restaurant
    'poste_11_1_1_1_2',  # " dans un café, bars ou assimilé
    'poste_11_1_2_1_1',  # cantines scolaire et professionnelle
    'poste_11_1_3_1',  # autres dépenses de restauration : séjours hors domicile, personnes vivant hors du domicile
    'poste_11_1_3_2',  # " : cadeau offert à destination d'un autre ménage
    'poste_11_2_1_1_1',  # serices d'hébergement (hôtels, gîtes, campings, CROUS, internats)
    'poste_02_2_1',
    'poste_02_2_2',
    'poste_02_2_3',
    'poste_agrege_11',
    'rev_disp_loyerimput',
    'depenses_tot',
    'ocde10',
    'strate'
    ]

survey_scenario = SurveyScenario.create(
    # elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'reforme_tva_2019',
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

for category in ['niveau_vie_decile']:  # ['niveau_vie_decile', 'age_group_pr', 'strate']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables)

    graph_builder_bar(df[['poste_02_2_1'] + ['poste_02_2_2'] + ['poste_02_2_3']], False)

    boum

    df['check_poste_agrege_11'] = (
        df['poste_11_1_1_1_1'] + df['poste_11_1_1_1_2'] + df['poste_11_1_2_1_1']
        + df['poste_11_1_3_1'] + df['poste_11_1_3_2'] + df['poste_11_2_1_1_1']
        ) - df['poste_agrege_11']
    assert(df['check_poste_agrege_11'].min() > -1e-06)
    assert(df['check_poste_agrege_11'].max() < 1e-06)

    df['part_poste_agrege_11_rev_disp_loyerimput'] = df['poste_agrege_11'] / df['rev_disp_loyerimput']
    df['part_poste_agrege_11_depenses_tot'] = df['poste_agrege_11'] / df['depenses_tot']

    # Réalisation de graphiques
    df_to_plot = df[
        ['poste_agrege_11'] + ['part_poste_agrege_11_rev_disp_loyerimput']
        + ['part_poste_agrege_11_depenses_tot']
        ]
    graph_builder_bar(df_to_plot['part_poste_agrege_11_rev_disp_loyerimput'], False)
    graph_builder_bar(df_to_plot['part_poste_agrege_11_depenses_tot'], False)
    # save_dataframe_to_graph(df_to_plot, 'Monetary/transfers_by_{}.csv'.format(category))
