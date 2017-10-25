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
    'ocde10',
    'pondmen',
    'rev_disponible',
    'reste_transferts_neutre_officielle_2018_in_2016',
    'revenu_reforme_officielle_2018_in_2016',
    'isolation_fenetres',
    'isolation_murs',
    'isolation_toit',
    'majorite_double_vitrage',
    'typmen',
    ]

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
df = dataframe_by_group(survey_scenario, 'niveau_vie_decile', simulated_variables)

#print (df_reforme['eligibilite_tarifs_sociaux_energies'] * df_reforme['pondmen']).sum()
#print df_reforme.query('tarifs_sociaux_electricite > 0')['pondmen'].sum()
#print df_reforme.query('tarifs_sociaux_gaz > 0')['pondmen'].sum()
#print df_reforme.query('cheques_energie_officielle_2018_in_2016 > 0')['pondmen'].sum()

print len(df_reforme.query('typmen == 2'))

print df_reforme['reste_transferts_neutre_officielle_2018_in_2016'].mean()
print df_reforme['revenu_reforme_officielle_2018_in_2016'].mean()
df_reforme['ratio'] = df_reforme['reste_transferts_neutre_officielle_2018_in_2016'] / df_reforme['rev_disponible']



