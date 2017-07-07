# -*- coding: utf-8 -*-

"""
Computing the Hellinger distance between two discrete
probability distributions
"""

import numpy as np

from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_2_homogenize_variables import \
    create_new_variables

data = create_new_variables()
data_enl = data[0]
data_bdf = data[1]


_SQRT2 = np.sqrt(2)     # sqrt(2) with default precision np.float64


def hellinger(p, q):
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / _SQRT2
    

data_bdf['part_energies_revtot'] = data_bdf['part_energies_revtot'].astype(float)
data_bdf = data_bdf.query('part_energies_revtot < 1').copy()
data_bdf['part_energies_revtot_groupe'] = data_bdf['part_energies_revtot'].round(decimals = 2)

data_enl['part_energies_revtot'] = data_enl['part_energies_revtot'].astype(float)
data_enl = data_enl.query('part_energies_revtot < 1').copy()
data_enl['part_energies_revtot_groupe'] = data_enl['part_energies_revtot'].round(decimals = 2)


total_pop_bdf = len(data_bdf)
distribution_bdf = dict()
for i in range(0,101):
    j = float(i)/100
    number_occurences = len(data_bdf.query('part_energies_revtot_groupe == {}'.format(j)))
    distribution_bdf['{}'.format(j)] = float(number_occurences) / total_pop_bdf

total_pop_enl = len(data_enl)
distribution_enl = dict()
for i in range(0,101):
    j = float(i)/100
    number_occurences = len(data_enl.query('part_energies_revtot_groupe == {}'.format(j)))
    distribution_enl['{}'.format(j)] = float(number_occurences) / total_pop_enl

hellinger_distance = hellinger(distribution_bdf.values(),distribution_enl.values())
