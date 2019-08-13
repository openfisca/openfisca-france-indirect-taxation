# -*- coding: utf-8 -*-


from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory


year = 2008
bdf_survey_collection = SurveyCollection.load(
    collection = 'enquete_transport', config_files_directory = config_files_directory
    )
survey = bdf_survey_collection.get_survey('enquete_transport_{}'.format(year))
menage_transports = survey.get_values(table = "q_menage")
