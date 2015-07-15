# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 19:04:58 2015

@author: thomas.douenne
"""

import pandas as pd

data_frame_for_pandas = \
    pd.DataFrame.from_csv('data_frame_for_pandas.csv',
        sep = ',')

data_frame_for_pandas.fillna(0, inplace=True)

for i in range(1, 10):
    data_frame_for_pandas['el_{}'.format(i)] = \
        data_frame_for_pandas['e_{}'.format(i)] * data_frame_for_pandas['part_depenses_tot']

resultats_elasticite_depenses = dict()
for i in range (1, 10):
    resultats_elasticite_depenses['el_{}'.format(i)] = sum(data_frame_for_pandas['el_{}'.format(i)])
