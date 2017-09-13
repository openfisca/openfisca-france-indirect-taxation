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


i = 0
variables_menages_bdf = ['poste_04_5_1_1_1_b', 'poste_04_5_2_1_1', 'poste_04_5_1_1_1_a']
variables_menages_enl = ['coml11', 'coml12', 'coml13']
bibi = menage_enl_keep.query('coml13 > 0')
bobo = conso_bdf_keep.query('poste_04_5_1_1_1_a > 0')

from openfisca_france_indirect_taxation.utils import get_input_data_frame
df = get_input_data_frame(year)
print df['strate']



postes_agreges = ['poste_agrege_{}'.format(index) for index in
    ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12"]
    ]
simulated_variables += postes_agreges





liste = survey_scenario.tax_benefit_system.column_by_name.keys()

for element in liste:
    if element[:9] == 'depenses_':
        print element

liste_variables = depenses.columns.tolist()
depenses['depenses_tot'] = 0
for element in liste_variables:
    if element[:6] == 'poste_':
        if element[:8] != 'poste_13':
            depenses['depenses_tot'] += depenses[element]

liste_variables = depenses.columns.tolist()
postes_agreges = ['poste_{}'.format(index) for index in
    ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12"]
    ]
depenses['depenses_tot_bis'] = 0
for element in liste_variables:
    for poste in postes_agreges:
        if element[:8] == poste:
            depenses['depenses_tot_bis'] += depenses[element]



year = 2000
year = 2005


