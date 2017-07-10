# -*- coding: utf-8 -*-

# Dans ce script les variables qui ont des différences de définition sont reconstruites
# sur le modèle de l'enquête BdF (ou ENL dans certains cas où la nomenclature ENL a plus de sens)
# de manière à avoir des définitions identiques.
# Les noms de variables sont aussi alignés.

import numpy as np
import pandas as pd

from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_1_build_dataframes import \
    load_data_bdf_enl


def homogenize_variables_definition_bdf_enl():
    data = load_data_bdf_enl()    
    data_enl = data[0]
    data_bdf = data[1]
    
    # Vérification que les données ENL ne contiennent pas les DOM
    assert (data_enl['dom'] == 2).any()
    del data_enl['dom']
    
    
    # Aides au logement : séparation propriétaire/locataire dans BdF -> création d'une unique variable
    check = data_bdf.query('aidlog1 != 0')
    assert (check['aidlog2'] == 0).any()
    
    data_bdf['aba'] = data_bdf['aidlog1'] + data_bdf['aidlog2']
    del check

    
    # Montant des aides au logement : séparation propriétaire/locataire dans BdF -> création d'une unique variable
    for i in [1, 2]:
        data_bdf['mall{}'.format(i)] = data_bdf['mall{}'.format(i)].fillna(0)
        check = data_bdf.query('aidlog{} != 1'.format(i))
        assert (check['mall{}'.format(i)] == 0).any()
    
    data_bdf['amr'] = data_bdf['mall1'] + data_bdf['mall2']
    del data_bdf['aidlog1'], data_bdf['aidlog2'], data_bdf['mall1'], data_bdf['mall2'], check
    
    
    # Les définitions du ménage dans BdF et ENL sont différentes : 
    # on vérifie que la variable HTL est définie de la même manière
    for i in [4, 6]:
        check = data_bdf.query('htl == {}'.format(i))
        assert len(check) == 0
        del check
    
    
    # Changement nomenclature variable année de construction du batiment :
    data_enl['ancons'] = 0
    data_enl.ancons.loc[data_enl.iaat < 4] = 1
    data_enl.ancons.loc[data_enl.iaat == 4] = 2
    data_enl.ancons.loc[data_enl.iaat == 5] = 3
    data_enl.ancons.loc[data_enl.iaat == 6] = 4
    data_enl.ancons.loc[data_enl.iaat == 7] = 5
    data_enl.ancons.loc[data_enl.iaat == 8] = 6
    data_enl.ancons.loc[data_enl.iaat == 9] = 7
    # Pour après 1998 on affecte aléatoirement 8 ou 9 (99-03 ou 03-et après)
    data_enl.ancons.loc[data_enl.iaat == 10] = np.random.choice(np.array([8, 9]))
    
    
    # dip14pr - dans ENL les sans diplômes sont notés 0 au lieu de 71
    data_enl.ndip14.loc[data_enl.ndip14 == 0] = 71
    
    
    # Situapr et Situacj vs Msitua
    data_enl['situapr'] = data_enl['msitua'].copy()
    data_enl.situapr.loc[data_enl.msitua == 8] = 7
    data_enl['situacj'] = data_enl['msituac'].copy()
    data_enl.situacj.loc[data_enl.msituac == 8] = 7
    
    del data_enl['msitua'], data_enl['msituac']
    
    # mfac_eg1_d
    #print data_bdf['poste_coicop_4511'].mean()
    #print data_enl['coml13'].mean()
    
    # OCDE10 vs MUC1
    data_enl['muc1'] = data_enl['muc1'].copy() / 10
    
    # Nbh1
    data_bdf['nbh1'] = data_bdf['nbh1'].fillna(0)
    
    # zeat : dans BdF certains ménages ont 6 et aucun 9, alors que 6 n'existe pas
    data_bdf.zeat.loc[data_bdf.zeat == 6] = 9

    # Rename
    data_enl.rename(
        columns = {
            'cataeu2010': 'cataeu',
            'cceml': 'mfac_eau1_d',
            'coml': 'depenses_energies',
            'coml11': 'poste_coicop_451',
            'coml12': 'poste_coicop_452',
            'coml2': 'poste_coicop_453',
            'enfhod': 'nbh1',
            'lchauf': 'mchof_d',
            'hnph1': 'nbphab',
            'hsh1': 'surfhab_d',
            'lmlm': 'mloy_d',
            'mag': 'agepr',
            'mcs': 'cs42pr',
            'mcsc': 'cs42cj',
            'mne1': 'nenfants',
            'mpa': 'nactifs',
            'mrtota2': 'revtot',
            'muc1': 'ocde10',
            'ndip14': 'dip14pr',
            'qex': 'pondmen',
            'tau2010': 'tau',
            'tu2010': 'tuu',
                   },
    
        inplace = True,
        )
    
    data_enl = data_enl.sort_index(axis = 1)
    data_bdf = data_bdf.sort_index(axis = 1)
    
    return data_enl, data_bdf


def create_new_variables():
    for i in [0,1]:
        data = homogenize_variables_definition_bdf_enl()[i]

        # Dummy variable pour la consommation de fioul
        data['fioul'] = 0
        data.loc[data['poste_coicop_453'] > 0, 'fioul'] = 1

        data['gaz'] = 0
        data.loc[data['poste_coicop_452'] > 0, 'gaz'] = 1

        data['electricite'] = 0
        data.loc[data['poste_coicop_451'] > 0, 'electricite'] = 1

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
    
        # Dummy variables pour l'ancienneté du batîment (1er norme importante sur l'isolation en 74)
        data['bat_av_49'] = 0
        data['bat_49_74'] = 0
        data['bat_ap_74'] = 0
    
        data.loc[data['ancons'] == 1, 'bat_av_49'] = 1
        data.loc[data['ancons'] < 5, 'bat_49_74'] = 1
        data.loc[data['ancons'] == 1, 'bat_49_74'] = 0
        data.loc[data['ancons'] > 4, 'bat_ap_74'] = 1
    
        # Dummy variables pour le type de logement
        data['log_indiv'] = 0
        data['log_colec'] = 1
    
        for j in [1,5,7]:    
            data.loc[data['htl'] == i, 'log_indiv'] = 1
            data.loc[data['htl'] == i, 'log_colec'] = 0
        del j
    
        # Creation de dummy variables pour la zone climatique
        data['ouest_sud'] = 0
        data['est_nord'] = 1
    
        for j in [5,7,9]:    
            data.loc[data['zeat'] == i, 'ouest_sud'] = 1
            data.loc[data['zeat'] == i, 'est_nord'] = 0
        del j
    
        # Création d'une variable pour la part des dépenses totales en énergies
        energie_logement = ['poste_coicop_451', 'poste_coicop_4511', 'poste_coicop_452',
        'poste_coicop_4522', 'poste_coicop_453', 'poste_coicop_454', 'poste_coicop_455',
        'poste_coicop_4552']
        
        if i == 1:
            data['depenses_energies'] = 0
            for energie in energie_logement:
                data['depenses_energies'] += data[energie]
            data['part_energies_depenses_tot'] = (
                data['depenses_energies'] / data['depenses_tot']
                )

        data = data.query('revtot > 0')
        data['part_energies_revtot'] = (
            data['depenses_energies'] / data['revtot']
            )

        # Suppression des outliers
        data = data.query('part_energies_revtot < 0.5')

        if i == 0:
            data_enl = data.copy()
        else:
            data_bdf = data.copy()

    return data_enl, data_bdf


def create_niveau_vie_quantiles():
    for i in [0,1]:
        data = create_new_variables()[i]
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
            data_enl = data.copy()
        else:
            data_bdf = data.copy()

    return data_enl, data_bdf


if __name__ == "__main__":
    data = create_niveau_vie_quantiles()
    data_enl = data[0]
    data_bdf = data[1]
