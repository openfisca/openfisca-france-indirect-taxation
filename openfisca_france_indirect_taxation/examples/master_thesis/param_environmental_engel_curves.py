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
    'rev_disp_loyerimput',
    'emissions_CO2_energies',
    'ocde10',
    'age_group_pr',
    'strate_agrege',
    'situacj',
    'situapr',
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

df_by_entity = survey_scenario.create_data_frame_by_entity_key_plural(simulated_variables)
menages = df_by_entity['menages']

menages = menages.query('rev_disp_loyerimput > 1000')
menages['rev_disp_loyerimput2'] = menages['rev_disp_loyerimput'] ** 2
menages['situa_cj'] = (1 * (menages['situacj'] < 4))
menages['situa_pr'] = (1 * (menages['situapr'] < 4))
del menages['situacj'], menages['situapr']
menages['age_group_pr2'] = menages['age_group_pr'] ** 2

reg_emissions = smf.ols(formula = 'emissions_CO2_energies ~ \
    rev_disp_loyerimput + rev_disp_loyerimput2 + ocde10 + strate_agrege + age_group_pr + \
    age_group_pr2 + situa_cj + situa_pr',
    data = menages).fit()
print reg_emissions.summary()

ocde10 = menages['ocde10'].mean()
strate_agrege = menages['strate_agrege'].mean()
age_group_pr = menages['age_group_pr'].mean()
age_group_pr2 = menages['age_group_pr2'].mean()
situa_cj = menages['situa_cj'].mean()
situa_pr = menages['situa_pr'].mean()

liste_revenus = numpy.arange(1000, 500000, 500)
simulation_menages = pandas.DataFrame(liste_revenus)
simulation_menages.rename(columns = {0: 'revenu_disponible'}, inplace = True)
simulation_menages['revenu_disponible'] = simulation_menages['revenu_disponible'].astype(numpy.int64)
simulation_menages['revenu_disponible2'] = (simulation_menages['revenu_disponible'] ** 2)

simulation_menages['emissions'] = -2777.7559 + (
    (1670.0499 * ocde10 + 951.3785 * strate_agrege + 969.5029 * age_group_pr +
    -62.6559 * age_group_pr2 + -406.3679 * situa_cj + 453.0660 * situa_pr) +
    0.0450 * simulation_menages['revenu_disponible'] +
    -1.985e-08 * (simulation_menages['revenu_disponible2'])
    )

save_dataframe_to_graph(
    simulation_menages, 'Emissions/parametric_eec.csv'
    )

plt.plot(simulation_menages['revenu_disponible'], simulation_menages['emissions'])