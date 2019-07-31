

# Dans ce script on utilise des histogrammes pour comparer la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

import os
import pkg_resources
import pandas as pd


from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes, plots_by_group
from openfisca_france_indirect_taxation.examples.utils_example import save_dataframe_to_graph


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


def data_distribution_distance_annuelle_group(data_matched, data_entd, distance, group, element):
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

    values = {'keys': list_keys, 'entd': list_values_entd, 'matched': list_values_matched}
    dataframe = pd.DataFrame.from_dict(values)
    dataframe = dataframe.set_index('keys')

    return dataframe


for i in range(1, 11):
    dataframe = data_distribution_distance_annuelle_group(data_matched_random, data_entd, 'distance', 'niveau_vie_decile', i)
    save_dataframe_to_graph(
        dataframe, 'Matching/distribution_distance_annuelle_decile_{}.csv'.format(i)
        )
