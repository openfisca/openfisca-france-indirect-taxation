# -*- coding: utf-8 -*-

# Dans ce script on crée deux fichiers .csv pour les deux bases de données
# homogènes, qui seront ensuite importées dans R pour l'appariement. On effectue
# au préalable les corrections nécessaires pour avoir des bases homogènes.


import os
import pkg_resources


from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_2_homogenize_variables import \
    create_niveau_vie_quantiles

assets_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )


def clean_data():
    data = create_niveau_vie_quantiles()
    data_enl = data[0]
    data_bdf = data[1]

    variables_to_drop_bdf = [
        'amr', 'cataeu', 'chaufp', 'cs42cj', 'cs42pr', 'decuc', 'dip14cj',
        'mchof', 'mchof_d', 'mfac_eau1_d', 'mfac_eg1_d',
        'mloy_d', 'nbh1', 'poste_04_5_1_1_1_a', 'poste_04_5_1_1_1_b',
        'poste_04_5_2_1_1', 'poste_04_5_5_1_1',
        'situacj', 'situapr', 'tau', 'tuu', 'typmen'
        ]

    for variable in variables_to_drop_bdf:
        del data_bdf[variable]

    variables_to_drop_enl = [
        'amr', 'cataeu', 'coml11', 'coml12', 'cs42cj', 'cs42pr',
        'gmoy1', 'gtt1', 'mchof_d', 'mfac_eau1_d',
        'mloy_d', 'nbh1', 'situacj', 'situapr', 'tau', 'tuu'
        ]

    for variable in variables_to_drop_enl:
        del data_enl[variable]

    return data_enl, data_bdf


def create_donation_classes():
    for base in [0, 1]:
        data = create_niveau_vie_quantiles()[base]

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
                                ] = '{}_{}_{}'.format(i, bat_1, bat_2, j)
                    else:
                        data.loc[
                            (data['niveau_vie_decile'] == i) & (data['bat_av_49'] == bat_1)
                            & (data['bat_49_74'] == bat_2),
                            'donation_class_4'
                            ] = '{}_{}_{}'.format(i, bat_1, bat_2)

        if base == 0:
            data_enl = data.copy()
        else:
            data_bdf = data.copy()

    return data_enl, data_bdf


def check_donation_classes_size(data, donation_class):
    elements_in_dc = data[donation_class].tolist()

    dict_dc = dict()
    for element in elements_in_dc:
        dict_dc['{}'.format(element)] = 1

    list_dc = list(dict_dc.keys())

    dict_dc_taille = dict()
    for element in list_dc:
        dict_dc_taille[element] = len(data_enl[data_enl[donation_class] == element])

    return dict_dc_taille

# dico = check_donation_classes_size(data_enl, 'donation_class_4')


if __name__ == "__main__":
    data = create_donation_classes()
    data_enl = data[0]
    data_bdf = data[1]

    # Sauvegarde des données dans des fichiers .csv
    data_enl.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'matching', 'data_matching_enl.csv'), sep = ',')
    data_bdf.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'matching', 'data_matching_bdf.csv'), sep = ',')
