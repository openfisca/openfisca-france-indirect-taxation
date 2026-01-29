import numpy as np
import pandas as pd
import os

from openfisca_france_indirect_taxation.examples.utils_example import df_weighted_average_grouped
from openfisca_france_indirect_taxation.projects.TVA.Utils import weighted_quantiles


def compute_bdf_decile(input_bdf):
    '''Calcule des déciles d'individus en niveau de vie à partir d'une base BdF donnée.'''

    input_bdf_copy = input_bdf.copy()

    input_bdf_copy['pondindiv'] = input_bdf_copy['pondmen'] * input_bdf_copy['npers']
    input_bdf_copy['pondindiv'] = input_bdf_copy['pondindiv'].astype(float)
    input_bdf_copy['niveau_de_vie_bdf'] = input_bdf_copy['rev_disponible'] / input_bdf_copy['ocde10']
    input_bdf_copy['niveau_de_vie_bdf'] = input_bdf_copy['niveau_de_vie_bdf'].astype(float)

    # On calcule des déciles d'individus par niveau de vie
    input_bdf_copy['decile_indiv_niveau_vie'] = weighted_quantiles(input_bdf_copy['niveau_de_vie_bdf'], labels = np.arange(1, 11), weights = input_bdf_copy['pondindiv'], return_quantiles= False)
    input_bdf_copy['decile_indiv_niveau_vie'] = input_bdf_copy['decile_indiv_niveau_vie'].astype(int)

    input_bdf_by_decile = df_weighted_average_grouped(input_bdf_copy, groupe = 'decile_indiv_niveau_vie', varlist = ['rev_disponible', 'niveau_de_vie_bdf', 'ocde10'], weights= 'pondindiv')

    return input_bdf_copy, input_bdf_by_decile


def compute_erfs_decile(target_year, path):
    '''Calcule des déciles d'individus en niveau de vie à partir de l'ERFS pour une année cible donnée.'''

    erfs_menage = pd.read_csv(os.path.join(path, "fpr_menage_{}.csv".format(target_year)), sep = ";")

    erfs_menage.columns = erfs_menage.columns.str.lower()
    erfs_menage.rename({'wprm': 'pondmen'}, axis = 1, inplace= True)

    erfs_menage['niveau_de_vie'] = erfs_menage['revdispm'] / erfs_menage['nb_uci']
    erfs_menage['decile_indiv_niveau_vie'] = weighted_quantiles(erfs_menage['niveau_de_vie'], labels = np.arange(1, 11), weights = erfs_menage['wpri'], return_quantiles=False)
    erfs_menage_by_decile = df_weighted_average_grouped(erfs_menage, groupe = 'decile_indiv_niveau_vie', varlist = ['revdispm', 'niveau_de_vie', 'nb_uci'], weights= 'wpri')

    return erfs_menage_by_decile


def get_coef_calage_niveau_vie(input_bdf, target_decile):
    '''Calcule le coefficient de calage sur les niveaux de vie entre une base BdF d'entrée et une base cible qui doit avoir les caractéristiques suivantes:
    avoir une colonne 'niveau_de_vie' et être indexée par 'decile_indiv_niveau_vie'. '''

    input_bdf_copy, bdf_decile = compute_bdf_decile(input_bdf)

    df_calage = bdf_decile.merge(target_decile, how = 'left', left_index = True, right_index= True)
    df_calage['coef_calage'] = df_calage['niveau_de_vie'] / df_calage['niveau_de_vie_bdf']

    return input_bdf_copy, df_calage.reset_index()


def calage_bdf_niveau_vie(input_bdf, target_decile):
    ''' Cale les niveaux de vie d'une base BdF d'entrée sur les déciles d'une base cible. '''
    input_bdf_copy = input_bdf.copy()

    input_bdf_copy, df_calage = get_coef_calage_niveau_vie(input_bdf_copy, target_decile)
    df_calage['test'] = df_calage['coef_calage'].apply(lambda x: abs(x - 1))

    while df_calage['test'].max(axis = 0) > 1E-5:
        df_calage = df_calage[['decile_indiv_niveau_vie', 'coef_calage']]
        if 'coef_calage' in input_bdf_copy.columns:
            input_bdf_copy.drop(labels = ['coef_calage'], axis = 1, inplace = True)
        input_bdf_copy = input_bdf_copy.merge(df_calage, how = 'left', on = 'decile_indiv_niveau_vie')
        input_bdf_copy['rev_disponible'] = input_bdf_copy['coef_calage'] * input_bdf_copy['rev_disponible']
        input_bdf_copy, df_calage = get_coef_calage_niveau_vie(input_bdf_copy, target_decile)
        df_calage['test'] = df_calage['coef_calage'].apply(lambda x: abs(x - 1))

    return input_bdf_copy, df_calage
