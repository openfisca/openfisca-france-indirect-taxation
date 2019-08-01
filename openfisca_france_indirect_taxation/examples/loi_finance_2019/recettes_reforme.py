# -*- coding: utf-8 -*-

# This script depicts households' net fiscal transfers from the reform.
# It is equal to the transfers received from the reform, minus the additional
# taxes paid. A positive value means the household received higher transfers than
# the increase in taxes he faced. These amounts do not take into account VAT.


from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'poste_11_1_1_1_1',
    'poste_11_1_1_1_2',
    'poste_11_1_3_1',
    'poste_11_1_3_2',
    'poste_11_1_1_1_1_reforme_tva_2019',
    'poste_11_1_1_1_2_reforme_tva_2019',
    'poste_11_1_3_1_reforme_tva_2019',
    'poste_11_1_3_2_reforme_tva_2019',
    'pondmen'
    ]

survey_scenario = SurveyScenario.create(
    # elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'reforme_tva_2019',
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

taux_tva_avant_reforme = 0.1
taux_tva_apres_reforme = 0.2

# poste_11_1_1_1_1
df_reforme['recettes_tva_avant_reforme_poste_11_1_1_1_1'] = (
    df_reforme['poste_11_1_1_1_1'] * taux_tva_avant_reforme / (1 + taux_tva_avant_reforme)
    )
df_reforme['recettes_tva_apres_reforme_poste_11_1_1_1_1'] = (
    df_reforme['poste_11_1_1_1_1_reforme_tva_2019'] * taux_tva_apres_reforme / (1 + taux_tva_apres_reforme)
    )
df_reforme['recettes_reforme_poste_11_1_1_1_1'] = (
    df_reforme['recettes_tva_apres_reforme_poste_11_1_1_1_1']
    - df_reforme['recettes_tva_avant_reforme_poste_11_1_1_1_1']
    )
recettes_poste_11_1_1_1_1 = (df_reforme['recettes_reforme_poste_11_1_1_1_1'] * df_reforme['pondmen']).sum() / 1e6

# poste_11_1_1_1_2
df_reforme['recettes_tva_avant_reforme_poste_11_1_1_1_2'] = (
    df_reforme['poste_11_1_1_1_2'] * taux_tva_avant_reforme / (1 + taux_tva_avant_reforme)
    )
df_reforme['recettes_tva_apres_reforme_poste_11_1_1_1_2'] = (
    df_reforme['poste_11_1_1_1_2_reforme_tva_2019'] * taux_tva_apres_reforme / (1 + taux_tva_apres_reforme)
    )
df_reforme['recettes_reforme_poste_11_1_1_1_2'] = (
    df_reforme['recettes_tva_apres_reforme_poste_11_1_1_1_2']
    - df_reforme['recettes_tva_avant_reforme_poste_11_1_1_1_2']
    )
recettes_poste_11_1_1_1_2 = (df_reforme['recettes_reforme_poste_11_1_1_1_2'] * df_reforme['pondmen']).sum() / 1e6

# poste_11_1_3_1
df_reforme['recettes_tva_avant_reforme_poste_11_1_3_1'] = (
    df_reforme['poste_11_1_3_1'] * taux_tva_avant_reforme / (1 + taux_tva_avant_reforme)
    )
df_reforme['recettes_tva_apres_reforme_poste_11_1_3_1'] = (
    df_reforme['poste_11_1_3_1_reforme_tva_2019'] * taux_tva_apres_reforme / (1 + taux_tva_apres_reforme)
    )
df_reforme['recettes_reforme_poste_11_1_3_1'] = (
    df_reforme['recettes_tva_apres_reforme_poste_11_1_3_1']
    - df_reforme['recettes_tva_avant_reforme_poste_11_1_3_1']
    )
recettes_poste_11_1_3_1 = (df_reforme['recettes_reforme_poste_11_1_3_1'] * df_reforme['pondmen']).sum() / 1e6

# poste_11_1_3_2
df_reforme['recettes_tva_avant_reforme_poste_11_1_3_2'] = (
    df_reforme['poste_11_1_3_2'] * taux_tva_avant_reforme / (1 + taux_tva_avant_reforme)
    )
df_reforme['recettes_tva_apres_reforme_poste_11_1_3_2'] = (
    df_reforme['poste_11_1_3_2_reforme_tva_2019'] * taux_tva_apres_reforme / (1 + taux_tva_apres_reforme)
    )
df_reforme['recettes_reforme_poste_11_1_3_2'] = (
    df_reforme['recettes_tva_apres_reforme_poste_11_1_3_2']
    - df_reforme['recettes_tva_avant_reforme_poste_11_1_3_2']
    )
recettes_poste_11_1_3_2 = (df_reforme['recettes_reforme_poste_11_1_3_2'] * df_reforme['pondmen']).sum() / 1e6

recettes_reforme = (
    recettes_poste_11_1_1_1_1
    + recettes_poste_11_1_1_1_2
    + recettes_poste_11_1_3_1
    + recettes_poste_11_1_3_2
    )
