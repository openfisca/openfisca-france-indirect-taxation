

# Dans ce script on utilise des histogrammes pour comparer la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

import os
import pandas as pd
import seaborn


from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes, plots_by_group
from openfisca_france_indirect_taxation.utils import assets_directory


seaborn.set_palette(seaborn.color_palette("Set2", 12))


# Importation des bases de données appariées et de la base de référence entd

data_entd = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matching_entd.csv'
        ), sep =',', decimal = '.'
    )


data_matched_distance = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matched_distance.csv'
        ), sep =',', decimal = '.'
    )


data_matched_random = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matched_random.csv'
        ), sep =',', decimal = '.'
    )

data_matched = data_matched_distance.copy()


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
    for element in range(min_element, max_element):
        data_matched_group = data_matched.query('{} == {}'.format(group, element))
        distance_matched = (
            sum(data_matched_group[distance] * data_matched_group['pondmen'])
            / data_matched_group['pondmen'].sum()
            )
        list_values_matched.append(distance_matched)

        data_entd_group = data_entd.query('{} == {}'.format(group, element))
        distance_entd = (
            sum(data_entd_group[distance] * data_entd_group['pondmen'])
            / data_entd_group['pondmen'].sum()
            )

        list_values_entd.append(distance_entd)
        list_keys.append('{}'.format(element))

    figure = histogrammes(list_keys, list_values_matched, list_values_entd, 'Matched', 'ENTD')

    return figure


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

    for i in range(0, 11):
        j = float(i) / 10
        part_matched = (
            sum(data_matched.query('{}_groupe == {}'.format(distance, j))['pondmen'])
            / data_matched['pondmen'].sum()
            )
        list_values_matched.append(part_matched)

    for i in range(0, 11):
        j = float(i) / 10
        part_entd = (
            sum(data_entd.query('{}_groupe == {}'.format(distance, j))['pondmen'])
            / data_entd['pondmen'].sum()
            )

        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(j))

    figure = histogrammes(list_keys, list_values_matched, list_values_entd, 'Matched', 'ENTD')

    return figure


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
    for i in range(0, 11):
        j = float(i) / 10
        part_matched = (
            sum(data_matched_decile.query('{}_groupe == {}'.format(distance, j))['pondmen'])
            / data_matched_decile['pondmen'].sum()
            )
        list_values_matched.append(part_matched)

    data_entd_decile = data_entd.query('{} == {}'.format(group, element))
    for i in range(0, 11):
        j = float(i) / 10
        part_entd = (
            sum(data_entd_decile.query('{}_groupe == {}'.format(distance, j))['pondmen'])
            / data_entd_decile['pondmen'].sum()
            )

        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(j))

    figure = histogrammes(list_keys, list_values_matched, list_values_entd, 'Matched', 'ENTD')

    return figure


histogram_distance_annuelle_group(data_matched_distance, data_entd, 'distance', 'niveau_vie_decile')
histogram_distribution_distance_annuelle(data_matched_distance, data_entd, 'distance')
plots_by_group(histogram_distribution_distance_annuelle_group, data_matched_distance, data_entd, 'distance_diesel', 'niveau_vie_decile')
