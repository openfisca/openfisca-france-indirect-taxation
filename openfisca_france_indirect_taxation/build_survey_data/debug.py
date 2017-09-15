# -*- coding: utf-8 -*-

from __future__ import division

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


simulated_variables = [
    'poste_04_5_1_1_1_b',
    'poste_04_5_2_1_1',
    'poste_04_5_2_2_1',
    'rev_disponible',
    'depenses_electricite',
    'depenses_gaz'
    ]

year = 2013
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
#del inflation_kwargs['inflator_by_variable']['somme_coicop12']

survey_scenario = SurveyScenario.create(
    inflation_kwargs = inflation_kwargs,
    year = year,
    data_year = data_year
    )

for category in ['niveau_vie_decile']:
    #df = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)
    indiv_df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']


elec = indiv_df['depenses_electricite'].mean()
gaz = indiv_df['depenses_gaz'].mean()
gpl = indiv_df['poste_04_5_2_2_1'].mean()

from openfisca_france_indirect_taxation.utils import get_input_data_frame
df = get_input_data_frame(year)
print df['strate']

df_postes = []
df_columns = df.columns.tolist()
for element in df_columns:
    if element[:5] == 'poste':
        df_postes.append(element)




liste = survey_scenario.tax_benefit_system.column_by_name.keys()
