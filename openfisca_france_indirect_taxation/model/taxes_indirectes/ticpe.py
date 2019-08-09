# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class combustibles_liquides_ticpe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de TICPE sur les combustibles liquides"

    def formula(menage, period, parameters):
        quantites_combustibles_liquides = menage('quantites_combustibles_liquides', period)
        accise_combustibles_liquides = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole_fioul_domestique_hectolitre
        combustibles_liquides_ticpe = quantites_combustibles_liquides * accise_combustibles_liquides / 100

        return combustibles_liquides_ticpe


class diesel_ticpe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de TICPE sur le diesel"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

        try:
            majoration_ticpe_diesel = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_gazole.alsace
            accise_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except Exception:
            accise_diesel_ticpe = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole

        prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
        taux_implicite_diesel = (
            (accise_diesel_ticpe * (1 + taux_plein_tva))
            / (prix_diesel_ttc - accise_diesel_ticpe * (1 + taux_plein_tva))
            )
        depenses_diesel = menage('depenses_diesel_corrigees', period)
        depenses_diesel_htva = depenses_diesel - tax_from_expense_including_tax(depenses_diesel, taux_plein_tva)
        montant_diesel_ticpe = tax_from_expense_including_tax(depenses_diesel_htva, taux_implicite_diesel)

        return montant_diesel_ticpe


class diesel_ticpe_ajustee(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de TICPE sur le diesel après réforme"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

        try:
            majoration_ticpe_diesel = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_gazole.alsace
            accise_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except Exception:
            accise_diesel_ticpe = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole

        reforme_diesel = parameters(period.start).rattrapage_diesel.diesel
        accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
        prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
        prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
        taux_implicite_diesel_ajuste = (
            (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
            / (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
            )

        depenses_diesel_ajustees = menage('depenses_diesel_ajustees', period)
        depenses_diesel_htva_ajustees = (
            depenses_diesel_ajustees - tax_from_expense_including_tax(depenses_diesel_ajustees, taux_plein_tva)
            )
        montant_diesel_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
            )

        return montant_diesel_ticpe_ajuste


class essence_ticpe(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur toutes les essences cumulées"
    definition_period = YEAR

    def formula_2009(menage, period):
        sp95_ticpe = menage('sp95_ticpe', period)
        sp98_ticpe = menage('sp98_ticpe', period)
        sp_e10_ticpe = menage('sp_e10_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe + sp_e10_ticpe)
        return essence_ticpe

    def formula_2007(menage, period):
        sp95_ticpe = menage('sp95_ticpe', period)
        sp98_ticpe = menage('sp98_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe)
        return essence_ticpe

    def formula_1990(menage, period):
        sp95_ticpe = menage('sp95_ticpe', period)
        sp98_ticpe = menage('sp98_ticpe', period)
        super_plombe_ticpe = menage('super_plombe_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe + super_plombe_ticpe)
        return essence_ticpe


class essence_ticpe_ajustee(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"
    definition_period = YEAR

    def formula_2009(menage, period):
        sp95_ticpe_ajustee = menage('sp95_ticpe_ajustee', period)
        sp98_ticpe_ajustee = menage('sp98_ticpe_ajustee', period)
        sp_e10_ticpe_ajustee = menage('sp_e10_ticpe_ajustee', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
        return essence_ticpe_ajustee

    def formula_2007(menage, period):
        sp95_ticpe_ajustee = menage('sp95_ticpe_ajustee', period)
        sp98_ticpe_ajustee = menage('sp98_ticpe_ajustee', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
        return essence_ticpe_ajustee

    def formula_1990(menage, period):
        sp95_ticpe_ajustee = menage('sp95_ticpe_ajustee', period)
        sp98_ticpe_ajustee = menage('sp98_ticpe_ajustee', period)
        super_plombe_ticpe_ajustee = menage('super_plombe_ticpe_ajustee', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
        return essence_ticpe_ajustee


class sp_e10_ticpe(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur le SP E10"
    definition_period = YEAR

    def formula_2009(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        try:
            accise_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e10
            majoration_ticpe_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
        except Exception:
            accise_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e10

        super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
        taux_implicite_sp_e10 = (
            (accise_ticpe_super_e10 * (1 + taux_plein_tva))
            / (super_95_e10_ttc - accise_ticpe_super_e10 * (1 + taux_plein_tva))
            )
        depenses_sp_e10 = menage('depenses_sp_e10', period)
        depenses_sp_e10_htva = \
            depenses_sp_e10 - tax_from_expense_including_tax(depenses_sp_e10, taux_plein_tva)
        montant_sp_e10_ticpe = \
            tax_from_expense_including_tax(depenses_sp_e10_htva, taux_implicite_sp_e10)

        return montant_sp_e10_ticpe

    def formula(menage, period):
        montant_sp_e10_ticpe = (0 * menage('depenses_sp_95', period))
        return montant_sp_e10_ticpe


# Check if there is no need to have period formulas
class sp_e10_ticpe_ajustee(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur le SP E10 après réforme"
    definition_period = YEAR

    def formula_2009(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        try:
            accise_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e10
            majoration_ticpe_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
        except Exception:
            accise_ticpe_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e10

        reforme_essence = parameters(period.start).rattrapage_diesel.essence
        accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
        super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
        super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
        taux_implicite_sp_e10_ajuste = (
            (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
            / (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees = menage('depenses_essence_ajustees', period)
        part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        sp_e10_depenses_ajustees = depenses_essence_ajustees * part_sp_e10
        sp_e10_depenses_htva_ajustees = \
            sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
        montant_sp_e10_ticpe_ajuste = \
            tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

        return montant_sp_e10_ticpe_ajuste


class sp95_ticpe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de TICPE sur le sp_95"

    def formula(menage, period, parameters):

        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        try:
            accise_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            majoration_ticpe_super95 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except Exception:
            accise_ticpe_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98

        super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
        taux_implicite_sp95 = (
            (accise_ticpe_super95 * (1 + taux_plein_tva))
            / (super_95_ttc - accise_ticpe_super95 * (1 + taux_plein_tva))
            )
        depenses_sp_95 = menage('depenses_sp_95', period)
        depenses_sp_95_htva = depenses_sp_95 - tax_from_expense_including_tax(depenses_sp_95, taux_plein_tva)
        montant_sp95_ticpe = tax_from_expense_including_tax(depenses_sp_95_htva, taux_implicite_sp95)

        return montant_sp95_ticpe


class sp95_ticpe_ajustee(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de TICPE sur le sp_95 après réforme"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

        try:
            accise_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            majoration_ticpe_super95 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except Exception:
            accise_ticpe_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98

        reforme_essence = parameters(period.start).rattrapage_diesel.essence
        accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
        super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
        super_95_ttc_ajuste = super_95_ttc + reforme_essence
        taux_implicite_sp95_ajuste = (
            (accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
            / (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees = menage('depenses_essence_ajustees', period)
        part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95_ajustees = depenses_essence_ajustees * part_sp95
        depenses_sp_95_htva_ajustees = (
            depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
            )
        montant_sp95_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
            )

        return montant_sp95_ticpe_ajuste


class sp98_ticpe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de TICPE sur le sp_98"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

        try:
            accise_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            majoration_ticpe_super98 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except Exception:
            accise_ticpe_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98

        super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc

        taux_implicite_sp98 = (
            (accise_ticpe_super98 * (1 + taux_plein_tva))
            / (super_98_ttc - accise_ticpe_super98 * (1 + taux_plein_tva))
            )
        depenses_sp_98 = menage('depenses_sp_98', period)
        depenses_sp_98_htva = depenses_sp_98 - tax_from_expense_including_tax(depenses_sp_98, taux_plein_tva)
        montant_sp98_ticpe = tax_from_expense_including_tax(depenses_sp_98_htva, taux_implicite_sp98)

        return montant_sp98_ticpe


class sp98_ticpe_ajustee(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de TICPE sur le sp_98 après réforme"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

        try:
            accise_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            majoration_ticpe_super98 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except Exception:
            accise_ticpe_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98

        reforme_essence = parameters(period.start).rattrapage_diesel.essence
        accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
        super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
        super_98_ttc_ajuste = super_98_ttc + reforme_essence
        taux_implicite_sp98_ajuste = (
            (accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
            / (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees = menage('depenses_essence_ajustees', period)
        part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98_ajustees = depenses_essence_ajustees * part_sp98
        depenses_sp_98_htva_ajustees = (
            depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
            )
        montant_sp98_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
            )

        return montant_sp98_ticpe_ajuste


class super_plombe_ticpe(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur le super plombé"
    definition_period = YEAR

    def formula_2007(menage, period):
        montant_super_plombe_ticpe = (0 * menage('depenses_sp_95', period))
        return montant_super_plombe_ticpe

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        accise_super_plombe_ticpe = \
            parameters(period.start).imposition_indirecte.ticpe.super_plombe_ticpe
        super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
        taux_implicite_super_plombe = (
            (accise_super_plombe_ticpe * (1 + taux_plein_tva))
            / (super_plombe_ttc - accise_super_plombe_ticpe * (1 + taux_plein_tva))
            )
        depenses_super_plombe = menage('depenses_super_plombe', period)
        depenses_super_plombe_htva = \
            depenses_super_plombe - tax_from_expense_including_tax(depenses_super_plombe, taux_plein_tva)
        montant_super_plombe_ticpe = \
            tax_from_expense_including_tax(depenses_super_plombe_htva, taux_implicite_super_plombe)

        return montant_super_plombe_ticpe


class super_plombe_ticpe_ajustee(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur le super plombé après réforme"
    definition_period = YEAR

    def formula_2007(menage, period):
        montant_super_plombe_ticpe = (0 * menage('depenses_sp_95', period))
        return montant_super_plombe_ticpe

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        accise_super_plombe_ticpe = \
            parameters(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

        reforme_essence = parameters(period.start).rattrapage_diesel.essence
        accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
        super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
        super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
        taux_implicite_super_plombe_ajuste = (
            (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
            / (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees = menage('depenses_essence_ajustees', period)
        part_super_plombe = \
            parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees * part_super_plombe
        depenses_super_plombe_htva_ajustees = (
            depenses_super_plombe_ajustees
            - tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
            )
        montant_super_plombe_ticpe_ajuste = \
            tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

        return montant_super_plombe_ticpe_ajuste


class ticpe_totale(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur tous les carburants cumulés"

    def formula(menage, period):
        essence_ticpe = menage('essence_ticpe', period)
        diesel_ticpe = menage('diesel_ticpe', period)
        ticpe_totale = diesel_ticpe + essence_ticpe

        return ticpe_totale


class ticpe_totale_ajustee(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

    def formula(menage, period):
        essence_ticpe_ajustee = menage('essence_ticpe_ajustee', period)
        diesel_ticpe_ajustee = menage('diesel_ticpe_ajustee', period)
        ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

        return ticpe_totale_ajustee


class total_taxes_energies(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur tous les carburants cumulés"

    def formula(menage, period):
        essence_ticpe = menage('essence_ticpe', period)
        diesel_ticpe = menage('diesel_ticpe', period)
        combustibles_liquides_ticpe = menage('combustibles_liquides_ticpe', period)
        total_taxes_energies = diesel_ticpe + essence_ticpe + combustibles_liquides_ticpe

        return total_taxes_energies


class difference_ticpe_diesel_reforme(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Différence entre les contributions à la TICPE sur le diesel avant et après la réforme"

    def formula(menage, period):
        diesel_ticpe_ajustee = menage('diesel_ticpe_ajustee', period)
        diesel_ticpe = menage('diesel_ticpe', period)
        difference = diesel_ticpe_ajustee - diesel_ticpe

        return difference


class difference_ticpe_essence_reforme(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Différence entre les contributions à la TICPE sur l'essence avant et après la réforme"

    def formula(menage, period):
        essence_ticpe_ajustee = menage('essence_ticpe_ajustee', period)
        essence_ticpe = menage('essence_ticpe', period)
        difference = essence_ticpe_ajustee - essence_ticpe

        return difference


class difference_ticpe_totale_reforme(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Différence entre les contributions à la TICPE avant et après la réforme"

    def formula(menage, period):
        ticpe_totale_ajustee = menage('ticpe_totale_ajustee', period)
        ticpe_totale = menage('ticpe_totale', period)
        difference = ticpe_totale_ajustee - ticpe_totale

        return difference
