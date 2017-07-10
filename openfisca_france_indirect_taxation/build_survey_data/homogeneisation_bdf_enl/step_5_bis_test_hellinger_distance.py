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

"""
data_matched = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matched.csv'
        ), sep =',', decimal = '.'
    )
"""
    
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
