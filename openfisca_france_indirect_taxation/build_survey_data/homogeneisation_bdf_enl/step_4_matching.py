# -*- coding: utf-8 -*-
from __future__ import division

import os
import pkg_resources


from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_2_homogenize_variables import \
    homogenize_variables_definition_bdf_enl

#from openfisca_survey_manager.matching import nnd_hotdeck_using_rpy2

#nnd_hotdeck_using_rpy2(receiver = data_enl, donor = data_bdf, matching_variables = 'revtot')

assets_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )

data = homogenize_variables_definition_bdf_enl()    
data_enl = data[0]
data_bdf = data[1]


# Réduit la taille des données pour éviter les erreurs de mémoire
data_enl = data_enl[0:10000]
data_bdf = data_bdf[0:10000]

data_enl['revtot'] = data_enl['revtot'].astype(float)
data_bdf['revtot'].astype(float, inplace = True)
data_enl = data_enl.query('revtot > 0')
data_bdf = data_bdf.query('revtot > 0')

data_enl['part_energies_revenu'] = (
    data_enl['poste_coicop_451']
    + data_enl['poste_coicop_452'] + data_enl['poste_coicop_453']
    ) / data_enl['revtot']
data_bdf['part_energies_revtot'] = (
    data_bdf['poste_coicop_451']
    + data_bdf['poste_coicop_452'] + data_bdf['poste_coicop_453']
    ) / data_bdf['revtot']

data_enl.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
    'matching', 'data_matching_enl_small.csv'), sep = ',')
data_bdf.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
    'matching', 'data_matching_bdf_small.csv'), sep = ',')
