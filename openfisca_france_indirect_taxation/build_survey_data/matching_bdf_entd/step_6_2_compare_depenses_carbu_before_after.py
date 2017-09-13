from __future__ import division

import os
import pkg_resources
import pandas as pd

from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes


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

    
def histogram_depenses_annuelle_group(data_matched, group):
    list_values_poste = []
    list_values_depenses_carburants = []
    list_keys = []
    if group == 'niveau_vie_decile':
        min_element = 1
        max_element = 11
    if group == 'tuu':
        min_element = 0
        max_element = 9
    for element in range(min_element,max_element):
        data_matched_group = data_matched.query('{} == {}'.format(group, element))
        poste = (
            sum(data_matched_group['poste_07_2_2_1_1'] * data_matched_group['pondmen']) /
            data_matched_group['pondmen'].sum()
            )
        list_values_poste.append(poste)
    
        data_matched_group = data_matched.query('{} == {}'.format(group, element))
        depenses_carburants = (
            sum(data_matched_group['depenses_carburants'] * data_matched_group['pondmen']) /
            data_matched_group['pondmen'].sum()
            )

        list_values_depenses_carburants.append(depenses_carburants)
        list_keys.append('{}'.format(element))

    figure = histogrammes(list_keys, list_values_poste, list_values_depenses_carburants, 'Ex ante', 'Ex post')

    return figure


def histogram_distribution_depenses_annuelle(data_matched):
    list_values_poste = []
    list_values_depenses_carburants = []
    list_keys = []
    for i in [.05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95]:
        list_values_poste.append(data_matched['poste_07_2_2_1_1'].quantile(i))
        list_values_depenses_carburants.append(data_matched['depenses_carburants'].quantile(i))
        list_keys.append('{}'.format(i)) 

    figure = histogrammes(list_keys, list_values_poste, list_values_depenses_carburants, 'Ex ante', 'Ex post')

    return figure
    
    
histogram_depenses_annuelle_group(data_matched, 'niveau_vie_decile')
histogram_distribution_depenses_annuelle(data_matched)
