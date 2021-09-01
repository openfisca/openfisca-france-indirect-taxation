# -*- coding: utf-8 -*-

"""Création deux fichiers csv pour les deux bases de données homogènes BDF et ENL.
Ils seront ensuite importées dans R pour l'appariement.
On effectue au préalable les corrections nécessaires pour avoir des bases homogènes.
"""

import os


from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_2_homogenize_variables import (
    create_niveau_vie_quantiles)
from openfisca_france_indirect_taxation.utils import assets_directory


def clean_data():
    data_enl, data_bdf = create_niveau_vie_quantiles()
    data_enl.drop(
        columns = [
            'amr', 'cataeu', 'coml11', 'coml12', 'cs42cj', 'cs42pr',
            'gmoy1', 'gtt1', 'mchof_d', 'mfac_eau1_d',
            'mloy_d', 'nbh1', 'situacj', 'situapr', 'tau', 'tuu'
            ],
        inplace = True
        )
    data_bdf.drop(
        columns = [
            'amr', 'cataeu', 'chaufp', 'cs42cj', 'cs42pr', 'decuc', 'dip14cj',
            'mchof', 'mchof_d', 'mfac_eau1_d', 'mfac_eg1_d',
            'mloy_d', 'nbh1', 'poste_04_5_1_1_1_a', 'poste_04_5_1_1_1_b',
            'poste_04_5_2_1_1', 'poste_04_5_5_1_1',
            'situacj', 'situapr', 'tau', 'tuu', 'typmen'
            ],
        inplace = True
        )
    return data_enl, data_bdf


def create_donation_classes():
    data_enl, data_bdf = create_niveau_vie_quantiles()

    def create_donation_classes_(data):
        # Classes based on niveau_vie_decile and aides_logement
        data['donation_class_1'] = 0
        for i in range(1, 11):
            if i < 5:
                for j in [0, 1]:
                    data.loc[(data['aides_logement'] == j) & (data['niveau_vie_decile'] == i), 'donation_class_1'] = '{}_{}'.format(i, j)
            else:
                data.loc[data['niveau_vie_decile'] == i, 'donation_class_1'] = '{}'.format(i)

        # Classes based on niveau_vie_decile, aides_logement, and log_indiv
        data['donation_class_2'] = 0
        for i in range(1, 11):
            for log in [0, 1]:
                if i < 5:
                    for j in [0, 1]:
                        data.loc[
                            (data['aides_logement'] == j) & (data['niveau_vie_decile'] == i) & (data['log_indiv'] == log),
                            'donation_class_2'
                            ] = '{}_{}_{}'.format(i, log, j)
                else:
                    data.loc[
                        (data['niveau_vie_decile'] == i) & (data['log_indiv'] == log),
                        'donation_class_2'
                        ] = '{}_{}'.format(i, log)

        data['donation_class_3'] = 0
        for i in range(1, 11):
            for strate in range(0, 5):
                if i < 5:
                    for j in [0, 1]:
                        data.loc[
                            (data['aides_logement'] == j) & (data['niveau_vie_decile'] == i) & (data['strate'] == strate),
                            'donation_class_3'
                            ] = '{}_{}_{}'.format(i, strate, j)
                else:
                    data.loc[
                        (data['niveau_vie_decile'] == i) & (data['strate'] == strate),
                        'donation_class_3'
                        ] = '{}_{}'.format(i, strate)

        data['donation_class_4'] = 0
        for i in range(1, 11):
            for bat_1 in [0, 1]:
                for bat_2 in [0, 1]:
                    if i < 5:
                        for j in [0, 1]:
                            data.loc[
                                (data['aides_logement'] == j) & (data['niveau_vie_decile'] == i)
                                & (data['bat_av_49'] == bat_1) & (data['bat_49_74'] == bat_2),
                                'donation_class_4'
                                ] = '{}_{}_{}_{}'.format(i, bat_1, bat_2, j)
                    else:
                        data.loc[
                            (data['niveau_vie_decile'] == i) & (data['bat_av_49'] == bat_1)
                            & (data['bat_49_74'] == bat_2),
                            'donation_class_4'
                            ] = '{}_{}_{}'.format(i, bat_1, bat_2)

        return data.copy()

    return create_donation_classes_(data_enl), create_donation_classes_(data_bdf)


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


def prepare_bdf_enl_matching_data():
    data_enl, data_bdf = create_donation_classes()
    # dico = check_donation_classes_size(data_enl, 'donation_class_4')

    # Sauvegarde des données dans des fichiers .csv
    data_enl.to_csv(os.path.join(assets_directory, 'matching', 'matching_enl', 'data_matching_enl.csv'), sep = ',')
    data_bdf.to_csv(os.path.join(assets_directory, 'matching', 'matching_enl', 'data_matching_bdf.csv'), sep = ',')
