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


def load_data_menages_bdf_entd():
    # Load ENTD data :
    
    year_entd = 2008
    
    entd_survey_collection = SurveyCollection.load(
        collection = 'enquete_transport', config_files_directory = config_files_directory
        )
    survey_entd = entd_survey_collection.get_survey('enquete_transport_{}'.format(year_entd))
    
    input_entd_tcm_menage = survey_entd.get_values(table = 'q_tcm_menage')
    input_entd_menage = survey_entd.get_values(table = 'q_menage')
    
    
    # Load BdF data :
    
    year_bdf = 2011
    
    openfisca_survey_collection = SurveyCollection.load(collection = 'openfisca_indirect_taxation')
    openfisca_survey = openfisca_survey_collection.get_survey('openfisca_indirect_taxation_data_{}'.format(year_bdf))
    input_bdf = openfisca_survey.get_values(table = 'input')
    input_bdf.reset_index(inplace = True)
    

    # Create variable for total spending
    liste_variables = input_bdf.columns.tolist()
    postes_agreges = ['poste_{}'.format(index) for index in
        ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12"]
        ]
    input_bdf['depenses_tot'] = 0
    for element in liste_variables:
        for poste in postes_agreges:
            if element[:8] == poste:
                input_bdf['depenses_tot'] += input_bdf[element]


    # Set variables :
    variables_tcm_menage_entd = [
        'ident_men',
        'agepr',
        'cs42pr',
        'dip14pr',
        'nactifs',
        'nbuc', #ocde10
        'nenfants',
        'nivie10', # déciles de revenu par uc
        'npers',
        'numcom_au2010', #cataeu
        'pondv1', #poids ménage
        'revuc', # revenus simulés par UC
        'rlog', # allocations logement
        'situapr',
        'tu99',
        'tau99',
        #'typlog',
        'typmen5', #type ménage
        # To be completed
        ]

    variables_menage_entd = [
        'ident_men',
        'v1_logpiec', # nombre de pièces dans logement
        'v1_logocc', # statut d'occupation du logement
        'v1_logloymens', # loyer mensuel calculé
        ]

    variables_menage_bdf = [
        'ident_men',
        'aidlog1',
        'aidlog2',
        'agepr', # âge de la pr
        'cataeu',
        'cs42pr',
        'dip14pr',
        'mloy_d', # loyer mensuel
        'nactifs',
        'nbphab',
        'nenfants',
        'npers',
        'ocde10', # nb unités de conso
        'pondmen',
        'poste_07_2_2_1_1',
        'revtot', # revenu total
        'situapr',
        'stalog',
        'tau',
        'tuu',
        #'typlog',
        'typmen',
        # To be completed
        ]

    # Keep relevant variables :
    tcm_menage_entd_keep = input_entd_tcm_menage[variables_tcm_menage_entd]
    menage_entd_keep = input_entd_menage[variables_menage_entd]
    menage_bdf_keep = input_bdf[variables_menage_bdf]

    # Merge entd tables into one dataframe
    data_entd = tcm_menage_entd_keep.merge(menage_entd_keep, on = 'ident_men')   

    del input_entd_tcm_menage, input_entd_menage, input_bdf

    return data_entd, menage_bdf_keep


if __name__ == "__main__":
    data = load_data_menages_bdf_entd()    
    data_entd = data[0]
    data_bdf = data[1]
