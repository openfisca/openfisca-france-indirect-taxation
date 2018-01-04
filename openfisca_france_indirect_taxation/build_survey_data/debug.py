# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


year = 2016
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
elasticities = get_elasticities_aidsills(data_year)

reforme = 'officielle_2018_in_2016'

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = reforme,
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'strate',
    'niveau_vie_decile',
    'identifiant_menage',
    'elas_price_1_1',
    'elas_price_2_2',
    'depenses_carburants_corrigees_officielle_2018_in_2016',
    'depenses_combustibles_liquides_officielle_2018_in_2016',
    ]

df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

print df.depenses_carburants_corrigees_officielle_2018_in_2016.mean() # 1376
print df.depenses_combustibles_liquides_officielle_2018_in_2016.mean() # 215.3

df_2_4 = df.query('strate == 2').query('niveau_vie_decile == 4')
print df_2_4.elas_price_1_1.mean()
