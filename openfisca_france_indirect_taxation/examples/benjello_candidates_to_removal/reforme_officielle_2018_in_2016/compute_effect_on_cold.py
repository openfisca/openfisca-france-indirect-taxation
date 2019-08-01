# -*- coding: utf-8 -*-

# In this script we take the estimates obtained in the estimation with ENL,
# and we compute the probabilities of being cold for BdF households.
# We then replicate this with adjusted expenditures and do the difference.


import numpy as np


from openfisca_france_indirect_taxation.surveys import SurveyScenario
# from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.reforme_officielle_2018_in_2016.variation_in_cold_enl import estimate_froid
from openfisca_france_indirect_taxation.examples.utils_example import cheque_par_energie

logit = estimate_froid()[1]
params = logit.params
params = params.to_frame().T
explanatory_vars = params.columns.tolist()

variables_use_baseline = [
    'agepr',
    'aides_logement',
    'depenses_combustibles_liquides',
    'depenses_electricite',
    'depenses_energies_logement',
    'depenses_gaz_ville',
    'dip14pr',
    'electricite',
    'froid_4_criteres_3_deciles',
    'gaz_ville',
    'isolation_fenetres',
    'isolation_murs',
    'isolation_toit',
    'majorite_double_vitrage',
    'nactifs',
    'nenfants',
    'niveau_vie_decile',
    'ocde10',
    'ouest_sud',
    'paris',
    'petite_ville',
    'pondmen',
    'revtot',
    'rural',
    'surfhab_d',
    ]

variables_reforme = [
    'agepr',
    'aides_logement',
    'cheques_energie_officielle_2018_in_2016',
    'depenses_combustibles_liquides_officielle_2018_in_2016',
    'depenses_electricite',
    'depenses_energies_logement_officielle_2018_in_2016',
    'depenses_gaz_ville_officielle_2018_in_2016',
    'dip14pr',
    'electricite',
    'froid_4_criteres_3_deciles',
    'gaz_ville',
    'isolation_fenetres',
    'isolation_murs',
    'isolation_toit',
    'majorite_double_vitrage',
    'nactifs',
    'nenfants',
    'niveau_vie_decile',
    'ocde10',
    'ouest_sud',
    'paris',
    'petite_ville',
    'pondmen',
    'reste_transferts_neutre_officielle_2018_in_2016',
    'revtot',
    'rural',
    'surfhab_d',
    ]

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
# elasticities = get_elasticities(data_year)
elasticities = get_elasticities_aidsills(data_year, True)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'officielle_2018_in_2016',
    year = year,
    data_year = data_year
    )

df_use_baseline = survey_scenario.create_data_frame_by_entity(variables_reference, period = year)['menage']
df_reforme = survey_scenario.create_data_frame_by_entity(variables_reforme, period = year)['menage']

# Reference case :
df_reference.rename(
    columns = {
        'depenses_energies_logement': 'depenses_energies',
        },
    inplace = True,
    )

df_use_baseline = df_reference.query('revtot > 0')
df_reference['revtot_2'] = df_reference['revtot'] ** 2
df_reference['part_energies_revtot'] = df_reference['depenses_energies'] / df_reference['revtot']

df_reference['predict_log_odds'] = 0
for var in explanatory_vars:
    df_reference['predict_log_odds'] += df_reference[var] * params[var][0]

df_reference['predict_odds'] = np.exp(df_reference['predict_log_odds'])
df_reference['predict_proba'] = df_reference['predict_odds'] / (1 + df_reference['predict_odds'])
df_reference.loc[df_reference['niveau_vie_decile'] > 3, 'predict_proba'] = 0

# Official reform :
df_reforme.rename(
    columns = {
        'depenses_energies_logement_officielle_2018_in_2016': 'depenses_energies',
        'depenses_combustibles_liquides_officielle_2018_in_2016': 'depenses_combustibles_liquides',
        'depenses_gaz_ville_officielle_2018_in_2016': 'depenses_gaz_ville',
        },
    inplace = True,
    )

df_reforme = cheque_par_energie(
    df_reforme,
    'depenses_combustibles_liquides',
    'depenses_electricite',
    'depenses_gaz_ville',
    'cheques_energie_officielle_2018_in_2016'
    )

df_reforme['depenses_combustibles_liquides'] = (
    df_reforme['depenses_combustibles_liquides'] - df_reforme['cheque_combustibles_liquides']
    )
df_reforme['depenses_electricite'] = (
    df_reforme['depenses_electricite'] - df_reforme['cheque_electricite']
    )
df_reforme['depenses_gaz_ville'] = (
    df_reforme['depenses_electricite'] - df_reforme['cheque_gaz_ville']
    )
df_reforme['depenses_energies'] = (
    df_reforme['depenses_energies'] - df_reforme['cheques_energie_officielle_2018_in_2016']
    )

df_reforme = df_reforme.query('revtot > 0')
df_reforme['revtot'] = df_reforme['revtot'] + df_reforme['reste_transferts_neutre_officielle_2018_in_2016']
df_reforme['revtot_2'] = df_reforme['revtot'] ** 2
df_reforme['part_energies_revtot'] = df_reforme['depenses_energies'] / df_reforme['revtot']

df_reforme['predict_log_odds'] = 0
for var in explanatory_vars:
    df_reforme['predict_log_odds'] += df_reforme[var] * params[var][0]

df_reforme['predict_odds'] = np.exp(df_reforme['predict_log_odds'])
df_reforme['predict_proba'] = df_reforme['predict_odds'] / (1 + df_reforme['predict_odds'])
df_reforme.loc[df_reforme['niveau_vie_decile'] > 3, 'predict_proba'] = 0

# Show some of the results
share_cold_use_baseline = (df_reference['predict_proba'] * df_reference['pondmen']).sum() / df_reference['pondmen'].sum()
share_cold_reforme = (df_reforme['predict_proba'] * df_reforme['pondmen']).sum() / df_reforme['pondmen'].sum()

percentage_increase_cold_reforme = (share_cold_reforme - share_cold_reference) / share_cold_reference

print(df_reference['predict_proba'].mean())
print(df_reforme['predict_proba'].mean())

print(df_reference.query('niveau_vie_decile < 4')['predict_proba'].mean())
print(df_reforme.query('niveau_vie_decile < 4')['predict_proba'].mean())
