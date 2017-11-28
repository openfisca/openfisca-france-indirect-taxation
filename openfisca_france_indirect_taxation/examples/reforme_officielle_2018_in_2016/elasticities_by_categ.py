# -*- coding: utf-8 -*-

from __future__ import division

import pandas as pd

from openfisca_france_indirect_taxation.examples.utils_example import \
    dataframe_by_group, graph_builder_bar, save_dataframe_to_graph, energy_modes
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


year = 2016
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
elasticities = get_elasticities(data_year)

reforme = 'officielle_2018_in_2016'

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = reforme,
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'elas_price_1_1',
    'elas_price_2_2',
    'elas_price_3_3',
    'elas_exp_1',
    'elas_exp_2',
    'elas_exp_3',
    'niveau_vie_decile',
    'strate',
    'age_group_pr',
    'pondmen',
    'combustibles_liquides',
    'gaz_ville',
    'depenses_carburants_corrigees',
    'depenses_energies_logement',
    'depenses_tot',
    ]

df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df = energy_modes(df)

def elasticities_by_categ(df, categ):
    i_min = df[categ].min()
    i_max = df[categ].max()
    df_to_plot = pd.DataFrame(index = range(i_min, i_max+1), columns = ['elas_transports', 'elas_housing'])
    for i in range(i_min, i_max+1):
        df_categ = df.query('{0} == {1}'.format(categ, i))
        df_to_plot['elas_transports'][i] = df_categ['elas_price_1_1'].mean()
        df_to_plot['elas_housing'][i] = df_categ['elas_price_2_2'].mean()
  
    graph_builder_bar(df_to_plot, False)
    save_dataframe_to_graph(df_to_plot, 'Elasticities/elasticities_by_{}.csv'.format(categ))

    return df_to_plot

df_to_plot = elasticities_by_categ(df, 'niveau_vie_decile')
df_to_plot = elasticities_by_categ(df, 'strate')
df_to_plot = elasticities_by_categ(df, 'age_group_pr')
df_to_plot = elasticities_by_categ(df, 'energy_mode')

df['part_carbu'] = (df['depenses_carburants_corrigees'] * df['pondmen']) / (df['depenses_carburants_corrigees'] * df['pondmen']).sum()

elas_price_1_ponderee = (df['part_carbu'] * df['elas_price_1_1']).sum()
elas_exp_1_ponderee = (df['part_carbu'] * df['elas_exp_1']).sum()

df['part_housing'] = (df['depenses_energies_logement'] * df['pondmen']) / (df['depenses_energies_logement'] * df['pondmen']).sum()
elas_price_2_ponderee = (df['part_housing'] * df['elas_price_2_2']).sum()
elas_exp_2_ponderee = (df['part_housing'] * df['elas_exp_2']).sum()

df['depenses_other'] = df['depenses_tot'] - df['depenses_carburants_corrigees'] - df['depenses_energies_logement']
df.loc[df['depenses_other'] < 0, 'depenses_other'] = 0

df['part_other'] = (df['depenses_other'] * df['pondmen']) / (df['depenses_other'] * df['pondmen']).sum()
elas_price_3_ponderee = (df['part_other'] * df['elas_price_3_3']).sum()
elas_exp_3_ponderee = (df['part_other'] * df['elas_exp_3']).sum()

categ = 'strate'

positive_elas = df.query('energy_mode != 0').query('elas_price_2_2 == 0')['pondmen'].sum()
sum_pop = df.query('energy_mode != 0')['pondmen'].sum()
ratio_positive_elas = float(positive_elas) / sum_pop

conso_null = (df.query('elas_price_2_2 == 0')['depenses_energies_logement'] * df.query('elas_price_2_2 == 0')['pondmen']).sum()
conso_tot = (df['depenses_energies_logement'] * df['pondmen']).sum()
ratio_conso = conso_null / conso_tot
