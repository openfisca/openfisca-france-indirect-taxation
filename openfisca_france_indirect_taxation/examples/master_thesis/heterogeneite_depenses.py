# -*- coding: utf-8 -*-

from __future__ import division

import statsmodels.formula.api as smf

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


inflators_by_year = get_inflators_by_year_energy(rebuild = False)

simulated_variables = [
    'depenses_energies_logement',
    'poste_coicop_452',
    'poste_coicop_453',
    'poste_coicop_722',
    'rev_disp_loyerimput',
    'ocde10',
    'strate_agrege',
    'vag',
    'situacj',
    'situapr',
    'age_group_pr'
    ]

year = 2014
data_year = 2011
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
del inflation_kwargs['inflator_by_variable']['somme_coicop12']


survey_scenario = SurveyScenario.create(
    inflation_kwargs = inflation_kwargs,
    year = year,
    data_year = data_year
    )

df_by_entity = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
menages = df_by_entity['menages']

menages['rev_disp_loyerimput_2'] = menages['rev_disp_loyerimput'] ** 2
menages['age_group_pr_2'] = menages['age_group_pr'] ** 2
menages['alone'] = 0 + (1 * menages['situacj'] == 0)
menages['occupe_both'] = (1 * (menages['situapr'] < 4)) * (1 * (menages['situacj'] < 4))
menages['fioul'] = 0 + (1 * menages['poste_coicop_453'] > 0)
menages['gaz'] = 0 + (1 * menages['poste_coicop_452'] > 0)

for i in range(23, 29):
    menages['vag_{}'.format(i)] = 0
    menages.loc[menages['vag'] == i, 'vag_{}'.format(i)] = 1

for i in range(1, 4):
    menages['strate_{}'.format(i)] = 0
    menages.loc[menages['strate_agrege'] == i, 'strate_{}'.format(i)] = 1

reg_transports = smf.ols(formula = 'poste_coicop_722 ~ \
    rev_disp_loyerimput + rev_disp_loyerimput_2 + ocde10 + strate_1 + strate_3 + age_group_pr + \
    age_group_pr_2 + alone + occupe_both + gaz + fioul + vag_23 + vag_24 + vag_25 + vag_26 + vag_27',
    data = menages).fit()
print reg_transports.summary()

reg_housing = smf.ols(formula = 'depenses_energies_logement ~ \
    rev_disp_loyerimput + rev_disp_loyerimput_2 + ocde10 + strate_1 + strate_3 + age_group_pr + \
    age_group_pr_2 + alone + occupe_both + gaz + fioul + vag_23 + vag_24 + vag_25 + vag_26 + vag_27',
    data = menages).fit()
print reg_housing.summary()
