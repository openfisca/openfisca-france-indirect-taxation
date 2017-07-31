
from __future__ import division



from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_survey_manager.temporary import TemporaryStore


temporary_store = TemporaryStore.create(file_name = 'transport_tmp')


def merge_tables_entd(): # WIP
    
    year_entd = 2008
    
    entd_survey_collection = SurveyCollection.load(
        collection = 'enquete_transport', config_files_directory = config_files_directory
        )
    survey_entd = entd_survey_collection.get_survey('enquete_transport_{}'.format(year_entd))
    
    input_entd_menages = survey_entd.get_values(table = 'q_tcm_menage')
    input_entd_usage_veh = survey_entd.get_values(table = 'qf_voitvul')
    
    
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
        'ident_numveh',
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
    
    # Merge entd tables into one dataframe
    menages_entd_keep['ident_men'] = menages_entd_keep['ident_men'].astype(str)
    usage_veh_entd_keep['ident_men'] = usage_veh_entd_keep['ident_men'].astype(str)

    # check whether ident_numveh has no duplicates :
    usage_bis = usage_veh_entd_keep.drop_duplicates(['ident_numveh'], keep='last')
    assert len(usage_bis) == len(usage_veh_entd_keep)
    del usage_bis
    
    data_entd = menages_entd_keep.merge(usage_veh_entd_keep, on = 'ident_men', how = 'outer')
    
    return data_entd
