# -*- coding: utf-8 -*-

# Dans ce script on crée deux fichiers .csv pour les deux bases de données
# homogènes, qui seront ensuite importées dans R pour l'appariement. On effectue
# au préalable les corrections nécessaires pour avoir des bases homogènes.


import os


from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_2_homogenize_variables import \
    create_niveau_vie_quantiles
from openfisca_france_indirect_taxation.utils import assets_directory


def clean_data():
    data_entd, data_bdf = create_niveau_vie_quantiles()
    data_entd = data_entd.fillna(0)
    data_bdf = data_bdf.fillna(0)
    return data_entd, data_bdf


def create_donation_classes():
    data_entd, data_bdf = clean_data()

    def create_donation_classes_(data):
        # Classes based on niveau_vie_decile and aides_logement
        data['donation_class_1'] = 0
        for i in range(1, 11):
            if i < 5:
                for j in [0, 1]:
                    data.loc[(data['aides_logement'] == j) & (data['niveau_vie_decile'] == i), 'donation_class_1'] = '{}_{}'.format(i, j)
            else:
                data.loc[data['niveau_vie_decile'] == i, 'donation_class_1'] = '{}'.format(i)

        data['donation_class_3'] = 0
        for i in range(1, 11):
            for rur in [0, 1]:
                data.loc[
                    (data['niveau_vie_decile'] == i) & (data['rural'] == rur),
                    'donation_class_3'
                    ] = '{}_{}'.format(i, rur)

        return data.copy()

    return create_donation_classes_(data_entd), create_donation_classes_(data_bdf)


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


def prepare_bdf_entd_matching_data():
    data_entd, data_bdf = create_donation_classes()
    matching_entd_directory = os.path.join(
        assets_directory,
        'matching',
        'matching_entd'
        )
    data_entd.to_csv(os.path.join(matching_entd_directory, 'data_matching_entd.csv'), sep = ',')
    data_bdf.to_csv(os.path.join(matching_entd_directory, 'data_matching_bdf.csv'), sep = ',')
