# -*- coding: utf-8 -*-

"""
Computing the Hellinger distance between two discrete
probability distributions
"""

import numpy as np

from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_2_homogenize_variables import \
    create_niveau_vie_quantiles

data = create_niveau_vie_quantiles()
data_enl = data[0]
data_bdf = data[1]


_SQRT2 = np.sqrt(2)     # sqrt(2) with default precision np.float64


def hellinger(p, q):
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / _SQRT2


def hellinger_agepr(data_bdf, data_enl):
    data_bdf['agepr'] = data_bdf['agepr'].astype(float)
    data_enl['agepr'] = data_enl['agepr'].astype(float)
    age_max = int(max(data_bdf['agepr'].max(), data_enl['agepr'].max()))

    distribution_bdf = dict()
    for i in range(0,age_max):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('agepr == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())
    
    distribution_enl = dict()
    for i in range(0,age_max):
        distribution_enl['{}'.format(i)] = (data_enl.query('agepr == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_agepr = hellinger_agepr(data_bdf, data_enl)


def hellinger_bat_annee(data_bdf, data_enl):
    distribution_bdf = dict()
    for i in ['bat_av_49', 'bat_49_74', 'bat_ap_74']:
        distribution_bdf[i] = (data_bdf.query('{} == 1'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_enl = dict()
    for i in ['bat_av_49', 'bat_49_74', 'bat_ap_74']:
        distribution_enl[i] = (data_enl.query('{} == 1'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_bat_annee = hellinger_bat_annee(data_bdf, data_enl)


# By construction, the distance should be extremely close to 0
def hellinger_deciles(data_bdf, data_enl):
    distribution_bdf = dict()
    for i in range(1,10):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('niveau_vie_decile == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_enl = dict()
    for i in range(1,10):
        distribution_enl['{}'.format(i)] = (data_enl.query('niveau_vie_decile == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_deciles = hellinger_deciles(data_bdf, data_enl)


def hellinger_depenses_energies(data_bdf, data_enl):
    data_bdf['depenses_energies'] = data_bdf['depenses_energies'].astype(float)
    data_bdf['depenses_energies_racine'] = (data_bdf['depenses_energies']) ** (0.5)
    depenses_energies_racine_max_bdf = data_bdf['depenses_energies_racine'].max()
    
    data_enl['depenses_energies'] = data_enl['depenses_energies'].astype(float)
    data_enl['depenses_energies_racine'] = (data_enl['depenses_energies']) ** (0.5)
    depenses_energies_racine_max_enl = data_enl['depenses_energies_racine'].max()

    depenses_energies_racine_max = max(depenses_energies_racine_max_bdf, depenses_energies_racine_max_enl)
    data_bdf['depenses_energies_groupe'] = (data_bdf['depenses_energies_racine'] / depenses_energies_racine_max).round(decimals = 2)
    data_enl['depenses_energies_groupe'] = (data_enl['depenses_energies_racine'] / depenses_energies_racine_max).round(decimals = 2)

    distribution_bdf = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_bdf['{}'.format(j)] = (data_bdf.query('depenses_energies_groupe == {}'.format(j))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())
    
    distribution_enl = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_enl['{}'.format(j)] = (data_enl.query('depenses_energies_groupe == {}'.format(j))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_depenses_energies = hellinger_depenses_energies(data_bdf, data_enl)


def hellinger_energies(data_bdf, data_enl):
    distribution_electricite_bdf = dict()
    distribution_gaz_bdf = dict()
    distribution_fioul_bdf = dict()
    distribution_electricite_enl = dict()
    distribution_fioul_enl = dict()
    distribution_gaz_enl = dict()
    for en in ['electricite', 'fioul', 'gaz']:
        for i in [0, 1]:
            if en == 'electricite':
                distribution_electricite_bdf['{}'.format(i)] = (data_bdf.query('electricite == {}'.format(i))['pondmen'].sum() /
                         data_bdf['pondmen'].sum())
            if en == 'fioul':
                distribution_fioul_bdf['{}'.format(i)] = (data_bdf.query('fioul == {}'.format(i))['pondmen'].sum() /
                         data_bdf['pondmen'].sum())
            else:
                distribution_gaz_bdf['{}'.format(i)] = (data_bdf.query('gaz == {}'.format(i))['pondmen'].sum() /
                         data_bdf['pondmen'].sum())
    
    for en in ['electricite', 'fioul', 'gaz']:
        for i in [0, 1]:
            if en == 'electricite':
                distribution_electricite_enl['{}'.format(i)] = (data_enl.query('electricite == {}'.format(i))['pondmen'].sum() /
                         data_enl['pondmen'].sum())
            if en == 'fioul':
                distribution_fioul_enl['{}'.format(i)] = (data_enl.query('fioul == {}'.format(i))['pondmen'].sum() /
                         data_enl['pondmen'].sum())
            else:
                distribution_gaz_enl['{}'.format(i)] = (data_enl.query('gaz == {}'.format(i))['pondmen'].sum() /
                         data_enl['pondmen'].sum())

    hellinger_distance_electricite = hellinger(distribution_electricite_bdf.values(),distribution_electricite_enl.values())
    hellinger_distance_fioul = hellinger(distribution_fioul_bdf.values(),distribution_fioul_enl.values())
    hellinger_distance_gaz = hellinger(distribution_gaz_bdf.values(),distribution_gaz_enl.values())

    return hellinger_distance_electricite, hellinger_distance_fioul, hellinger_distance_gaz
    
hellinger_electricite = hellinger_energies(data_bdf, data_enl)[0]
hellinger_fioul = hellinger_energies(data_bdf, data_enl)[1]
hellinger_gaz = hellinger_energies(data_bdf, data_enl)[2]


def hellinger_log_colec(data_bdf, data_enl):
    distribution_bdf = dict()
    for i in [0, 1]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('log_colec == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_enl = dict()
    for i in [0, 1]:
        distribution_enl['{}'.format(i)] = (data_enl.query('log_colec == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_log_colec = hellinger_log_colec(data_bdf, data_enl)


def hellinger_nbphab(data_bdf, data_enl):
    distribution_bdf = dict()
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('nbphab == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_enl = dict()
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        distribution_enl['{}'.format(i)] = (data_enl.query('nbphab == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_nbphab = hellinger_nbphab(data_bdf, data_enl)


def hellinger_ocde10(data_bdf, data_enl):
    distribution_bdf = dict()
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('ocde10 == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_enl = dict()
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        distribution_enl['{}'.format(i)] = (data_enl.query('ocde10 == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_ocde10 = hellinger_ocde10(data_bdf, data_enl)


def hellinger_part_energies_revtot(data_bdf, data_enl):
    data_bdf['part_energies_revtot'] = data_bdf['part_energies_revtot'].astype(float)
    data_bdf = data_bdf.query('part_energies_revtot < 1').copy()
    data_bdf['part_energies_revtot_groupe'] = data_bdf['part_energies_revtot'].round(decimals = 2)
    
    data_enl['part_energies_revtot'] = data_enl['part_energies_revtot'].astype(float)
    data_enl = data_enl.query('part_energies_revtot < 1').copy()
    data_enl['part_energies_revtot_groupe'] = data_enl['part_energies_revtot'].round(decimals = 2)
    
    
    distribution_bdf = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_bdf['{}'.format(j)] = (data_bdf.query('part_energies_revtot_groupe == {}'.format(j))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())
    
    distribution_enl = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_enl['{}'.format(j)] = (data_enl.query('part_energies_revtot_groupe == {}'.format(j))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_part_energies_revtot = hellinger_part_energies_revtot(data_bdf, data_enl)


# Test if two opposite distributions have hellinger distance = 1
def hellinger_test(data_bdf, data_enl):
    distribution_bdf = dict()
    for i in range(1,51):
        distribution_bdf['{}'.format(i)] = 0.02
    for i in range(51,101):
        distribution_bdf['{}'.format(i)] = 0
    
    distribution_enl = dict()
    for i in range(1,51):
        distribution_enl['{}'.format(i)] = 0
    for i in range(51,101):
        distribution_enl['{}'.format(i)] = 0.02

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_test = hellinger_test(data_bdf, data_enl)


def hellinger_postes_energies(data_bdf, data_enl):
    distribution_bdf_1 = dict()
    distribution_bdf_2 = dict()
    distribution_bdf_3 = dict()
    distribution_enl_1 = dict()
    distribution_enl_2 = dict()
    distribution_enl_3 = dict()
    for en in [1,2,3]:
        data_bdf['poste_coicop_45{}'.format(en)] = data_bdf['poste_coicop_45{}'.format(en)].astype(float)
        poste_max_bdf = data_bdf['poste_coicop_45{}'.format(en)].max()        
        data_enl['poste_coicop_45{}'.format(en)] = data_enl['poste_coicop_45{}'.format(en)].astype(float)
        poste_max_enl = data_enl['poste_coicop_45{}'.format(en)].max()

        poste_max = max(poste_max_bdf, poste_max_enl)
        data_bdf['poste_coicop_45{}_groupe'.format(en)] = (data_bdf['poste_coicop_45{}'.format(en)] / poste_max).round(decimals = 2)
        data_enl['poste_coicop_45{}_groupe'.format(en)] = (data_enl['poste_coicop_45{}'.format(en)] / poste_max).round(decimals = 2)    
    
        for i in range(0,101):
            j = float(i)/100
            if en == 1:
                distribution_bdf_1['{}'.format(j)] = (data_bdf.query('poste_coicop_45{}_groupe == {}'.format(en, j))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())
            if en == 2:
                distribution_bdf_2['{}'.format(j)] = (data_bdf.query('poste_coicop_45{}_groupe == {}'.format(en, j))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())
            else:
                distribution_bdf_3['{}'.format(j)] = (data_bdf.query('poste_coicop_45{}_groupe == {}'.format(en, j))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())
        
        for i in range(0,101):
            j = float(i)/100
            if en == 1:
                distribution_enl_1['{}'.format(j)] = (data_enl.query('poste_coicop_45{}_groupe == {}'.format(en, j))['pondmen'].sum() /
                 data_enl['pondmen'].sum())
            if en == 2:
                distribution_enl_2['{}'.format(j)] = (data_enl.query('poste_coicop_45{}_groupe == {}'.format(en, j))['pondmen'].sum() /
                 data_enl['pondmen'].sum())
            else:
                distribution_enl_3['{}'.format(j)] = (data_enl.query('poste_coicop_45{}_groupe == {}'.format(en, j))['pondmen'].sum() /
                 data_enl['pondmen'].sum())
    
        hellinger_distance_1 = hellinger(distribution_bdf_1.values(),distribution_enl_1.values())
        hellinger_distance_2 = hellinger(distribution_bdf_2.values(),distribution_enl_2.values())
        hellinger_distance_3 = hellinger(distribution_bdf_3.values(),distribution_enl_3.values())
    
    return hellinger_distance_1, hellinger_distance_2, hellinger_distance_3
    
hellinger_poste_coicop_451 = hellinger_postes_energies(data_bdf, data_enl)[0]
hellinger_poste_coicop_452 = hellinger_postes_energies(data_bdf, data_enl)[1]
hellinger_poste_coicop_453 = hellinger_postes_energies(data_bdf, data_enl)[2]


# By construction, the distance should be extremely close to 0
def hellinger_quintiles(data_bdf, data_enl):
    distribution_bdf = dict()
    for i in range(1,10):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('niveau_vie_quintile == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_enl = dict()
    for i in range(1,10):
        distribution_enl['{}'.format(i)] = (data_enl.query('niveau_vie_quintile == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_quintiles = hellinger_quintiles(data_bdf, data_enl)



def hellinger_revtot(data_bdf, data_enl):
    data_bdf['revtot'] = data_bdf['revtot'].astype(float)
    data_bdf['revtot_racine'] = (data_bdf['revtot']) ** (0.5)
    revtot_racine_max_bdf = data_bdf['revtot_racine'].max()
    
    data_enl['revtot'] = data_enl['revtot'].astype(float)
    data_enl['revtot_racine'] = (data_enl['revtot']) ** (0.5)
    revtot_racine_max_enl = data_enl['revtot_racine'].max()

    revtot_racine_max = max(revtot_racine_max_bdf, revtot_racine_max_enl)
    data_bdf['revtot_groupe'] = (data_bdf['revtot_racine'] / revtot_racine_max).round(decimals = 2)
    data_enl['revtot_groupe'] = (data_enl['revtot_racine'] / revtot_racine_max).round(decimals = 2)

    distribution_bdf = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_bdf['{}'.format(j)] = (data_bdf.query('revtot_groupe == {}'.format(j))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())
    
    distribution_enl = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_enl['{}'.format(j)] = (data_enl.query('revtot_groupe == {}'.format(j))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_revtot = hellinger_revtot(data_bdf, data_enl)


def hellinger_surfhab_d(data_bdf, data_enl):
    data_bdf['surfhab_d'] = data_bdf['surfhab_d'].astype(float)
    surfhab_d_max_bdf = data_bdf['surfhab_d'].max()    
    data_enl['surfhab_d'] = data_enl['surfhab_d'].astype(float)
    surfhab_d_max_enl = data_enl['surfhab_d'].max()

    surfhab_d_max = max(surfhab_d_max_bdf, surfhab_d_max_enl)
    data_bdf['surfhab_d_groupe'] = (data_bdf['surfhab_d'] / surfhab_d_max).round(decimals = 2)
    data_enl['surfhab_d_groupe'] = (data_enl['surfhab_d'] / surfhab_d_max).round(decimals = 2)

    distribution_bdf = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_bdf['{}'.format(j)] = (data_bdf.query('surfhab_d_groupe == {}'.format(j))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())
    
    distribution_enl = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_enl['{}'.format(j)] = (data_enl.query('surfhab_d_groupe == {}'.format(j))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_surfhab_d = hellinger_surfhab_d(data_bdf, data_enl)


def hellinger_tau(data_bdf, data_enl):
    distribution_bdf = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('tau == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_enl = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        distribution_enl['{}'.format(i)] = (data_enl.query('tau == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_tau = hellinger_tau(data_bdf, data_enl)


def hellinger_tuu(data_bdf, data_enl):
    distribution_bdf = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('tuu == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_enl = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8]:
        distribution_enl['{}'.format(i)] = (data_enl.query('tuu == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_tuu = hellinger_tuu(data_bdf, data_enl)


def hellinger_zeat(data_bdf, data_enl):
    distribution_bdf = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('zeat == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_enl = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        distribution_enl['{}'.format(i)] = (data_enl.query('zeat == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_zeat = hellinger_zeat(data_bdf, data_enl)
