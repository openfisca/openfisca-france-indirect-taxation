# -*- coding: utf-8 -*-

# This script computes the share of households that financial lose from the reform,
# after transfers. This share is given by category (in particular by income deciles).
# Losses are computed on the basis of total financial gains and losses : a person
# loses from the reform if the transfer is lower than the additional spending induced
# by the reform.


import pandas as pd

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar_percent, save_dataframe_to_graph
# from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


year = 2016
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
# elasticities = get_elasticities(data_year)
elasticities = get_elasticities_aidsills(data_year, True)

reforme = 'officielle_2018_in_2016'

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform = reforme,
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'revenu_reforme_officielle_2018_in_2016',
    'pertes_financieres_avant_redistribution_officielle_2018_in_2016',
    'cheques_energie_officielle_2018_in_2016',
    'cheques_energie_by_energy_officielle_2018_in_2016',
    'reste_transferts_neutre_officielle_2018_in_2016',
    'niveau_vie_decile',
    'pondmen',
    ]

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df_reforme['gains_cheque_officiel'] = (
    df_reforme['cheques_energie_officielle_2018_in_2016']
    + df_reforme['reste_transferts_neutre_officielle_2018_in_2016']
    - df_reforme['pertes_financieres_avant_redistribution_officielle_2018_in_2016']
    )
df_reforme['perdant_total_cheque_officiel'] = 1 * (df_reforme['gains_cheque_officiel'] < 0)

df_reforme['transfert_net_cheque_officiel'] = (
    df_reforme['cheques_energie_officielle_2018_in_2016']
    + df_reforme['reste_transferts_neutre_officielle_2018_in_2016']
    - df_reforme['revenu_reforme_officielle_2018_in_2016']
    )
df_reforme['perdant_fiscal_cheque_officiel'] = 1 * (df_reforme['transfert_net_cheque_officiel'] < 0)


df_by_categ = pd.DataFrame(index = list(range(1, 11)), columns = ['perdant_total_cheque_officiel', 'perdant_fiscal_cheque_officiel'])
for i in range(1, 11):
    part_perdants_total_officiel = (
        float(df_reforme.query('niveau_vie_decile == {}'.format(i)).query('perdant_total_cheque_officiel == 1')['pondmen'].sum())
        / df_reforme.query('niveau_vie_decile == {}'.format(i))['pondmen'].sum()
        )
    df_by_categ['perdant_total_cheque_officiel'][i] = part_perdants_total_officiel

    part_perdants_fiscal_officiel = (
        float(df_reforme.query('niveau_vie_decile == {}'.format(i)).query('perdant_fiscal_cheque_officiel == 1')['pondmen'].sum())
        / df_reforme.query('niveau_vie_decile == {}'.format(i))['pondmen'].sum()
        )
    df_by_categ['perdant_fiscal_cheque_officiel'][i] = part_perdants_fiscal_officiel


graph_builder_bar_percent(df_by_categ[['perdant_fiscal_cheque_officiel']])
save_dataframe_to_graph(df_by_categ, 'Monetary/share_loosers_within_income_deciles.csv')
