

import pandas as pd

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = ['depenses_carburants', 'depenses_combustibles_liquides', 'depenses_combustibles_solides',
    'depenses_electricite', 'depenses_tot', 'depenses_gaz', 'loyer_impute', 'rev_disp_loyerimput', 'rev_disponible']

survey_scenario_2011 = SurveyScenario.create(
    year = 2011,
    data_year = 2011
    )
df_2011 = survey_scenario_2011.create_data_frame_by_entity(simulated_variables, period = 2011)['menage']

survey_scenario_year = SurveyScenario.create(
    inflation_kwargs = inflation_kwargs,
    year = year,
    data_year = data_year
    )
df_year = survey_scenario_year.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df_compare = pd.DataFrame()
for var in simulated_variables:
    df_2011[var + '_inflated'] = (df_2011[var] * inflation_kwargs['inflator_by_variable'][var]).copy()
    df_compare[var] = (df_2011[var + '_inflated'] - df_year[var]).copy()
    assert max(df_compare[var]) < 1  # check the difference is less than 1€
