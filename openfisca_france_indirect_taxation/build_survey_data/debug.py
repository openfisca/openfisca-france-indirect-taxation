from __future__ import division

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario


simulated_variables = [
    'quantites_sp_e10',
    ]

year = 2011
data_year = 2011
survey_scenario = SurveyScenario.create(year = year, data_year = data_year)

for category in ['niveau_vie_decile']: #['niveau_vie_decile', 'age_group_pr', 'strate_agrege']
    df = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)
    #taxe_indirectes['depenses_tot'] = taxe_indirectes[postes_agreges].sum(axis = 1)





postes_agreges = ['poste_agrege_{}'.format(index) for index in
    ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12"]
    ]
simulated_variables += postes_agreges





liste = survey_scenario.tax_benefit_system.column_by_name.keys()

for element in liste:
    if element[:9] == 'depenses_':
        print element

taxe_indirectes['poste_04_5_1_1_1_a'].mean()
taxe_indirectes['poste_04_5_1_1_1_b'].mean()

df['Housing energy share in {}'.format(resource)] = df['depenses_energies_logement'] / df[resource]


print df['depenses_combustibles_solides'] / df[resource]

df[df.index.duplicated()]

data_year = 2011
target_year = 2011

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





print depenses['depenses_tot_bis'].mean()
print depenses['depenses_tot'].mean()
print depenses['rev_disponible'].mean()

print masses_cn_data_frame['poste']
print masses_cn_data_frame.dtypes


momo = masses_cn_data_frame.drop_duplicates('poste')
mimi = masses_cn_data_frame.query('poste == 0')

mama = masses_cn_data_frame[masses_cn_data_frame.poste != '0']


