

# Dans ce script on utilise des histogrammes pour comparer la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

import os
import pkg_resources
import pandas as pd

from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes

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


def histogram_froid_niveau_vie_decile(data_matched, data_enl):
    list_values_matched = []
    list_values_enl = []
    list_keys = []
    for i in range(1, 11):
        data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))

        part_enl = (
            100
            * sum(data_enl_decile['pondmen'] * (data_enl_decile['froid'] == 1))
            / sum(data_enl_decile['pondmen'])
            )
        part_matched = (
            100
            * sum(data_matched_decile['pondmen'] * (data_matched_decile['froid'] == 1))
            / sum(data_matched_decile['pondmen'])
            )

        list_values_matched.append(part_matched)
        list_values_enl.append(part_enl)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_matched, list_values_enl, 'Matched', 'ENL')

    return figure


def histogram_froid_cout_niveau_vie_decile(data_matched, data_enl):
    list_values_matched = []
    list_values_enl = []
    list_keys = []
    for i in range(1, 11):
        data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
        data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))

        part_enl = (
            100
            * sum(data_enl_decile['pondmen'] * (data_enl_decile['froid_cout'] == 1))
            / sum(data_enl_decile['pondmen'])
            )
        part_matched = (
            100
            * sum(data_matched_decile['pondmen'] * (data_matched_decile['froid_cout'] == 1))
            / sum(data_matched_decile['pondmen'])
            )

        list_values_matched.append(part_matched)
        list_values_enl.append(part_enl)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_matched, list_values_enl, 'Matched', 'ENL')

    return figure


def histogram_froid_tuu(data_matched, data_enl):
    list_values_matched = []
    list_values_enl = []
    list_keys = []
    for i in range(1, 9):
        data_enl_tuu = data_enl.query('tuu == {}'.format(i))
        data_matched_tuu = data_matched.query('tuu == {}'.format(i))

        part_enl = (
            100
            * sum(data_enl_tuu['pondmen'] * (data_enl_tuu['froid'] == 1))
            / sum(data_enl_tuu['pondmen'])
            )
        part_matched = (
            100
            * sum(data_matched_tuu['pondmen'] * (data_matched_tuu['froid'] == 1))
            / sum(data_matched_tuu['pondmen'])
            )

        list_values_matched.append(part_matched)
        list_values_enl.append(part_enl)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_matched, list_values_enl, 'Matched', 'ENL')

    return figure


histogram_froid_niveau_vie_decile(data_matched_distance, data_enl)
histogram_froid_niveau_vie_decile(data_matched_random, data_enl)
histogram_froid_niveau_vie_decile(data_matched_rank, data_enl)

histogram_froid_cout_niveau_vie_decile(data_matched_distance, data_enl)
histogram_froid_cout_niveau_vie_decile(data_matched_random, data_enl)
histogram_froid_cout_niveau_vie_decile(data_matched_rank, data_enl)

histogram_froid_tuu(data_matched_distance, data_enl)
histogram_froid_tuu(data_matched_random, data_enl)
histogram_froid_tuu(data_matched_rank, data_enl)
