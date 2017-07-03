# -*- coding: utf-8 -*-

from __future__ import division


# We compare distribution of variables in the two surveys and assess if they need a correction or not to be homogenous

from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_2_homogenize_variables import \
    homogenize_variables_definition_bdf_enl

from openfisca_survey_manager.matching import nnd_hotdeck_using_rpy2

data = homogenize_variables_definition_bdf_enl()    
data_enl = data[0]
data_bdf = data[1]


nnd_hotdeck_using_rpy2(receiver = data_enl, donor = data_bdf, matching_variables = 'revtot')
