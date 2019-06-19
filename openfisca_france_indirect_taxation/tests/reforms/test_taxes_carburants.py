# -*- coding: utf-8 -*-


import datetime


from openfisca_core import periods
from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation.tests import base


def test_rattrapage_diesel():
    year = 2014
    reform = base.get_cached_reform(
        reform_key = 'rattrapage_diesel',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        period = periods.period(year),
        personne_de_reference =dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        menage = dict(
            depenses_essence = 1000,
            elas_price_1_1 = -0.4,
            ),
        )
    reform_simulation = scenario.new_simulation(debug = True)
    absolute_error_margin = 0.01
    reform_depenses_essence_ajustees_rattrapage_diesel = reform_simulation.calculate('depenses_essence_ajustees_rattrapage_diesel')
    assert_near(
        reform_depenses_essence_ajustees_rattrapage_diesel,
        1000 * (1 + (1 + -.4) * 10 / 148.4583),
        absolute_error_margin = absolute_error_margin
        )


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
