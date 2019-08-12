# -*- coding: utf-8 -*-


from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory



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
    # "eq_chauf",
    # "eq_combu",
    # "eq_nb_vo",
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
    # "rmact",
    "totreven",
    ]

menage_comp_to_keep = menage_comp[variables_to_keep_comp]
