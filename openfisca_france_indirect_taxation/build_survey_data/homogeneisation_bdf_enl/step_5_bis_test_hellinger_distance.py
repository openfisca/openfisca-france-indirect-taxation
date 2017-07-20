# -*- coding: utf-8 -*-

"""
Computing the Hellinger distance between two discrete
probability distributions
"""

# Dans ce script, on test la qualité de l'appariement.

from __future__ import division


import pandas as pd

import os
import pkg_resources

from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_3_bis_compute_hellinger_distance import \
    hellinger

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

def hellinger_gchauf_n(data_matched, data_enl):
    distribution_matched = dict()
    for i in [0, 1]:
        distribution_matched['{}'.format(i)] = (data_matched.query('gchauf_n == {}'.format(i))['pondmen'].sum() /
                 data_matched['pondmen'].sum())

    distribution_enl = dict()
    for i in [0, 1]:
        distribution_enl['{}'.format(i)] = (data_enl.query('gchauf_n == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_matched.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_gchauf_n_random = hellinger_gchauf_n(data_matched_random, data_enl)
hellinger_gchauf_n_rank = hellinger_gchauf_n(data_matched_rank, data_enl)


def hellinger_gchauf_3(data_matched, data_enl):
    distribution_matched = dict()
    for i in [0, 1]:
        distribution_matched['{}'.format(i)] = (data_matched.query('gchauf_3 == {}'.format(i))['pondmen'].sum() /
                 data_matched['pondmen'].sum())

    distribution_enl = dict()
    for i in [0, 1]:
        distribution_enl['{}'.format(i)] = (data_enl.query('gchauf_3 == {}'.format(i))['pondmen'].sum() /
                 data_enl['pondmen'].sum())

    hellinger_distance = hellinger(distribution_matched.values(),distribution_enl.values())
    
    return hellinger_distance
    
hellinger_gchauf_3_random = hellinger_gchauf_3(data_matched_random, data_enl)
hellinger_gchauf_3_rank = hellinger_gchauf_3(data_matched_rank, data_enl)


def hellinger_froid_niveau_vie_decile(data_matched, data_enl):
    distribution_matched = dict()
    distribution_enl = dict()
    for i in range(1,11):
        data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
        distribution_enl['{}'.format(i)] = (
            100 *
            sum(data_enl_decile['pondmen'] * (data_enl_decile['gchauf_n'] != 0)) /
            sum(data_enl_decile['pondmen'])
                )
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))
        distribution_matched['{}'.format(i)] = (
            100 *
            sum(data_matched_decile['pondmen'] * (data_matched_decile['gchauf_n'] != 0)) /
            sum(data_matched_decile['pondmen'])
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
    for i in range(1,11):
        data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
        distribution_enl['{}'.format(i)] = (
            100 * sum(data_enl_decile['pondmen'] *
            (data_enl_decile['gchauf_3'] == 1)) / sum(data_enl_decile['pondmen'])
                             )
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))
        distribution_matched['{}'.format(i)] = (
            100 * sum(data_matched_decile['pondmen'] *
            (data_matched_decile['gchauf_3'] == 1)) / sum(data_matched_decile['pondmen'])
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
