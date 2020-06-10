# -*- coding: utf-8 -*-

import os
import pandas as pd
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
        (
            df_reforme['pondmen'] * (df_reforme['cheques_energie_officielle_2019_in_2017'] > 0)
            ).sum() / 1e6
        )
    )
print(
    "Nombre de ménages bénéficiant du chèque énergie (après extension) : {} millions".format(
        (
            df_reforme['pondmen'] * (df_reforme['cheques_energie_philippe_officielle_2019_in_2017'] > 0)
            ).sum() / 1e6)
    )

# Résultats agrégés par déciles de niveau de vie
df = dataframe_by_group(survey_scenario, category = 'niveau_vie_decile', variables = simulated_variables)

# Simulation des effets de différentes réformes

# A PARTIR DE LA REFORME 2019_IN_2017
df['cout_reforme_pures_taxes'] = (
    df['revenu_reforme_officielle_2019_in_2017']
    - df['tarifs_sociaux_electricite'] - df['tarifs_sociaux_gaz']
    ) / df['rev_disponible']
df['cout_passage_tarifs_sociaux_cheque_energie'] = (
    df['cheques_energie_officielle_2019_in_2017']
    - df['tarifs_sociaux_electricite'] - df['tarifs_sociaux_gaz']
    ) / df['rev_disponible']
df['cout_majoration_cheque_energie'] = (
    df['cheques_energie_majore_officielle_2019_in_2017']
    - df['cheques_energie_officielle_2019_in_2017']
    ) / df['rev_disponible']
df['cout_majoration_et_extension_cheque_energie'] = (
    df['cheques_energie_philippe_officielle_2019_in_2017']
    - df['cheques_energie_officielle_2019_in_2017']
    ) / df['rev_disponible']
df['cout_total_reforme'] = (
    - df['cout_reforme_pures_taxes']
    + df['cout_majoration_et_extension_cheque_energie']
    + df['cout_passage_tarifs_sociaux_cheque_energie']
    )

graph_builder_bar(df['cout_total_reforme'], False)
print("Coût total de la réforme : {} milliards d'euros".format(
    df['cout_total_reforme'].mean() * df_reforme['pondmen'].sum() / 1e9)
    )

# Tests

from openfisca_france_indirect_taxation.assets.tests.resultats_reformes_energie_thomas_initial import results

for variables in results.columns:
    assert (abs(df['{}'.format(variables)] - results['{}'.format(variables)]) < 1).all()
