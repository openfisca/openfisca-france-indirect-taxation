# -*- coding: utf-8 -*-

"""
Computing the Hellinger distance between two discrete
probability distributions
"""

import numpy as np

from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_2_homogenize_variables import \
    create_new_variables

data = create_new_variables()
data_enl = data[0]
data_bdf = data[1]


_SQRT2 = np.sqrt(2)     # sqrt(2) with default precision np.float64


def hellinger(p, q):
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / _SQRT2
    

def hellinger_part_energies_revtot(data_bdf, data_enl):
    data_bdf['part_energies_revtot'] = data_bdf['part_energies_revtot'].astype(float)
    data_bdf = data_bdf.query('part_energies_revtot < 1').copy()
    data_bdf['part_energies_revtot_groupe'] = data_bdf['part_energies_revtot'].round(decimals = 2)
    
    data_enl['part_energies_revtot'] = data_enl['part_energies_revtot'].astype(float)
    data_enl = data_enl.query('part_energies_revtot < 1').copy()
    data_enl['part_energies_revtot_groupe'] = data_enl['part_energies_revtot'].round(decimals = 2)
    
    
    total_pop_bdf = len(data_bdf)
    distribution_bdf = dict()
    for i in range(0,101):
        j = float(i)/100
        #number_occurences = len(data_bdf.query('part_energies_revtot_groupe == {}'.format(j)))
        #distribution_bdf['{}'.format(j)] = float(number_occurences) / total_pop_bdf
        distribution_bdf['{}'.format(j)] = (data_bdf.query('part_energies_revtot_groupe == {}'.format(j))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())
    
    total_pop_enl = len(data_enl)
    distribution_enl = dict()
    for i in range(0,101):
        j = float(i)/100
        #number_occurences = len(data_enl.query('part_energies_revtot_groupe == {}'.format(j)))
        #distribution_enl['{}'.format(j)] = float(number_occurences) / total_pop_enl
        distribution_enl['{}'.format(j)] = (data_enl.query('part_energies_revtot_groupe == {}'.format(j))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_part_energies_revtot = hellinger_part_energies_revtot(data_bdf, data_enl)


def hellinger_revtot(data_bdf, data_enl):
    data_bdf['revtot'] = data_bdf['revtot'].astype(float)
    data_bdf['revtot_racine'] = (data_bdf['revtot']) ** (0.5)
    revtot_racine_max = data_bdf['revtot_racine'].max()
    data_bdf['revtot_groupe'] = (data_bdf['revtot_racine'] / revtot_racine_max).round(decimals = 2)
    
    data_enl['revtot'] = data_enl['revtot'].astype(float)
    data_enl['revtot_racine'] = (data_enl['revtot']) ** (0.5)
    revtot_racine_max = data_enl['revtot_racine'].max()
    data_enl['revtot_groupe'] = (data_enl['revtot_racine'] / revtot_racine_max).round(decimals = 2)


    total_pop_bdf = len(data_bdf)
    distribution_bdf = dict()
    for i in range(0,101):
        j = float(i)/100
        number_occurences = len(data_bdf.query('revtot_groupe == {}'.format(j)))
        distribution_bdf['{}'.format(j)] = float(number_occurences) / total_pop_bdf
    
    total_pop_enl = len(data_enl)
    distribution_enl = dict()
    for i in range(0,101):
        j = float(i)/100
        number_occurences = len(data_enl.query('revtot_groupe == {}'.format(j)))
        distribution_enl['{}'.format(j)] = float(number_occurences) / total_pop_enl

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_revtot = hellinger_revtot(data_bdf, data_enl)


def hellinger_depenses_energies(data_bdf, data_enl):
    data_bdf['depenses_energies'] = data_bdf['depenses_energies'].astype(float)
    data_bdf['depenses_energies_racine'] = (data_bdf['depenses_energies']) ** (0.5)
    depenses_energies_racine_max = data_bdf['depenses_energies_racine'].max()
    data_bdf['depenses_energies_groupe'] = (data_bdf['depenses_energies_racine'] / depenses_energies_racine_max).round(decimals = 2)
    
    data_enl['depenses_energies'] = data_enl['depenses_energies'].astype(float)
    data_enl['depenses_energies_racine'] = (data_enl['depenses_energies']) ** (0.5)
    depenses_energies_racine_max = data_enl['depenses_energies_racine'].max()
    data_enl['depenses_energies_groupe'] = (data_enl['depenses_energies_racine'] / depenses_energies_racine_max).round(decimals = 2)


    total_pop_bdf = len(data_bdf)
    distribution_bdf = dict()
    for i in range(0,101):
        j = float(i)/100
        number_occurences = len(data_bdf.query('depenses_energies_groupe == {}'.format(j)))
        distribution_bdf['{}'.format(j)] = float(number_occurences) / total_pop_bdf
    
    total_pop_enl = len(data_enl)
    distribution_enl = dict()
    for i in range(0,101):
        j = float(i)/100
        number_occurences = len(data_enl.query('depenses_energies_groupe == {}'.format(j)))
        distribution_enl['{}'.format(j)] = float(number_occurences) / total_pop_enl

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_depenses_energies = hellinger_depenses_energies(data_bdf, data_enl)


def hellinger_surfhab_d(data_bdf, data_enl):
    data_bdf['surfhab_d'] = data_bdf['surfhab_d'].astype(float)
    surfhab_d_max = data_bdf['surfhab_d'].max()
    data_bdf['surfhab_d_groupe'] = (data_bdf['surfhab_d'] / surfhab_d_max).round(decimals = 2)
    
    data_enl['surfhab_d'] = data_enl['surfhab_d'].astype(float)
    surfhab_d_max = data_enl['surfhab_d'].max()
    data_enl['surfhab_d_groupe'] = (data_enl['surfhab_d'] / surfhab_d_max).round(decimals = 2)


    total_pop_bdf = len(data_bdf)
    distribution_bdf = dict()
    for i in range(0,101):
        j = float(i)/100
        number_occurences = len(data_bdf.query('surfhab_d_groupe == {}'.format(j)))
        distribution_bdf['{}'.format(j)] = float(number_occurences) / total_pop_bdf
    
    total_pop_enl = len(data_enl)
    distribution_enl = dict()
    for i in range(0,101):
        j = float(i)/100
        number_occurences = len(data_enl.query('surfhab_d_groupe == {}'.format(j)))
        distribution_enl['{}'.format(j)] = float(number_occurences) / total_pop_enl

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_surfhab_d = hellinger_surfhab_d(data_bdf, data_enl)


def hellinger_postes_energies(data_bdf, data_enl):
    distribution_bdf_1 = dict()
    distribution_bdf_2 = dict()
    distribution_bdf_3 = dict()
    distribution_enl_1 = dict()
    distribution_enl_2 = dict()
    distribution_enl_3 = dict()
    for en in [1,2,3]:
        data_bdf['poste_coicop_45{}'.format(en)] = data_bdf['poste_coicop_45{}'.format(en)].astype(float)
        poste_max = data_bdf['poste_coicop_45{}'.format(en)].max()
        data_bdf['poste_coicop_45{}_groupe'.format(en)] = (data_bdf['poste_coicop_45{}'.format(en)] / poste_max).round(decimals = 2)
        
        data_enl['poste_coicop_45{}'.format(en)] = data_enl['poste_coicop_45{}'.format(en)].astype(float)
        poste_max = data_enl['poste_coicop_45{}'.format(en)].max()
        data_enl['poste_coicop_45{}_groupe'.format(en)] = (data_enl['poste_coicop_45{}'.format(en)] / poste_max).round(decimals = 2)    
    
        total_pop_bdf = len(data_bdf)
        for i in range(0,101):
            j = float(i)/100
            number_occurences = len(data_bdf.query('poste_coicop_45{}_groupe == {}'.format(en, j)))
            if en == 1:
                distribution_bdf_1['{}'.format(j)] = float(number_occurences) / total_pop_bdf
            if en == 2:
                distribution_bdf_2['{}'.format(j)] = float(number_occurences) / total_pop_bdf
            else:
                distribution_bdf_3['{}'.format(j)] = float(number_occurences) / total_pop_bdf
        
        total_pop_enl = len(data_enl)
        for i in range(0,101):
            j = float(i)/100
            number_occurences = len(data_enl.query('poste_coicop_45{}_groupe == {}'.format(en, j)))
            if en == 1:
                distribution_enl_1['{}'.format(j)] = float(number_occurences) / total_pop_enl
            if en == 2:
                distribution_enl_2['{}'.format(j)] = float(number_occurences) / total_pop_enl
            else:
                distribution_enl_3['{}'.format(j)] = float(number_occurences) / total_pop_enl
    
        hellinger_distance_1 = hellinger(distribution_bdf_1.values(),distribution_enl_1.values())
        hellinger_distance_2 = hellinger(distribution_bdf_2.values(),distribution_enl_2.values())
        hellinger_distance_3 = hellinger(distribution_bdf_3.values(),distribution_enl_3.values())
    
    return hellinger_distance_1, hellinger_distance_2, hellinger_distance_3
    
hellinger_poste_coicop_451 = hellinger_postes_energies(data_bdf, data_enl)[0]
hellinger_poste_coicop_452 = hellinger_postes_energies(data_bdf, data_enl)[1]
hellinger_poste_coicop_453 = hellinger_postes_energies(data_bdf, data_enl)[2]

