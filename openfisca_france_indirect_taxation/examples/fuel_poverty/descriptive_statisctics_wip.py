# -*- coding: utf-8 -*-

# Dans ce script, on test la qualité de l'appariement.


import pandas as pd

import os
import pkg_resources

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_4_clean_data import \
    clean_data


data_enl = clean_data()[0]

# Importation de la base de données appariée
default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)


data_matched_random = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matched_random.csv'
        ), sep =',', decimal = '.'
    )


data_matched_rank = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matched_rank.csv'
        ), sep =',', decimal = '.'
    )

# Sentiment du ménage par rapport à son budget actuel :
# y arrive difficilement (4) ou n'y arrive pas sans dettes (5)
print(float(len(data_matched_random.query('aise > 3'))) / len(data_matched_random) * 100)
for i in range(1, 11):
    print(float(
        len(data_matched_random.query('niveau_vie_decile == {}'.format(i)).query('aise > 3'))
        ) / len(data_matched_random.query('niveau_vie_decile == {}'.format(i))) * 100)

# Indicateurs propres au sentiment de froid, à la consommation d'énergies, et indicateurs croisés.
data_matched_random['aise_froid'] = 0
data_matched_random['aise_froid'] = \
    (data_matched_random['froid'] == 1) * (data_matched_random['aise'] > 3) * 1

print(float(len(data_matched_random.query('aise_froid == 1'))) / len(data_matched_random) * 100)
for i in range(1, 11):
    print(float(
        len(data_matched_random.query('niveau_vie_decile == {}'.format(i)).query('aise_froid == 1'))
        ) / len(data_matched_random.query('niveau_vie_decile == {}'.format(i))) * 100)

data_matched_random['aise_froid_cout'] = \
    (data_matched_random['aise_froid'] == 1) * (data_matched_random['froid_cout'] == 1) * 1

print("Parmi les personnes déclarant avoir eu froid à cause du prix de l'énergie, quelle est la part \
    ayant des difficultés dans leur budget ?")
print(" ")

for i in range(1, 11):
    print(float(len(data_matched_random.query('niveau_vie_decile == {}'.format(i)).query('aise_froid_cout == 1'))) /
        len(data_matched_random.query('niveau_vie_decile == {}'.format(i)).query('froid_cout == 1')))
print(" ")

print("Parmi les personnes ayant des difficultés dans leur budget, et ayant froid dans leur logement \
    quelle est la part de ceux déclarant avoir eu froid à cause du prix de l'énergie ?")
print(" ")

for i in range(1, 11):
    print(float(len(data_matched_random.query('niveau_vie_decile == {}'.format(i)).query('aise_froid_cout == 1'))) /
        len(data_matched_random.query('niveau_vie_decile == {}'.format(i)).query('aise_froid == 1')))
