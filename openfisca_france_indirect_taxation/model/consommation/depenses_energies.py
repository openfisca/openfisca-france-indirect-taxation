# -*- coding: utf-8 -*-

from __future__ import division


from datetime import date

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore
import numpy


class depenses_diesel_htva(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Dépenses en diesel htva (mais incluant toujours la TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        depenses_diesel_htva = depenses_diesel - tax_from_expense_including_tax(depenses_diesel, taux_plein_tva)

        return period, depenses_diesel_htva


class depenses_diesel_ht(Variable):
    column = FloatCol
    entity_class = Menage
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
    entity_class = Menage
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
    entity_class = Menage
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
    entity_class = Menage
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
    entity_class = Menage
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
    entity_class = Menage
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
    entity_class = Menage
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


class depenses_gaz_prix_unitaire(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Prix unitaire du gaz rencontré par les ménages"

    def function(self, simulation, period):
        quantite_base = simulation.calculate('quantites_gaz_contrat_base', period)
        quantite_b0 = simulation.calculate('quantites_gaz_contrat_b0', period)
        quantite_b1 = simulation.calculate('quantites_gaz_contrat_b1', period)
        quantite_b2i = simulation.calculate('quantites_gaz_contrat_b2i', period)
        quantite_optimale = simulation.calculate('quantites_gaz_contrat_optimal', period)

        prix_unitaire_base = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_base_ttc
        prix_unitaire_b0 = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b0_ttc
        prix_unitaire_b1 = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b1_ttc
        prix_unitaire_b2i = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b2i_ttc

        prix_unitaire_optimal = (
            (quantite_base == quantite_optimale) * prix_unitaire_base +
            (quantite_b0 == quantite_optimale) * prix_unitaire_b0 +
            (quantite_b1 == quantite_optimale) * prix_unitaire_b1 +
            (quantite_b2i == quantite_optimale) * (quantite_b1 != quantite_optimale) * prix_unitaire_b2i
            )

        return period, prix_unitaire_optimal


class depenses_gaz_tarif_fixe(Variable):
    column = FloatCol
    entity_class = Menage
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
            (quantite_b2i == quantite_optimale) * (quantite_b1 != quantite_optimale) * tarif_fixe_b2i
            )

        return period, tarif_fixe_optimal


class depenses_gaz_variables(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Dépenses en gaz des ménages, hors coût fixe de l'abonnement"

    def function(self, simulation, period):
        depenses_gaz = simulation.calculate('poste_coicop_452', period)
        tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)

        depenses_gaz_variables = depenses_gaz - tarif_fixe
        depenses_gaz_variables = numpy.maximum(depenses_gaz_variables, 0)

        return period, depenses_gaz_variables


class depenses_electricite_percentile(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Classement par percentile des dépenses d'électricité"

    def function(self, simulation, period):
        depenses_electricite = simulation.calculate('poste_coicop_451', period)
        depenses_electricite_rank = depenses_electricite.argsort().argsort()
        depenses_electricite_percentile = depenses_electricite_rank / len(depenses_electricite_rank) * 100

        return period, depenses_electricite_percentile


class depenses_electricite_prix_unitaire(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Prix unitaire de l'électricité de chaque ménage, après affectation d'un compteur"

    def function(self, simulation, period):
        depenses_electricite_percentile = simulation.calculate('depenses_electricite_percentile', period)

        # Note : les barèmes ne donnent que les prix unitaires pour 3 et 6 kva. Pour les puissances supérieures,
        # les valeurs sont assez proches de celles du compteur 6kva que nous utilisons comme proxy.
        prix_unitaire_3kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_3_kva
        prix_unitaire_6kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva

        prix_unitaire = (
            (depenses_electricite_percentile < 4) * prix_unitaire_3kva +
            (depenses_electricite_percentile > 4) * prix_unitaire_6kva
            )

        return period, prix_unitaire


class depenses_electricite_tarif_fixe(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Dépenses en électricité des ménages sur le coût fixe de l'abonnement, après affectation d'un compteur"

    def function(self, simulation, period):
        depenses_electricite_percentile = simulation.calculate('depenses_electricite_percentile', period)

        tarif_fixe_3kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_3_kva
        tarif_fixe_6kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_6_kva
        tarif_fixe_9kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_9_kva
        tarif_fixe_12kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_12_kva
        tarif_fixe_15kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_15_kva

        tarif_fixe = (
            (depenses_electricite_percentile < 4) * tarif_fixe_3kva +
            (depenses_electricite_percentile > 4) * (depenses_electricite_percentile < 52) * tarif_fixe_6kva +
            (depenses_electricite_percentile > 52) * (depenses_electricite_percentile < 78) * tarif_fixe_9kva +
            (depenses_electricite_percentile > 78) * (depenses_electricite_percentile < 88) * tarif_fixe_12kva +
            (depenses_electricite_percentile > 88) * tarif_fixe_15kva
            )

        return period, tarif_fixe


class depenses_electricite_variables(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Dépenses en électricité des ménages, hors coût fixe de l'abonnement"

    def function(self, simulation, period):
        depenses_electricite = simulation.calculate('poste_coicop_451', period)
        depenses_electricite_tarif_fixe = simulation.calculate('depenses_electricite_tarif_fixe', period)
        depenses_electricite_variables = depenses_electricite - depenses_electricite_tarif_fixe
        depenses_electricite_variables = numpy.maximum(depenses_electricite_variables, 0)

        return period, depenses_electricite_variables
