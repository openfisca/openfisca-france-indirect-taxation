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

    
histogram_distance_annuelle(data_matched_distance, data_entd)

    
    
    

    
def histogram_distance_annuelle_niveau_vie_decile(data_matched, data_entd):
    list_values_matched = []
    list_values_entd = []
    list_keys = []
    for i in range(1,11):
        data_entd_decile = data_entd.query('niveau_vie_decile == {}'.format(i))
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))

        part_entd = (
            100 *
            sum(data_entd_decile['pondmen'] * (data_entd_decile['froid'] == 1)) /
            sum(data_entd_decile['pondmen'])
            )
        part_matched = (
            100 *
            sum(data_matched_decile['pondmen'] * (data_matched_decile['froid'] == 1)) /
            sum(data_matched_decile['pondmen'])
            )

        list_values_matched.append(part_matched)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)
    
    return plt

    
    
    
    
    
    
def histogram_froid_niveau_vie_decile(data_matched, data_entd):
    list_values_matched = []
    list_values_entd = []
    list_keys = []
    for i in range(1,11):
        data_entd_decile = data_entd.query('niveau_vie_decile == {}'.format(i))
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))

        part_entd = (
            100 *
            sum(data_entd_decile['pondmen'] * (data_entd_decile['froid'] == 1)) /
            sum(data_entd_decile['pondmen'])
            )
        part_matched = (
            100 *
            sum(data_matched_decile['pondmen'] * (data_matched_decile['froid'] == 1)) /
            sum(data_matched_decile['pondmen'])
            )

        list_values_matched.append(part_matched)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)
    
    return plt


def histogram_froid_cout_niveau_vie_decile(data_matched, data_entd):
    list_values_matched = []
    list_values_entd = []
    list_keys = []
    for i in range(1,11):
        data_entd_decile = data_entd.query('niveau_vie_decile == {}'.format(i))
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))

        part_entd = (
            100 *
            sum(data_entd_decile['pondmen'] * (data_entd_decile['froid_cout'] == 1)) /
            sum(data_entd_decile['pondmen'])
            )
        part_matched = (
            100 *
            sum(data_matched_decile['pondmen'] * (data_matched_decile['froid_cout'] == 1)) /
            sum(data_matched_decile['pondmen'])
            )
    
        list_values_matched.append(part_matched)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)
    
    return plt


def histogram_froid_tuu(data_matched, data_entd):
    list_values_matched = []
    list_values_entd = []
    list_keys = []
    for i in range(1,9):
        data_entd_tuu = data_entd.query('tuu == {}'.format(i))
        data_matched_tuu = data_matched.query('tuu == {}'.format(i))

        part_entd = (
            100 *
            sum(data_entd_tuu['pondmen'] * (data_entd_tuu['froid'] == 1)) /
            sum(data_entd_tuu['pondmen'])
            )
        part_matched = (
            100 *
            sum(data_matched_tuu['pondmen'] * (data_matched_tuu['froid'] == 1)) /
            sum(data_matched_tuu['pondmen'])
            )

        list_values_matched.append(part_matched)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_matched, list_values_entd)
    
    return plt


histogram_froid_niveau_vie_decile(data_matched_distance, data_entd)
histogram_froid_niveau_vie_decile(data_matched_random, data_entd)

histogram_froid_cout_niveau_vie_decile(data_matched_distance, data_entd)
histogram_froid_cout_niveau_vie_decile(data_matched_random, data_entd)

histogram_froid_tuu(data_matched_distance, data_entd)
histogram_froid_tuu(data_matched_random, data_entd)


