# -*- coding: utf-8 -*-

# Dans ce script on importe les données des enquêtes BdF 2011 et ENL 2013.
# Pour chacune des deux enquêtes on importe les variables qui seront
# susceptibles d'êtres utilisées dans l'appariement des bases de données.

from __future__ import division

import pandas

from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_survey_manager.temporary import TemporaryStore


temporary_store = TemporaryStore.create(file_name = 'revenus_fiscaux_sociaux_tmp')


def load_data_bdf_erfs():
    # Load ERFS data
    year_erfs = 2013
    
    erfs_survey_collection = SurveyCollection.load(
        collection = 'enquete_revenus_fiscaux_sociaux', config_files_directory = config_files_directory
        )
    survey_erfs = erfs_survey_collection.get_survey('enquete_revenus_fiscaux_sociaux_{}'.format(year_erfs))
    
    revenus_erfs = survey_erfs.get_values(table = 'fpr_menage_2013')
    menages_erfs = survey_erfs.get_values(table = 'fpr_mrf13e13t4')
    
    menages_erfs = pandas.merge(revenus_erfs, menages_erfs, on = 'ident')
    
    
    # Load BdF data
    year_bdf = 2011
    
    openfisca_survey_collection = SurveyCollection.load(collection = 'openfisca_indirect_taxation')
    openfisca_survey = openfisca_survey_collection.get_survey('openfisca_indirect_taxation_data_{}'.format(year_bdf))
    input_bdf = openfisca_survey.get_values(table = 'input')
    input_bdf.reset_index(inplace = True)
    
    # Add some variables for revenue from BdF using directly the surveys (not the input)
    bdf_survey_collection = SurveyCollection.load(
        collection = 'budget_des_familles', config_files_directory = config_files_directory
        )
    survey_bdf = bdf_survey_collection.get_survey('budget_des_familles_{}'.format(year_bdf))
    menages_bdf = survey_bdf.get_values(table = 'menage')
    menages_bdf['ident_men'] = menages_bdf['ident_men'].astype(str)
    
    columns_menages = menages_bdf.columns.difference(input_bdf.columns).tolist()
    columns_menages.append('ident_men')
    menages_bdf = menages_bdf[columns_menages]
    
    menages_bdf = pandas.merge(menages_bdf, input_bdf, on = 'ident_men')    
    
    # Set variables to keep
    variables_erfs = [
        'ident',
        'wprm', # pondération ménage
        'ageprm', # âge de la PR au moment de l'enquête
        'catau2010', # catégorie zone urbaine
        'cstotprm', # categ socio pro
        'm_rsa_actm', # RSA activité
        'metrodom', # métropole ou DOM
        'nb_uci', # nombre d'uc
        'nbactif', # nombre d'actifs
        'nbactop', # nombre d'actifs occupés
        'nbind', # nombre personnes dans le logement
        'nivviem', # niveau vie ménage (rev_disponible / nb_UCI)
        'prest_precarite_hand', # prestation précarité handicap
        'prest_precarite_rsa', # prestation précarité RSA hors RSA activité
        'prest_precarite_vieil', # prestation précarité vieillesse
        'retraites', # retraites et pensions hors CSG-CRDS hors pensions alimentaires
        'rev_etranger', # revenus de l'étranger du ménage
        'rev_valeurs_mobilieres_bruts', # revenus de valeurs mobilières
        'revdecm', # Variable à imputer : revenu déclaré par le ménage
        'revdispm', # revenu disponible
        'salaires', # salaires et traitements hors CSG-CRDS
        'sexeprm', # sexe personne de référence
        'so', # statut d'occupation du logement
        'tau2010', # taille aire urbaine
        'th', # taxe habitation payée en 2013
        'tuu2010', # taille unité urbaine
        'typmen7', # type de ménage
        ]
    
    variables_bdf = [
        'ident_men',
        'pondmen', # pondération ménage
        'agepr', # âge de la PR au moment de l'enquête
        'cataeu', # catégorie zone urbaine
        'chomage', # chômage et pré-retraite
        'cs42pr', # categ socio pro
        #'mhab_d', # montant définitif de la taxe d'habitation
        'nactifs', # nombre d'actifs
        'nactoccup', # nombre d'actifs occupés
        'npers', # nombre personnes dans le logement
        'ocde10', # nombre d'uc
        'prest_precarite_hand', # prestation précarité handicap
        'prest_precarite_rsa', # prestation précarité RSA hors RSA activité
        'prest_precarite_vieil', # prestation précarité vieillesse
        'retraites', # retraites
        'rev502', # intérêt valeurs mobilières
        'rev_etranger', # revenus de l'étranger du ménage
        'rev_disponible', # revenu disponible
        'rsa_act', # RSA activité
        'salaires', # salaires et autres rémunérations
        'stalog', # statut d'occupation du logement
        'tau', # taille aire urbaine
        'tuu', # taille unité urbaine
        'typmen', # type de ménage
        ]

    menages_erfs = menages_erfs[variables_erfs]
    menages_bdf = menages_bdf[variables_bdf] # mhab_d
        
    return menages_erfs, menages_bdf


if __name__ == "__main__":
    data = load_data_bdf_erfs()    
    data_erfs = data[0]
    data_bdf = data[1]
      