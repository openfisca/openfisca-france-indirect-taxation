# -*- coding: utf-8 -*-


import datetime


from openfisca_core import periods
from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation.tests import base


def test_taxes_carburants():
    year = 2014
    reform = base.get_cached_reform(
        reform_key = 'taxes_carburants',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        period = periods.period('year', year),
        personne_de_reference = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        menage = dict(
            depenses_essence = 1000,
            carburants_elasticite_prix = 0,
            ),
        )
    reform_simulation = scenario.new_simulation(debug = True)
    absolute_error_margin = 0.01
    reform_depenses_essence_ajustees = reform_simulation.calculate('depenses_essence_ajustees')
    assert_near(
        reform_depenses_essence_ajustees,
        1000 * (1 + (1 + (0)) * 10 / 148.4583),
        absolute_error_margin = absolute_error_margin
        )


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_taxes_carburants()
