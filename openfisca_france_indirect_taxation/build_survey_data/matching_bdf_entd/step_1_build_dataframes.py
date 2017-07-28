# -*- coding: utf-8 -*-

# Dans ce script on importe les données des enquêtes BdF 2011 et ENTD 2008.
# Pour chacune des deux enquêtes on importe les variables qui seront
# susceptibles d'êtres utilisées dans l'appariement des bases de données.

from __future__ import division



from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_survey_manager.temporary import TemporaryStore


temporary_store = TemporaryStore.create(file_name = 'transport_tmp')


def load_data_bdf_entd():
    # Load ENL data :
    
    year_entd = 2008
    
    entd_survey_collection = SurveyCollection.load(
        collection = 'enquete_transport', config_files_directory = config_files_directory
        )
    survey_entd = entd_survey_collection.get_survey('enquete_transport_{}'.format(year_entd))
    
    input_entd_menages = survey_entd.get_values(table = 'q_tcm_menage')
    input_entd_usage_veh = survey_entd.get_values(table = 'qf_voitvul')
    
    
    # Load BdF data :
    
    year_bdf = 2011
    
    openfisca_survey_collection = SurveyCollection.load(collection = 'openfisca_indirect_taxation')
    openfisca_survey = openfisca_survey_collection.get_survey('openfisca_indirect_taxation_data_{}'.format(year_bdf))
    input_bdf = openfisca_survey.get_values(table = 'input')
    input_bdf.reset_index(inplace = True)
    

    # Create variable for total spending
    produits = [column for column in input_bdf.columns if column[:13] == 'poste_coicop_']
    del column

    input_bdf['depenses_tot'] = 0
    for produit in produits:
        if produit[13:15] != '99' and produit[13:15] != '13':
            input_bdf['depenses_tot'] += input_bdf[produit]


    # Set variables :
    
    variables_menages_bdf = [
        'agepr', # âge de la pr
        'ident_men',
        'ocde10', # nb unités de conso
        'pondmen',
        'poste_coicop_722',
        'revtot', # revenu total
        'tuu',
        # To be completed
        ]
    
    variables_tcm_menages_entd = [
        'ident_men',
        'rg', # region de residence
        'tu99',
        'tau99',
        'zus', # logement en zus
        'typlog',
        'axe2', #activite/chômage
        'agpr',
        'cs42pr',
        'dip14pr',
        'nactifs',
        'nenfants',
        'npers',
        'revuc', # revenus simulés par UC
        'nbuc', #ocde10
        'nivie10', # déciles de revenu par uc
        'rlog', # allocations logement
        'situapr',
        'typmen5', #type ménage
        'pondv1', #poids ménage
        'numcom_au2010', #cataeu
        # To be completed
        ]

    variables_menages_entd = [
        'ident_men',
        'pondv1',
        'v1_logdist01', #distance commerces et supermarchés
        'v1_logdist15', # distance arrêts transports en commun
        'v1_logpiec', # nombre de pièces dans logement
        'v1_logocc', # statut d'occupation du logement
        'v1_logloymens', # loyer mensuel calculé
        'v1_jnbveh', # nb de voitures particulières
        'v1_jnbmoto',
        'v1_jnbcyclo',
        'v1_jpasvoitb', # questions sur l'utilité du VP
        ]

    variables_qr_voitul_entd = [
        'ident_men',
        'mveh', # numéro du véhicule
        'v1_ken', # type de carburant majoritairement utilisé
        'v1_puiss_corr', # puissance fiscale corrigée
        'v1_rang_veh', # place du veh dans le ménage
        ]

    variables_qf_voitvul_entd = [
        'ident_men',
        'poids_veh1', # poids du véhicule
        'mveh', # numéro du véhicule
        'v1_ken', # type de carburant majoritairement utilisé
        'v1_puiss_corr', # puissance fiscale corrigée
        'v1_age_veh',
        'v1_rang_veh', # place du veh dans le ménage
        'v1_sfvcosorout', # consommation du veh
        'v1_sfvkm', # nombre de km au compteur aujourd'hui
        'v1_km_annu', # nombre de km sur les 12 derniers mois redressés
        ]

    variables_q_individu_entd = [
        'ident_men',
        'noi', # numéro de l'individu dans le logement
        'datenq',
        'v1_gpermis', # X possède le permis B
        ]

    variables_q_ind_lieu_teg_entd = [
        'ident_men',
        'noi',
        'v1_btravdist', # distance parcourue jusqu'au lieu de TEG
        'v1_btravnbarj', # nb de déplacement par jour
        ]
        
    variables_k_deploc_entd = [
        'ident_men',
        'datenq',
        'pondki', #poids individu kish
        'v2_mtp', # mode principal du déplacement,
        'v2_midsttot', # distance du déplacement
        ]

    variables_c_dep_carnet_entd = [
        'ident_men',
        'poids_car1', # poids carnet
        'danteq', # date de la visite 1
        'distance', # distance parcourue
        ]

    # Keep relevant variables :
    menages_entd_keep = input_entd_menages[variables_tcm_menages_entd]
    usage_veh_entd_keep = input_entd_usage_veh[variables_qf_voitvul_entd]
    menages_bdf_keep = input_bdf[variables_menages_bdf]
    
    indiv_enl_keep = indiv_enl_keep.query('igreflog == 1')
    del indiv_enl_keep['igreflog']
    menages_entd_keep_bis = menages_entd_keep.merge(usage_veh_entd_keep, on = 'ident_men')


    del input_entd_menages, input_bdf
        
    return menages_entd_keep, menages_bdf_keep


if __name__ == "__main__":
    data = load_data_bdf_entd()    
    data_enl = data[0]
    data_bdf = data[1]
