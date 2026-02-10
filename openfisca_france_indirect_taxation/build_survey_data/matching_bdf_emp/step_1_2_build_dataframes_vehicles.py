# -*- coding: utf-8 -*-

# Dans ce script on importe les données des enquêtes BdF 2017 et EMP 2019.
# Pour chacune des deux enquêtes on importe les variables qui seront
# susceptibles d'êtres utilisées dans l'appariement des bases de données.

import pandas as pd
import numpy as np
from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager.paths import default_config_files_directory as config_files_directory

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_emp.step_1_1_build_dataframes_menages import \
    load_data_menages_bdf_emp


def load_data_vehicules_bdf_emp(year_data):
    year_emp = 2019

    emp_survey_collection = SurveyCollection.load(
        collection = 'enquete_transports', config_files_directory = config_files_directory
        )
    survey_emp = emp_survey_collection.get_survey('enquete_transports_{}'.format(year_emp))
    input_emp_vehicule = survey_emp.get_values(table = 'q_voitvul_public_V2')
    input_emp_menage = survey_emp.get_values(table = 'q_menage_public_V2')

    # Load BdF data :

    year_bdf = year_data

    openfisca_survey_collection = SurveyCollection.load(collection = 'budget_des_familles')
    openfisca_survey = openfisca_survey_collection.get_survey('budget_des_familles_{}'.format(year_bdf))
    input_bdf = openfisca_survey.get_values(table = 'AUTOMOBILE')
    input_bdf.reset_index(inplace = True)

    variables_vehicules_emp = [
        'ident_men',        # identifiant du ménage
        'ident_numveh',     # identifiant du véhicule
        'num_veh',          # numéro du véhicule
        'energie_agrege',   # carburant principal
        'puis_fisc_fin',    # puissance fiscale
        'age',              # age du véhicule (en mois)
        # 'v1_rang_veh',    # rang du véhicule dans le ménage
        # 'v1_sfvachat',    # état du véhicule à l'achat
        'kvcons',           # consommation
        # 'v1_sfvdatcg',    # date carte grise
        'annee_1mec',       # Année mise en circulation
        'kvkm1anv'          # nb kilomètres 12 derniers mois, redressés
        ]

    variables_menage_emp = [
        'ident_men',
        'pond_menc',           # poids ménage
        # 'v1_logdist01',     # distance commerces et supermarchés                       (pas dans q_menage regarder ailleurs ?)
        # 'v1_logdist15',     # distance arrêts transports en commun                     (pas dans q_menage regarder ailleurs ?)
        'jnbveh',             # nb de voitures particulières
        # 'v1_jpasvoit_b',    # utilité du VP : se rendre au travail                     (pas dans q_menage regarder ailleurs ?)
        # 'v1_jpasvoit_c',    # utilité du VP : déplacements dans le cadre du travail    (pas dans q_menage regarder ailleurs ?)
        ]

    if year_bdf == 2011:
        variables_vehicules_bdf = [
            'ident_men',
            'acqvoi',           # état du véhicule à l'achat
            'anvoi',            # année du véhicule
            'carbu',            # carburant utilisé
            'expvoi1',          # est utilisé pour les trajets domicile-travail
            'expvoi2',          # est utilisé pour les déplacements professionnels
            'km_auto',
            'nbvehic',          # nb de véhicules du ménage
            'numvehic',         # numéro du véhicule
            'privoi_d',         # prix à l'achat, redressé
            'recvoi',           # année d'achat
            ]
    if year_bdf == 2017:
        variables_vehicules_bdf = [
            'ident_men',
            'acqvoi',           # état du véhicule à l'achat
            'anvoi',            # année du véhicule
            'carbu1',           # le carburant utilisé est l'essence
            'carbu2',           # diesel
            'carbu3',           # GPL
            'carbu4',           # electrique
            'carbu5',           # autre type de carburant
            'expvoi1',          # est utilisé pour les trajets domicile-travail
            'expvoi2',          # est utilisé pour les déplacements professionnels
            'km_auto',
            'nbvehic',          # nb de véhicules du ménage
            'numvehic',         # numéro du véhicule
            'privoi_d',         # prix à l'achat, redressé
            'recvoi',           # année d'achat
            ]

    # Keep relevant variables :
    vehicule_menage_emp_keep = input_emp_vehicule[variables_vehicules_emp]
    menage_emp_keep = input_emp_menage[variables_menage_emp]
    vehicule_bdf_keep = input_bdf[variables_vehicules_bdf]

    return vehicule_bdf_keep, vehicule_menage_emp_keep, menage_emp_keep


def imputation_carburants(df, var_carbu, var_nb_vehicule, weight_col):
    '''
    Impute les valeurs manquantes de la variable de carburant en utilisant les proportions de chaque carburant par ménage si le ménage a au moins un véhicule dont le carburant est connue
    ou les proportions globales si le ménage a des véhicules mais aucun carburant connu.

    Args:
        df(DataFrame): les données à imputer
        var_carbu(str): variable de carburant à imputer
        var_nb_vehicule(str): variable du nombre de véhicules dans le ménage
        weight_col(str): variable de pondération des ménages

    Returns:
        df(DataFrame): les données avec la variable de carburant imputée
    '''
    # Définition des véhicules par carburant
    df['essence'] = 0
    df.loc[df[var_carbu] == 1, 'essence'] = 1
    df['diesel'] = 0
    df.loc[df[var_carbu] == 2, 'diesel'] = 1
    df['autre_carbu'] = 0
    df.loc[df[var_carbu] > 2, 'autre_carbu'] = 1

    # Calculer les proportions par ménage (pour les ménages ayant des véhicules avec carburant connu)
    proportions = (
        df.groupby('ident_men')
        [['essence', 'diesel', 'autre_carbu']]
        .sum()
        .pipe(lambda df: df.assign(tot_carbu=df.sum(axis=1)))
        .assign(
            prop_essence=lambda x: x['essence'] / x['tot_carbu'],
            prop_diesel=lambda x: x['diesel'] / x['tot_carbu'],
            prop_autre_carbu=lambda x: x['autre_carbu'] / x['tot_carbu']
            )
        )

    # Fusionner les proportions avec la base originale
    df = df.merge(
        proportions[['prop_essence', 'prop_diesel', 'prop_autre_carbu']],
        left_on='ident_men',
        right_index=True,
        how='left'
        )

    # Imputer les carburants manquants en fonction des proportions par ménage
    df.loc[df[var_carbu].isna() & df['prop_essence'].notna(), 'var_imputee'] = df.loc[df[var_carbu].isna() & df['prop_essence'].notna()].apply(
        lambda row: np.random.choice([1, 2, 6], p=[row['prop_essence'], row['prop_diesel'], row['prop_autre_carbu']]), axis=1)

    # Calculer les proportions sur toute la population
    proportions_globale = (
        df[['essence', 'diesel', 'autre_carbu']]
        .mul(df[weight_col], axis=0)  # Multiplier chaque colonne par pond_menc
        .sum()
        .to_frame().T  # Convertir en DataFrame avec une seule ligne
        .assign(tot_carbu=lambda df: df.sum(axis=1))
        .assign(
            prop_essence=lambda x: x['essence'] / x['tot_carbu'],
            prop_diesel=lambda x: x['diesel'] / x['tot_carbu'],
            prop_autre_carbu=lambda x: x['autre_carbu'] / x['tot_carbu']
            )
        )
    # Imputer les carburants manquants en fonction des proportions globales
    df.loc[df[var_carbu].isna() & df['prop_essence'].isna() & df[var_nb_vehicule] > 0, 'var_imputee'] = df.loc[df[var_carbu].isna() & df['prop_essence'].isna() & df[var_nb_vehicule] > 0].apply(
        lambda row: np.random.choice([1, 2, 6], p=[proportions_globale['prop_essence'][0], proportions_globale['prop_diesel'][0], proportions_globale['prop_autre_carbu'][0]]), axis=1)

    # Remplacer la variabe intiale par la variable imputée
    df.loc[:, var_carbu] = df[var_carbu].fillna(df['var_imputee'])
    df = df.drop(columns=['essence', 'diesel', 'autre_carbu', 'prop_essence', 'prop_diesel', 'prop_autre_carbu', 'var_imputee'])

    return df


def merge_vehicule_menage(year_data):

    data_bdf, data_emp, data_emp_menage = load_data_vehicules_bdf_emp(2017)
    data_emp_full = data_emp_menage.merge(data_emp, on = 'ident_men', how = 'left')
    data_emp_full = imputation_carburants(data_emp_full, 'energie_agrege', 'jnbveh', 'pond_menc')
    year_data = 2017

    # Calcul de l'âge du véhicule
    data_emp_full['anvoi'] = pd.to_numeric(data_emp_full['annee_1mec'], errors = 'coerce')

    data_emp_full['age_vehicule'] = 0
    data_emp_full.loc[data_emp_full['anvoi'] != 0, 'age_vehicule'] = 2019 - data_emp_full['anvoi']

    data_bdf['anvoi'] = data_bdf['anvoi'].fillna(0).astype(int)
    data_bdf['age_vehicule'] = 0
    data_bdf.loc[data_bdf['anvoi'] != 0, 'age_vehicule'] = year_data - data_bdf['anvoi']

    # Définition des véhicules par carburant
    data_emp_full['essence'] = 0
    data_emp_full.loc[data_emp_full['energie_agrege'] == 1, 'essence'] = 1
    data_emp_full['diesel'] = 0
    data_emp_full.loc[data_emp_full['energie_agrege'] == 2, 'diesel'] = 1
    data_emp_full['autre_carbu'] = 0
    data_emp_full.loc[data_emp_full['energie_agrege'] > 2, 'autre_carbu'] = 1

    if year_data == 2017:
        carbu_cols = ['carbu1', 'carbu2', 'carbu3', 'carbu4', 'carbu5']
        data_bdf['carbu'] = data_bdf[carbu_cols].idxmax(axis=1).str.extract(r'(\d)').astype(int)
        data_bdf.drop(carbu_cols, axis = 1, inplace = True)

    data_bdf['essence'] = 0
    data_bdf.loc[data_bdf['carbu'] == 1, 'essence'] = 1
    data_bdf['diesel'] = 0
    data_bdf.loc[data_bdf['carbu'] == 2, 'diesel'] = 1
    data_bdf['autre_carbu'] = 0
    data_bdf.loc[data_bdf['carbu'] > 2, 'autre_carbu'] = 1

    # déf des distances parcourues par carburant
    data_emp_full['distance_essence'] = 0.0
    data_emp_full.loc[data_emp_full['essence'] == 1, 'distance_essence'] = data_emp_full['kvkm1anv']
    data_emp_full['distance_diesel'] = 0.0
    data_emp_full.loc[data_emp_full['diesel'] == 1, 'distance_diesel'] = data_emp_full['kvkm1anv']
    data_emp_full['distance_autre_carbu'] = 0.0
    data_emp_full.loc[data_emp_full['autre_carbu'] == 1, 'distance_autre_carbu'] = data_emp_full['kvkm1anv']

    # Df avec le nombre de véhicule et les distances pour chaque type de carburant
    data_vehicule_emp = data_emp_full[
        ['essence',
        'diesel',
        'autre_carbu',
        'distance_essence',
        'distance_diesel',
        'distance_autre_carbu',
        'ident_men']
        ].groupby(by = 'ident_men').sum()
    data_vehicule_emp = data_vehicule_emp.reset_index()

    # Df avec les infos du véhicule principal (dans emp)
    data_emp_full = data_emp_full.sort_values(by = 'kvkm1anv', ascending= False)
    data_emp_full = data_emp_full.drop_duplicates(['ident_men'], keep='first')
    data_emp_full.rename(
        columns = {
            'puis_fisc_fin': 'puissance',
            'kvcons': 'consommation',
            },
        inplace = True,
        )
    data_emp = data_emp_full[['ident_men', 'puissance', 'consommation', 'age_vehicule']]

    # déf des distances parcourues par carburant
    data_bdf['km_essence'] = 0.0
    data_bdf.loc[data_bdf['essence'] == 1, 'km_essence'] = data_bdf['km_auto']
    data_bdf['km_diesel'] = 0.0
    data_bdf.loc[data_bdf['diesel'] == 1, 'km_diesel'] = data_bdf['km_auto']
    data_bdf['km_autre_carbu'] = 0.0
    data_bdf.loc[data_bdf['autre_carbu'] == 1, 'km_autre_carbu'] = data_bdf['km_auto']

    # Df avec le nombre de véhicule et les distances pour chaque type de carburant
    data_vehicule_bdf = data_bdf[
        ['essence',
        'diesel',
        'autre_carbu',
        'km_essence',
        'km_diesel',
        'km_autre_carbu',
        'ident_men']
        ].groupby(by = 'ident_men').sum()
    data_vehicule_bdf = data_vehicule_bdf.reset_index()

    # Df avec les infos du véhicule principal (dans BdF)
    data_bdf = data_bdf.sort_values(by = ['nbvehic'])
    data_bdf = data_bdf.drop_duplicates(['ident_men'], keep='first')
    data_bdf.rename(
        columns = {
            'acqvoi': 'etat_veh_achat',
            'expvoi1': 'vp_domicile_travail',
            'expvoi2': 'vp_deplacements_pro',
            'nbvehic': 'veh_tot',
            'privoi_d': 'prix_achat',
            },
        inplace = True,
        )
    data_bdf = data_bdf[
        ['ident_men', 'prix_achat', 'veh_tot', 'etat_veh_achat', 'age_vehicule', 'vp_domicile_travail', 'vp_deplacements_pro']
        ]

    # Merge les différentes df
    data_emp_final = data_vehicule_emp.merge(data_emp, on = 'ident_men', how = 'left')
    data_bdf_full = data_vehicule_bdf.merge(data_bdf, on = 'ident_men', how = 'left')

    return data_bdf_full, data_emp_final


def build_df_menages_vehicles(year_data):
    data_menages_bdf, data_menages_emp = load_data_menages_bdf_emp(year_data)

    data_vehicules_bdf, data_vehicules_emp = merge_vehicule_menage(year_data)
    data_vehicules_bdf['ident_men'] = data_vehicules_bdf['ident_men'].astype(str)

    data_emp = data_menages_emp.merge(data_vehicules_emp, on = 'ident_men')
    data_bdf = data_menages_bdf.merge(data_vehicules_bdf, on = 'ident_men', how = 'left')

    return data_bdf, data_emp


if __name__ == '__main__':
    data_bdf, data_emp = build_df_menages_vehicles(2017)
