# -*- coding: utf-8 -*-


import os
import pandas
import pkg_resources

from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_survey_manager.survey_collections import SurveyCollection



year = 2011
aliss_survey_collection = SurveyCollection.load(
    collection = 'aliss', config_files_directory = config_files_directory
    )
aliss_survey_collection
survey = aliss_survey_collection.get_survey('aliss_{}'.format(year))

df = survey.get_values(table = 'Base_ALISS_2011')


liste_produits_path = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'aliss',
    'liste_produits.xlsx'
    )

liste_produits = pandas.read_excel(liste_produits_path)
liste_produits.columns
sous_codes = liste_produits.sous_code.dropna().tolist()
postes = list()
for sous_code in sous_codes:
    postes.append(sous_code[0:4])