# -*- coding: utf-8 -*-

# Dans ce script on crée deux fichiers .csv pour les deux bases de données
# homogènes, qui seront ensuite importées dans R pour l'appariement. On effectue
# au préalable les corrections nécessaires pour avoir des bases homogènes.


import os
import pkg_resources


from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_2_homogenize_variables import \
    create_niveau_vie_quantiles

assets_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )


def clean_data():
    data = create_niveau_vie_quantiles()
    data_entd = data[0]
    data_bdf = data[1]

    variables_to_drop_bdf = [
        ]

    for variable in variables_to_drop_bdf:
        del data_bdf[variable]

    variables_to_drop_entd = [
        ]

    for variable in variables_to_drop_entd:
        del data_entd[variable]

    data_entd = data_entd.fillna(0)
    data_bdf = data_bdf.fillna(0)

    return data_entd, data_bdf


def create_donation_classes():
    for base in [0, 1]:
        data = clean_data()[base]

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

        if base == 0:
            data_entd = data.copy()
        else:
            data_bdf = data.copy()

    return data_entd, data_bdf


def check_donation_classes_size(data, donation_class):
    elements_in_dc = data[donation_class].tolist()

    dict_dc = dict()
    for element in elements_in_dc:
        dict_dc['{}'.format(element)] = 1

    list_dc = list(dict_dc.keys())

    dict_dc_taille = dict()
    for element in list_dc:
        dict_dc_taille[element] = len(data_entd[data_entd[donation_class] == element])

    return dict_dc_taille


if __name__ == "__main__":
    data = create_donation_classes()
    data_entd = data[0]
    data_bdf = data[1]

    # Sauvegarde des données dans des fichiers .csv
    data_entd.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'matching', 'matching_entd', 'data_matching_entd.csv'), sep = ',')
    data_bdf.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'matching', 'matching_entd', 'data_matching_bdf.csv'), sep = ',')
