# -*- coding: utf-8 -*-

'''
Computing the Hellinger distance between two discrete
probability distributions
'''

# Dans ce script, on test la qualité de l'appariement.


import pandas as pd

import os

from openfisca_france_indirect_taxation.build_survey_data.utils import \
    hellinger

from openfisca_france_indirect_taxation.utils import assets_directory

# Importation des bases de données appariées et de la base de référence ENL

data_enl = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'data_matching_enl.csv'
        ),
    sep =',',
    decimal = '.'
    )


data_matched_distance = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'data_matched_distance.csv'
        ),
    sep =',',
    decimal = '.'
    )


data_matched_random = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'data_matched_random.csv'
        ),
    sep =',',
    decimal = '.'
    )


data_matched_rank = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'data_matched_rank.csv'
        ), sep =',', decimal = '.'
    )


def hellinger_froid(data_matched, data_enl):
    distribution_matched = dict()
    for i in [0, 1]:
        distribution_matched['{}'.format(i)] = (data_matched.query('froid == {}'.format(i))['pondmen'].sum()
/ data_matched['pondmen'].sum())

    distribution_enl = dict()
    for i in [0, 1]:
        distribution_enl['{}'.format(i)] = (data_enl.query('froid == {}'.format(i))['pondmen'].sum()
/ data_enl['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_matched.values()), list(distribution_enl.values()))

    return hellinger_distance


def hellinger_froid_cout(data_matched, data_enl):
    distribution_matched = dict()
    for i in [0, 1]:
        distribution_matched['{}'.format(i)] = (data_matched.query('froid_cout == {}'.format(i))['pondmen'].sum()
/ data_matched['pondmen'].sum())

    distribution_enl = dict()
    for i in [0, 1]:
        distribution_enl['{}'.format(i)] = (data_enl.query('froid_cout == {}'.format(i))['pondmen'].sum()
/ data_enl['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_matched.values()), list(distribution_enl.values()))

    return hellinger_distance


def hellinger_froid_niveau_vie_decile(data_matched, data_enl):
    distribution_matched = dict()
    distribution_enl = dict()
    part_froid_enl = sum(data_enl['pondmen'] * data_enl['froid']) / sum(data_enl['pondmen'])
    part_froid_matched = sum(data_matched['pondmen'] * data_matched['froid']) / sum(data_matched['pondmen'])
    part_froid = max(part_froid_enl, part_froid_matched)
    for i in range(1, 11):
        part_froid_decile_enl = (
            sum(data_enl['pondmen'] * (data_enl['froid'] == 1) * (data_enl['niveau_vie_decile'] == i))
            / sum(data_enl['pondmen'])
            )
        part_froid_decile_matched = (
            sum(data_matched['pondmen'] * (data_matched['froid'] == 1) * (data_matched['niveau_vie_decile'] == i))
            / sum(data_matched['pondmen'])
            )
        distribution_enl['{}'.format(i)] = (
            part_froid_decile_enl / part_froid
            )
        distribution_matched['{}'.format(i)] = (
            part_froid_decile_matched / part_froid
            )

    hellinger_distance = hellinger(list(distribution_matched.values()), list(distribution_enl.values()))

    return hellinger_distance


def hellinger_froid_tuu(data_matched, data_enl):
    distribution_matched = dict()
    distribution_enl = dict()
    part_froid_enl = sum(data_enl['pondmen'] * data_enl['froid']) / sum(data_enl['pondmen'])
    part_froid_matched = sum(data_matched['pondmen'] * data_matched['froid']) / sum(data_matched['pondmen'])
    part_froid = max(part_froid_enl, part_froid_matched)
    for i in range(1, 9):
        part_froid_tuu_enl = (
            sum(data_enl['pondmen'] * (data_enl['froid'] == 1) * (data_enl['tuu'] == i))
            / sum(data_enl['pondmen'])
            )
        part_froid_tuu_matched = (
            sum(data_matched['pondmen'] * (data_matched['froid'] == 1) * (data_matched['tuu'] == i))
            / sum(data_matched['pondmen'])
            )
        distribution_enl['{}'.format(i)] = (
            part_froid_tuu_enl / part_froid
            )
        distribution_matched['{}'.format(i)] = (
            part_froid_tuu_matched / part_froid
            )

    hellinger_distance = hellinger(list(distribution_matched.values()), list(distribution_enl.values()))

    return hellinger_distance


def hellinger_froid_zeat(data_matched, data_enl):
    distribution_matched = dict()
    distribution_enl = dict()
    part_froid_enl = sum(data_enl['pondmen'] * data_enl['froid']) / sum(data_enl['pondmen'])
    part_froid_matched = sum(data_matched['pondmen'] * data_matched['froid']) / sum(data_matched['pondmen'])
    part_froid = max(part_froid_enl, part_froid_matched)
    for i in range(1, 10):
        part_froid_zeat_enl = (
            sum(data_enl['pondmen'] * (data_enl['froid'] == 1) * (data_enl['zeat'] == i))
            / sum(data_enl['pondmen'])
            )
        part_froid_zeat_matched = (
            sum(data_matched['pondmen'] * (data_matched['froid'] == 1) * (data_matched['zeat'] == i))
            / sum(data_matched['pondmen'])
            )
        distribution_enl['{}'.format(i)] = (
            part_froid_zeat_enl / part_froid
            )
        distribution_matched['{}'.format(i)] = (
            part_froid_zeat_matched / part_froid
            )

    hellinger_distance = hellinger(list(distribution_matched.values()), list(distribution_enl.values()))

    return hellinger_distance


def hellinger_froid_revtot(data_matched, data_enl):
    distribution_matched = dict()
    distribution_enl = dict()

    part_froid_enl = sum(data_enl['pondmen'] * data_enl['froid']) / sum(data_enl['pondmen'])
    part_froid_matched = sum(data_matched['pondmen'] * data_matched['froid']) / sum(data_matched['pondmen'])
    part_froid = max(part_froid_enl, part_froid_matched)

    data_matched['revtot'] = data_matched['revtot'].astype(float)
    data_matched['revtot_racine'] = (data_matched['revtot']) ** (0.5)
    revtot_racine_max_matched = data_matched['revtot_racine'].max()

    data_enl['revtot'] = data_enl['revtot'].astype(float)
    data_enl['revtot_racine'] = (data_enl['revtot']) ** (0.5)
    revtot_racine_max_enl = data_enl['revtot_racine'].max()

    revtot_racine_max = max(revtot_racine_max_matched, revtot_racine_max_enl)
    data_matched['revtot_groupe'] = (data_matched['revtot_racine'] / revtot_racine_max).round(decimals = 2)
    data_enl['revtot_groupe'] = (data_enl['revtot_racine'] / revtot_racine_max).round(decimals = 2)

    for i in range(1, 101):
        j = float(i) / 100
        part_froid_surf_enl = (
            sum(data_enl['pondmen'] * (data_enl['froid'] == 1) * (data_enl['revtot_groupe'] == j))
            / sum(data_enl['pondmen'])
            )
        part_froid_surf_matched = (
            sum(data_matched['pondmen'] * (data_matched['froid'] == 1) * (data_matched['revtot_groupe'] == j))
            / sum(data_matched['pondmen'])
            )
        distribution_enl['{}'.format(i)] = (
            part_froid_surf_enl / part_froid
            )
        distribution_matched['{}'.format(i)] = (
            part_froid_surf_matched / part_froid
            )

    hellinger_distance = hellinger(list(distribution_matched.values()), list(distribution_enl.values()))

    return hellinger_distance


def hellinger_froid_surfhab_d(data_matched, data_enl):
    distribution_matched = dict()
    distribution_enl = dict()

    part_froid_enl = sum(data_enl['pondmen'] * data_enl['froid']) / sum(data_enl['pondmen'])
    part_froid_matched = sum(data_matched['pondmen'] * data_matched['froid']) / sum(data_matched['pondmen'])
    part_froid = max(part_froid_enl, part_froid_matched)

    data_matched['surfhab_d'] = data_matched['surfhab_d'].astype(float)
    surfhab_d_max_bdf = data_matched['surfhab_d'].max()
    data_enl['surfhab_d'] = data_enl['surfhab_d'].astype(float)
    surfhab_d_max_enl = data_enl['surfhab_d'].max()

    surfhab_d_max = max(surfhab_d_max_bdf, surfhab_d_max_enl)
    data_matched['surfhab_d_groupe'] = (data_matched['surfhab_d'] / surfhab_d_max).round(decimals = 2)
    data_enl['surfhab_d_groupe'] = (data_enl['surfhab_d'] / surfhab_d_max).round(decimals = 2)

    for i in range(1, 101):
        j = float(i) / 100
        part_froid_surf_enl = (
            sum(data_enl['pondmen'] * (data_enl['froid'] == 1) * (data_enl['surfhab_d_groupe'] == j))
            / sum(data_enl['pondmen'])
            )
        part_froid_surf_matched = (
            sum(data_matched['pondmen'] * (data_matched['froid'] == 1) * (data_matched['surfhab_d_groupe'] == j))
            / sum(data_matched['pondmen'])
            )
        distribution_enl['{}'.format(i)] = (
            part_froid_surf_enl / part_froid
            )
        distribution_matched['{}'.format(i)] = (
            part_froid_surf_matched / part_froid
            )

    hellinger_distance = hellinger(list(distribution_matched.values()), list(distribution_enl.values()))

    return hellinger_distance


def hellinger_froid_cout_niveau_vie_decile(data_matched, data_enl):
    distribution_matched = dict()
    distribution_enl = dict()
    part_froid_enl = sum(data_enl['pondmen'] * data_enl['froid_cout']) / sum(data_enl['pondmen'])
    part_froid_matched = sum(data_matched['pondmen'] * data_matched['froid_cout']) / sum(data_matched['pondmen'])
    part_froid = max(part_froid_enl, part_froid_matched)
    for i in range(1, 11):
        part_froid_decile_enl = (
            sum(data_enl['pondmen'] * (data_enl['froid_cout'] == 1) * (data_enl['niveau_vie_decile'] == i))
            / sum(data_enl['pondmen'])
            )
        part_froid_decile_matched = (
            sum(data_matched['pondmen'] * (data_matched['froid_cout'] == 1) * (data_matched['niveau_vie_decile'] == i))
            / sum(data_matched['pondmen'])
            )
        distribution_enl['{}'.format(i)] = (
            part_froid_decile_enl / part_froid
            )
        distribution_matched['{}'.format(i)] = (
            part_froid_decile_matched / part_froid
            )

    hellinger_distance = hellinger(list(distribution_matched.values()), list(distribution_enl.values()))

    return hellinger_distance


hellinger_froid_niveau_vie_decile_random = (
    hellinger_froid_niveau_vie_decile(data_matched_distance, data_enl)
    )

hellinger_froid_cout_niveau_vie_decile_random = (
    hellinger_froid_cout_niveau_vie_decile(data_matched_distance, data_enl)
    )

hellinger_froid_revtot_random = (
    hellinger_froid_revtot(data_matched_distance, data_enl)
    )

hellinger_froid_surf_random = (
    hellinger_froid_surfhab_d(data_matched_distance, data_enl)
    )

hellinger_froid_tuu_random = (
    hellinger_froid_tuu(data_matched_distance, data_enl)
    )

hellinger_froid_zeat_random = (
    hellinger_froid_zeat(data_matched_distance, data_enl)
    )
