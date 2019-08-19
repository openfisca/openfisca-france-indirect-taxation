# -*- coding: utf-8 -*-

from numpy.testing import assert_equal

from openfisca_france_indirect_taxation.examples.utils_example import simulate


def test_depense_carburants_ht():
    simulated_variables = [
        'depenses_diesel_ht',
        'depenses_diesel_htva',
        'diesel_ticpe',
        'depenses_diesel',
        'depenses_diesel_recalculees'
        ]
    for year in [2011]:  # 2000, 2005,
        df = simulate(simulated_variables = simulated_variables, year = year)
        assert (df.depenses_diesel_ht > 0).any()
        assert_equal(
            df.depenses_diesel_ht.values,
            df.depenses_diesel_htva.values - df.diesel_ticpe.values
            )
        df['check_diesel_recalcule'] = df['depenses_diesel'] - df['depenses_diesel_recalculees']
        assert (df['check_diesel_recalcule'] == 0).any()
