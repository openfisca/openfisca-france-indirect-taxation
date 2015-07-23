# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 19:04:58 2015

@author: thomas.douenne
"""

import pandas as pd

# Import data_frame_for_pandas to get the results of the estimation run on Stata.

data_frame_for_pandas = \
    pd.DataFrame.from_csv('data_frame_for_pandas_2005.csv',
        sep = ',')

data_frame_for_pandas.fillna(0, inplace=True)
assert 0.999 < sum(data_frame_for_pandas['part_depenses_tot']) < 1.001, "the sum of the shares is not equal to 1"

# Create a weighted average of each individual elasticity.

for i in range(1, 10):
    data_frame_for_pandas['el_{}'.format(i)] = \
        data_frame_for_pandas['e_{}'.format(i)] * data_frame_for_pandas['part_depenses_tot']

resultats_elasticite_depenses = dict()
for i in range(1, 10):
    resultats_elasticite_depenses['el_{}'.format(i)] = sum(data_frame_for_pandas['el_{}'.format(i)])

# Create a confidence interval at the 95% level for each elasticity.

borne_inferieure_el_dep = dict()
borne_superieure_el_dep = dict()
for i in range(1, 10):
    borne_superieure_el_dep['borne_sup_{}'.format(i)] = (
        resultats_elasticite_depenses['el_{}'.format(i)] + 1.96 *
        (data_frame_for_pandas['e_{}'.format(i)].describe()['std'] /
        len(data_frame_for_pandas['e_{}'.format(i)]) ** 0.5)
        )
    borne_inferieure_el_dep['borne_inf_{}'.format(i)] = (
        resultats_elasticite_depenses['el_{}'.format(i)] - 1.96 *
        (data_frame_for_pandas['e_{}'.format(i)].describe()['std'] /
        len(data_frame_for_pandas['e_{}'.format(i)]) ** 0.5)
        )
