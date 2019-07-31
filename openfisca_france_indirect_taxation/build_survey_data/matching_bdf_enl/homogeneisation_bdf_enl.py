# Trouver un moyen d'importer facilement les données ENL

# Importer toutes les variables communes suscpetibles de nous intéresser

# Les comparer : échelle, unité -> homogénéiser

# Comparer leur distribution -> homogénéiser

# Regarder code StatMatch


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
from openfisca_france_indirect_taxation.utils import get_transfert_data_frames
from openfisca_survey_manager.temporary import temporary_store_decorator

from openfisca_france_indirect_taxation.build_survey_data.utils \
    import ident_men_dtype

temporary_store = TemporaryStore.create(file_name = "logement_tmp")


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

variables_bdf = [
    'agepr',
    # 'aidlog1',
    # 'aidlog2',
    # 'ancons',
    # 'cataeu',
    # 'chaufp',
    # 'cs42',
    # 'dip14',
    # 'h_trans1',
    # 'htl',
    # 'mall1',
    # 'mall2',
    # 'mchof',
    # 'mchof_d',
    # 'mfac_eau1',
    # 'mfac_eau1_d',
    # 'mfac_eg1',
    # 'mfac_eg1_d',
    # 'mloy',
    # 'mloy_d',
    # 'mode_trans1',
    # 'nbh1',
    # 'nbphab',
    'nactifs',
    'nenfants',
    'ocde10',
    'poste_coicop_451',
    'poste_coicop_452',
    'poste_coicop_453',
    'revtot',
    'situapr',
    'situacj',
    # 'surfhab',
    # 'tau',
    # 'tchof',
    # 'tuu',
    'typmen',
    'zeat',
    ]


variables_enl = [
    'cataeu2010',
    'coml11',
    'coml12',
    'coml2',
    'coml3',
    'hsh1',
    'mne1',
    'msitua',
    'msituac'
    ]


# Keep relevant variables :

menage_enl_keep = input_enl[variables_enl]
conso_bdf_keep = input_data_frame[variables_bdf]


# Compare surveys :

menage_enl_keep['depenses_gaz'] = menage_enl_keep['coml12'] + menage_enl_keep['coml3']
print(menage_enl_keep['depenses_gaz'].mean())
print(conso_bdf_keep['poste_coicop_452'].mean())

print(menage_enl_keep['msituac'].hist())
print(conso_bdf_keep['situacj'].hist())

print(menage_enl_keep['mne1'].hist())
print(conso_bdf_keep['nenfants'].hist())

menage_enl_keep['mne1'].plot.density()
conso_bdf_keep['nenfants'].plot.density()

menage_enl_keep['coml11'].plot.density()
conso_bdf_keep['poste_coicop_451'].plot.density()

menage_enl_keep['coml11'].quantile([.1, .2, .3, .4, .5, .6, .7, .8, .9])
conso_bdf_keep['poste_coicop_451'].quantile([.1, .2, .3, .4, .5, .6, .7, .8, .9])
