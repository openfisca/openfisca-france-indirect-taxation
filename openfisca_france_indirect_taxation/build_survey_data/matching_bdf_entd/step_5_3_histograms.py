from __future__ import division


# Dans ce script on utilise des histogrammes pour comparer la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

import matplotlib.pyplot as plt
import seaborn

import os
import pkg_resources
import pandas as pd
import numpy as np

seaborn.set_palette(seaborn.color_palette("Set2", 12))


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

    
def histogrammes(list_keys, list_values_bdf, list_values_entd):
    size_hist = np.arange(len(list_keys))
    plot_bdf = plt.bar(size_hist-0.125, list_values_bdf, color = 'b', align='center', width=0.25)
    plot_entd = plt.bar(size_hist+0.125, list_values_entd, color = 'r', align='center', width=0.25)
    plt.xticks(size_hist, list_keys)
    plt.legend((plot_bdf[0], plot_entd[0]), ('Matched', 'entd'))
    
    return plt


def plots_by_group(function, data_matched, distance, group):    
    fig = plt.figure()
    
    if group == 'tuu':
        corr = -1
    else:
        corr = 0

    ax1 = fig.add_subplot(521)
    ax1 = function(data_matched, data_entd, distance, group, 1+corr)
    
    ax2 = fig.add_subplot(522)
    ax2 = function(data_matched, data_entd, distance, group, 2+corr)
    
    ax3 = fig.add_subplot(523)
    ax3 = function(data_matched, data_entd, distance, group, 3+corr)
    
    ax4 = fig.add_subplot(524)
    ax4 = function(data_matched, data_entd, distance, group, 4+corr)

    ax5 = fig.add_subplot(525)
    ax5 = function(data_matched, data_entd, distance, group, 5+corr)
    
    ax6 = fig.add_subplot(526)
    ax6 = function(data_matched, data_entd, distance, group, 6+corr)

    ax7 = fig.add_subplot(527)
    ax7 = function(data_matched, data_entd, distance, group, 7+corr)

    ax8 = fig.add_subplot(528)
    ax8 = function(data_matched, data_entd, distance, group, 8+corr)

    ax9 = fig.add_subplot(529)
    ax9 = function(data_matched, data_entd, distance, group, 9+corr)

    if group == 'niveau_vie_decile':
        ax10 = fig.add_subplot(5,2,10)
        ax10 = function(data_matched, data_entd, distance, group, 10+corr)


def histogram_distance_annuelle_group(data_matched, data_entd, distance, group):
    list_values_matched = []
    list_values_entd = []
    list_keys = []
    if group == 'niveau_vie_decile':
        min_element = 1
        max_element = 11
    if group == 'tuu':
        min_element = 0
        max_element = 9
    for element in range(min_element,max_element):
        data_matched_group = data_matched.query('{} == {}'.format(group, element))
        distance_matched = (
            sum(data_matched_group[distance] * data_matched_group['pondmen']) /
            data_matched_group['pondmen'].sum()
            )
        list_values_matched.append(distance_matched)
    
        data_entd_group = data_entd.query('{} == {}'.format(group, element))
        distance_entd = (
            sum(data_entd_group[distance] * data_entd_group['pondmen']) /
            data_entd_group['pondmen'].sum()
            )

        list_values_entd.append(distance_entd)
        list_keys.append('{}'.format(element))

    histogrammes(list_keys, list_values_matched, list_values_entd)

    return plt


def histogram_distribution_distance_annuelle(data_matched, data_entd, distance):
    list_values_matched = []
    list_values_entd = []
    list_keys = []

    data_matched[distance] = data_matched[distance].astype(float)
    data_matched['{}_racine'.format(distance)] = (data_matched[distance]) ** (0.5)
    distance_essence_racine_max_matched = data_matched['{}_racine'.format(distance)].max()

    data_entd[distance] = data_entd[distance].astype(float)
    data_entd['{}_racine'.format(distance)] = (data_entd[distance]) ** (0.5)
    distance_essence_racine_max_entd = data_entd['{}_racine'.format(distance)].max()

    distance_essence_racine_max = max(distance_essence_racine_max_matched, distance_essence_racine_max_entd)
    data_matched['{}_groupe'.format(distance)] = (data_matched['{}_racine'.format(distance)] / distance_essence_racine_max).round(decimals = 1)
    data_entd['{}_groupe'.format(distance)] = (data_entd['{}_racine'.format(distance)] / distance_essence_racine_max).round(decimals = 1)

    for i in range(0,11):
        j = float(i)/10
        part_matched = (
            sum(data_matched.query('{}_groupe == {}'.format(distance, j))['pondmen']) /
            data_matched['pondmen'].sum()
            )
        list_values_matched.append(part_matched)
    
    for i in range(0,11):
        j = float(i)/10
        part_entd = (
            sum(data_entd.query('{}_groupe == {}'.format(distance, j))['pondmen']) /
            data_entd['pondmen'].sum()
            )

        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)
    
    return plt


def histogram_distribution_distance_annuelle_group(data_matched, data_entd, distance, group, element):
    data_matched[distance] = data_matched[distance].astype(float)
    data_matched['{}_racine'.format(distance)] = (data_matched[distance]) ** (0.5)
    distance_essence_racine_max_matched = data_matched['{}_racine'.format(distance)].max()

    data_entd[distance] = data_entd[distance].astype(float)
    data_entd['{}_racine'.format(distance)] = (data_entd[distance]) ** (0.5)
    distance_essence_racine_max_entd = data_entd['{}_racine'.format(distance)].max()

    distance_essence_racine_max = max(distance_essence_racine_max_matched, distance_essence_racine_max_entd)
    data_matched['{}_groupe'.format(distance)] = (data_matched['{}_racine'.format(distance)] / distance_essence_racine_max).round(decimals = 1)
    data_entd['{}_groupe'.format(distance)] = (data_entd['{}_racine'.format(distance)] / distance_essence_racine_max).round(decimals = 1)

    list_values_matched = []
    list_values_entd = []
    list_keys = []
    data_matched_decile = data_matched.query('{} == {}'.format(group, element))
    for i in range(0,11):
        j = float(i)/10
        part_matched = (
            sum(data_matched_decile.query('{}_groupe == {}'.format(distance, j))['pondmen']) /
            data_matched_decile['pondmen'].sum()
            )
        list_values_matched.append(part_matched)
    
    data_entd_decile = data_entd.query('{} == {}'.format(group, element))
    for i in range(0,11):
        j = float(i)/10
        part_entd = (
            sum(data_entd_decile.query('{}_groupe == {}'.format(distance, j))['pondmen']) /
            data_entd_decile['pondmen'].sum()
            )

        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)

    return plt


histogram_distance_annuelle_group(data_matched_distance, data_entd, 'distance', 'tuu')
histogram_distribution_distance_annuelle(data_matched_distance, data_entd)
plots_by_group(histogram_distribution_distance_annuelle_group, data_matched_random, 'distance_diesel', 'tuu')
