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
# from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.reforms.officielle_2019_in_2017 import officielle_2019_in_2017

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
# elasticities = get_elasticities(data_year)
elasticities = get_elasticities_aidsills(data_year, True)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'revenu_reforme_officielle_2019_in_2017',
    'cheques_energie_officielle_2019_in_2017',
    'cheques_energie_philippe_officielle_2019_in_2017',
    'cheques_energie_majore_officielle_2019_in_2017',
    'reste_transferts_neutre_officielle_2019_in_2017',
    'rev_disp_loyerimput',
    'rev_disponible',
    'niveau_de_vie',
    'depenses_tot',
    'ocde10',
    'tarifs_sociaux_electricite',
    'tarifs_sociaux_gaz',
    'pondmen'
    ]

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform = officielle_2019_in_2017,
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df_reforme['cheque'] = 1 * (df_reforme['cheques_energie_officielle_2019_in_2017'] > 0)
df_reforme['cheque_philippe'] = 1 * (df_reforme['cheques_energie_philippe_officielle_2019_in_2017'] > 0)
print((df_reforme['pondmen'] * df_reforme['cheque']).sum())
print((df_reforme['pondmen'] * df_reforme['cheque_philippe']).sum())

for category in ['niveau_vie_decile']:  # ['niveau_vie_decile', 'age_group_pr', 'strate']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables)

    df['cout_reforme_uc_avant_cheque_energie'] = (
        df['revenu_reforme_officielle_2019_in_2017']
        - df['tarifs_sociaux_electricite'] - df['tarifs_sociaux_gaz']
        )
    df['cout_reforme_uc_cheque_officiel'] = (
        df['revenu_reforme_officielle_2019_in_2017']
        - df['cheques_energie_officielle_2019_in_2017']
        )
    df['cout_reforme_uc_cheque_majore'] = (
        df['revenu_reforme_officielle_2019_in_2017']
        - df['cheques_energie_majore_officielle_2019_in_2017']
        )
    df['cout_reforme_uc_cheque_philippe'] = (
        df['revenu_reforme_officielle_2019_in_2017']
        - df['cheques_energie_philippe_officielle_2019_in_2017']
        )

    df['taux_effort_avant_cheque_energie'] = df['cout_reforme_uc_avant_cheque_energie'] / df['rev_disponible']
    df['taux_effort_cheque_officiel'] = df['cout_reforme_uc_cheque_officiel'] / df['rev_disponible']
    df['taux_effort_cheque_majore'] = df['cout_reforme_uc_cheque_majore'] / df['rev_disponible']
    df['taux_effort_cheque_philippe'] = df['cout_reforme_uc_cheque_philippe'] / df['rev_disponible']

    graph_builder_bar(df['niveau_de_vie'], False)
    graph_builder_bar(df['cout_reforme_uc_avant_cheque_energie'], False)
    graph_builder_bar(df['cout_reforme_uc_cheque_officiel'], False)
    graph_builder_bar(df['cout_reforme_uc_cheque_philippe'], False)
    graph_builder_bar(df['cout_reforme_uc_cheque_majore'], False)
    graph_builder_bar(df['taux_effort_cheque_philippe'], False)

    # Calcul du revenu de la taxe :
    df_reforme['cout_reforme_uc_avant_cheque_energie'] = (
        df_reforme['revenu_reforme_officielle_2019_in_2017']
        - df_reforme['tarifs_sociaux_electricite'] - df_reforme['tarifs_sociaux_gaz']
        )
    df_reforme['cout_reforme_uc_cheque_officiel'] = (
        df_reforme['revenu_reforme_officielle_2019_in_2017']
        - df_reforme['cheques_energie_officielle_2019_in_2017']
        )
    df_reforme['cout_reforme_uc_cheque_majore'] = (
        df_reforme['revenu_reforme_officielle_2019_in_2017']
        - df_reforme['cheques_energie_majore_officielle_2019_in_2017']
        )
    df_reforme['cout_reforme_uc_cheque_philippe'] = (
        df_reforme['revenu_reforme_officielle_2019_in_2017']
        - df_reforme['cheques_energie_philippe_officielle_2019_in_2017']
        )
    print((df_reforme['cout_reforme_uc_avant_cheque_energie'] * df_reforme['pondmen']).sum() / 1e6)
    print((df_reforme['cout_reforme_uc_cheque_officiel'] * df_reforme['pondmen']).sum() / 1e6)
    print((df_reforme['cout_reforme_uc_cheque_majore'] * df_reforme['pondmen']).sum() / 1e6)
    print((df_reforme['cout_reforme_uc_cheque_philippe'] * df_reforme['pondmen']).sum() / 1e6)
    print((df_reforme['cheques_energie_officielle_2019_in_2017'] * df_reforme['pondmen']).sum() / 1e6)
    print((df_reforme['cheques_energie_majore_officielle_2019_in_2017'] * df_reforme['pondmen']).sum() / 1e6)
    print((df_reforme['cheques_energie_philippe_officielle_2019_in_2017'] * df_reforme['pondmen']).sum() / 1e6)
