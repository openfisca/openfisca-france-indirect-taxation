# -*- coding: utf-8 -*-

# Dans ce script, on test la qualité de l'appariement.

from __future__ import division


import pandas as pd

import os
import pkg_resources


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

# In total
print sum(data_enl['pondmen'] * (data_enl['gchauf_n'] != 0)) / sum(data_enl['pondmen'])
print sum(data_matched_distance['pondmen'] * (data_matched_distance['gchauf_n'] != 0)) / sum(data_matched_distance['pondmen'])
print sum(data_matched_random['pondmen'] * (data_matched_random['gchauf_n'] != 0)) / sum(data_matched_random['pondmen'])
print sum(data_matched_rank['pondmen'] * (data_matched_rank['gchauf_n'] != 0)) / sum(data_matched_rank['pondmen'])

# By income decile
for i in range(1,11):
    data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
    data_matched_distance_decile = data_matched_distance.query('niveau_vie_decile == {}'.format(i))
    data_matched_random_decile = data_matched_random.query('niveau_vie_decile == {}'.format(i))
    data_matched_rank_decile = data_matched_rank.query('niveau_vie_decile == {}'.format(i))
    
    print i, 100 * sum(data_enl_decile['pondmen'] * (data_enl_decile['gchauf_n'] != 0)) / sum(data_enl_decile['pondmen']), \
        100 * sum(data_matched_distance_decile['pondmen'] * (data_matched_distance_decile['gchauf_n'] != 0)) / sum(data_matched_distance_decile['pondmen']), \
        100 * sum(data_matched_random_decile['pondmen'] * (data_matched_random_decile['gchauf_n'] != 0)) / sum(data_matched_random_decile['pondmen']), \
        100 * sum(data_matched_rank_decile['pondmen'] * (data_matched_rank_decile['gchauf_n'] != 0)) / sum(data_matched_rank_decile['pondmen'])

    del data_enl_decile, data_matched_distance_decile, data_matched_random_decile, data_matched_rank_decile


"""
Test : share of people having trouble with heat because of the cost
    With sampling weights
"""

# In total
print 100 * sum(data_enl['pondmen'] * (data_enl['gchauf_3'] == 1)) / sum(data_enl['pondmen'])
print 100 * sum(data_matched_distance['pondmen'] * (data_matched_distance['gchauf_3'] == 1)) / sum(data_matched_distance['pondmen'])
print 100 * sum(data_matched_random['pondmen'] * (data_matched_random['gchauf_3'] == 1)) / sum(data_matched_random['pondmen'])
print 100 * sum(data_matched_rank['pondmen'] * (data_matched_rank['gchauf_3'] == 1)) / sum(data_matched_rank['pondmen'])

# By income decile
for i in range(1,11):
    data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
    data_matched_distance_decile = data_matched_distance.query('niveau_vie_decile == {}'.format(i))
    data_matched_random_decile = data_matched_random.query('niveau_vie_decile == {}'.format(i))
    data_matched_rank_decile = data_matched_rank.query('niveau_vie_decile == {}'.format(i))
    
    print i, 100 * sum(data_enl_decile['pondmen'] * (data_enl_decile['gchauf_3'] == 1)) / sum(data_enl_decile['pondmen']), \
        100 * sum(data_matched_distance_decile['pondmen'] * (data_matched_distance_decile['gchauf_3'] == 1)) / sum(data_matched_distance_decile['pondmen']), \
        100 * sum(data_matched_random_decile['pondmen'] * (data_matched_random_decile['gchauf_3'] == 1)) / sum(data_matched_random_decile['pondmen']), \
        100 * sum(data_matched_rank_decile['pondmen'] * (data_matched_rank_decile['gchauf_3'] == 1)) / sum(data_matched_rank_decile['pondmen'])

    del data_enl_decile, data_matched_distance_decile, data_matched_random_decile, data_matched_rank_decile
