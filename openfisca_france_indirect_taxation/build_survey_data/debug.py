# -*- coding: utf-8 -*-

from __future__ import division

import pandas

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
    'cheques_energie_ruraux_officielle_2018_in_2016',
    'cheques_energie_officielle_2018_in_2016',
    'cheques_energie_combustibles_liquides_officielle_2018_in_2016',
    'cheques_energie_ruraux_combustibles_liquides_officielle_2018_in_2016',
    'strate',
    'combustibles_liquides',
    'pondmen',
    'depenses_energies_totales',
    'gaz_ville',
    'niveau_vie_decile',
    ]

df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df_dec = df.query('niveau_vie_decile == 2')
print df_dec.query('combustibles_liquides == 1')['depenses_energies_totales'].mean()
print df_dec.query('gaz_ville == 1')['depenses_energies_totales'].mean()
print df_dec['depenses_energies_totales'].mean()