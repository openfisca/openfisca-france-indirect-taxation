# -*- coding: utf-8 -*-

# Dans ce script on crée deux fichiers .csv pour les deux bases de données
# homogènes, qui seront ensuite importées dans R pour l'appariement. On effectue
# au préalable les corrections nécessaires pour avoir des bases homogènes.


from __future__ import division

import os
import pkg_resources


from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_2_homogenize_variables import \
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
        'dip14pr', 'mchof', 'mchof_d', 'mfac_eau1_d', 'mfac_eg1_d',
        'mloy_d', 'nactifs', 'nbh1', 'nenfants', 'poste_coicop_4511',
        'poste_coicop_451', 'poste_coicop_452', 'poste_coicop_453',
        'situacj', 'situapr', 'tau', 'tuu', 'typmen'
        ]
    
    for variable in variables_to_drop_bdf:
        del data_bdf[variable]

    variables_to_drop_enl = [
        'amr', 'cataeu', 'coml13', 'coml3', 'cs42cj', 'cs42pr',
        'dip14pr', 'gmoy1', 'gtt1', 'gvit1', 'gvit1b', 'mchof_d', 'mfac_eau1_d',
        'mloy_d', 'nactifs', 'nbh1', 'nenfants',
        'poste_coicop_451', 'poste_coicop_452', 'poste_coicop_453',
        'situacj', 'situapr', 'tau', 'tuu'
        ]

    for variable in variables_to_drop_enl:
        del data_enl[variable]

    return data_enl, data_bdf


if __name__ == "__main__":
    data = clean_data()    
    data_enl = data[0]
    data_bdf = data[1]

    # Sauvegarde des données dans des fichiers .csv
    data_enl.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'matching', 'data_matching_enl.csv'), sep = ',')
    data_bdf.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'matching', 'data_matching_bdf.csv'), sep = ',')
