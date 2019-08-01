

# Dans ce script on utilise des histogrammes pour comparer la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes
import os
import pkg_resources
import pandas as pd
import seaborn

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import save_dataframe_to_graph

seaborn.set_palette(seaborn.color_palette("Set2", 12))


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


def histogram_froid_4_criteres_niveau_vie_decile(data_matched, data_enl, category):
    list_values_matched = []
    list_values_enl = []
    list_keys = []
    if category == 'niveau_vie_decile':
        i_max = 11
    if category == 'tuu':
        i_max = 9
    else:
        print('Wrong category')
    for i in range(1, i_max):
        data_enl_decile = data_enl.query('{} == {}'.format(category, i))
        data_matched_decile = data_matched.query('{} == {}'.format(category, i))

        data_enl_decile['froid_2_criteres'] = (
            data_enl_decile['froid_cout'] + data_enl_decile['froid_impaye']
            - (data_enl_decile['froid_cout'] * data_enl_decile['froid_impaye'])
            )
        data_enl_decile['froid_2_criteres_bis'] = (
            data_enl_decile['froid_installation'] + data_enl_decile['froid_isolation']
            - (data_enl_decile['froid_installation'] * data_enl_decile['froid_isolation'])
            )
        data_enl_decile['froid_4_criteres'] = (
            data_enl_decile['froid_2_criteres'] + data_enl_decile['froid_2_criteres_bis']
            - (data_enl_decile['froid_2_criteres'] * data_enl_decile['froid_2_criteres_bis'])
            )

        data_matched_decile['froid_2_criteres'] = (
            data_matched_decile['froid_cout'] + data_matched_decile['froid_impaye']
            - (data_matched_decile['froid_cout'] * data_matched_decile['froid_impaye'])
            )
        data_matched_decile['froid_2_criteres_bis'] = (
            data_matched_decile['froid_installation'] + data_matched_decile['froid_isolation']
            - (data_matched_decile['froid_installation'] * data_matched_decile['froid_isolation'])
            )
        data_matched_decile['froid_4_criteres'] = (
            data_matched_decile['froid_2_criteres'] + data_matched_decile['froid_2_criteres_bis']
            - (data_matched_decile['froid_2_criteres'] * data_matched_decile['froid_2_criteres_bis'])
            )

        part_enl = (
            100
            * sum(data_enl_decile['pondmen'] * (data_enl_decile['froid_4_criteres'] == 1))
            / sum(data_enl_decile['pondmen'])
            )
        part_matched = (
            100
            * sum(data_matched_decile['pondmen'] * (data_matched_decile['froid_4_criteres'] == 1))
            / sum(data_matched_decile['pondmen'])
            )

        list_values_matched.append(part_matched)
        list_values_enl.append(part_enl)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_matched, list_values_enl, 'Matched', 'ENL')

    values = {'keys': list_keys, 'enl': list_values_enl, 'matched': list_values_matched}
    dataframe = pd.DataFrame.from_dict(values)
    dataframe = dataframe.set_index('keys')

    return figure, dataframe


for category in ['niveau_vie_decile', 'tuu']:
    dataframe = histogram_froid_4_criteres_niveau_vie_decile(data_matched_rank, data_enl, category)[1]
    save_dataframe_to_graph(
        dataframe, 'Matching/froid_4_criteres_{}.csv'.format(category)
        )
