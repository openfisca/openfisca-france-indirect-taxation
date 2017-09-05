# -*- coding: utf-8 -*-

# Dans ce script, on test la qualité de l'appariement.

from __future__ import division


import pandas as pd

import os
import pkg_resources


# Importation des bases de données appariées et de la base de référence entd
default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)


data_entd = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'matching_entd',
        'data_matching_entd.csv'
        ), sep =',', decimal = '.'
    )


data_matched_distance = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'matching_entd',
        'data_matched_distance.csv'
        ), sep =',', decimal = '.'
    )

    
data_matched_random = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'matching_entd',
        'data_matched_random.csv'
        ), sep =',', decimal = '.'
    )


data_matched_rank = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'matching_entd',
        'data_matched_rank.csv'
        ), sep =',', decimal = '.'
    )


def test_distance_niveau_vie_decile(data_entd, data_matched):
    dict_froid = dict()
    average_froid_entd = sum(data_entd['pondmen'] * (data_entd['distance'])) / sum(data_entd['pondmen'])
    average_froid_matched = sum(data_matched['pondmen'] * (data_matched['distance'])) / sum(data_matched['pondmen'])
    dict_froid['Average'] = [average_froid_entd, average_froid_matched]
    for i in range(1,11):
        data_entd_decile = data_entd.query('niveau_vie_decile == {}'.format(i))
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))
    
        part_froid_entd = sum(data_entd_decile['pondmen'] * (data_entd_decile['distance'])) / sum(data_entd_decile['pondmen'])
        part_froid_matched = sum(data_matched_decile['pondmen'] * (data_matched_decile['distance'])) / sum(data_matched_decile['pondmen'])
    
        dict_froid['{}'.format(i)] = \
            [part_froid_entd, part_froid_matched]
    
    return dict_froid

    
def test_distance_diesel_niveau_vie_decile(data_entd, data_matched):
    dict_froid = dict()
    average_froid_entd = sum(data_entd['pondmen'] * (data_entd['distance_diesel'])) / sum(data_entd['pondmen'])
    average_froid_matched = sum(data_matched['pondmen'] * (data_matched['distance_diesel'])) / sum(data_matched['pondmen'])
    dict_froid['Average'] = [average_froid_entd, average_froid_matched]
    for i in range(1,11):
        data_entd_decile = data_entd.query('niveau_vie_decile == {}'.format(i))
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))
    
        part_froid_entd = sum(data_entd_decile['pondmen'] * (data_entd_decile['distance_diesel'])) / sum(data_entd_decile['pondmen'])
        part_froid_matched = sum(data_matched_decile['pondmen'] * (data_matched_decile['distance_diesel'])) / sum(data_matched_decile['pondmen'])
    
        dict_froid['{}'.format(i)] = \
            [part_froid_entd, part_froid_matched]
    
    return dict_froid

def test_distance_essence_niveau_vie_decile(data_entd, data_matched):
    dict_froid = dict()
    average_froid_entd = sum(data_entd['pondmen'] * (data_entd['distance_essence'])) / sum(data_entd['pondmen'])
    average_froid_matched = sum(data_matched['pondmen'] * (data_matched['distance_essence'])) / sum(data_matched['pondmen'])
    dict_froid['Average'] = [average_froid_entd, average_froid_matched]
    for i in range(1,11):
        data_entd_decile = data_entd.query('niveau_vie_decile == {}'.format(i))
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))
    
        part_froid_entd = sum(data_entd_decile['pondmen'] * (data_entd_decile['distance_essence'])) / sum(data_entd_decile['pondmen'])
        part_froid_matched = sum(data_matched_decile['pondmen'] * (data_matched_decile['distance_essence'])) / sum(data_matched_decile['pondmen'])
    
        dict_froid['{}'.format(i)] = \
            [part_froid_entd, part_froid_matched]
    
    return dict_froid


test_distance_niveau_vie_decile_distance = test_distance_niveau_vie_decile(data_entd, data_matched_distance)
test_distance_niveau_vie_decile_random = test_distance_niveau_vie_decile(data_entd, data_matched_random)
test_distance_niveau_vie_decile_rank = test_distance_niveau_vie_decile(data_entd, data_matched_rank)

test_distance_diesel_niveau_vie_decile_distance = test_distance_diesel_niveau_vie_decile(data_entd, data_matched_distance)
test_distance_diesel_niveau_vie_decile_random = test_distance_diesel_niveau_vie_decile(data_entd, data_matched_random)
test_distance_diesel_niveau_vie_decile_rank = test_distance_diesel_niveau_vie_decile(data_entd, data_matched_rank)

test_distance_essence_niveau_vie_decile_distance_essence = test_distance_essence_niveau_vie_decile(data_entd, data_matched_distance)
test_distance_essence_niveau_vie_decile_random = test_distance_essence_niveau_vie_decile(data_entd, data_matched_random)
test_distance_essence_niveau_vie_decile_rank = test_distance_essence_niveau_vie_decile(data_entd, data_matched_rank)
