

# Dans ce script on utilise des histogrammes pour comparer la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

import os
import pkg_resources
import pandas as pd

from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes

# Importation des bases de données appariées et de la base de référence erfs
default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)


data_erfs = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'matching_erfs',
        'data_matching_erfs.csv'
        ), sep =',', decimal = '.'
    )


data_matched_rank = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'matching_erfs',
        'data_matched_rank.csv'
        ), sep =',', decimal = '.'
    )


def histogram_revdecm(data_matched, data_erfs):
    list_values_matched = []
    list_values_erfs = []
    list_keys = []
    for i in [.01, .02, .04, .06, .08, .1, .2, .35, .5, .65, .8, .95, .99]:
        list_values_matched.append(data_matched['revdecm'].quantile(i))
        list_values_erfs.append(data_erfs['revdecm'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_matched, list_values_erfs, 'Matched', 'ERFS')

    return figure


histogram_revdecm(data_matched_rank, data_erfs)
