import pytest

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem


def test_prix_carburants():
    '''
    This test is made to preprocessing of prix_carburants works as some indirect taxes on fuel
    '''

    date = "2022-11-01"
    parameters = FranceIndirectTaxationTaxBenefitSystem().parameters(date)
    assert round(parameters.prix_carburants.super_95_ttc, 2) == 149.95
    assert round(parameters.prix_carburants.super_95_e10_ttc, 2) == 149.95
    accise_super95 = parameters.imposition_indirecte.produits_energetiques.ticpe.super_95_98
    majoration_ticpe_super95 = parameters.imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10.alsace
    assert round(accise_super95 + majoration_ticpe_super95, 2) == 63.19
    accise_super_e10 = parameters.imposition_indirecte.produits_energetiques.ticpe.super_e10
    majoration_ticpe_super_e10 = \
        parameters.imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10.alsace
    assert round(accise_super_e10 + majoration_ticpe_super_e10, 2) == 63.19

def test_prix_carburants():
    '''
    This test is made to preprocessing of prix_carburants works as some indirect taxes on fuel
    '''

    year = "2024"
    parameters = FranceIndirectTaxationTaxBenefitSystem().parameters(year)
    assert round(parameters.prix_carburants.super_95_ttc, 2) == 149.95
    assert round(parameters.prix_carburants.super_95_e10_ttc, 2) == 149.95
    accise_super95 = parameters.imposition_indirecte.produits_energetiques.ticpe.super_95_98
    majoration_ticpe_super95 = parameters.imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10.alsace
    assert round(accise_super95 + majoration_ticpe_super95, 2) == 63.19
    accise_super_e10 = parameters.imposition_indirecte.produits_energetiques.ticpe.super_e10
    majoration_ticpe_super_e10 = \
        parameters.imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10.alsace
    assert round(accise_super_e10 + majoration_ticpe_super_e10, 2) == 63.19
