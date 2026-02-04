# -*- coding: utf-8 -*-

# Dans ce script on crée deux fichiers .csv pour les deux bases de données
# homogènes, qui seront ensuite importées dans R pour l'appariement. On effectue
# au préalable les corrections nécessaires pour avoir des bases homogènes.

import os
import pandas as pd

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_2_homogenize_variables import \
    create_niveau_vie_quantiles
from openfisca_france_indirect_taxation.utils import assets_directory


def clean_data(year_data):
    data_bdf, data_entd = create_niveau_vie_quantiles(year_data)
    data_bdf = data_bdf.apply(pd.to_numeric, errors='coerce').fillna(0)
    data_entd = data_entd.apply(pd.to_numeric, errors='coerce').fillna(0)
    return data_bdf, data_entd


def create_donation_classes(year_data):
    data_bdf, data_entd = clean_data(year_data)

    def create_donation_classes_(data):
        # Classes based on niveau_vie_decile and aides_logement (oas possible avec EMP 2019)
        # data['donation_class_1'] = 0
        # for i in range(1, 11):
        #     if i < 5:
        #         for j in [0, 1]:
        #             data.loc[(data['aides_logement'] == j) & (data['niveau_vie_decile'] == i), 'donation_class_1'] = '{}_{}'.format(i, j)
        #     else:
        #         data.loc[data['niveau_vie_decile'] == i, 'donation_class_1'] = '{}'.format(i)

        # Classes based on niveau_vie_decile and rural
        data['donation_class_3'] = 0
        data['donation_class_3'] = data.apply(lambda row: '{}_{}'.format(int(row['niveau_vie_decile']), int(row['rural'])), axis=1)
        return data.copy()

    return create_donation_classes_(data_bdf), create_donation_classes_(data_entd)


def check_donation_classes_size(data, donation_class):
    elements_in_dc = data[donation_class].tolist()

    dict_dc = dict()
    for element in elements_in_dc:
        dict_dc['{}'.format(element)] = 1

    list_dc = list(dict_dc.keys())

    dict_dc_taille = dict()
    for element in list_dc:
        dict_dc_taille[element] = len(data[data[donation_class] == element])

    return dict_dc_taille


def prepare_bdf_entd_matching_data(year_data):
    data_bdf, data_entd = create_donation_classes(year_data)
    matching_entd_directory = os.path.join(
        assets_directory,
        'matching',
        'matching_entd'
        )
    data_entd.to_csv(os.path.join(matching_entd_directory, 'data_matching_entd.csv'), sep = ',')
    data_bdf.to_csv(os.path.join(matching_entd_directory, 'data_matching_bdf.csv'), sep = ',')
