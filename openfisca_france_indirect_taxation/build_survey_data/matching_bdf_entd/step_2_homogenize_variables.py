# -*- coding: utf-8 -*-

# Dans ce script les variables qui ont des différences de définition sont reconstruites
# sur le modèle de l'enquête BdF (ou entd dans certains cas où la nomenclature entd a plus de sens)
# de manière à avoir des définitions identiques.
# Les noms de variables sont aussi alignés.

import numpy as np

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_1_build_dataframes import \
    load_data_menages_bdf_entd


def homogenize_variables_definition_bdf_entd():
    data = load_data_menages_bdf_entd()    
    data_entd = data[0]
    data_bdf = data[1]
    
    # Aides au logement : séparation propriétaire/locataire dans BdF -> création d'une unique variable
    check = data_bdf.query('aidlog1 != 0')
    assert (check['aidlog2'] == 0).any()
    
    data_bdf['aba'] = data_bdf['aidlog1'] + data_bdf['aidlog2']
    del check, data_bdf['aidlog1'], data_bdf['aidlog2']
    
    # Distribution des ménages parisiens dans les catégories des grands pôles
    data_entd.numcom_au2010.loc[data_entd.numcom_au2010 == 113] = 111
    data_entd.numcom_au2010.loc[data_entd.numcom_au2010 == 114] = 112

    # Rename
    data_entd.rename(
        columns = {
            'nbuc' : 'ocde10',
            'numcom_au2010': 'cataeu',
            'pondv1' : 'pondmen',
            'rlog': 'aba',
            'tau99' : 'tau',
            'tu99' : 'tuu',
            'typmen5' : 'typmen',
            'v1_logpiec' : 'nbphab',
            'v1_logloymens' : 'mloy_d',
            'v1_logocc' : 'stalog'
                   },
    
        inplace = True,
        )
    
    data_entd = data_entd.sort_index(axis = 1)
    data_bdf = data_bdf.sort_index(axis = 1)
    
    return data_entd, data_bdf


def create_new_variables():
    for i in [0,1]:
        data = homogenize_variables_definition_bdf_entd()[i]

        # Création de dummy variables pour la commune de résidence
        data['rural'] = 0
        data['petite_ville'] = 0
        data['moyenne_ville'] = 0
        data['grande_ville'] = 0
        data['paris'] = 0
    
        data.loc[data['tuu'] == 0, 'rural'] = 1
        data.loc[data['tuu'] == 1, 'petite_ville'] = 1
        data.loc[data['tuu'] == 2, 'petite_ville'] = 1
        data.loc[data['tuu'] == 3, 'petite_ville'] = 1
        data.loc[data['tuu'] == 4, 'moyenne_ville'] = 1
        data.loc[data['tuu'] == 5, 'moyenne_ville'] = 1
        data.loc[data['tuu'] == 6, 'moyenne_ville'] = 1
        data.loc[data['tuu'] == 7, 'grande_ville'] = 1
        data.loc[data['tuu'] == 8, 'paris'] = 1
            
        data['aides_logement'] = 0
        data['aides_logement'].loc[data['aba'] == 1] = 1

        if i == 0:
            data_entd = data.copy()
        else:
            data_bdf = data.copy()

    return data_entd, data_bdf


def create_niveau_vie_quantiles():
    for i in [0,1]:
        data = create_new_variables()[i]
        if i == 0:
            data['niveau_vie'] = data['revuc'].copy() * 12
            del data['revuc']
        else :
            data['niveau_vie'] = data['revtot'] / data['ocde10']
        

        data = data.sort_values(by = ['niveau_vie'])
        data['sum_pondmen'] = data['pondmen'].cumsum()
        
        population_totale = data['sum_pondmen'].max()
        data['niveau_vie_decile'] = 0
        for j in range(1,11):
            data.niveau_vie_decile.loc[data.sum_pondmen > population_totale*(float(j)/10 - 0.1)] = j
        
        data['niveau_vie_quintile'] = 0
        for j in range(1,6):
            data.niveau_vie_quintile.loc[data.sum_pondmen > population_totale*(float(j)/5 - 0.2)] = j

        data = data.sort_index()
        del data['sum_pondmen']

        if i == 0:
            data_entd = data.copy()
        else:
            data_bdf = data.copy()

    return data_entd, data_bdf


if __name__ == "__main__":
    data = create_niveau_vie_quantiles()
    data_entd = data[0]
    data_bdf = data[1]
