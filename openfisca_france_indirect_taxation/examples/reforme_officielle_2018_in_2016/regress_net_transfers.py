# -*- coding: utf-8 -*-

from __future__ import division

import pandas as pd
import statsmodels.formula.api as smf

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group, age_group, energy_modes
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities


inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'officielle_2018_in_2016',
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'revenu_reforme_officielle_2018_in_2016',
    'cheques_energie_officielle_2018_in_2016',
    'reste_transferts_neutre_officielle_2018_in_2016',
    'strate',
    'niveau_vie_decile',
    'pondmen',
    'combustibles_liquides',
    'gaz_ville',
    'agepr',
    'isolation_murs',
    'isolation_fenetres',
    'majorite_double_vitrage',
    'nenfants',
    'ocde10',
    'rev_disp_loyerimput',
    'situacj',
    'situapr',
    'log_indiv',
    'bat_av_49',
    'bat_49_74',
    'ouest_sud',
    'surfhab_d',
    'aides_logement',
    
    ]

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df_reforme['transferts_nets_apres_redistribution'] = (
    df_reforme['cheques_energie_officielle_2018_in_2016'] +
    df_reforme['reste_transferts_neutre_officielle_2018_in_2016'] -
    df_reforme['revenu_reforme_officielle_2018_in_2016']
    )

df_reforme = age_group(df_reforme)
df_reforme = energy_modes(df_reforme)

df_reforme['rev_disp_loyerimput_2'] = df_reforme['rev_disp_loyerimput'] ** 2
df_reforme['alone'] = 0 + (1 * df_reforme['situacj'] == 0)
df_reforme['occupe_both'] = (1 * (df_reforme['situapr'] < 4)) * (1 * (df_reforme['situacj'] < 4))
for i in range(0, 5):
    df_reforme['strate_{}'.format(i)] = 0
    df_reforme.loc[df_reforme['strate'] == i, 'strate_{}'.format(i)] = 1

df_reforme['majorite_double_vitrage'] = 1 * (df_reforme['majorite_double_vitrage'] == 1)
df_reforme['mauvaise_isolation_fenetres'] = 1 * (df_reforme['isolation_fenetres'] == 1)
df_reforme['bonne_isolation_murs'] = 1 * (df_reforme['isolation_murs'] == 1)
df_reforme['mauvaise_isolation_murs'] = 1 * (df_reforme['isolation_murs'] == 3)


regression_ols = smf.ols(formula = 'transferts_nets_apres_redistribution ~ \
    rev_disp_loyerimput + rev_disp_loyerimput_2 + \
    majorite_double_vitrage + mauvaise_isolation_fenetres + mauvaise_isolation_murs + bonne_isolation_murs + \
    ouest_sud + surfhab_d + aides_logement + agepr + ocde10 + bat_av_49 + bat_49_74 + log_indiv + \
    combustibles_liquides + gaz_ville + strate_0 + strate_1 + strate_3 + strate_4',
    data = df_reforme).fit()
print regression_ols.summary()
