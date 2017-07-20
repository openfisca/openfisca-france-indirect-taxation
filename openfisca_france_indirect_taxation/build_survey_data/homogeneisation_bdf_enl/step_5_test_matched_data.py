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


def test_froid_niveau_vie_decile(data_enl, data_matched):
    dict_froid = dict()
    average_froid_enl = 100 * sum(data_enl['pondmen'] * (data_enl['gchauf_n'] != 0)) / sum(data_enl['pondmen'])
    average_froid_matched = 100 * sum(data_matched['pondmen'] * (data_matched['gchauf_n'] != 0)) / sum(data_matched['pondmen'])
    dict_froid['Average'] = [average_froid_enl, average_froid_matched]
    for i in range(1,11):
        data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))
    
        part_froid_enl = 100 * sum(data_enl_decile['pondmen'] * (data_enl_decile['gchauf_n'] != 0)) / sum(data_enl_decile['pondmen'])
        part_froid_matched = 100 * sum(data_matched_decile['pondmen'] * (data_matched_decile['gchauf_n'] != 0)) / sum(data_matched_decile['pondmen'])
    
        dict_froid['{}'.format(i)] = \
            [part_froid_enl, part_froid_matched]
    
    return dict_froid

test_froid_niveau_vie_decile_distance = test_froid_niveau_vie_decile(data_enl, data_matched_distance)
test_froid_niveau_vie_decile_random = test_froid_niveau_vie_decile(data_enl, data_matched_random)
test_froid_niveau_vie_decile_rank = test_froid_niveau_vie_decile(data_enl, data_matched_rank)


def test_froid_cout_niveau_vie_decile(data_enl, data_matched):
    dict_froid = dict()
    average_froid_enl = 100 * sum(data_enl['pondmen'] * (data_enl['gchauf_3'] == 1)) / sum(data_enl['pondmen'])
    average_froid_matched = 100 * sum(data_matched['pondmen'] * (data_matched['gchauf_3'] == 1)) / sum(data_matched['pondmen'])
    dict_froid['Average'] = [average_froid_enl, average_froid_matched]
    for i in range(1,11):
        data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))
    
        part_froid_enl = 100 * sum(data_enl_decile['pondmen'] * (data_enl_decile['gchauf_3'] == 1)) / sum(data_enl_decile['pondmen'])
        part_froid_matched = 100 * sum(data_matched_decile['pondmen'] * (data_matched_decile['gchauf_3'] == 1)) / sum(data_matched_decile['pondmen'])
    
        dict_froid['{}'.format(i)] = \
            [part_froid_enl, part_froid_matched]
    
    return dict_froid

test_froid_cout_niveau_vie_decile_distance = test_froid_cout_niveau_vie_decile(data_enl, data_matched_distance)
test_froid_cout_niveau_vie_decile_random = test_froid_cout_niveau_vie_decile(data_enl, data_matched_random)
test_froid_cout_niveau_vie_decile_rank = test_froid_cout_niveau_vie_decile(data_enl, data_matched_rank)
