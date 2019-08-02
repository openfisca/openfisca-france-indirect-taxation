# -*- coding: utf-8 -*-

import pytest


from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation.utils import get_input_data_frame

@pytest.mark.skipif(reason = "KeyError: '['poste_coicop_07_2_2_1_1'] not in index'")
@pytest.mark.parametrize("year", [2000, 2005, 2011])
def test_carburants_builder(year):
    aggregates_data_frame = get_input_data_frame(year)
    if year == 2000:
        df = aggregates_data_frame[[
            'coicop12_7',
            'poste_coicop_07_2_2_1_1',
            'poste_coicop_711',
            'poste_coicop_712',
            'poste_coicop_713',
            'poste_coicop_721',
            'poste_coicop_723',
            'poste_coicop_724',
            'poste_coicop_731',
            'poste_coicop_732',
            'poste_coicop_733',
            'poste_coicop_734',
            'poste_coicop_736'
            ]].copy()
        df['check'] = (
            df['poste_coicop_711']
            + df['poste_coicop_712']
            + df['poste_coicop_713']
            + df['poste_coicop_721']
            + df['poste_coicop_07_2_2_1_1']
            + df['poste_coicop_723']
            + df['poste_coicop_724']
            + df['poste_coicop_731']
            + df['poste_coicop_732']
            + df['poste_coicop_733']
            + df['poste_coicop_734']
            + df['poste_coicop_736']
            - df['coicop12_7']
            )
    else:
        df = aggregates_data_frame[
            ['poste_coicop_07_2_2_1_1', 'coicop12_7', 'poste_coicop_711']
            + ['poste_coicop_712', 'poste_coicop_735', 'poste_coicop_713', 'poste_coicop_721']
            + ['poste_coicop_723', 'poste_coicop_724', 'poste_coicop_731', 'poste_coicop_732']
            + ['poste_coicop_733', 'poste_coicop_734', 'poste_coicop_736']
            ].copy()
        df['check'] = (
            df['poste_coicop_711'] + df['poste_coicop_712'] + df['poste_coicop_713'] + df['poste_coicop_721']
            + df['poste_coicop_07_2_2_1_1'] + df['poste_coicop_723'] + df['poste_coicop_724'] + df['poste_coicop_731']
            + df['poste_coicop_732'] + df['poste_coicop_733'] + df['poste_coicop_734'] + df['poste_coicop_736']
            + df['poste_coicop_735'] - df['coicop12_7']
            )
    assert_near(df['check'].any(), 0, 0.0001), "the total of transport differs from the sum of its components"
