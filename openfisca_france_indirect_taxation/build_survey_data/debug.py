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
    'isolation_murs',
    'isolation_fenetres',
    ]

df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

print df_reforme['rev_disponible'].mean()
print df_reforme['depenses_energies_logement_officielle_2018_in_2016'].mean()

df_reforme['tee'] = ((df_reforme['depenses_carburants_corrigees_officielle_2018_in_2016'] / df_reforme['rev_disponible']) > 0.1)*1

bibi = df_reforme[['tee_10_3_rev_disponible_transport_bis'] + ['tee_10_3_rev_disponible_transport'] + ['niveau_vie_decile']]

bibi['tee'] = bibi['tee_10_3_rev_disponible_transport'] + bibi['tee_10_3_rev_disponible_transport_bis']

bibi = bibi.query('tee > 0')

print df_reforme['']


dataframe_bis = dataframe_bis.rename(columns={
    'depenses_carburants_corrigees_officielle_2018_in_2016': 'depenses_carburants_corrigees_officielle_2018_in_2016_bis',
    'rev_disponible': 'rev_disponible_bis',
    'tee_10_3_rev_disponible_transport': 'tee_10_3_rev_disponible_transport_bis'
    })

difi = pandas.concat([dataframe, dataframe_bis], axis = 1)
difi['tee'] = difi['tee_10_3_rev_disponible_transport'] + difi['tee_10_3_rev_disponible_transport_bis']
difi_bis = difi.query('tee > 0')
difi_bis_bis = difi_bis.query('ere_bis < 0.1')
del difi['tee']

difi['ere'] = difi['depenses_carburants_corrigees_officielle_2018_in_2016'] / difi['rev_disponible']
difi['ere_bis'] = difi['depenses_carburants_corrigees_officielle_2018_in_2016_bis'] / difi['rev_disponible_bis']


bibi = df_reforme.query('ere_carbu_before < ere_carbu_after')
