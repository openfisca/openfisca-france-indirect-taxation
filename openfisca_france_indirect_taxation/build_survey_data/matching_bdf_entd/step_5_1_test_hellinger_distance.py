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

data_matched = data_matched_distance.copy()
    
    
def hellinger(p, q):
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / _SQRT2


def hellinger_distance_annuelle(data_matched, data_entd):
    data_matched['distance'] = data_matched['distance'].astype(float)
    data_matched['distance_racine'] = (data_matched['distance']) ** (0.5)
    distance_racine_max_matched = data_matched['distance_racine'].max()

    data_entd['distance'] = data_entd['distance'].astype(float)
    data_entd['distance_racine'] = (data_entd['distance']) ** (0.5)
    distance_racine_max_entd = data_entd['distance_racine'].max()

    distance_racine_max = max(distance_racine_max_matched, distance_racine_max_entd)
    data_matched['distance_groupe'] = (data_matched['distance_racine'] / distance_racine_max).round(decimals = 2)
    data_entd['distance_groupe'] = (data_entd['distance_racine'] / distance_racine_max).round(decimals = 2)

    distribution_matched = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_matched['{}'.format(j)] = (data_matched.query('distance_groupe == {}'.format(j))['pondmen'].sum() /
                 data_matched['pondmen'].sum())
    
    distribution_entd = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_entd['{}'.format(j)] = (data_entd.query('distance_groupe == {}'.format(j))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(distribution_matched.values(),distribution_entd.values())
    
    return hellinger_distance
    

def hellinger_distance_diesel_annuelle(data_matched, data_entd):
    data_matched['distance_diesel'] = data_matched['distance_diesel'].astype(float)
    data_matched['distance_diesel_racine'] = (data_matched['distance_diesel']) ** (0.5)
    distance_diesel_racine_max_matched = data_matched['distance_diesel_racine'].max()
    
    data_entd['distance_diesel'] = data_entd['distance_diesel'].astype(float)
    data_entd['distance_diesel_racine'] = (data_entd['distance_diesel']) ** (0.5)
    distance_diesel_racine_max_entd = data_entd['distance_diesel_racine'].max()

    distance_diesel_racine_max = max(distance_diesel_racine_max_matched, distance_diesel_racine_max_entd)
    data_matched['distance_diesel_groupe'] = (data_matched['distance_diesel_racine'] / distance_diesel_racine_max).round(decimals = 2)
    data_entd['distance_diesel_groupe'] = (data_entd['distance_diesel_racine'] / distance_diesel_racine_max).round(decimals = 2)

    distribution_matched = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_matched['{}'.format(j)] = (data_matched.query('distance_diesel_groupe == {}'.format(j))['pondmen'].sum() /
                 data_matched['pondmen'].sum())
    
    distribution_entd = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_entd['{}'.format(j)] = (data_entd.query('distance_diesel_groupe == {}'.format(j))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance_diesel = hellinger(distribution_matched.values(),distribution_entd.values())
    
    return hellinger_distance_diesel
    

    
def hellinger_distance_essence_annuelle(data_matched, data_entd):
    data_matched['distance_essence'] = data_matched['distance_essence'].astype(float)
    data_matched['distance_essence_racine'] = (data_matched['distance_essence']) ** (0.5)
    distance_essence_racine_max_matched = data_matched['distance_essence_racine'].max()
    
    data_entd['distance_essence'] = data_entd['distance_essence'].astype(float)
    data_entd['distance_essence_racine'] = (data_entd['distance_essence']) ** (0.5)
    distance_essence_racine_max_entd = data_entd['distance_essence_racine'].max()

    distance_essence_racine_max = max(distance_essence_racine_max_matched, distance_essence_racine_max_entd)
    data_matched['distance_essence_groupe'] = (data_matched['distance_essence_racine'] / distance_essence_racine_max).round(decimals = 2)
    data_entd['distance_essence_groupe'] = (data_entd['distance_essence_racine'] / distance_essence_racine_max).round(decimals = 2)

    distribution_matched = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_matched['{}'.format(j)] = (data_matched.query('distance_essence_groupe == {}'.format(j))['pondmen'].sum() /
                 data_matched['pondmen'].sum())
    
    distribution_entd = dict()
    for i in range(0,101):
        j = float(i)/100
        distribution_entd['{}'.format(j)] = (data_entd.query('distance_essence_groupe == {}'.format(j))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance_essence = hellinger(distribution_matched.values(),distribution_entd.values())
    
    return hellinger_distance_essence


def hellinger_distance_annuelle_niveau_vie_decile(data_matched, data_entd):
    data_matched['distance'] = data_matched['distance'].astype(float)
    data_matched['distance_racine'] = (data_matched['distance']) ** (0.5)
    distance_racine_max_matched = data_matched['distance_racine'].max()

    data_entd['distance'] = data_entd['distance'].astype(float)
    data_entd['distance_racine'] = (data_entd['distance']) ** (0.5)
    distance_racine_max_entd = data_entd['distance_racine'].max()

    distance_racine_max = max(distance_racine_max_matched, distance_racine_max_entd)
    data_matched['distance_groupe'] = (data_matched['distance_racine'] / distance_racine_max).round(decimals = 1)
    data_entd['distance_groupe'] = (data_entd['distance_racine'] / distance_racine_max).round(decimals = 1)

    distribution_matched = dict()
    for d in range(1,11):
        for i in range(0,11):
            j = float(i)/10
            distribution_matched['{} - {}'.format(d,j)] = (
                (data_matched.query('niveau_vie_decile == {}'.format(d)).query('distance_groupe == {}'.format(j))['pondmen']).sum() /
                data_matched['pondmen'].sum()
                ) 
    
    distribution_entd = dict()
    for d in range(1,11):
        for i in range(0,11):
            j = float(i)/10
            distribution_entd['{} - {}'.format(d,j)] = (
                (data_entd.query('niveau_vie_decile == {}'.format(d)).query('distance_groupe == {}'.format(j))['pondmen']).sum() /
                data_entd['pondmen'].sum()
                ) 

    hellinger_distance = hellinger(distribution_matched.values(),distribution_entd.values())
    
    return hellinger_distance


def hellinger_distance_annuelle_tuu(data_matched, data_entd):
    data_matched['distance'] = data_matched['distance'].astype(float)
    data_matched['distance_racine'] = (data_matched['distance']) ** (0.5)
    distance_racine_max_matched = data_matched['distance_racine'].max()

    data_entd['distance'] = data_entd['distance'].astype(float)
    data_entd['distance_racine'] = (data_entd['distance']) ** (0.5)
    distance_racine_max_entd = data_entd['distance_racine'].max()

    distance_racine_max = max(distance_racine_max_matched, distance_racine_max_entd)
    data_matched['distance_groupe'] = (data_matched['distance_racine'] / distance_racine_max).round(decimals = 1)
    data_entd['distance_groupe'] = (data_entd['distance_racine'] / distance_racine_max).round(decimals = 1)

    distribution_matched = dict()
    for t in range(0,9):
        for i in range(0,11):
            j = float(i)/10
            distribution_matched['{} - {}'.format(t,j)] = (
                (data_matched.query('tuu == {}'.format(t)).query('distance_groupe == {}'.format(j))['pondmen']).sum() /
                data_matched['pondmen'].sum()
                ) 
    
    distribution_entd = dict()
    for t in range(0,9):
        for i in range(0,11):
            j = float(i)/10
            distribution_entd['{} - {}'.format(t,j)] = (
                (data_entd.query('tuu == {}'.format(t)).query('distance_groupe == {}'.format(j))['pondmen']).sum() /
                data_entd['pondmen'].sum()
                ) 

    hellinger_distance = hellinger(distribution_matched.values(),distribution_entd.values())
    
    return hellinger_distance


    
hellinger_distance_annuelle = hellinger_distance_annuelle(data_matched_distance, data_entd) 

hellinger_distance_diesel_annuelle = hellinger_distance_diesel_annuelle(data_matched_distance, data_entd)

hellinger_distance_essence_annuelle = hellinger_distance_essence_annuelle(data_matched_distance, data_entd)

hellinger_distance_annuelle_nvd = hellinger_distance_annuelle_niveau_vie_decile(data_matched_distance, data_entd)

hellinger_distance_annuelle_tuu = hellinger_distance_annuelle_tuu(data_matched_distance, data_entd)
