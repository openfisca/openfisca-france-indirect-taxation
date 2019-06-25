# -*- coding: utf-8 -*-


from __future__ import division


import datetime


from openfisca_core import periods
from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.scenarios import init_single_entity
from openfisca_france_indirect_taxation.reforms.rattrapage_diesel import reforme_rattrapage_diesel


# Initialize a tax_benefit_system
tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()


def test_rattrapage_diesel():
    year = 2014
    period = periods.period(year)
    reform = reforme_rattrapage_diesel(tax_benefit_system)
    scenario = init_single_entity(
        scenario = reform.new_scenario(),
        period = period,
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
    reform_depenses_essence_ajustees_rattrapage_diesel = reform_simulation.calculate(
        'depenses_essence_ajustees_rattrapage_diesel', period =period)
    assert_near(
        reform_depenses_essence_ajustees_rattrapage_diesel,
        1000 * (1 + (1 + -.4) * 10 / 148.4583),
        absolute_error_margin = absolute_error_margin
        )


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
