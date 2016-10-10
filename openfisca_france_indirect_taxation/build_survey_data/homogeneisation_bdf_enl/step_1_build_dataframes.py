# -*- coding: utf-8 -*-

from __future__ import division


import logging
import os
import pandas
import numpy

from matplotlib import pyplot

from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager.surveys import Survey
from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_france_indirect_taxation.build_survey_data.utils \
    import find_nearest_inferior

from openfisca_survey_manager.temporary import TemporaryStore

from openfisca_france_indirect_taxation.build_survey_data.utils \
    import ident_men_dtype

temporary_store = TemporaryStore.create(file_name = "logement_tmp")


from openfisca_survey_manager.temporary import temporary_store_decorator

from openfisca_france_indirect_taxation.utils import get_transfert_data_frames

# Load ENL data :

year_enl = 2013

enl_survey_collection = SurveyCollection.load(
    collection = 'enquete_logement', config_files_directory = config_files_directory
    )
survey_enl = enl_survey_collection.get_survey('enquete_logement_{}'.format(year_enl))

input_enl = survey_enl.get_values(table = "menlogfm_diff")


# Load BdF data :

year_bdf = 2011

openfisca_survey_collection = SurveyCollection.load(collection = "openfisca_indirect_taxation")
openfisca_survey = openfisca_survey_collection.get_survey("openfisca_indirect_taxation_data_{}".format(year_bdf))
input_data_frame = openfisca_survey.get_values(table = "input")
input_data_frame.reset_index(inplace = True)


# Set variables :

variables_homogeneisation_bdf = [
    'agepr',
    'aidlog1',
    'aidlog2',
    'ancons',
    'cataeu',
    'chaufp',
    'cs42pr',
    'cs42cj',
    'dip14cj',
    'dip14pr',
    #'h_trans1',
    'htl',
    'mall1',
    'mall2',
    'mchof',
    'mchof_d',
    'mfac_eau1_d',
    'mfac_eg1_d',
    'mloy_d',
    #'mode_trans1', depindiv
    'nbh1',
    'nbphab',
    'nactifs',
    'nenfants',
    'ocde10',
    'pondmen',
    'poste_coicop_451',
    'poste_coicop_452',
    'poste_coicop_453',
    'revtot',
    'situapr',
    'situacj',
    'surfhab_d',
    'tau',
    'tuu',
    'typmen',
    'zeat',
    ]

variables_homogeneisation_enl = [
    "aba",
    "amr",
    "cataeu2010",
    "cceml",
    "coml11",
    "coml12",
    "coml13",
    "coml2",
    "coml3",
    "enfhod",
    "fchauf",
    "gmoy1",
    "gtt1",
    "hnph1",
    "hsh1",
    "htl",
    "iaat",
    "lmlm",
    "mag",
    "mcs",
    "mcsc",
    "mdiplo",
    "mdiploc",
    "mne1",
    "mpa",
    "mrtota2",
    "msitua",
    "msituac",
    "mtyad",
    "muc1",
    "qex",
    "tau2010",
    "tu2010",
    "zeat",
    ]

# Keep relevant variables :

menage_enl_keep = input_enl[variables_homogeneisation_enl]
conso_bdf_keep = input_data_frame[variables_homogeneisation_bdf]

