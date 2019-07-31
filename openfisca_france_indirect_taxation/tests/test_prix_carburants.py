# This test is made to verify that when prices are called to construct variables, they take their right value.
# The corresponding variables are defined in model\taxes_indirectes\ticpe.
# These variables have been constructed just for the test.


from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario

simulated_variables = [
    'prix_super_95_ttc',
    'prix_super_95_e10_ttc',
    'prix_super_plombe_ttc',
    'accise_sp_95',
    'accise_sp_95_e10'
    ]

year = 2011
data_year = 2011
survey_scenario = SurveyScenario.create(year = year, data_year = data_year)

for category in ['niveau_vie_decile']:
    taxe_indirectes = dataframe_by_group(survey_scenario, category, simulated_variables, use_baseline =True)

assert 63.18 < taxe_indirectes['accise_sp_95'].mean() < 63.20  # accise en 2011 : 60.69 + 2.5 majoration régionale
assert taxe_indirectes['accise_sp_95'].mean() == taxe_indirectes['accise_sp_95_e10'].mean()  # same taxes at this time
assert 149 < taxe_indirectes['prix_super_95_ttc'].mean() < 150  # exact price of 149.95
assert taxe_indirectes['prix_super_95_e10_ttc'].mean() == taxe_indirectes['prix_super_95_ttc'].mean()  # same prices at this time
