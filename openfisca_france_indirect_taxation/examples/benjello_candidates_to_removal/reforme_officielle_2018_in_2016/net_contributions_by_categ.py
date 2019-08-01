# -*- coding: utf-8 -*-

# This script depicts households' net fiscal transfers from the reform.
# It is equal to the transfers received from the reform, minus the additional
# taxes paid. A positive value means the household received higher transfers than
# the increase in taxes he faced. These amounts do not take into account VAT.


from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
# from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
# elasticities = get_elasticities(data_year)
elasticities = get_elasticities_aidsills(data_year, True)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'revenu_reforme_officielle_2018_in_2016',
    'cheques_energie_officielle_2018_in_2016',
    'cheques_energie_by_energy_officielle_2018_in_2016',
    'reste_transferts_neutre_officielle_2018_in_2016',
    'rev_disp_loyerimput',
    'depenses_tot',
    'ocde10',
    'tarifs_sociaux_electricite',
    'tarifs_sociaux_gaz',
    # 'cheques_energie_integral_inconditionnel_officielle_2018_in_2016',
    ]

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'officielle_2018_in_2016',
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

for category in ['niveau_vie_decile']:  # ['niveau_vie_decile', 'age_group_pr', 'strate']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables)
    df['transferts_nets_apres_redistribution_uc'] = (
        df['cheques_energie_officielle_2018_in_2016']
        + df['reste_transferts_neutre_officielle_2018_in_2016']
        - df['revenu_reforme_officielle_2018_in_2016']
        ) / df['ocde10']

    df['regressivite_revenu'] = (df['revenu_reforme_officielle_2018_in_2016'] - df['tarifs_sociaux_electricite'] - df['tarifs_sociaux_gaz']) / df['rev_disp_loyerimput']
    df['regressivite_depenses'] = (df['revenu_reforme_officielle_2018_in_2016'] - df['tarifs_sociaux_electricite'] - df['tarifs_sociaux_gaz']) / df['depenses_tot']

    # Réalisation de graphiques
    df_to_plot = df[
        ['regressivite_revenu']
        + ['regressivite_depenses']
        + ['transferts_nets_apres_redistribution_uc']
        ]
    graph_builder_bar(df_to_plot['regressivite_revenu'], False)
    graph_builder_bar(df_to_plot['regressivite_depenses'], False)
    graph_builder_bar(df_to_plot['transferts_nets_apres_redistribution_uc'], False)
    save_dataframe_to_graph(df_to_plot, 'Monetary/transfers_by_{}.csv'.format(category))
