# -*- coding: utf-8 -*-

import os
import pkg_resources

from openfisca_france_indirect_taxation.examples.utils_example import (
    dataframe_by_group,
    graph_builder_bar,
    )
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.reforms.officielle_2019_in_2017 import officielle_2019_in_2017


inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
elasticities = get_elasticities_aidsills(data_year, True)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'revenu_reforme_officielle_2019_in_2017',
    'cheques_energie_officielle_2019_in_2017',
    'cheques_energie_philippe_officielle_2019_in_2017',
    'cheques_energie_majore_officielle_2019_in_2017',
    'rev_disp_loyerimput',
    'rev_disponible',
    'niveau_de_vie',
    'tarifs_sociaux_electricite',
    'tarifs_sociaux_gaz',
    'pondmen'
    ]

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform = officielle_2019_in_2017,
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

print(
    "Nombre de ménages bénéficiant du chèque énergie (avant extension) : {} millions".format(
    (df_reforme['pondmen'] * (df_reforme['cheques_energie_officielle_2019_in_2017'] > 0)).sum()/1e6)
    )
print(
    "Nombre de ménages bénéficiant du chèque énergie (après extension) : {} millions".format(
    (df_reforme['pondmen'] * (df_reforme['cheques_energie_philippe_officielle_2019_in_2017'] > 0)).sum()/1e6)
    )

# Résultats agrégés par déciles de niveau de vie
df = dataframe_by_group(survey_scenario, category = 'niveau_vie_decile', variables = simulated_variables)

# Simulation des effets de différentes réformes

df['cout_reforme_uc_avant_cheque_energie'] = (
    df['revenu_reforme_officielle_2019_in_2017']
    - df['tarifs_sociaux_electricite'] - df['tarifs_sociaux_gaz']
    )
df['cout_reforme_uc_cheque_officiel'] = (
    df['revenu_reforme_officielle_2019_in_2017']
    - df['cheques_energie_officielle_2019_in_2017']
    )
df['cout_reforme_uc_cheque_majore'] = (
    df['revenu_reforme_officielle_2019_in_2017']
    - df['cheques_energie_majore_officielle_2019_in_2017']
    )
df['cout_reforme_uc_cheque_philippe'] = (
    df['revenu_reforme_officielle_2019_in_2017']
    - df['cheques_energie_philippe_officielle_2019_in_2017']
    )

df['taux_effort_avant_cheque_energie'] = df['cout_reforme_uc_avant_cheque_energie'] / df['rev_disponible']
df['taux_effort_cheque_officiel'] = df['cout_reforme_uc_cheque_officiel'] / df['rev_disponible']
df['taux_effort_cheque_majore'] = df['cout_reforme_uc_cheque_majore'] / df['rev_disponible']
df['taux_effort_cheque_philippe'] = df['cout_reforme_uc_cheque_philippe'] / df['rev_disponible']
graph_builder_bar(df['taux_effort_cheque_philippe'], False)
print("Coût total de la réforme : {} milliards d'euros".format(df['cout_reforme_uc_cheque_philippe'].mean() * df_reforme['pondmen'].sum()/1e9))

## Tests

test_assets_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'tests'
    )

test_variables = [
    'niveau_de_vie',
    'cout_reforme_uc_avant_cheque_energie',
    'cout_reforme_uc_cheque_officiel',
    'cout_reforme_uc_cheque_philippe',
    'cout_reforme_uc_cheque_majore',
    'taux_effort_cheque_philippe',
    ]

df[test_variables].to_csv(
    os.path.join(
        test_assets_directory,
        'net_contributions_by_categ_2019_in_2017.csv'
        )
    )
