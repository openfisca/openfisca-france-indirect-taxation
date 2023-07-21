from ipmportlib import metadata

from openfisca_france_indirect_taxation.france_indirect_taxation_taxbenefitsystem import FranceIndirectTaxationTaxBenefitSystem


openfisca_france_indirect_taxation_location = Path(
    metadata.distribution('openfisca-france-indirect-taxation').files[0]
    ).parent

CountryTaxBenefitSystem = FranceIndirectTaxationTaxBenefitSystem
