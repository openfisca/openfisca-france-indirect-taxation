# -*- coding: utf-8 -*-

from __future__ import division

import os
import pkg_resources
import pandas


default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)

data_matched_enl = pandas.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matched_rank.csv'
        ), sep =',', decimal = '.'
    )

data_matched_entd = pandas.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'matching_entd',
        'data_matched_final.csv'
        ), sep =',', decimal = '.'
    )

data_matched_enl = data_matched_enl[
    ['froid'] + ['froid_cout'] + ['froid_isolation'] + ['ident_men']
    ]

data_matched_entd = data_matched_entd[
    ['distance'] + ['distance_diesel'] + ['distance_essence'] +
    ['depenses_carburants_corrigees'] + ['depenses_diesel_corrigees'] +
    ['depenses_essence_corrigees'] + ['ident_men']
    ]


data_frame = pandas.merge(data_matched_entd, data_matched_enl, on = 'ident_men', how = 'left')
data_frame['ident_men'] = data_frame['ident_men'].astype(str)
data_frame = data_frame.fillna(0)

data_frame.to_csv(os.path.join(default_config_files_directory, 'openfisca_france_indirect_taxation', 'assets',
    'matching', 'data_for_run_all.csv'), sep = ',')
