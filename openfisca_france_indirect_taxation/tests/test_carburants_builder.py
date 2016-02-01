# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:27:32 2015

@author: thomas.douenne
"""


from __future__ import division


from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation.examples.utils_example import get_input_data_frame

for year in [2000, 2005, 2011]:
    aggregates_data_frame = get_input_data_frame(year)
    if year == 2000:
        df = aggregates_data_frame[['poste_coicop_722', 'coicop12_7', 'poste_coicop_711'] +
            ['poste_coicop_712', 'poste_coicop_713', 'poste_coicop_721', 'poste_coicop_723'] +
            ['poste_coicop_724', 'poste_coicop_731', 'poste_coicop_732', 'poste_coicop_733'] +
            ['poste_coicop_734', 'poste_coicop_736']].copy()
        df['check'] = (
            df['poste_coicop_711'] + df['poste_coicop_712'] + df['poste_coicop_713'] + df['poste_coicop_721'] +
            df['poste_coicop_722'] + df['poste_coicop_723'] + df['poste_coicop_724'] + df['poste_coicop_731'] +
            df['poste_coicop_732'] + df['poste_coicop_733'] + df['poste_coicop_734'] + df['poste_coicop_736'] -
            df['coicop12_7']
            )
    else:
        df = aggregates_data_frame[['poste_coicop_722', 'coicop12_7', 'poste_coicop_711'] +
            ['poste_coicop_712', 'poste_coicop_735', 'poste_coicop_713', 'poste_coicop_721'] +
            ['poste_coicop_723', 'poste_coicop_724', 'poste_coicop_731', 'poste_coicop_732'] +
            ['poste_coicop_733', 'poste_coicop_734', 'poste_coicop_736']].copy()
        df['check'] = (
            df['poste_coicop_711'] + df['poste_coicop_712'] + df['poste_coicop_713'] + df['poste_coicop_721'] +
            df['poste_coicop_722'] + df['poste_coicop_723'] + df['poste_coicop_724'] + df['poste_coicop_731'] +
            df['poste_coicop_732'] + df['poste_coicop_733'] + df['poste_coicop_734'] + df['poste_coicop_736'] +
            df['poste_coicop_735'] - df['coicop12_7']
            )
    assert_near(df['check'].any(), 0, 0.0001), "the total of transport differs from the sum of its components"
