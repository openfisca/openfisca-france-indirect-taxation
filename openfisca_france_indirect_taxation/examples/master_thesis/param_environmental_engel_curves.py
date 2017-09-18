# -*- coding: utf-8 -*-

from __future__ import division

import statsmodels.formula.api as smf
import numpy
import pandas

import matplotlib.pyplot as plt

from openfisca_france_indirect_taxation.examples.utils_example import save_dataframe_to_graph
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


inflators_by_year = get_inflators_by_year_energy(rebuild = False)

simulated_variables = [
    'depenses_energies_logement',
    'emissions_CO2_energies',
    'depenses_gaz_ville',
    'depenses_combustibles_liquides',
    'poste_coicop_722',
    'rev_disp_loyerimput',
    'ocde10',
    'strate',
    'vag',
    'situacj',
    'situapr',
    'age_group_pr'
    ]

year = 2014
data_year = 2011
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

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
menages['fioul'] = 0 + (1 * menages['depenses_combustibles_liquides'] > 0)
menages['gaz'] = 0 + (1 * menages['depenses_gaz_ville'] > 0)

for i in range(23, 29):
    menages['vag_{}'.format(i)] = 0
    menages.loc[menages['vag'] == i, 'vag_{}'.format(i)] = 1

for i in range(1, 4):
    menages['strate_{}'.format(i)] = 0
    menages.loc[menages['strate'] == i, 'strate_{}'.format(i)] = 1

reg_emissions = smf.ols(formula = 'emissions_CO2_energies ~ \
    rev_disp_loyerimput + rev_disp_loyerimput_2 + ocde10 + strate_0 + strate_1 + strate_3 + strate_4 + age_group_pr + \
    age_group_pr_2 + alone + occupe_both + gaz + fioul + vag_23 + vag_24 + vag_25 + vag_26 + vag_27',
    data = menages).fit()
print reg_emissions.summary()

ocde10 = menages['ocde10'].mean()
strate_1 = menages['strate_1'].mean()
strate_3 = menages['strate_3'].mean()
age_group_pr = menages['age_group_pr'].mean()
age_group_pr_2 = menages['age_group_pr_2'].mean()
alone = menages['alone'].mean()
occupe_both = menages['occupe_both'].mean()
gaz = menages['gaz'].mean()
fioul = menages['fioul'].mean()

liste_revenus = numpy.arange(1000, 500000, 500)
simulation_menages = pandas.DataFrame(liste_revenus)
simulation_menages.rename(columns = {0: 'revenu_disponible'}, inplace = True)
simulation_menages['revenu_disponible'] = simulation_menages['revenu_disponible'].astype(numpy.int64)
simulation_menages['revenu_disponible2'] = (simulation_menages['revenu_disponible'] ** 2)

# Change parameters to fit new results
simulation_menages['emissions'] = -233.6354 + (
    (873.8949 * ocde10 -1425.8345 * strate_1 + 172.7004 * strate_3 + 538.9584 * age_group_pr +
    -50.8012 * age_group_pr_2 + -946.6144 * alone + 479.9245 * occupe_both + 4344.2562 * gaz + 8265.1751 * fioul) +
    0.0403 * simulation_menages['revenu_disponible'] +
    -1.715e-08 * (simulation_menages['revenu_disponible2'])
    )

save_dataframe_to_graph(
    simulation_menages, 'Emissions/parametric_eec.csv'
    )

plt.plot(simulation_menages['revenu_disponible'], simulation_menages['emissions'])
