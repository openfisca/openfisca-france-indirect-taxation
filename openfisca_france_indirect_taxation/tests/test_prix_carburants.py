from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem


def test_prix_carburants():
    '''
    This test is made to preprocessing of prix_carburants works as some indirect taxes on fuel
    '''

    year = 2011
    parameters = FranceIndirectTaxationTaxBenefitSystem().parameters(year)
    assert round(parameters.prix_carburants.super_95_ttc, 2) == 149.95
    assert round(parameters.prix_carburants.super_95_e10_ttc, 2) == 149.95
    accise_super95 = parameters.imposition_indirecte.produits_energetiques.ticpe.super_95_98
    majoration_ticpe_super95 = parameters.imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
    assert round(accise_super95 + majoration_ticpe_super95, 2) == 63.19
    accise_super_e10 = parameters.imposition_indirecte.produits_energetiques.ticpe.super_e10
    majoration_ticpe_super_e10 = \
        parameters.imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
    assert round(accise_super_e10 + majoration_ticpe_super_e10, 2) == 63.19
