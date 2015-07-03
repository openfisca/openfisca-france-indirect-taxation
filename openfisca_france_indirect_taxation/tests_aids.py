# -*- coding: utf-8 -*-
"""
Created on Fri Jul 03 16:45:31 2015

@author: thomas.douenne
"""

from openfisca_france_indirect_taxation.aids_dataframe_builder import aggregates_data_frame

produits = [column for column in aggregates_data_frame.columns if column.isdigit()]
aggregates_data_frame['dep_tot'] = aggregates_data_frame[produits].sum(axis=1)
aggregates_data_frame['diff'] = aggregates_data_frame['dep_tot'] - aggregates_data_frame['depenses_tot']
assert (aggregates_data_frame['diff'] < 0.0001).any()[(aggregates_data_frame['diff'] < 0.0001).any()], \
    'Issue in depenses_tot calculation'
