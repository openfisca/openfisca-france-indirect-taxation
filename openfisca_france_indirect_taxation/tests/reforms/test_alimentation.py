# -*- coding: utf-8 -*-


from __future__ import division


import datetime


from openfisca_core import periods
from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.scenarios import init_single_entity
from openfisca_france_indirect_taxation.reforms.alimentation import reforme_alimentation

# Initialize a tax_benefit_system
tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()


def test_reforme_alimentation():
    year = 2014
    period = periods.period(year)
    reform = reforme_alimentation(tax_benefit_system)
    scenario = init_single_entity(
        scenario = reform.new_scenario(),
        period = period,
        personne_de_reference =dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        menage = dict(
            poste_06_1_1_1_1 = 100,  # tva_taux_super_reduit mais non imposé dans réforme
            poste_09_5_2_1_1 = 100,  # tva_taux_super_reduit
            poste_02_1_2_1_1 = 100,  # vin mais non imposé dans réforme (catégorie fiscale inexistante)
            ),
        )
    reform_simulation = scenario.new_simulation(debug = True)
    reference_simulation = scenario.new_simulation(debug = True, use_baseline =True)

    reference_tva_taux_super_reduit = reference_simulation.calculate('tva_taux_super_reduit', period)
    reform_tva_taux_super_reduit = reform_simulation.calculate('tva_taux_super_reduit', period)

    absolute_error_margin = 0.01

    assert_near(
        reform_tva_taux_super_reduit,
        100 * 0.021 / (1 + .021),
        absolute_error_margin = absolute_error_margin
        )

    assert_near(
        reference_tva_taux_super_reduit,
        2 * 100 * 0.021 / (1 + .021),
        absolute_error_margin = absolute_error_margin
        )

    reference_depenses_vin = reference_simulation.calculate('depenses_vin', period)
    reform_depenses_vin = reform_simulation.calculate('depenses_vin', period)
    assert_near(
        reference_depenses_vin,
        100,
        absolute_error_margin = absolute_error_margin
        )
    assert_near(
        reform_depenses_vin,
        0,
        absolute_error_margin = absolute_error_margin
        )


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    test_reforme_alimentation()
