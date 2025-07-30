import datetime


from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem


# Exceptionally for this test do not import TaxBenefitSystem from tests.base.
tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()


def test_parameters():
    parameters = tax_benefit_system.parameters
    assert parameters is not None
    for year in range(1995, datetime.date.today().year + 1):
        parameters_at_instant = tax_benefit_system.get_parameters_at_instant(year)
        assert parameters_at_instant is not None
