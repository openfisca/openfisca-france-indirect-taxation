# -*- coding: utf-8 -*-

from __future__ import division

import statsmodels.formula.api as smf
import numpy
import pandas

import matplotlib.pyplot as plt

from openfisca_france_indirect_taxation.examples.utils_example import save_dataframe_to_graph
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities


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
    'depenses_energies_logement',
    'emissions_CO2_energies_totales',
    'depenses_gaz_ville',
    'depenses_combustibles_liquides',
    'depenses_carburants_corrigees',
    'rev_disp_loyerimput',
    'ocde10',
    'strate',
    'vag',
    'situacj',
    'situapr',
    'age_group_pr',
    'combustibles_liquides',
    'gaz_ville',
    ]


menages = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

menages['rev_disp_loyerimput_2'] = menages['rev_disp_loyerimput'] ** 2
menages['age_group_pr_2'] = menages['age_group_pr'] ** 2
menages['alone'] = 0 + (1 * menages['situacj'] == 0)
menages['occupe_both'] = (1 * (menages['situapr'] < 4)) * (1 * (menages['situacj'] < 4))
menages['fioul'] = 0 + (1 * menages['depenses_combustibles_liquides'] > 0)
menages['gaz'] = 0 + (1 * menages['depenses_gaz_ville'] > 0)

for i in range(0, 5):
    menages['strate_{}'.format(i)] = 0
    menages.loc[menages['strate'] == i, 'strate_{}'.format(i)] = 1

reg_emissions = smf.ols(formula = 'emissions_CO2_energies_totales ~ \
    rev_disp_loyerimput + rev_disp_loyerimput_2 + ocde10 + strate_0 + strate_1 + strate_3 + strate_4 + age_group_pr + \
    age_group_pr_2 + alone + occupe_both + gaz_ville + combustibles_liquides',
    data = menages).fit()
print reg_emissions.summary()
