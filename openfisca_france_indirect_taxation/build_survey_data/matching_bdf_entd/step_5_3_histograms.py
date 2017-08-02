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


def plots_by_decile(function, data_matched):    
    fig = plt.figure()
    
    ax1 = fig.add_subplot(521)
    ax1 = function(data_matched, data_entd, 1)
    
    ax2 = fig.add_subplot(522)
    ax2 = function(data_matched, data_entd, 2)
    
    ax3 = fig.add_subplot(523)
    ax3 = function(data_matched, data_entd, 3)
    
    ax4 = fig.add_subplot(524)
    ax4 = function(data_matched, data_entd, 4)

    ax5 = fig.add_subplot(525)
    ax5 = function(data_matched, data_entd, 5)
    
    ax6 = fig.add_subplot(526)
    ax6 = function(data_matched, data_entd, 6)

    ax7 = fig.add_subplot(527)
    ax7 = function(data_matched, data_entd, 7)

    ax8 = fig.add_subplot(528)
    ax8 = function(data_matched, data_entd, 8)

    ax9 = fig.add_subplot(529)
    ax9 = function(data_matched, data_entd, 9)
    
    ax10 = fig.add_subplot(5,2,10)
    ax10 = function(data_matched, data_entd, 10)


def plots_by_tuu(function, data_matched):    
    fig = plt.figure()

    ax1 = fig.add_subplot(521)
    ax1 = function(data_matched, data_entd, 0)
    
    ax2 = fig.add_subplot(522)
    ax2 = function(data_matched, data_entd, 1)
    
    ax3 = fig.add_subplot(523)
    ax3 = function(data_matched, data_entd, 2)
    
    ax4 = fig.add_subplot(524)
    ax4 = function(data_matched, data_entd, 3)

    ax5 = fig.add_subplot(525)
    ax5 = function(data_matched, data_entd, 4)
    
    ax6 = fig.add_subplot(526)
    ax6 = function(data_matched, data_entd, 5)

    ax7 = fig.add_subplot(527)
    ax7 = function(data_matched, data_entd, 6)

    ax8 = fig.add_subplot(528)
    ax8 = function(data_matched, data_entd, 7)

    ax9 = fig.add_subplot(529)
    ax9 = function(data_matched, data_entd, 8)


def histogram_distance_annuelle(data_matched, data_entd):
    list_values_matched = []
    list_values_entd = []
    list_keys = []

    data_matched['distance'] = data_matched['distance'].astype(float)
    data_matched['distance_racine'] = (data_matched['distance']) ** (0.5)
    distance_racine_max_matched = data_matched['distance_racine'].max()

    data_entd['distance'] = data_entd['distance'].astype(float)
    data_entd['distance_racine'] = (data_entd['distance']) ** (0.5)
    distance_racine_max_entd = data_entd['distance_racine'].max()

    distance_racine_max = max(distance_racine_max_matched, distance_racine_max_entd)
    data_matched['distance_groupe'] = (data_matched['distance_racine'] / distance_racine_max).round(decimals = 1)
    data_entd['distance_groupe'] = (data_entd['distance_racine'] / distance_racine_max).round(decimals = 1)

    for i in range(0,11):
        j = float(i)/10
        part_matched = (
            sum(data_matched.query('distance_groupe == {}'.format(j))['pondmen']) /
            data_matched['pondmen'].sum()
            )
        list_values_matched.append(part_matched)
    
    for i in range(0,11):
        j = float(i)/10
        part_entd = (
            sum(data_entd.query('distance_groupe == {}'.format(j))['pondmen']) /
            data_entd['pondmen'].sum()
            )

        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)
    
    return plt


def histogram_distance_diesel_annuelle(data_matched, data_entd):
    list_values_matched = []
    list_values_entd = []
    list_keys = []

    data_matched['distance_diesel'] = data_matched['distance_diesel'].astype(float)
    data_matched['distance_diesel_racine'] = (data_matched['distance_diesel']) ** (0.5)
    distance_diesel_racine_max_matched = data_matched['distance_diesel_racine'].max()

    data_entd['distance_diesel'] = data_entd['distance_diesel'].astype(float)
    data_entd['distance_diesel_racine'] = (data_entd['distance_diesel']) ** (0.5)
    distance_diesel_racine_max_entd = data_entd['distance_diesel_racine'].max()

    distance_diesel_racine_max = max(distance_diesel_racine_max_matched, distance_diesel_racine_max_entd)
    data_matched['distance_diesel_groupe'] = (data_matched['distance_diesel_racine'] / distance_diesel_racine_max).round(decimals = 1)
    data_entd['distance_diesel_groupe'] = (data_entd['distance_diesel_racine'] / distance_diesel_racine_max).round(decimals = 1)

    for i in range(0,11):
        j = float(i)/10
        part_matched = (
            sum(data_matched.query('distance_diesel_groupe == {}'.format(j))['pondmen']) /
            data_matched['pondmen'].sum()
            )
        list_values_matched.append(part_matched)
    
    for i in range(0,11):
        j = float(i)/10
        part_entd = (
            sum(data_entd.query('distance_diesel_groupe == {}'.format(j))['pondmen']) /
            data_entd['pondmen'].sum()
            )

        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)
    
    return plt
    

def histogram_distance_essence_annuelle(data_matched, data_entd):
    list_values_matched = []
    list_values_entd = []
    list_keys = []

    data_matched['distance_essence'] = data_matched['distance_essence'].astype(float)
    data_matched['distance_essence_racine'] = (data_matched['distance_essence']) ** (0.5)
    distance_essence_racine_max_matched = data_matched['distance_essence_racine'].max()

    data_entd['distance_essence'] = data_entd['distance_essence'].astype(float)
    data_entd['distance_essence_racine'] = (data_entd['distance_essence']) ** (0.5)
    distance_essence_racine_max_entd = data_entd['distance_essence_racine'].max()

    distance_essence_racine_max = max(distance_essence_racine_max_matched, distance_essence_racine_max_entd)
    data_matched['distance_essence_groupe'] = (data_matched['distance_essence_racine'] / distance_essence_racine_max).round(decimals = 1)
    data_entd['distance_essence_groupe'] = (data_entd['distance_essence_racine'] / distance_essence_racine_max).round(decimals = 1)

    for i in range(0,11):
        j = float(i)/10
        part_matched = (
            sum(data_matched.query('distance_essence_groupe == {}'.format(j))['pondmen']) /
            data_matched['pondmen'].sum()
            )
        list_values_matched.append(part_matched)
    
    for i in range(0,11):
        j = float(i)/10
        part_entd = (
            sum(data_entd.query('distance_essence_groupe == {}'.format(j))['pondmen']) /
            data_entd['pondmen'].sum()
            )

        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)
    
    return plt


def histogram_distance_annuelle_niveau_vie_decile(data_matched, data_entd, decile):
    data_matched['distance'] = data_matched['distance'].astype(float)
    data_matched['distance_racine'] = (data_matched['distance']) ** (0.5)
    distance_racine_max_matched = data_matched['distance_racine'].max()

    data_entd['distance'] = data_entd['distance'].astype(float)
    data_entd['distance_racine'] = (data_entd['distance']) ** (0.5)
    distance_racine_max_entd = data_entd['distance_racine'].max()

    distance_racine_max = max(distance_racine_max_matched, distance_racine_max_entd)
    data_matched['distance_groupe'] = (data_matched['distance_racine'] / distance_racine_max).round(decimals = 1)
    data_entd['distance_groupe'] = (data_entd['distance_racine'] / distance_racine_max).round(decimals = 1)

    list_values_matched = []
    list_values_entd = []
    list_keys = []
    data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(decile))
    for i in range(0,11):
        j = float(i)/10
        part_matched = (
            sum(data_matched_decile.query('distance_groupe == {}'.format(j))['pondmen']) /
            data_matched_decile['pondmen'].sum()
            )
        list_values_matched.append(part_matched)
    
    data_entd_decile = data_entd.query('niveau_vie_decile == {}'.format(decile))
    for i in range(0,11):
        j = float(i)/10
        part_entd = (
            sum(data_entd_decile.query('distance_groupe == {}'.format(j))['pondmen']) /
            data_entd_decile['pondmen'].sum()
            )

        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)

    return plt


def histogram_distance_diesel_annuelle_niveau_vie_decile(data_matched, data_entd, decile):
    data_matched['distance_diesel'] = data_matched['distance_diesel'].astype(float)
    data_matched['distance_diesel_racine'] = (data_matched['distance_diesel']) ** (0.5)
    distance_diesel_racine_max_matched = data_matched['distance_diesel_racine'].max()

    data_entd['distance_diesel'] = data_entd['distance_diesel'].astype(float)
    data_entd['distance_diesel_racine'] = (data_entd['distance_diesel']) ** (0.5)
    distance_diesel_racine_max_entd = data_entd['distance_diesel_racine'].max()

    distance_diesel_racine_max = max(distance_diesel_racine_max_matched, distance_diesel_racine_max_entd)
    data_matched['distance_diesel_groupe'] = (data_matched['distance_diesel_racine'] / distance_diesel_racine_max).round(decimals = 1)
    data_entd['distance_diesel_groupe'] = (data_entd['distance_diesel_racine'] / distance_diesel_racine_max).round(decimals = 1)

    list_values_matched = []
    list_values_entd = []
    list_keys = []
    data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(decile))
    for i in range(0,11):
        j = float(i)/10
        part_matched = (
            sum(data_matched_decile.query('distance_diesel_groupe == {}'.format(j))['pondmen']) /
            data_matched_decile['pondmen'].sum()
            )
        list_values_matched.append(part_matched)
    
    data_entd_decile = data_entd.query('niveau_vie_decile == {}'.format(decile))
    for i in range(0,11):
        j = float(i)/10
        part_entd = (
            sum(data_entd_decile.query('distance_diesel_groupe == {}'.format(j))['pondmen']) /
            data_entd_decile['pondmen'].sum()
            )

        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)

    return plt


def histogram_distance_essence_annuelle_niveau_vie_decile(data_matched, data_entd, decile):
    data_matched['distance_essence'] = data_matched['distance_essence'].astype(float)
    data_matched['distance_essence_racine'] = (data_matched['distance_essence']) ** (0.5)
    distance_essence_racine_max_matched = data_matched['distance_essence_racine'].max()

    data_entd['distance_essence'] = data_entd['distance_essence'].astype(float)
    data_entd['distance_essence_racine'] = (data_entd['distance_essence']) ** (0.5)
    distance_essence_racine_max_entd = data_entd['distance_essence_racine'].max()

    distance_essence_racine_max = max(distance_essence_racine_max_matched, distance_essence_racine_max_entd)
    data_matched['distance_essence_groupe'] = (data_matched['distance_essence_racine'] / distance_essence_racine_max).round(decimals = 1)
    data_entd['distance_essence_groupe'] = (data_entd['distance_essence_racine'] / distance_essence_racine_max).round(decimals = 1)

    list_values_matched = []
    list_values_entd = []
    list_keys = []
    data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(decile))
    for i in range(0,11):
        j = float(i)/10
        part_matched = (
            sum(data_matched_decile.query('distance_essence_groupe == {}'.format(j))['pondmen']) /
            data_matched_decile['pondmen'].sum()
            )
        list_values_matched.append(part_matched)
    
    data_entd_decile = data_entd.query('niveau_vie_decile == {}'.format(decile))
    for i in range(0,11):
        j = float(i)/10
        part_entd = (
            sum(data_entd_decile.query('distance_essence_groupe == {}'.format(j))['pondmen']) /
            data_entd_decile['pondmen'].sum()
            )

        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)

    return plt



def histogram_distance_annuelle_tuu(data_matched, data_entd, element):
    data_matched['distance'] = data_matched['distance'].astype(float)
    data_matched['distance_racine'] = (data_matched['distance']) ** (0.5)
    distance_racine_max_matched = data_matched['distance_racine'].max()

    data_entd['distance'] = data_entd['distance'].astype(float)
    data_entd['distance_racine'] = (data_entd['distance']) ** (0.5)
    distance_racine_max_entd = data_entd['distance_racine'].max()

    distance_racine_max = max(distance_racine_max_matched, distance_racine_max_entd)
    data_matched['distance_groupe'] = (data_matched['distance_racine'] / distance_racine_max).round(decimals = 1)
    data_entd['distance_groupe'] = (data_entd['distance_racine'] / distance_racine_max).round(decimals = 1)

    list_values_matched = []
    list_values_entd = []
    list_keys = []
    data_matched_decile = data_matched.query('tuu == {}'.format(element))
    for i in range(0,11):
        j = float(i)/10
        part_matched = (
            sum(data_matched_decile.query('distance_groupe == {}'.format(j))['pondmen']) /
            data_matched_decile['pondmen'].sum()
            )
        list_values_matched.append(part_matched)
    
    data_entd_decile = data_entd.query('tuu == {}'.format(element))
    for i in range(0,11):
        j = float(i)/10
        part_entd = (
            sum(data_entd_decile.query('distance_groupe == {}'.format(j))['pondmen']) /
            data_entd_decile['pondmen'].sum()
            )

        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    print histogrammes(list_keys, list_values_matched, list_values_entd)

    return plt


histogram_distance_annuelle(data_matched_distance, data_entd)
histogram_distance_diesel_annuelle(data_matched_distance, data_entd)
histogram_distance_essence_annuelle(data_matched_distance, data_entd)

plots_by_decile(histogram_distance_annuelle_niveau_vie_decile, data_matched_random)
plots_by_tuu(histogram_distance_annuelle_tuu, data_matched_random)

plots_by_decile(histogram_distance_diesel_annuelle_niveau_vie_decile, data_matched_random)
plots_by_decile(histogram_distance_essence_annuelle_niveau_vie_decile, data_matched_random)
