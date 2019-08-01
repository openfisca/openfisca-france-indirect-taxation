# -*- coding: utf-8 -*-


from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_france_indirect_taxation.build_survey_data.utils \
    import find_nearest_inferior

from openfisca_survey_manager.temporary import TemporaryStore

from openfisca_france_indirect_taxation.build_survey_data.utils \
    import ident_men_dtype

temporary_store = TemporaryStore.create(file_name = "transport_tmp")


year = 2008

bdf_survey_collection = SurveyCollection.load(
    collection = 'enquete_transport', config_files_directory = config_files_directory
    )
survey = bdf_survey_collection.get_survey('enquete_transport_{}'.format(year))

menage_transports = survey.get_values(table = "q_menage")
