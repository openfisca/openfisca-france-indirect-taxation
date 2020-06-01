# -*- coding: utf-8 -*-

from openfisca_france_indirect_taxation.examples.utils_example import (
    graph_builder_bar,
    dataframe_by_group,
    )
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.reforms.reforme_tva_2019 import reforme_tva_2019


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
    'ocde10',
    'pondmen',
    'nadultes',
    ]

survey_scenario = SurveyScenario.create(
    # elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform = reforme_tva_2019,
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

nombre_paquets_annuel = 2.21e9  # Nb de paquets de 20 cigarettes consommés en France par an en 2017
paquets_par_menage = nombre_paquets_annuel / (df_reforme['pondmen']).sum()  # Nombre moyen de paquets par ménage en 2017


df = dataframe_by_group(survey_scenario, category = 'niveau_vie_decile', variables = simulated_variables)

# Calibration du nombre de paquets moyen par ménage
df['nombre_paquets_moyen'] = paquets_par_menage * (df['depenses_cigarettes'] * 10) / (df['depenses_cigarettes'].sum())

# Elasticité
elas_tabac = -0.5  # valeur provenant de la littérature. Hill & Legoupil (2018) -0,5 sur la période 1950-2015 et -0,4 sur la période 2000-2015

# REFORME CIGARETTES : Effet d'une augmentation de 80c du prix du paquet en 2018, 50c en avril 2019, puis 50c en novembre, avec élasticité :
df['depenses_cigarettes_2017'] = df['nombre_paquets_moyen'] * 7.1
df['depenses_cigarettes_janvier_2019'] = df['depenses_cigarettes_2017'] * (1 + (1 + elas_tabac) * ((7.9 - 7.1) / 7.1))
df['depenses_cigarettes_avril_2019'] = df['depenses_cigarettes_2017'] * (1 + (1 + elas_tabac) * ((8.4 - 7.1) / 7.1))
df['depenses_cigarettes_novembre_2019'] = df['depenses_cigarettes_2017'] * (1 + (1 + elas_tabac) * ((8.9 - 7.1) / 7.1))

# Coût cumulé réformes budget 2018 et 2019 en 2019
# Pas de notion de contrefactuel ici car la législation ne "vieillit" pas chaque année
df['cout_reforme_cigarettes_elasticite_2019'] = (
    3 * df['depenses_cigarettes_janvier_2019'] + 7 * df['depenses_cigarettes_avril_2019'] + 2 * df['depenses_cigarettes_novembre_2019']
    ) / 12 - df['depenses_cigarettes_2017']


# REFORME TABAC A ROULER : Effet d'une augmentation du prix de la bague de tabac de 10.8€ à 11.7€ en avril, puis 12.6€ en novembre, avec élasticité
df['depenses_tabac_a_rouler_janvier_2019'] = df['depenses_tabac_a_rouler'] * (1 + (1 + elas_tabac) * ((10.8 - 8.8) / 8.8))
df['depenses_tabac_a_rouler_avril_2019'] = df['depenses_tabac_a_rouler'] * (1 + (1 + elas_tabac) * ((11.7 - 8.8) / 8.8))
df['depenses_tabac_a_rouler_novembre_2019'] = df['depenses_tabac_a_rouler'] * (1 + (1 + elas_tabac) * ((12.6 - 8.8) / 8.8))
df['cout_reforme_tabac_rouler_elasticite_2019'] = (
    3 * df['depenses_tabac_a_rouler_janvier_2019'] + 7 * df['depenses_tabac_a_rouler_avril_2019'] + 2 * df['depenses_tabac_a_rouler_novembre_2019']
    ) / 12 - df['depenses_tabac_a_rouler']

# Effet pour l'ensemble des réformes, avec élasticités
df['cout_reforme_elasticite_2019'] = df['cout_reforme_cigarettes_elasticite_2019'] + df['cout_reforme_tabac_rouler_elasticite_2019']
df['cout_reforme_rev_disp_loyerimput_elasticite_2019'] = df['cout_reforme_elasticite_2019'] / df['rev_disp_loyerimput']
df['cout_reforme_depenses_tot_elasticite_2019'] = df['cout_reforme_elasticite_2019'] / df['depenses_tot']

# Représentation graphique
graph_builder_bar(df['cout_reforme_rev_disp_loyerimput_elasticite_2019'], False)

# Calculer le budget total
print("Coût total de la réforme : {} milliards d'euros".format(df['cout_reforme_elasticite_2019'].mean() * df_reforme['pondmen'].sum()/1e9))
