# -*- coding: utf-8 -*-

# Dans ce script on crée deux fichiers .csv pour les deux bases de données
# homogènes, qui seront ensuite importées dans R pour l'appariement..


import os
import pkg_resources


from openfisca_france_indirect_taxation.build_survey_data.matching_erfs.step_2_homogenize_variables import \
    homogenize_definitions
from openfisca_france_indirect_taxation.utils import assets_directory


def create_donation_classes():
    for base in [0, 1]:
        data = homogenize_definitions()[base]

        # Classes based on niveau_vie_decile and aides_logement
        data['donation_class_1'] = data['nactifs']
        data.loc[data['nactifs'] > 2, 'nactifs'] = 3

        if base == 0:
            data_erfs = data
        else:
            data_bdf = data

    return data_erfs, data_bdf


data_erfs, data_bdf = create_donation_classes()

# Sauvegarde des données dans des fichiers .csv
data_erfs.to_csv(os.path.join(assets_directory, 'matching', 'matching_erfs', 'data_matching_erfs.csv'), sep = ',')
data_bdf.to_csv(os.path.join(assets_directory, 'matching', 'matching_erfs', 'data_matching_bdf.csv'), sep = ',')
