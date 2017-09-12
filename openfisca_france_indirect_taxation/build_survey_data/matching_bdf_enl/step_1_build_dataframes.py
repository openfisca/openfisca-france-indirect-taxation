# -*- coding: utf-8 -*-

# Dans ce script on importe les données des enquêtes BdF 2011 et ENL 2013.
# Pour chacune des deux enquêtes on importe les variables qui seront
# susceptibles d'êtres utilisées dans l'appariement des bases de données.

from __future__ import division



from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_survey_manager.temporary import TemporaryStore


temporary_store = TemporaryStore.create(file_name = 'logement_tmp')


def load_data_bdf_enl():
    # Load ENL data :
    
    year_enl = 2013
    
    enl_survey_collection = SurveyCollection.load(
        collection = 'enquete_logement', config_files_directory = config_files_directory
        )
    survey_enl = enl_survey_collection.get_survey('enquete_logement_{}'.format(year_enl))
    
    input_enl = survey_enl.get_values(table = 'menlogfm_diff')
    input_enl_indiv = survey_enl.get_values(table = 'indivfm_diff')
    
    
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
    
    variables_menages_bdf = [
        'agepr', # âge de la pr
        'aidlog1', # aides au logement
        'aidlog2',
        'aise', # à l'aise avec le budget
        'ancons',
        'cataeu', # type de commune
        'chaufp',
        'cs42pr', # catégorie socio-pro
        'cs42cj',
        'decuc',
        'depenses_tot',
        'dip14cj', # diplômes
        'dip14pr',
        #'h_trans1',
        'htl', # type de logement
        'ident_men',
        'mall1',
        'mall2',
        'mchof',
        'mchof_d',
        'mfac_eau1_d',
        'mfac_eg1_d',
        'mloy_d',
        #'mode_trans1', depindiv
        'nbh1',
        'nbphab',
        'nactifs',
        'nenfants',
        'ocde10', # nb unités de conso
        'pondmen',
        'poste_04_5_1_1_1_a',
        'poste_04_5_1_1_1_b',
        'poste_04_5_2_1_1',
        'poste_04_5_2_2_1',
        'poste_04_5_3_1_1',
        'poste_04_5_4_1_1',
        'poste_04_5_5_1_1',
        #'poste_07_2_2_1_1',
        'revtot', # revenu total
        'situapr', # situation pro
        'situacj',
        'surfhab_d', # surface habitable
        'tau',
        'tuu',
        'typmen',
        'zeat', # zone climatique
        ]
    
    variables_menages_enl = [
        'aba',
        'amr',
        'cataeu2010',
        'cceml',
        'coml',
        'coml11',
        'coml12',
        'coml13',
        'coml2',
        'coml3',
        'dom',
        'enfhod',
        'gchauf_1', #raisons du froid dans le logement
        'gchauf_2',
        'gchauf_3',
        'gchauf_4',
        'gchauf_5',
        'gchauf_6',
        'gchauf_7',
        'gchauf_n', # nombre de raisons du froid
        'gchaufs_1', #solutions contre le froid
        'gchaufs_2',
        'gchaufs_3',
        'gchaufs_4',
        'gchaufs_5',
        'gmoy1', #moyen utilisé trajet travail
        'gmur', #isolation thermique murs
        'gtoit2', #isolation thermique toit
        'gtt1', #durée trajet domicile-travail
        'gvit1', #majorité double vitrage
        'gvit1b', #fenêtres laissent passer l'air
        'hnph1',
        'hsh1',
        'htl',
        'iaat',
        'idlog',
        'lchauf',
        'lmlm',
        'mag',
        'mcs',
        'mcsc',
        'mne1',
        'mpa',
        'mrtota2',
        'msitua',
        'msituac',
        'muc1',
        'qex',
        'tau2010',
        'tu2010',
        'zeat',
        ]
    
    variables_indiv_enl = [
        'idlog',
        'igreflog', # = 1 si l'individu est la personne de référence
        'ndip14',
        ]
    
    # Keep relevant variables :
    indiv_enl_keep = input_enl_indiv[variables_indiv_enl]
    menage_enl_keep = input_enl[variables_menages_enl]
    conso_bdf_keep = input_bdf[variables_menages_bdf]
    del input_enl_indiv, input_enl, input_bdf
    
    indiv_enl_keep = indiv_enl_keep.query('igreflog == 1')
    del indiv_enl_keep['igreflog']
    menage_enl_keep = menage_enl_keep.merge(indiv_enl_keep, on = 'idlog')
    
    return menage_enl_keep, conso_bdf_keep


if __name__ == "__main__":
    data = load_data_bdf_enl()    
    data_enl = data[0]
    data_bdf = data[1]