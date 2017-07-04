# -*- coding: utf-8 -*-

# Dans ce script, on test la qualité de l'appariement.

import pandas as pd

import os
import pkg_resources

# Importation de la base de données appariée
default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)

data_matched = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matched.csv'
        ), sep =',', decimal = '.'
    )


"""
Placebo test for share of revenue spent in energies :
    How well do we do among income deciles, area and age ?
"""

# Incomes deciles :
for i in range(1,11):
    data_decuc = data_matched.query('decuc == {}'.format(i))
    before = (data_decuc['part_energies_revtot_before'] * data_decuc['pondmen']).sum() / data_decuc['pondmen'].sum()
    after = (data_decuc['part_energies_revtot_after'] * data_decuc['pondmen']).sum() / data_decuc['pondmen'].sum()

    print i, before * 100, after * 100
    del data_decuc

# Area of residence :
for i in [111, 112, 120, 211, 212, 221, 300, 400]: #222
    data_cataeu = data_matched.query('cataeu == {}'.format(i))
    after = (data_cataeu['part_energies_revenu'] * data_cataeu['pondmen']).sum() / data_cataeu['pondmen'].sum()
    before = (data_cataeu['part_energies_revtot'] * data_cataeu['pondmen']).sum() / data_cataeu['pondmen'].sum()

    print i, before * 100, after * 100
    del data_cataeu

# Age :
for i in [25, 35, 45, 55, 65, 75, 85]: 
    data_age = data_matched.query('{0} < agepr < {1}'.format(i - 11, i))
    after = (data_age['part_energies_revenu'] * data_age['pondmen']).sum() / data_age['pondmen'].sum()
    before = (data_age['part_energies_revtot'] * data_age['pondmen']).sum() / data_age['pondmen'].sum()

    print i, before * 100, after * 100
    del data_age


"""
...
"""
    