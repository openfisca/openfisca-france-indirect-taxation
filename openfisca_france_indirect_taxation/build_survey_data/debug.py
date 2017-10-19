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
    'cheques_energie_integral_inconditionnel_officielle_2018_in_2016',
    'cheques_energie_integral_inconditionnel_officielle_2018_in_2016_plus_cspe',
    'cheques_energie_integral_inconditionnel_cce_seulement',
    'cheques_energie_integral_inconditionnel_rattrapage_integral',
    'revenu_reforme_officielle_2018_in_2016',
    'revenu_reforme_officielle_2018_in_2016_plus_cspe',
    'revenu_reforme_rattrapage_integral',
    'revenu_reforme_cce_seulement',
    'pertes_financieres_avant_redistribution_officielle_2018_in_2016',
    'ocde10',
    'pondmen',
    'npers',
    #'tchof',
    #'revtot',
    #'quantites_gaz_final',
    #'quantites_gaz_contrat_optimal',
    ]

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

nombre_parts = sum(df_reforme['pondmen'] * df_reforme['ocde10'])

#print sum(df_reforme['pondmen'] * df_reforme['revenu_reforme_officielle_2018_in_2016']) / nombre_parts
#print sum(df_reforme['pondmen'] * df_reforme['revenu_reforme_officielle_2018_in_2016_plus_cspe']) / nombre_parts
#print sum(df_reforme['pondmen'] * df_reforme['revenu_reforme_rattrapage_integral']) / nombre_parts
#print sum(df_reforme['pondmen'] * df_reforme['revenu_reforme_cce_seulement']) / nombre_parts

print (df_reforme['cheques_energie_integral_inconditionnel_officielle_2018_in_2016']).mean()
#print (df_reforme['cheques_energie_integral_inconditionnel_officielle_2018_in_2016_plus_cspe']).mean()
#print (df_reforme['cheques_energie_integral_inconditionnel_cce_seulement']).mean()
#print (df_reforme['cheques_energie_integral_inconditionnel_rattrapage_integral']).mean()

print (df_reforme['pertes_financieres_avant_redistribution_officielle_2018_in_2016']).mean()

#df_reforme['eligible'] = (
#    1 * (df_reforme['revtot'] < 8723) * (df_reforme['npers'] == 1) +
#    1 * (df_reforme['revtot'] < 13085) * (df_reforme['npers'] == 2) +
#    1 * (df_reforme['revtot'] < 15701) * (df_reforme['npers'] == 3) +
#    1 * (df_reforme['revtot'] < 18318) * (df_reforme['npers'] == 4) +
#    1 * (df_reforme['revtot'] < 18318 + (df_reforme['npers'] - 4) * 3489) * (df_reforme['npers'] > 4)
#    )



bibi = data_erfs.query('cataeu == 211')
print data_erfs['cataeu'].dtype

