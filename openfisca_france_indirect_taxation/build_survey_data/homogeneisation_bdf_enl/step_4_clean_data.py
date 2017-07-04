# -*- coding: utf-8 -*-

# Dans ce script on crée deux fichiers .csv pour les deux bases de données
# homogènes, qui seront ensuite importées dans R pour l'appariement. On effectue
# au préalable les corrections nécessaires pour avoir des bases homogènes.


from __future__ import division

import os
import pkg_resources


from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_2_homogenize_variables import \
    homogenize_variables_definition_bdf_enl

assets_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )


def clean_data():
    data = homogenize_variables_definition_bdf_enl()    
    data_enl = data[0]
    data_bdf = data[1]
    
    # Suppression des outliers
    data_bdf = data_bdf.query('part_energies_revtot_before < 0.5')
    data_enl = data_enl.query('part_energies_revtot_after < 0.5')

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
