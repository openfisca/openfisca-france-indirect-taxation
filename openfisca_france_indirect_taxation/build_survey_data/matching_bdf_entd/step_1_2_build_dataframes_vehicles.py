# -*- coding: utf-8 -*-

# Dans ce script on importe les données des enquêtes BdF 2011 et ENTD 2008.
# Pour chacune des deux enquêtes on importe les variables qui seront
# susceptibles d'êtres utilisées dans l'appariement des bases de données.


# To do : add information about vehicles

from __future__ import division

from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_survey_manager.temporary import TemporaryStore


temporary_store = TemporaryStore.create(file_name = 'transport_tmp')


def load_data_vehicules_bdf_entd():
    # Load ENTD data :
    # Ajouter les variables d'appariement ET les variables à apparier
    
    year_entd = 2008
    
    entd_survey_collection = SurveyCollection.load(
        collection = 'enquete_transport', config_files_directory = config_files_directory
        )
    survey_entd = entd_survey_collection.get_survey('enquete_transport_{}'.format(year_entd))
    input_entd_vehicule = survey_entd.get_values(table = 'qf_voitvul')
    input_entd_menage = survey_entd.get_values(table = 'q_menage')

    
    # Load BdF data :
    
    year_bdf = 2011
    
    openfisca_survey_collection = SurveyCollection.load(collection = 'budget_des_familles')
    openfisca_survey = openfisca_survey_collection.get_survey('budget_des_familles_{}'.format(year_bdf))
    input_bdf = openfisca_survey.get_values(table = 'AUTOMOBILE')
    input_bdf.reset_index(inplace = True)
    
    variables_vehicules_entd = [
        'ident_men',
        'ident_numveh', # identifiant du véhicule
        'mveh', # numéro du véhicule
        'v1_ken', # carburant principal
        'v1_puiss_corr', # puissance fiscale corrigée
        'v1_age_veh', # age du véhicule
        'v1_rang_veh', # rang du véhicule dans le ménage
        'v1_sfvachat', # état du véhicule à l'achat
        'v1_sfvcosorout', # consommation
        'v1_sfvdatcg', # date carte grise
        'v1_sfvdat1mc', # date mise en circulation
        'v1_km_annu' # nb kilomètres 12 derniers mois, redressés
        ]

    variables_menage_entd = [
        'ident_men',
        'v1_logdist01', # distance commerces et supermarchés
        'v1_logdist15', # distance arrêts transports en commun
        'v1_jnbveh', # nb de voitures particulières
        'v1_jpasvoit_b', # utilité du VP : se rendre au travail
        'v1_jpasvoit_c', # utilité du VP : déplacements dans le cadre du travail
        ]

    variables_vehicules_bdf = [
        'ident_men',
        'acqvoi', # état du véhicule à l'achat
        'anvoi', # année du véhicule
        'carbu', # carburant utilisé
        'expvoi1', #  est utilisé pour les trajets domicile-travail
        'expvoi2', # est utilisé pour les déplacements professionnels
        'km_auto',
        'nbvehic', # nb de véhicules du ménage
        'numvehic', # numéro du véhicule
        'privoi_d', # prix à l'achat, redressé
        'recvoi', # année d'achat
        ]


    # Keep relevant variables :
    vehicule_menage_entd_keep = input_entd_vehicule[variables_vehicules_entd]
    menage_entd_keep = input_entd_menage[variables_menage_entd]
    vehicule_bdf_keep = input_bdf[variables_vehicules_bdf]

    return vehicule_menage_entd_keep,  menage_entd_keep, vehicule_bdf_keep


def merge_vehicule_menage():
    data = load_data_vehicules_bdf_entd()
    data_entd = data[0]
    data_entd_menage = data[1]
    data_bdf = data[2]

    # Calcul de l'âge du véhicule et de la carte grise
    data_entd['anvoi'] = 0
    data_entd['check_annee'] = data_entd['v1_sfvdat1mc'].str[2]
    data_entd.loc[data_entd['check_annee'] == '/', 'anvoi'] = data_entd['v1_sfvdat1mc'].str[6:].copy()
    del data_entd['v1_sfvdat1mc'], data_entd['check_annee']

    data_entd['recvoi'] = 0
    data_entd['check_annee'] = data_entd['v1_sfvdatcg'].str[2]
    data_entd.loc[data_entd['check_annee'] == '/', 'recvoi'] = data_entd['v1_sfvdatcg'].str[6:].copy()
    del data_entd['v1_sfvdatcg'], data_entd['check_annee']

    data_entd[['anvoi'] + ['recvoi']] = data_entd[['anvoi'] + ['recvoi']].astype(int, inplace = True)

    data_bdf[['anvoi'] + ['recvoi']] = data_bdf[['anvoi'] + ['recvoi']].fillna(0)
    data_bdf[['anvoi'] + ['recvoi']] = data_bdf[['anvoi'] + ['recvoi']].astype(int, inplace = True)


    data_entd['age_vehicule'] = 0
    data_bdf['age_vehicule'] = 0
    data_entd.loc[data_entd['anvoi'] != 0, 'age_vehicule'] = 2008 - data_entd['anvoi']
    data_bdf.loc[data_bdf['anvoi'] != 0, 'age_vehicule'] = 2011 - data_bdf['anvoi']

    data_entd['age_carte_grise'] = 0
    data_bdf['age_carte_grise'] = 0
    data_entd.loc[data_entd['recvoi'] != 0, 'age_carte_grise'] = 2008 - data_entd['recvoi']
    data_bdf.loc[data_bdf['recvoi'] != 0, 'age_carte_grise'] = 2011 - data_bdf['recvoi']
    
    # Définition des véhicules par carburant
    data_entd['essence'] = 0
    data_entd.loc[data_entd['v1_ken'] < 4, 'essence'] = 1
    data_entd['diesel'] = 0
    data_entd.loc[data_entd['v1_ken'] == 4, 'diesel'] = 1  
    data_entd['autre_carbu'] = 0    
    data_entd.loc[data_entd['v1_ken'] > 4, 'autre_carbu'] = 1  

    # déf des distances parcourues par carburant
    data_entd['distance_essence'] = 0
    data_entd.loc[data_entd['essence'] == 1, 'distance_essence'] = data_entd['v1_km_annu']
    data_entd['distance_diesel'] = 0
    data_entd.loc[data_entd['diesel'] == 1, 'distance_diesel'] = data_entd['v1_km_annu']
    data_entd['distance_autre_carbu'] = 0
    data_entd.loc[data_entd['autre_carbu'] == 1, 'distance_autre_carbu'] = data_entd['v1_km_annu']

    data_vehicule_entd = data_entd.groupby(by = 'ident_men')['essence',
        'diesel', 'autre_carbu', 'distance_essence', 'distance_diesel', 'distance_autre_carbu'].sum()
    data_vehicule_entd = data_vehicule_entd.reset_index()

    data_entd_diesel = data_entd.query('diesel == 1').copy()
    data_entd_diesel = data_entd_diesel.sort_values(by = ['v1_rang_veh'])
    data_entd_diesel_pr = data_entd_diesel.drop_duplicates(['ident_men'], keep='first')
    
    data_entd_diesel_pr.rename(
        columns = {
            'age_carte_grise' : 'age_carte_grise_diesel',
            'age_vehicule' : 'age_vehicule_diesel',
            'v1_puiss_corr' : 'puissance_diesel',
            'v1_sfvachat' : 'etat_veh_achat_diesel',
            'v1_sfvcosorout' : 'consommation_diesel',
                   },
        inplace = True,
        )

    data_entd_diesel_pr = data_entd_diesel_pr[['ident_men'] + ['puissance_diesel'] +
        ['etat_veh_achat_diesel'] + ['consommation_diesel'] + ['age_vehicule_diesel'] +
        ['age_carte_grise_diesel']
        ]

    data_entd_essence = data_entd.query('essence == 1').copy()
    data_entd_essence = data_entd_essence.sort_values(by = ['v1_rang_veh'])
    data_entd_essence_pr = data_entd_essence.drop_duplicates(['ident_men'], keep='first')

    data_entd_essence_pr.rename(
        columns = {
            'age_carte_grise' : 'age_carte_grise_essence',
            'age_vehicule' : 'age_vehicule_essence',
            'v1_puiss_corr' : 'puissance_essence',
            'v1_sfvachat' : 'etat_veh_achat_essence',
            'v1_sfvcosorout' : 'consommation_essence',
                   },
        inplace = True,
        )

    data_entd_essence_pr = data_entd_essence_pr[['ident_men'] + ['puissance_essence'] +
        ['etat_veh_achat_essence'] + ['consommation_essence'] + ['age_vehicule_essence'] +
        ['age_carte_grise_essence']
        ]


    data_entd_autre_carbu = data_entd.query('autre_carbu == 1').copy()
    data_entd_autre_carbu = data_entd_autre_carbu.sort_values(by = ['v1_rang_veh'])
    data_entd_autre_carbu_pr = data_entd_autre_carbu.drop_duplicates(['ident_men'], keep='first')

    data_entd_autre_carbu_pr.rename(
        columns = {
            'age_carte_grise' : 'age_carte_grise_autre_carbu',
            'age_vehicule' : 'age_vehicule_autre_carbu',
            'v1_puiss_corr' : 'puissance_autre_carbu',
            'v1_sfvachat' : 'etat_veh_achat_autre_carbu',
            'v1_sfvcosorout' : 'consommation_autre_carbu',
                   },
        inplace = True,
        )

    data_entd_autre_carbu_pr = data_entd_autre_carbu_pr[['ident_men'] + ['puissance_autre_carbu'] +
        ['etat_veh_achat_autre_carbu'] + ['consommation_autre_carbu'] + ['age_vehicule_autre_carbu'] +
        ['age_carte_grise_autre_carbu']
        ]

    data_entd_menage.rename(
        columns = {
            'v1_logdist01' : 'distance_commerces',
            'v1_logdist15' : 'distance_transports_communs',
            'v1_jnbveh' : 'veh_tot',
            'v1_jpasvoit_b' : 'vp_domicile_travail',
            'v1_jpasvoit_c' : 'vp_deplacements_pro'
                   },
        inplace = True,
        )

    # Merge les différentes df
    data_entd_full = data_vehicule_entd.merge(data_entd_diesel_pr, on = 'ident_men', how = 'left')
    data_entd_full = data_entd_full.merge(data_entd_essence_pr, on = 'ident_men', how = 'left')
    data_entd_full = data_entd_full.merge(data_entd_autre_carbu_pr, on = 'ident_men', how = 'left')
    data_entd_final = data_entd_menage.merge(data_entd_full, on = 'ident_men', how = 'left')


    return data_entd_final


if __name__ == "__main__":
    data = merge_vehicule_menage()  
    #data_entd = data[0]
    #data_bdf = data[1]
