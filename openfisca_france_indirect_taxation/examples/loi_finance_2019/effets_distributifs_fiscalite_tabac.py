# -*- coding: utf-8 -*-

# This script depicts households' net fiscal transfers from the reform.
# It is equal to the transfers received from the reform, minus the additional
# taxes paid. A positive value means the household received higher transfers than
# the increase in taxes he faced. These amounts do not take into account VAT.

# Import general modules


# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
#elasticities = get_elasticities(data_year)
#elasticities = get_elasticities_aidsills(data_year, True)
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
    #elasticities = elasticities,
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
paquets_par_menage = nombre_paquets_annuel / nombre_menages  # Nombre moyen de paquets par adulte en 2017

for category in ['niveau_vie_decile']:  # ['niveau_vie_decile', 'age_group_pr', 'strate']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables)

    # Calibration du nombre de paquets moyen par ménage
    df['nombre_paquets_moyen'] = paquets_par_menage * (df['poste_02_2_1'] * 10) / (df['poste_02_2_1'].sum())

    # Elasticité
    elas_tabac = -0.5

    # Effet d'une augmentation de 50c du prix du paquet en avril, puis 50c en novembre, avec élasticité :
    df['depenses_cigarettes_janvier'] = df['nombre_paquets_moyen'] * 7.9
    df['depenses_cigarettes_avril'] = df['depenses_cigarettes_janvier'] * (1 + (1 + elas_tabac) * ((8.4 - 7.9) / 7.9))
    df['depenses_cigarettes_novembre'] = df['depenses_cigarettes_janvier'] * (1 + (1 + elas_tabac) * ((8.9 - 7.9) / 7.9))
    df['cout_reforme_cigarettes_elasticite'] = (
        3 * df['depenses_cigarettes_janvier'] + 7 * df['depenses_cigarettes_avril'] + 2 * df['depenses_cigarettes_novembre']
        ) / 12 - df['depenses_cigarettes_janvier']

    df['reduction_nombre_paquets_avril'] = - df['nombre_paquets_moyen'] * elas_tabac * (0.5 / 7.9)
    df['reduction_nombre_paquets_novembre'] = (
        -(df['nombre_paquets_moyen'] - df['reduction_nombre_paquets_avril']) * elas_tabac * (0.5 / 7.9)
        )

    # Effet d'une augmentation du prix de la bague de tabac de 10.8€ à 11.7€ en avril, puis 12.6€ en novembre, avec élasticité
    df['poste_02_2_3_avril'] = df['poste_02_2_3'] * (1 + (1 + elas_tabac) * ((11.7 - 10.8) / 10.8))
    df['poste_02_2_3_novembre'] = df['poste_02_2_3'] * (1 + (1 + elas_tabac) * ((12.6 - 10.8) / 10.8))
    df['cout_reforme_tabac_rouler_elasticite'] = (
        3 * df['poste_02_2_3'] + 7 * df['poste_02_2_3_avril'] + 2 * df['poste_02_2_3_novembre']
        ) / 12 - df['poste_02_2_3']

    # Effet pour l'ensemble de la réforme, avec élasticités
    df['cout_reforme_elasticite'] = df['cout_reforme_cigarettes_elasticite'] + df['cout_reforme_tabac_rouler_elasticite']

    df['cout_reforme_rev_disp_loyerimput_elasticite'] = df['cout_reforme_elasticite'] / df['rev_disp_loyerimput']
    df['cout_reforme_depenses_tot_elasticite'] = df['cout_reforme_elasticite'] / df['depenses_tot']

    df['taux_effort_reforme'] = df['cout_reforme_elasticite'] / df['rev_disp_loyerimput']

    graph_builder_bar(df['cout_reforme_elasticite'], False)
    graph_builder_bar(df['cout_reforme_rev_disp_loyerimput_elasticite'], False)
    graph_builder_bar(df['cout_reforme_depenses_tot_elasticite'], False)

    # Calculer le budget total
    print(df['cout_reforme_elasticite'].mean())
    print(df['cout_reforme_elasticite'].mean() * df_reforme['pondmen'].sum())
