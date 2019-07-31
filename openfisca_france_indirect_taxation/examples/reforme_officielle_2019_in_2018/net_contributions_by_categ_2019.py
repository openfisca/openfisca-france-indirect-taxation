# -*- coding: utf-8 -*-

# This script depicts households' net fiscal transfers from the reform.
# It is equal to the transfers received from the reform, minus the additional
# taxes paid. A positive value means the household received higher transfers than
# the increase in taxes he faced. These amounts do not take into account VAT.


# Import general modules


# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
#elasticities = get_elasticities(data_year)
elasticities = get_elasticities_aidsills(data_year, True)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'revenu_reforme_officielle_2019_in_2018',
    'cheques_energie_officielle_2019_in_2018',
    'reste_transferts_neutre_officielle_2019_in_2018',
    'rev_disponible',
    'depenses_tot',
    'ocde10',
    'tarifs_sociaux_electricite',
    'tarifs_sociaux_gaz',
    'total_taxes_energies_officielle_2019_in_2018',
    'total_taxes_energies',
    'cheques_energie_majore_officielle_2019_in_2018',
    'cheques_energie_philippe_officielle_2019_in_2018',
    'ticpe_totale_officielle_2019_in_2018',
    'pondmen'
    # 'cheques_energie_integral_inconditionnel_officielle_2019_in_2018',
    ]

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'officielle_2019_in_2018',
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
print((df_reforme['pondmen'] * df_reforme['ticpe_totale_officielle_2019_in_2018']).sum() / 1000000000)


for category in ['niveau_vie_decile']:  # ['niveau_vie_decile', 'age_group_pr', 'strate']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables)

    df['cout_reforme'] = df['total_taxes_energies_officielle_2019_in_2018'] - df['total_taxes_energies']
    df['cout_reforme_cheque_majore'] = df['cout_reforme'] + df['cheques_energie_officielle_2019_in_2018'] - df['cheques_energie_majore_officielle_2019_in_2018']
    df['cout_reforme_cheque_philippe'] = df['cout_reforme'] + df['cheques_energie_officielle_2019_in_2018'] - df['cheques_energie_philippe_officielle_2019_in_2018']

    df['regressivite_revenu'] = df['cout_reforme'] / df['rev_disponible']
    df['regressivite_depenses'] = df['cout_reforme'] / df['depenses_tot']
    df['regressivite_revenu_cheque_philippe'] = df['cout_reforme_cheque_philippe'] / df['rev_disponible']

    # Réalisation de graphiques
    df_to_plot = df[
        ['cout_reforme']
        + ['cout_reforme_cheque_majore']
        + ['cout_reforme_cheque_philippe']
        + ['regressivite_revenu_cheque_philippe']
        + ['regressivite_revenu']
        + ['regressivite_depenses']
        ]
    graph_builder_bar(df_to_plot['cout_reforme'], False)
    graph_builder_bar(df_to_plot['cout_reforme_cheque_majore'], False)
    graph_builder_bar(df_to_plot['cout_reforme_cheque_philippe'], False)
    graph_builder_bar(df_to_plot['regressivite_revenu'], False)
    graph_builder_bar(df_to_plot['regressivite_depenses'], False)

    df_reforme['cout_reforme_cheque_officiel'] = (
        df_reforme['total_taxes_energies_officielle_2019_in_2018'] - df_reforme['total_taxes_energies']
        )
    df_reforme['cout_reforme_cheque_majore'] = (
        df_reforme['cout_reforme_cheque_officiel'] + df_reforme['cheques_energie_officielle_2019_in_2018'] - df_reforme['cheques_energie_majore_officielle_2019_in_2018']
        )
    df_reforme['cout_reforme_cheque_philippe'] = (
        df_reforme['cout_reforme_cheque_officiel'] + df_reforme['cheques_energie_officielle_2019_in_2018'] - df_reforme['cheques_energie_philippe_officielle_2019_in_2018']
        )
    print((df_reforme['cout_reforme_cheque_officiel'] * df_reforme['pondmen']).sum() / 1000000)
    print((df_reforme['cout_reforme_cheque_majore'] * df_reforme['pondmen']).sum() / 1000000)
    print((df_reforme['cout_reforme_cheque_philippe'] * df_reforme['pondmen']).sum() / 1000000)

    print((df_reforme['cheques_energie_officielle_2019_in_2018'] * df_reforme['pondmen']).sum() / 1000000)
    print((df_reforme['cheques_energie_majore_officielle_2019_in_2018'] * df_reforme['pondmen']).sum() / 1000000)
    print((df_reforme['cheques_energie_philippe_officielle_2019_in_2018'] * df_reforme['pondmen']).sum() / 1000000)
