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
    
    input_entd_menages = survey_entd.get_values(table = 'q_menage')
    
    
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
    
    variables_menages_entd = [
        'ident_men'
        # To be completed
        ]


    # Keep relevant variables :
    menages_entd_keep = input_entd_menages[variables_menages_entd]
    menages_bdf_keep = input_bdf[variables_menages_bdf]
    del input_entd_menages, input_bdf
        
    return menages_entd_keep, menages_bdf_keep


if __name__ == "__main__":
    data = load_data_bdf_entd()    
    data_enl = data[0]
    data_bdf = data[1]
