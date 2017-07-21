# -*- coding: utf-8 -*-

"""
Computing the Hellinger distance between two discrete
probability distributions
"""

# Dans ce script, on test la qualité de l'appariement.

from __future__ import division


import pandas as pd
import numpy as np

import os
import pkg_resources

_SQRT2 = np.sqrt(2)     # sqrt(2) with default precision np.float64

# Importation des bases de données appariées et de la base de référence ENL
default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)


data_enl = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matching_enl.csv'
        ), sep =',', decimal = '.'
    )


data_matched_distance = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matched_distance.csv'
        ), sep =',', decimal = '.'
    )

    
data_matched_random = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matched_random.csv'
        ), sep =',', decimal = '.'
    )


data_matched_rank = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matched_rank.csv'
        ), sep =',', decimal = '.'
    )



"""
Test : share of people having trouble with heat in general
    With sampling weights
"""

def hellinger(p, q):
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / _SQRT2


def hellinger_froid(data_matched, data_enl):
    distribution_matched = dict()
    for i in [0, 1]:
        distribution_matched['{}'.format(i)] = (data_matched.query('froid == {}'.format(i))['pondmen'].sum() /
                 data_matched['pondmen'].sum())

    distribution_enl = dict()
    for i in [0, 1]:
        distribution_enl['{}'.format(i)] = (data_enl.query('froid == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_matched.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_froid_random = hellinger_froid(data_matched_random, data_enl)
hellinger_froid_rank = hellinger_froid(data_matched_rank, data_enl)


def hellinger_froid_cout(data_matched, data_enl):
    distribution_matched = dict()
    for i in [0, 1]:
        distribution_matched['{}'.format(i)] = (data_matched.query('froid_cout == {}'.format(i))['pondmen'].sum() /
                 data_matched['pondmen'].sum())

    distribution_enl = dict()
    for i in [0, 1]:
        distribution_enl['{}'.format(i)] = (data_enl.query('froid_cout == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_matched.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_froid_cout_random = hellinger_froid_cout(data_matched_random, data_enl)
hellinger_froid_cout_rank = hellinger_froid_cout(data_matched_rank, data_enl)


def hellinger_froid_niveau_vie_decile(data_matched, data_enl):
    distribution_matched = dict()
    distribution_enl = dict()
    part_froid_enl = sum(data_enl['pondmen'] * data_enl['froid']) / sum(data_enl['pondmen'])
    part_froid_matched = sum(data_matched['pondmen'] * data_matched['froid']) / sum(data_matched['pondmen'])
    part_froid = max(part_froid_enl, part_froid_matched)
    for i in range(1,11):
        part_froid_decile_enl = (
            sum(data_enl['pondmen'] * (data_enl['froid'] == 1) * (data_enl['niveau_vie_decile'] == i)) /
            sum(data_enl['pondmen'])
            )
        part_froid_decile_matched = (
            sum(data_matched['pondmen'] * (data_matched['froid'] == 1) * (data_matched['niveau_vie_decile'] == i)) /
            sum(data_matched['pondmen'])
            )
        distribution_enl['{}'.format(i)] = (
            part_froid_decile_enl / part_froid
                )
        distribution_matched['{}'.format(i)] = (
            part_froid_decile_matched / part_froid
                )

    hellinger_distance = hellinger(distribution_matched.values(),distribution_enl.values())
    
    return hellinger_distance


    
hellinger_froid_niveau_vie_decile_distance = (
    hellinger_froid_niveau_vie_decile(data_matched_distance, data_enl)
    )
hellinger_froid_niveau_vie_decile_random = (
    hellinger_froid_niveau_vie_decile(data_matched_random, data_enl)
    )
hellinger_froid_niveau_vie_decile_rank = (
    hellinger_froid_niveau_vie_decile(data_matched_rank, data_enl)
    )


def hellinger_froid_cout_niveau_vie_decile(data_matched, data_enl):
    distribution_matched = dict()
    distribution_enl = dict()
    part_froid_enl = sum(data_enl['pondmen'] * data_enl['froid_cout']) / sum(data_enl['pondmen'])
    part_froid_matched = sum(data_matched['pondmen'] * data_matched['froid_cout']) / sum(data_matched['pondmen'])
    part_froid = max(part_froid_enl, part_froid_matched)
    for i in range(1,11):
        part_froid_decile_enl = (
            sum(data_enl['pondmen'] * (data_enl['froid_cout'] == 1) * (data_enl['niveau_vie_decile'] == i)) /
            sum(data_enl['pondmen'])
            )
        part_froid_decile_matched = (
            sum(data_matched['pondmen'] * (data_matched['froid_cout'] == 1) * (data_matched['niveau_vie_decile'] == i)) /
            sum(data_matched['pondmen'])
            )
        distribution_enl['{}'.format(i)] = (
            part_froid_decile_enl / part_froid
                )
        distribution_matched['{}'.format(i)] = (
            part_froid_decile_matched / part_froid
                )

    hellinger_distance = hellinger(distribution_matched.values(),distribution_enl.values())

    return hellinger_distance

hellinger_froid_cout_niveau_vie_decile_distance = (
    hellinger_froid_cout_niveau_vie_decile(data_matched_distance, data_enl)
    )
hellinger_froid_cout_niveau_vie_decile_random = (
    hellinger_froid_cout_niveau_vie_decile(data_matched_random, data_enl)
    )
hellinger_froid_cout_niveau_vie_decile_rank = (
    hellinger_froid_cout_niveau_vie_decile(data_matched_rank, data_enl)
    )
