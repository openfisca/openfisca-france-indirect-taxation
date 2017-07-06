# -*- coding: utf-8 -*-

import datetime


from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem


# Exceptionally for this test do not import TaxBenefitSystem from tests.base.
tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()


def check_legislation_xml_file(year):
    compact_legislation = tax_benefit_system.get_compact_legislation(year)
    assert compact_legislation is not None


def test_legislation_xml_file():
    for year in range(1995, datetime.date.today().year + 1):
        yield check_legislation_xml_file, year
