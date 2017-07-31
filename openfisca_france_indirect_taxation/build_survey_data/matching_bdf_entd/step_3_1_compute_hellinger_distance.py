# -*- coding: utf-8 -*-

"""
Computing the Hellinger distance between two discrete
probability distributions
"""

# To be completed : add missing variables

import numpy as np

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_2_homogenize_variables import \
    create_niveau_vie_quantiles

data = create_niveau_vie_quantiles()
data_entd = data[0]
data_bdf = data[1]


_SQRT2 = np.sqrt(2)     # sqrt(2) with default precision np.float64


def hellinger(p, q):
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / _SQRT2


def hellinger_agepr(data_bdf, data_entd):
    data_bdf['agepr'] = data_bdf['agepr'].astype(float)
    data_entd['agepr'] = data_entd['agepr'].astype(float)
    age_max = int(max(data_bdf['agepr'].max(), data_entd['agepr'].max()))

    distribution_bdf = dict()
    for i in range(0,age_max):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('agepr == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())
    
    distribution_entd = dict()
    for i in range(0,age_max):
        distribution_entd['{}'.format(i)] = (data_entd.query('agepr == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_entd.values())
    
    return hellinger_distance
    
hellinger_agepr = hellinger_agepr(data_bdf, data_entd)


# By construction, the distance should be extremely close to 0
def hellinger_deciles(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(1,11):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('niveau_vie_decile == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(1,11):
        distribution_entd['{}'.format(i)] = (data_entd.query('niveau_vie_decile == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_entd.values())
    
    return hellinger_distance
    
hellinger_deciles = hellinger_deciles(data_bdf, data_entd)


def hellinger_nbphab(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('nbphab == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        distribution_entd['{}'.format(i)] = (data_entd.query('nbphab == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_entd.values())
    
    return hellinger_distance
    
hellinger_nbphab = hellinger_nbphab(data_bdf, data_entd)


def hellinger_ocde10(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('ocde10 == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        distribution_entd['{}'.format(i)] = (data_entd.query('ocde10 == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_entd.values())
    
    return hellinger_distance
    
hellinger_ocde10 = hellinger_ocde10(data_bdf, data_entd)


# Test if two opposite distributions have hellinger distance = 1
def hellinger_test(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(1,51):
        distribution_bdf['{}'.format(i)] = 0.02
    for i in range(51,101):
        distribution_bdf['{}'.format(i)] = 0
    
    distribution_entd = dict()
    for i in range(1,51):
        distribution_entd['{}'.format(i)] = 0
    for i in range(51,101):
        distribution_entd['{}'.format(i)] = 0.02

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_entd.values())
    
    return hellinger_distance
    
hellinger_test = hellinger_test(data_bdf, data_entd)


# By construction, the distance should be extremely close to 0
def hellinger_quintiles(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(1,10):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('niveau_vie_quintile == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(1,10):
        distribution_entd['{}'.format(i)] = (data_entd.query('niveau_vie_quintile == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_entd.values())
    
    return hellinger_distance
    
hellinger_quintiles = hellinger_quintiles(data_bdf, data_entd)



def hellinger_niveau_vie(data_bdf, data_entd):
    data_bdf['niveau_vie'] = data_bdf['niveau_vie'].astype(float)
    data_bdf['niveau_vie_racine'] = (data_bdf['niveau_vie']) ** (0.5)
    niveau_vie_racine_max_bdf = data_bdf['niveau_vie_racine'].max()
    
    data_entd['niveau_vie'] = data_entd['niveau_vie'].astype(float)
    data_entd['niveau_vie_racine'] = (data_entd['niveau_vie']) ** (0.5)
    niveau_vie_racine_max_entd = data_entd['niveau_vie_racine'].max()

    niveau_vie_racine_max = max(niveau_vie_racine_max_bdf, niveau_vie_racine_max_entd)
    data_bdf['niveau_vie_groupe'] = (data_bdf['niveau_vie_racine'] / niveau_vie_racine_max).round(decimals = 2)
    data_entd['niveau_vie_groupe'] = (data_entd['niveau_vie_racine'] / niveau_vie_racine_max).round(decimals = 2)

    distribution_bdf = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_bdf['{}'.format(j)] = (data_bdf.query('niveau_vie_groupe == {}'.format(j))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())
    
    distribution_entd = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_entd['{}'.format(j)] = (data_entd.query('niveau_vie_groupe == {}'.format(j))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_entd.values())
    
    return hellinger_distance
    
hellinger_niveau_vie = hellinger_niveau_vie(data_bdf, data_entd)


def hellinger_tau(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('tau == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        distribution_entd['{}'.format(i)] = (data_entd.query('tau == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_entd.values())
    
    return hellinger_distance
    
hellinger_tau = hellinger_tau(data_bdf, data_entd)


def hellinger_tuu(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('tuu == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8]:
        distribution_entd['{}'.format(i)] = (data_entd.query('tuu == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(distribution_bdf.values(),distribution_entd.values())
    
    return hellinger_distance
    
hellinger_tuu = hellinger_tuu(data_bdf, data_entd)
