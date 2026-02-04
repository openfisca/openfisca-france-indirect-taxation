# -*- coding: utf-8 -*-

# Dans ce script, on test la qualité de l'appariement en calculant la distance de Hellinger entre la base de données appariée et la base de référence EMP.

import pandas as pd
import os

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_3_1_compute_hellinger_distance import hellinger_distance 
from openfisca_france_indirect_taxation.utils import assets_directory

# Importation des bases de données appariées et de la base de référence entd

data_entd = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matching_entd.csv'
        ),
    sep =',',
    decimal = '.'
    )

data_matched_distance = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matched_distance.csv'
        ),
    sep =',',
    decimal = '.'
    )

data_matched_random = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matched_random.csv'
        ),
    sep =',',
    decimal = '.'
    )

data_matched_rank = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matched_rank.csv'
        ),
    sep =',',
    decimal = '.'
    )

data_matched = data_matched_distance.copy()


varlist = ['distance_annuelle', 'distance_diesel_annuelle', 'distance_essence_annuelle', 'distance_annuelle_niveau_vie_decile', 'distance_annuelle_tuu']
for var in varlist:
    hellinger_distance(data_matched, data_matched_distance, var, weight_col="pondmen")