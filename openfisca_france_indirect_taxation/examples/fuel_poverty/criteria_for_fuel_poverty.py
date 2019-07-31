# -*- coding: utf-8 -*-

# Dans ce script, on mesure, par décile de revenu, la part des ménages souffrant de précarité énergétique
# On évalue la précarité énergétique selon plusieurs critères.


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


"""
Part des ménages ayant eu froid pendant l'hiver
"""

print("Sur l'ensemble des ménages :")
print(" ")
print((100 * sum(data_enl['pondmen'] * (data_enl['froid'] == 1)) / sum(data_enl['pondmen'])))
print(" ")
print("Par décile de niveau de vie :")
print(" ")
for i in range(1, 11):
    data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
    print(i, "-", 100 * sum(data_enl_decile['pondmen'] * (data_enl_decile['froid'] == 1)) / sum(data_enl_decile['pondmen']))


"""
Part des ménages ayant eu froid pendant l'hiver en raison du coût de l'énergie
"""

print("Sur l'ensemble des ménages :")
print(" ")
print((100 * sum(data_enl['pondmen'] * (data_enl['froid_cout'] == 1)) / sum(data_enl['pondmen'])))
print(" ")
print("Par décile de niveau de vie :")
print(" ")
for i in range(1, 11):
    data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
    print((i, "-", 100 * sum(data_enl_decile['pondmen'] * (data_enl_decile['froid_cout'] == 1)) / sum(data_enl_decile['pondmen'])))


"""
Part des ménages ayant eu froid pendant l'hiver, et ayant des difficultés avec leur budget
"""

data_matched_random['aise_froid'] = 0
data_matched_random['aise_froid'] = \
    (data_matched_random['froid'] == 1) * (data_matched_random['aise'] > 3) * 1

print("Sur l'ensemble des ménages :")
print(" ")
print((100 * sum(data_matched_random['pondmen'] * (data_matched_random['aise_froid'] == 1)) / sum(data_matched_random['pondmen'])))
print(" ")
print("Par décile de niveau de vie :")
print(" ")
for i in range(1, 11):
    data_matched_random_decile = data_matched_random.query('niveau_vie_decile == {}'.format(i))
    print((i, "-", 100 * sum(data_matched_random_decile['pondmen'] * (data_matched_random_decile['aise_froid'] == 1)) / sum(data_matched_random_decile['pondmen'])))


"""
Part des ménages ayant eu froid pendant l'hiver en raison du coût de l'énergie,
et ayant des difficultés avec leur budget
"""

data_matched_random['aise_froid_cout'] = \
    (data_matched_random['aise_froid'] == 1) * (data_matched_random['froid_cout'] == 1) * 1

print("Sur l'ensemble des ménages :")
print(" ")
print((100 * sum(data_matched_random['pondmen'] * (data_matched_random['aise_froid_cout'] == 1)) / sum(data_matched_random['pondmen'])))
print(" ")
print("Par décile de niveau de vie :")
print(" ")
for i in range(1, 11):
    data_matched_random_decile = data_matched_random.query('niveau_vie_decile == {}'.format(i))
    print((i, "-", (
        100 * sum(data_matched_random_decile['pondmen']
* (data_matched_random_decile['aise_froid_cout'] == 1))
        / sum(data_matched_random_decile['pondmen'])
        )))


"""
Part des ménages affectant plus de 15% de leurs revenus à l'énergie
"""

print("Sur l'ensemble des ménages :")
print(" ")
print((100 * float(sum(data_matched_random['part_energies_revtot'] > 0.15)) / len(data_matched_random)))
print(" ")
print("Par décile de niveau de vie :")
print(" ")
for i in range(1, 11):
    data_matched_random_decile = data_matched_random.query('niveau_vie_decile == {}'.format(i))
    print((i, "-", (
        100 * sum(data_matched_random_decile['pondmen']
* (data_matched_random_decile['part_energies_revtot'] > 0.15))
        / sum(data_matched_random_decile['pondmen'])
        )))


"""
Part des ménages affectant plus de 10% de leurs revenus à l'énergie
"""

print("Sur l'ensemble des ménages :")
print(" ")
print((100 * float(sum(data_matched_random['part_energies_revtot'] > 0.1)) / len(data_matched_random)))
print(" ")
print("Par décile de niveau de vie :")
print(" ")
for i in range(1, 11):
    data_matched_random_decile = data_matched_random.query('niveau_vie_decile == {}'.format(i))
    print((i, "-", (
        100 * sum(data_matched_random_decile['pondmen']
* (data_matched_random_decile['part_energies_revtot'] > 0.1))
        / sum(data_matched_random_decile['pondmen'])
        )))


"""
Part des ménages affectant plus de 15% de leurs dépenses à l'énergie
"""

print("Sur l'ensemble des ménages :")
print(" ")
print((100 * float(sum(data_matched_random['part_energies_depenses_tot'] > 0.15)) / len(data_matched_random)))
print(" ")
print("Par décile de niveau de vie :")
print(" ")
for i in range(1, 11):
    data_matched_random_decile = data_matched_random.query('niveau_vie_decile == {}'.format(i))
    print((i, "-", (
        100 * sum(data_matched_random_decile['pondmen']
* (data_matched_random_decile['part_energies_depenses_tot'] > 0.15))
        / sum(data_matched_random_decile['pondmen'])
        )))


"""
Part des ménages affectant plus de 10% de leurs dépenses à l'énergie
"""

print("Sur l'ensemble des ménages :")
print(" ")
print((100 * float(sum(data_matched_random['part_energies_depenses_tot'] > 0.1)) / len(data_matched_random)))
print(" ")
print("Par décile de niveau de vie :")
print(" ")
for i in range(1, 11):
    data_matched_random_decile = data_matched_random.query('niveau_vie_decile == {}'.format(i))
    print((i, "-", (
        100 * sum(data_matched_random_decile['pondmen']
* (data_matched_random_decile['part_energies_depenses_tot'] > 0.1))
        / sum(data_matched_random_decile['pondmen'])
        )))
