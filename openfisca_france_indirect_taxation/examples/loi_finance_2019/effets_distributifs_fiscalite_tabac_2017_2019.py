# -*- coding: utf-8 -*-

# This script depicts households' net fiscal transfers from the reform.
# It is equal to the transfers received from the reform, minus the additional
# taxes paid. A positive value means the household received higher transfers than
# the increase in taxes he faced. These amounts do not take into account VAT.


from openfisca_france_indirect_taxation.examples.utils_example import (
    graph_builder_bar,
    dataframe_by_group,
    )
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'poste_02_2_1',  # cigarettes
    'poste_02_2_2',  # cigares et cigarillos
    'poste_02_2_3',  # tabac sous d'autres formes
    'rev_disp_loyerimput',
    'depenses_tot',
    'ocde10',
    'pondmen',
    'nadultes',
    ]

survey_scenario = SurveyScenario.create(
    # elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'reforme_tva_2019',
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
df_reforme['depenses_tabac'] = df_reforme['poste_02_2_1'] + df_reforme['poste_02_2_2'] + df_reforme['poste_02_2_3']
print((df_reforme['poste_02_2_3'] * df_reforme['pondmen']).sum() / (df_reforme['depenses_tabac'] * df_reforme['pondmen']).sum())

nombre_paquets_annuel = 2.21e9  # Nb de paquets de 20 cigarettes consommés en France par an en 2017
nombre_menages = (df_reforme['pondmen']).sum()
paquets_par_menage = nombre_paquets_annuel / nombre_menages  # Nombre moyen de paquets par ménage en 2017

for category in ['niveau_vie_decile']:  # ['niveau_vie_decile', 'age_group_pr', 'strate']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables)

    # Calibration du nombre de paquets moyen par ménage
    df['nombre_paquets_moyen'] = paquets_par_menage * (df['poste_02_2_1'] * 10) / (df['poste_02_2_1'].sum())

    # Elasticité
    elas_tabac = -0.5  # valeur provenant de la littérature. Sur la période 2005-2015 elle a été estimée à -0.41

    # Effet d'une augmentation de 80c du prix du paquet en 2018, 50c en avril 2019, puis 50c en novembre, avec élasticité :
    df['depenses_cigarettes_2017'] = df['nombre_paquets_moyen'] * 7.1
    df['depenses_cigarettes_janvier_2019'] = df['depenses_cigarettes_2017'] * (1 + (1 + elas_tabac) * ((7.9 - 7.1) / 7.1))
    df['depenses_cigarettes_avril_2019'] = df['depenses_cigarettes_2017'] * (1 + (1 + elas_tabac) * ((8.4 - 7.1) / 7.1))
    df['depenses_cigarettes_novembre_2019'] = df['depenses_cigarettes_2017'] * (1 + (1 + elas_tabac) * ((8.9 - 7.1) / 7.1))
    df['cout_reforme_cigarettes_elasticite_2019'] = (
        3 * df['depenses_cigarettes_janvier_2019'] + 7 * df['depenses_cigarettes_avril_2019'] + 2 * df['depenses_cigarettes_novembre_2019']
        ) / 12 - df['depenses_cigarettes_2017']

    df['reduction_nombre_paquets_janvier'] = - df['nombre_paquets_moyen'] * elas_tabac * (0.5 / 7.1)
    df['reduction_nombre_paquets_avril'] = (
        -(df['nombre_paquets_moyen'] - df['reduction_nombre_paquets_janvier']) * elas_tabac * (0.5 / 7.1)
        )
    df['reduction_nombre_paquets_novembre'] = (
        -(df['nombre_paquets_moyen'] - df['reduction_nombre_paquets_janvier'] - df['reduction_nombre_paquets_avril']) * elas_tabac * (0.5 / 7.1)
        )

    # Effet d'une augmentation du prix de la bague de tabac de 10.8€ à 11.7€ en avril, puis 12.6€ en novembre, avec élasticité
    df['poste_02_2_3_janvier_2019'] = df['poste_02_2_3'] * (1 + (1 + elas_tabac) * ((10.8 - 8.8) / 8.8))
    df['poste_02_2_3_avril_2019'] = df['poste_02_2_3'] * (1 + (1 + elas_tabac) * ((11.7 - 8.8) / 8.8))
    df['poste_02_2_3_novembre_2019'] = df['poste_02_2_3'] * (1 + (1 + elas_tabac) * ((12.6 - 8.8) / 8.8))
    df['cout_reforme_tabac_rouler_elasticite_2019'] = (
        3 * df['poste_02_2_3_janvier_2019'] + 7 * df['poste_02_2_3_avril_2019'] + 2 * df['poste_02_2_3_novembre_2019']
        ) / 12 - df['poste_02_2_3']

    # Effet pour l'ensemble de la réforme, avec élasticités
    df['cout_reforme_elasticite_2019'] = df['cout_reforme_cigarettes_elasticite_2019'] + df['cout_reforme_tabac_rouler_elasticite_2019']

    df['cout_reforme_rev_disp_loyerimput_elasticite_2019'] = df['cout_reforme_elasticite_2019'] / df['rev_disp_loyerimput']
    df['cout_reforme_depenses_tot_elasticite_2019'] = df['cout_reforme_elasticite_2019'] / df['depenses_tot']

    graph_builder_bar(df['cout_reforme_elasticite_2019'], False)
    graph_builder_bar(df['cout_reforme_rev_disp_loyerimput_elasticite_2019'], False)
    graph_builder_bar(df['cout_reforme_depenses_tot_elasticite_2019'], False)

    # Calculer le budget total
    print(df['cout_reforme_elasticite_2019'].mean() * df_reforme['pondmen'].sum())
