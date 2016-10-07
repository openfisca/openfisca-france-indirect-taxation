# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division


import logging
import os
import pandas
import numpy


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

year = 2013

bdf_survey_collection = SurveyCollection.load(
    collection = 'enquete_logement', config_files_directory = config_files_directory
    )
survey = bdf_survey_collection.get_survey('enquete_logement_{}'.format(year))

menage = survey.get_values(table = "menlogfm_diff")

variables_to_keep = [
    "aba",
    "aenq",
    "amr",
    "cataeu2010",
    "cceml",
    "cfn2",
    "coml",
    "coml11",
    "coml12",
    "coml13",
    "coml2",
    "coml3",
    "coml41",
    "coml42",
    "dep_idf",
    "dom",
    "enfhod",
    #"eq_chauf",
    #"eq_combu",
    #"eq_nb_vo",
    "fchauf",
    "fpbel",
    "gchauf_1",
    "gchauf_2",
    "gchauf_3",
    "gchauf_4",
    "gchauf_5",
    "gchauf_6",
    "gchauf_7",
    "gchauf_n",
    "gchaufbis",
    "gchaufs_1",
    "gchaufs_2",
    "gchaufs_3",
    "gchaufs_4",
    "gchaufs_5",
    "gmoy1",
    "gmoy2",
    "gmur",
    "gtoit2",
    "gtt1",
    "gtt2",
    "gvit1",
    "gvit1b",
    "gzc2",
    "hautb",
    "hnph1",
    "hsh1",
    "htl",
    "iaat",
    "iaatcd",
    "idlog",
    "kair",
    "kbst",
    "kcui_1",
    "kcui_2",
    "kcui_3",
    "kcui_4",
    "kcui_5",
    "kcui_6",
    "kcui_n",
    "kdep",
    "kmod_p",
    "kren",
    "ktps",
    "ktransb",
    "lchauf",
    "lmlm",
    "lmobis",
    "lpba",
    "mag",
    "mcs",
    "mcs14",
    "mcsc",
    "mdiplo",
    "mdiploc",
    "menq",
    "mne1",
    "mpa",
    "mrtota2",
    "msitua",
    "msituac",
    "mtyad",
    "muc1",
    "qex",
    "ren_n",
    "rg",
    "rmact",
    "tau2010",
    "tu2010",
    "zeat",
    "zus"
    ]

menage_to_keep = menage[variables_to_keep]

menage_comp = survey.get_values(table = "menlogfm_comp_diff")

variables_to_keep_comp = [
    "eq_chauf",
    "eq_combu",
    "eq_nb_vo",
    "idlog",
    #"rmact",
    "totreven",
    ]

menage_comp_to_keep = menage_comp[variables_to_keep_comp]

