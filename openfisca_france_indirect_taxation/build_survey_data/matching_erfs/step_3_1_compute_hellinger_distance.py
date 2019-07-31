# -*- coding: utf-8 -*-

"""
Computing the Hellinger distance between two discrete
probability distributions
"""

from openfisca_france_indirect_taxation.build_survey_data.matching_erfs.step_2_homogenize_variables import \
    homogenize_definitions
from openfisca_france_indirect_taxation.build_survey_data.utils import \
    hellinger

data = homogenize_definitions()
data_erfs = data[0]
data_bdf = data[1]


def hellinger_agepr(data_bdf, data_erfs):
    data_bdf['agepr'] = data_bdf['agepr'].astype(float)
    data_erfs['agepr'] = data_erfs['agepr'].astype(float)
    age_max = int(max(data_bdf['agepr'].max(), data_erfs['agepr'].max()))

    distribution_bdf = dict()
    for i in range(0, age_max):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('agepr == {}'.format(i))['pondmen'].sum()
/ data_bdf['pondmen'].sum())

    distribution_erfs = dict()
    for i in range(0, age_max):
        distribution_erfs['{}'.format(i)] = (data_erfs.query('agepr == {}'.format(i))['pondmen'].sum()
/ data_erfs['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_erfs.values()))

    return hellinger_distance


hellinger_agepr = hellinger_agepr(data_bdf, data_erfs)


def hellinger_cataeu(data_bdf, data_erfs):
    distribution_bdf = dict()
    for i in [111, 112, 120, 211, 212, 221, 222, 300, 400]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('cataeu == {}'.format(i))['pondmen'].sum()
/ data_bdf['pondmen'].sum())

    distribution_erfs = dict()
    for i in [111, 112, 120, 211, 212, 221, 222, 300, 400]:
        distribution_erfs['{}'.format(i)] = (data_erfs.query('cataeu == {}'.format(i))['pondmen'].sum()
/ data_erfs['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_erfs.values()))

    return hellinger_distance


hellinger_cataeu = hellinger_cataeu(data_bdf, data_erfs)


def hellinger_ocde10(data_bdf, data_erfs):
    distribution_bdf = dict()
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('ocde10 == {}'.format(i))['pondmen'].sum()
/ data_bdf['pondmen'].sum())

    distribution_erfs = dict()
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        distribution_erfs['{}'.format(i)] = (data_erfs.query('ocde10 == {}'.format(i))['pondmen'].sum()
/ data_erfs['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_erfs.values()))

    return hellinger_distance


hellinger_ocde10 = hellinger_ocde10(data_bdf, data_erfs)


def hellinger_rev_disponible(data_bdf, data_erfs):
    data_bdf['rev_disponible'] = data_bdf['rev_disponible'].astype(float)
    data_bdf['rev_disponible_racine'] = (data_bdf['rev_disponible']) ** (0.5)
    rev_disponible_racine_max_bdf = data_bdf['rev_disponible_racine'].max()

    data_erfs['rev_disponible'] = data_erfs['rev_disponible'].astype(float)
    data_erfs['rev_disponible_racine'] = (data_erfs['rev_disponible']) ** (0.5)
    rev_disponible_racine_max_erfs = data_erfs['rev_disponible_racine'].max()

    rev_disponible_racine_max = max(rev_disponible_racine_max_bdf, rev_disponible_racine_max_erfs)
    data_bdf['rev_disponible_groupe'] = (data_bdf['rev_disponible_racine'] / rev_disponible_racine_max).round(decimals = 2)
    data_erfs['rev_disponible_groupe'] = (data_erfs['rev_disponible_racine'] / rev_disponible_racine_max).round(decimals = 2)

    distribution_bdf = dict()
    for i in range(0, 101):
        j = float(i) / 100
        distribution_bdf['{}'.format(j)] = (data_bdf.query('rev_disponible_groupe == {}'.format(j))['pondmen'].sum()
/ data_bdf['pondmen'].sum())

    distribution_erfs = dict()
    for i in range(0, 101):
        j = float(i) / 100
        distribution_erfs['{}'.format(j)] = (data_erfs.query('rev_disponible_groupe == {}'.format(j))['pondmen'].sum()
/ data_erfs['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_erfs.values()))

    return hellinger_distance


hellinger_rev_disponible = hellinger_rev_disponible(data_bdf, data_erfs)


def hellinger_tau(data_bdf, data_erfs):
    distribution_bdf = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('tau == {}'.format(i))['pondmen'].sum()
/ data_bdf['pondmen'].sum())

    distribution_erfs = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        distribution_erfs['{}'.format(i)] = (data_erfs.query('tau == {}'.format(i))['pondmen'].sum()
/ data_erfs['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_erfs.values()))

    return hellinger_distance


hellinger_tau = hellinger_tau(data_bdf, data_erfs)


def hellinger_tuu(data_bdf, data_erfs):
    distribution_bdf = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('tuu == {}'.format(i))['pondmen'].sum()
/ data_bdf['pondmen'].sum())

    distribution_erfs = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8]:
        distribution_erfs['{}'.format(i)] = (data_erfs.query('tuu == {}'.format(i))['pondmen'].sum()
/ data_erfs['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_erfs.values()))

    return hellinger_distance


hellinger_tuu = hellinger_tuu(data_bdf, data_erfs)
