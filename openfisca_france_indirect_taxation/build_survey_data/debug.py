# -*- coding: utf-8 -*-

from __future__ import division

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario


simulated_variables = [
    'strate_agrege',
    'strate',
    ]

year = 2011
data_year = 2011
survey_scenario = SurveyScenario.create(year = year, data_year = data_year)

for category in ['niveau_vie_decile']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)
    indiv_df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)





from openfisca_france_indirect_taxation.utils import get_input_data_frame
df = get_input_data_frame(year)
print df['strate']

df_postes = []
df_columns = df.columns.tolist()
for element in df_columns:
    if element[:5] == 'poste':
        df_postes.append(element)




liste = survey_scenario.tax_benefit_system.column_by_name.keys()
