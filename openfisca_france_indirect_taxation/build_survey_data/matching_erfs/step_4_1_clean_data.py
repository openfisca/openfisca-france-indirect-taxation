# -*- coding: utf-8 -*-


'''Prépapration de deux fichiers .csv homogénéiser pour l'appariement via R de BDF et ERFS
'''


import os


from openfisca_france_indirect_taxation.build_survey_data.matching_erfs.step_2_homogenize_variables import homogenize_definitions
from openfisca_france_indirect_taxation.utils import assets_directory


def create_donation_classes(year_data):
    for base in [0, 1]:
        data = homogenize_definitions(year_data)[base]

        # Classes based on niveau_vie_decile and aides_logement
        data['donation_class_1'] = data['nactifs']
        data.loc[data['nactifs'] > 2, 'nactifs'] = 3

        if base == 0:
            data_erfs = data
        else:
            data_bdf = data

    return data_erfs, data_bdf


def prepare_bdf_erfs_matching_data(year_data):
    data_erfs, data_bdf = create_donation_classes(year_data)
    data_erfs.to_csv(os.path.join(assets_directory, 'matching', 'matching_erfs', 'data_matching_erfs.csv'), sep = ',')
    data_bdf.to_csv(os.path.join(assets_directory, 'matching', 'matching_erfs', 'data_matching_bdf.csv'), sep = ',')
