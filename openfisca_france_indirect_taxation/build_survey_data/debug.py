# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
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
    'depenses_diesel_corrigees',
    'depenses_essence_corrigees',
    'depenses_carburants_corrigees',
    'depenses_combustibles_liquides',
    'depenses_gaz_ville_officielle_2018_in_2016',
    'niveau_vie_decile',
    'ocde10',
    'nactifs',
    'revdecm',
    'niveau_de_vie',
    'agepr',
    'pondmen',
    ]

df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

for i in range(1,11):
    df_nvd = df.query('niveau_vie_decile == {}'.format(i))
    print df_nvd['depenses_diesel_corrigees'].mean() / df_nvd['depenses_carburants_corrigees'].mean()


df_die = df.query('depenses_diesel_corrigees > depenses_essence_corrigees')
df_ess = df.query('depenses_diesel_corrigees < depenses_essence_corrigees')

print df_die['depenses_carburants_corrigees'].mean()
print df_ess['depenses_carburants_corrigees'].mean()

print float((df.query('depenses_combustibles_liquides > 0')['pondmen']).sum()) / df['pondmen'].sum()
print float((df.query('depenses_gaz_ville_officielle_2018_in_2016 > 0')['pondmen']).sum()) / df['pondmen'].sum()

group = 'strate'
i = 3