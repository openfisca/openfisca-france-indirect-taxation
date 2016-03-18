# -*- coding: utf-8 -*-

from __future__ import division


from datetime import date

from ..base import *  # noqa analysis:ignore
import numpy


class depenses_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de ticpe"

    def function(self, simulation, period):
        categorie_fiscale_14 = simulation.calculate('categorie_fiscale_14', period)
        return period, categorie_fiscale_14


class depenses_diesel_htva(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en diesel htva (mais incluant toujours la TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        depenses_diesel_htva = depenses_diesel - tax_from_expense_including_tax(depenses_diesel, taux_plein_tva)

        return period, depenses_diesel_htva


class depenses_diesel_ht(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en diesel ht (prix brut sans TVA ni TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        taux_implicite_diesel = (
            (accise_diesel_ticpe * (1 + taux_plein_tva)) /
            (prix_diesel_ttc - accise_diesel_ticpe * (1 + taux_plein_tva))
            )

        depenses_diesel_htva = simulation.calculate('depenses_diesel_htva', period)
        depenses_diesel_ht = \
            depenses_diesel_htva - tax_from_expense_including_tax(depenses_diesel_htva, taux_implicite_diesel)

        return period, depenses_diesel_ht


class depenses_diesel_recalculees(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en diesel recalculées à partir du prix ht"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_diesel_ht = simulation.calculate('depenses_diesel_ht', period)

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        taux_implicite_diesel = (
            (accise_diesel_ticpe * (1 + taux_plein_tva)) /
            (prix_diesel_ttc - accise_diesel_ticpe * (1 + taux_plein_tva))
            )

        depenses_diesel_recalculees = depenses_diesel_ht * (1 + taux_plein_tva) * (1 + taux_implicite_diesel)

        return period, depenses_diesel_recalculees


class depenses_essence_ht(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence hors taxes (HT, i.e. sans TVA ni TICPE)"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_super_plombe_ht = simulation.calculate('depenses_super_plombe_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht + depenses_super_plombe_ht)
        return period, depenses_essence_ht

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht)
        return period, depenses_essence_ht

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_sp_e10_ht = simulation.calculate('depenses_sp_e10_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht + depenses_sp_e10_ht)
        return period, depenses_essence_ht


class depenses_sp_e10_ht(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence sans plomb e10 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10 = depenses_essence * part_sp_e10
        depenses_sp_e10_htva = depenses_sp_e10 - tax_from_expense_including_tax(depenses_sp_e10, taux_plein_tva)

        try:
            accise_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10
            majoration_ticpe_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
        except:
            accise_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10

        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        taux_implicite_sp_e10 = (
            (accise_ticpe_super_e10 * (1 + taux_plein_tva)) /
            (super_95_e10_ttc - accise_ticpe_super_e10 * (1 + taux_plein_tva))
            )
        depenses_sp_e10_ht = \
            depenses_sp_e10_htva - tax_from_expense_including_tax(depenses_sp_e10_htva, taux_implicite_sp_e10)

        return period, depenses_sp_e10_ht


class depenses_sp_95_ht(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence sans plomb 95 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        taux_implicite_sp95 = (
            (accise_ticpe_super95 * (1 + taux_plein_tva)) /
            (super_95_ttc - accise_ticpe_super95 * (1 + taux_plein_tva))
            )
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95 = depenses_essence * part_sp95
        depenses_sp_95_htva = depenses_sp_95 - tax_from_expense_including_tax(depenses_sp_95, taux_plein_tva)
        depenses_sp_95_ht = \
            depenses_sp_95_htva - tax_from_expense_including_tax(depenses_sp_95_htva, taux_implicite_sp95)

        return period, depenses_sp_95_ht


class depenses_sp_98_ht(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence sans plomb 98 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        taux_implicite_sp98 = (
            (accise_ticpe_super98 * (1 + taux_plein_tva)) /
            (super_98_ttc - accise_ticpe_super98 * (1 + taux_plein_tva))
            )
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98 = depenses_essence * part_sp98
        depenses_sp_98_htva = depenses_sp_98 - tax_from_expense_including_tax(depenses_sp_98, taux_plein_tva)
        depenses_sp_98_ht = \
            depenses_sp_98_htva - tax_from_expense_including_tax(depenses_sp_98_htva, taux_implicite_sp98)

        return period, depenses_sp_98_ht


class depenses_super_plombe_ht(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence super plombée hors taxes (HT, i.e. sans TVA ni TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        taux_implicite_super_plombe = (
            (accise_super_plombe_ticpe * (1 + taux_plein_tva)) /
            (super_plombe_ttc - accise_super_plombe_ticpe * (1 + taux_plein_tva))
            )
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe = depenses_essence * part_super_plombe
        depenses_super_plombe_htva = \
            depenses_super_plombe - tax_from_expense_including_tax(depenses_super_plombe, taux_plein_tva)
        depenses_super_plombe_ht = (depenses_super_plombe_htva -
            tax_from_expense_including_tax(depenses_super_plombe_htva, taux_implicite_super_plombe))

        return period, depenses_super_plombe_ht


class depenses_gaz_tarif_fixe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en gaz des ménages sur le coût fixe de l'abonnement"

    def function(self, simulation, period):
        quantite_base = simulation.calculate('quantites_gaz_contrat_base', period)
        quantite_b0 = simulation.calculate('quantites_gaz_contrat_b0', period)
        quantite_b1 = simulation.calculate('quantites_gaz_contrat_b1', period)
        quantite_b2i = simulation.calculate('quantites_gaz_contrat_b2i', period)
        quantite_optimale = simulation.calculate('quantites_gaz_contrat_optimal', period)

        tarif_fixe_base = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.base_0_1000
        tarif_fixe_b0 = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b0_1000_6000
        tarif_fixe_b1 = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b1_6_30000
        tarif_fixe_b2i = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b2i_30000

        tarif_fixe_optimal = (
            (quantite_base == quantite_optimale) * tarif_fixe_base +
            (quantite_b0 == quantite_optimale) * tarif_fixe_b0 +
            (quantite_b1 == quantite_optimale) * tarif_fixe_b1 +
            (quantite_b2i == quantite_optimale) * tarif_fixe_b2i
            )

        return period, tarif_fixe_optimal


class depenses_gaz_variables(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en gaz des ménages, hors coût fixe de l'abonnement"

    def function(self, simulation, period):
        depenses_gaz = simulation.calculate('poste_coicop_452', period)
        tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)

        depenses_gaz_variables = depenses_gaz - tarif_fixe
        depenses_gaz_variables = numpy.maximum(depenses_gaz_variables, 0)

        return period, depenses_gaz_variables
