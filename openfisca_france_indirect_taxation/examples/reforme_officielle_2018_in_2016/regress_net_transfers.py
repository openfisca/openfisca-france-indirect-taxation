# -*- coding: utf-8 -*-

from __future__ import division

import pandas as pd
import statsmodels.formula.api as smf

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, graph_builder_line, save_dataframe_to_graph, \
    dataframe_by_group, age_group, energy_modes
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills


inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
#elasticities = get_elasticities(data_year)
elasticities = get_elasticities_aidsills(data_year, True)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])


# Homogeneous + SL :
#elasticities['elas_price_1_1'] = -0.466
#elasticities['elas_price_2_2'] = -0.214

# Homogeneous, no SL :
#elasticities['elas_price_1_1'] = -0.440
#elasticities['elas_price_2_2'] = -0.139

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'officielle_2018_in_2016',
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'revenu_reforme_officielle_2018_in_2016',
    'cheques_energie_officielle_2018_in_2016',
    'reste_transferts_neutre_officielle_2018_in_2016',
    'strate',
    'niveau_vie_decile',
    'pondmen',
    'combustibles_liquides',
    'gaz_ville',
    'agepr',
    'isolation_murs',
    'isolation_fenetres',
    'majorite_double_vitrage',
    'nactifs',
    'nenfants',
    'ocde10',
    'rev_disp_loyerimput',
    'situacj',
    'situapr',
    'log_indiv',
    'bat_av_49',
    'bat_49_74',
    'ouest_sud',
    'surfhab_d',
    'aides_logement',
    'typmen',
    'distance',
    'distance_routiere_hebdomadaire_teg',
    'duree_moyenne_trajet_aller_retour_teg',
    'age_vehicule',
    'stalog',
    'situapr',
    ]

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df_reforme['transferts_nets_apres_redistribution_uc'] = (
    df_reforme['cheques_energie_officielle_2018_in_2016'] +
    df_reforme['reste_transferts_neutre_officielle_2018_in_2016'] -
    df_reforme['revenu_reforme_officielle_2018_in_2016']
    ) / df_reforme['ocde10']

df_reforme = age_group(df_reforme)
df_reforme = energy_modes(df_reforme)

df_reforme['rev_disp_loyerimput_2'] = df_reforme['rev_disp_loyerimput'] ** 2
df_reforme['alone'] = 0 + (1 * df_reforme['situacj'] == 0)
df_reforme['occupe_both'] = (1 * (df_reforme['situapr'] < 4)) * (1 * (df_reforme['situacj'] < 4))
for i in range(0, 5):
    df_reforme['strate_{}'.format(i)] = 0
    df_reforme.loc[df_reforme['strate'] == i, 'strate_{}'.format(i)] = 1

df_reforme['majorite_double_vitrage'] = 1 * (df_reforme['majorite_double_vitrage'] == 1)
df_reforme['mauvaise_isolation_fenetres'] = 1 * (df_reforme['isolation_fenetres'] == 1)
df_reforme['bonne_isolation_murs'] = 1 * (df_reforme['isolation_murs'] == 1)
df_reforme['mauvaise_isolation_murs'] = 1 * (df_reforme['isolation_murs'] == 3)

df_reforme['agepr_2'] = df_reforme['agepr'] ** 2
df_reforme['monoparental'] = 0
df_reforme.loc[df_reforme['typmen'] == 2, 'monoparental'] = 1

df_reforme['proprietaire'] = 0
df_reforme.loc[df_reforme.stalog.isin([1, 2]), 'proprietaire'] = 1

df_reforme['etudiant'] = 0
df_reforme.loc[df_reforme.situapr == 3, 'etudiant'] = 1

df_reforme['distance_routiere_hebdomadaire_teg'] = (
    df_reforme['distance_routiere_hebdomadaire_teg'] * (df_reforme['distance'] > 0)
    )
df_reforme['part_distance_teg'] = \
    df_reforme['distance_routiere_hebdomadaire_teg'] / df_reforme['distance']
df_reforme['part_distance_teg'] = df_reforme['part_distance_teg'].fillna(0) * 47

df_reforme.rename(
    columns = {
        'transferts_nets_apres_redistribution_uc' : 'Net_transfers_by_cu_after_recycling',
        'rev_disp_loyerimput' : 'Disposable_income',
        'rev_disp_loyerimput_2' : 'Disposable_income_squared',
        'combustibles_liquides' : 'Domestic_fuel',
        'gaz_ville' : 'Natural_gas',
        'strate_0' : 'Rural',
        'strate_1' : 'Small_cities',
        'strate_3' : 'Large_cities',
        'strate_4' : 'Paris',
        'majorite_double_vitrage' : 'Majority_double_glazing',
        'mauvaise_isolation_murs' : 'Bad_walls_isolation',
        'bonne_isolation_murs' : 'Good_walls_isolation',
        'ouest_sud' : 'Ouest_south',
        'surfhab_d' : 'Living_area_m2',
        'aides_logement' : 'Housing_benefits',
        'etudiant': 'Student',
        'agepr' : 'Age_representative',
        'agepr_2' : 'Age_representative_squared',
        'nactifs' : 'Number_in_labor_force',
        'age_vehicule' : 'Vehicule_age',
        'part_distance_teg' : 'Share_distance_to_work',
        'ocde10' : 'Consumption_units',
        'monoparental' : 'Monoparental',
        'bat_av_49' : 'Building_before_1949',
        'bat_49_74' : 'Building_1949_74',
        'log_indiv' : 'Individual_housing',
        'proprietaire' : 'Owner'
        },
    inplace = True)


regression_ols = smf.ols(formula = 'Net_transfers_by_cu_after_recycling ~ \
    Disposable_income + Disposable_income_squared + \
    Domestic_fuel + Natural_gas + Rural + Small_cities + Large_cities + Paris + Ouest_south + \
    Majority_double_glazing + Bad_walls_isolation + Good_walls_isolation + \
    Building_before_1949 + Building_1949_74 + Individual_housing + Owner + \
    Living_area_m2 + Housing_benefits + \
    Consumption_units + Monoparental + Number_in_labor_force + Student + Age_representative + Age_representative_squared + \
    Share_distance_to_work + Vehicule_age',
    data = df_reforme).fit()
print regression_ols.summary()

"""

# Compute transfers by income
params = regression_ols.params
params = params.to_frame().T

param_income = params['Disposable_income'][0]
param_income_2 = params['Disposable_income_squared'][0]
del params['Disposable_income'],  params['Disposable_income_squared']

explanatory_vars = params.columns.tolist()

df_reforme['average_transfers_by_income'] = 0
df_reforme['Intercept'] = 1
average_transfers_by_income = 0
for var in explanatory_vars:
    average_transfers_by_income += df_reforme[var].mean() * params[var][0]

df_income = pd.DataFrame(index = range(0, 200000), columns = ['transfers'])
df_income = df_income.reset_index()
df_income['transfers'] = average_transfers_by_income + df_income['index'] * param_income + (df_income['index'] ** 2) * param_income_2
graph_builder_line(df_income['transfers'])

# Compute transfers by age
params = regression_ols.params
params = params.to_frame().T

param_age = params['Age_representative'][0]
param_age_2 = params['Age_representative_squared'][0]
del params['Age_representative'],  params['Age_representative_squared']

explanatory_vars = params.columns.tolist()

df_reforme['average_transfers_by_age'] = 0
df_reforme['Intercept'] = 1
average_transfers_by_age = 0
for var in explanatory_vars:
    average_transfers_by_age += df_reforme[var].mean() * params[var][0]

df_age = pd.DataFrame(index = range(15, 91), columns = ['transfers'])
df_age = df_age.reset_index()
df_age['transfers'] = average_transfers_by_age + df_age['index'] * param_age + (df_age['index'] ** 2) * param_age_2
graph_builder_line(df_age['transfers'])

"""
