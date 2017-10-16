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

reforme = 'rattrapage_diesel'

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = reforme,
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'cmu',
    'depenses_electricite',
    'tarifs_sociaux_electricite',
    'tarifs_sociaux_gaz',
    'ocde10',
    'pondmen',
    'npers',
    'tchof',
    'revtot',
    'quantites_gaz_final',
    'quantites_gaz_contrat_optimal',
    ]

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
print len(df_reforme.query('cmu > 0'))

print sum(df_reforme['pondmen'] * df_reforme['cmu'])

bibi = df_reforme.query('tarifs_sociaux_electricite > 0')
print sum(bibi['pondmen'])

bobo = df_reforme.query('tarifs_sociaux_gaz > 0')
print sum(bobo['pondmen'])

df_reforme['eligible'] = (
    1 * (df_reforme['revtot'] < 8723) * (df_reforme['npers'] == 1) +
    1 * (df_reforme['revtot'] < 13085) * (df_reforme['npers'] == 2) +
    1 * (df_reforme['revtot'] < 15701) * (df_reforme['npers'] == 3) +
    1 * (df_reforme['revtot'] < 18318) * (df_reforme['npers'] == 4) +
    1 * (df_reforme['revtot'] < 18318 + (df_reforme['npers'] - 4) * 3489) * (df_reforme['npers'] > 4)
    )

baba = df_reforme.query('eligible > 0')
print sum(baba['pondmen'])
