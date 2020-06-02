# -*- coding: utf-8 -*-

import os
import pandas as pd
import pkg_resources

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, dataframe_by_group
from openfisca_france_indirect_taxation.reforms.reforme_tva_2019 import reforme_tva_2019
from openfisca_france_indirect_taxation.projects.base import elasticite_tabac


inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'depenses_cigarettes',
    'depenses_cigares',
    'depenses_tabac_a_rouler',
    'rev_disp_loyerimput',
    'depenses_tot',
    'pondmen',
    ]

survey_scenario = SurveyScenario.create(
    inflation_kwargs = inflation_kwargs,
    reform = reforme_tva_2019,
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

prix_paquet = {'2017': 7.1, '2018': 7.9}
prix_tabac_rouler = {'2017': 8.8, '2018': 10.8}


for baseline_year in ['2018']:
    
    # Résultats agrégés par déciles de niveau de vie
    df = dataframe_by_group(survey_scenario, category = 'niveau_vie_decile', variables = simulated_variables)
    
    # Calibration du nombre de paquets moyen par ménage
    nombre_paquets_annuel = 2.21e9  # Nb de paquets de 20 cigarettes consommés en France par an en 2017
    paquets_par_menage = nombre_paquets_annuel / (df_reforme['pondmen']).sum()  # Nombre moyen de paquets par ménage en 2017
    df['nombre_paquets_moyen'] = paquets_par_menage * (df['depenses_cigarettes'] * 10) / (df['depenses_cigarettes'].sum())
    df['depenses_cigarettes'] = df['nombre_paquets_moyen'] * prix_paquet[baseline_year]
    
    # REFORME CIGARETTES : Effet d'une augmentation de 80c du prix du paquet en 2018, 50c en avril 2019, puis 50c en novembre, avec élasticité :
    df['depenses_cigarettes_janvier_2019'] = df['depenses_cigarettes'] * (1 + (1 + elasticite_tabac) * ((7.9 - prix_paquet[baseline_year]) / prix_paquet[baseline_year]))
    df['depenses_cigarettes_avril_2019'] = df['depenses_cigarettes'] * (1 + (1 + elasticite_tabac) * ((8.4 - prix_paquet[baseline_year]) / prix_paquet[baseline_year]))
    df['depenses_cigarettes_novembre_2019'] = df['depenses_cigarettes'] * (1 + (1 + elasticite_tabac) * ((8.9 - prix_paquet[baseline_year]) / prix_paquet[baseline_year]))
    df['cout_reforme_cigarettes_elasticite'] = (
        3 * df['depenses_cigarettes_janvier_2019'] 
        + 7 * df['depenses_cigarettes_avril_2019'] 
        + 2 * df['depenses_cigarettes_novembre_2019']
        ) / 12 - df['depenses_cigarettes']
    
    # REFORME TABAC A ROULER : Effet d'une augmentation du prix de la bague de tabac de 10.8€ à 11.7€ en avril, puis 12.6€ en novembre, avec élasticité
    df['depenses_tabac_a_rouler_janvier_2019'] = df['depenses_tabac_a_rouler'] * (1 + (1 + elasticite_tabac) * ((10.8 - prix_tabac_rouler[baseline_year]) / prix_tabac_rouler[baseline_year]))
    df['depenses_tabac_a_rouler_avril_2019'] = df['depenses_tabac_a_rouler'] * (1 + (1 + elasticite_tabac) * ((11.7 - prix_tabac_rouler[baseline_year]) / prix_tabac_rouler[baseline_year]))
    df['depenses_tabac_a_rouler_novembre_2019'] = df['depenses_tabac_a_rouler'] * (1 + (1 + elasticite_tabac) * ((12.6 - prix_tabac_rouler[baseline_year]) / prix_tabac_rouler[baseline_year]))
    df['cout_reforme_tabac_rouler_elasticite'] = (
        3 * df['depenses_tabac_a_rouler_janvier_2019']
        + 7 * df['depenses_tabac_a_rouler_avril_2019'] 
        + 2 * df['depenses_tabac_a_rouler_novembre_2019']
        ) / 12 - df['depenses_tabac_a_rouler']

    # Effet pour l'ensemble des réformes, avec élasticités
    df['cout_reforme_elasticite'] = df['cout_reforme_cigarettes_elasticite'] + df['cout_reforme_tabac_rouler_elasticite']
    df['cout_reforme_rev_disp_loyerimput_elasticite'] = df['cout_reforme_elasticite'] / df['rev_disp_loyerimput']
    df['cout_reforme_depenses_tot_elasticite'] = df['cout_reforme_elasticite'] / df['depenses_tot']
    graph_builder_bar(df['cout_reforme_rev_disp_loyerimput_elasticite'], False)
    print("Coût total de la réforme : {} milliards d'euros".format(df['cout_reforme_elasticite'].mean() * df_reforme['pondmen'].sum()/1e9))
    
    ## Test
    if baseline_year == '2017':
        reforme = "2018_2019"
    if baseline_year == '2018':
        reforme = "2019"
    test_assets_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
        'openfisca_france_indirect_taxation',
        'assets',
        'tests'
        )
    resultats_a_reproduire = pd.read_csv(os.path.join(test_assets_directory,"resultats_reformes_tabac_budget_{}.csv".format(reforme)), header = None)
    assert (abs(df['cout_reforme_rev_disp_loyerimput_elasticite'].values - resultats_a_reproduire[0].values) < 1e-6).all()
