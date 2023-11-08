def get_accise_diesel_ticpe(parameters, period):
    majoration_ticpe_diesel = \
        parameters(period.start).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_gazole

    accise_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole

    accise_diesel_ticpe = (
        accise_diesel
        if len(majoration_ticpe_diesel._children) == 0  # majoration_ticpe_diesel should return None
        else accise_diesel + majoration_ticpe_diesel[42]  # alsace
        )

    return accise_diesel_ticpe
