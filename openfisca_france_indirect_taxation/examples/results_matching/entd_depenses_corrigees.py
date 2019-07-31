

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

default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )

data_matched = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'matching_entd',
        'data_matched_final.csv'
        ), sep =',', decimal = '.'
    )


def data_histogram_distribution_depenses_annuelle(data_matched):
    list_values_poste = []
    list_values_depenses_carburants = []
    list_keys = []
    for i in [.05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95]:
        list_values_poste.append(data_matched['poste_07_2_2_1_1'].quantile(i))
        list_values_depenses_carburants.append(data_matched['depenses_carburants_corrigees_entd'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_poste, list_values_depenses_carburants, 'Ex ante', 'Ex post')

    values = {'keys': list_keys, 'Ex ante': list_values_poste, 'Ex post': list_values_depenses_carburants}
    dataframe = pd.DataFrame.from_dict(values)
    dataframe = dataframe.set_index('keys')

    return figure, dataframe


dataframe = data_histogram_distribution_depenses_annuelle(data_matched)[1]
save_dataframe_to_graph(
    dataframe, 'Matching/distributions_depenses_carburants_ex_ante_ex_post.csv'
    )
