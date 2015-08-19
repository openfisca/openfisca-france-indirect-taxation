# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:27:32 2015

@author: thomas.douenne
"""


from __future__ import division


from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame

for year in [2000, 2005, 2011]:
    aggregates_data_frame = get_input_data_frame(year)
    if year == 2000:
        df = aggregates_data_frame[['07220'] + ['coicop12_7'] + ['07110'] + ['07120'] + ['07130'] + ['07210'] +
            ['07230'] + ['07240'] + ['07310'] + ['07320'] + ['07330'] + ['07340'] + ['07360']]
        df['check'] = (
            df['07110'] + df['07120'] + df['07130'] + df['07210'] + df['07220'] + df['07230'] + df['07240'] +
            df['07310'] + df['07320'] + df['07330'] + df['07340'] + df['07360'] - df['coicop12_7']
            ).copy()
    else:
        df = aggregates_data_frame[['07220'] + ['coicop12_7'] + ['07110'] + ['07120'] + ['07350'] + ['07130'] +
            ['07210'] + ['07230'] + ['07240'] + ['07310'] + ['07320'] + ['07330'] + ['07340'] + ['07360']]
        df['check'] = (
            df['07110'] + df['07120'] + df['07130'] + df['07210'] + df['07220'] + df['07230'] + df['07240'] +
            df['07310'] + df['07320'] + df['07330'] + df['07340'] + df['07360'] + df['07350'] - df['coicop12_7']
            ).copy()
    assert_near(df['check'].any(), 0, 0.0001), "the total of transport differs from the sum of its components"

    df2 = aggregates_data_frame[['07220'] + ['categorie_fiscale_14']]
    df2['check'] = df2['07220'] - df2['categorie_fiscale_14']
    assert_near(df2['check'].any(), 0, 0.0001), "categorie_fiscale_14 is not correctly constructed"
