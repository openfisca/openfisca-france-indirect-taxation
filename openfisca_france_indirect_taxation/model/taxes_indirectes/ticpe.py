# -*- coding: utf-8 -*-

from __future__ import division


from datetime import date

from ..base import *  # noqa analysis:ignore


class depenses_diesel(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Construction par pondération des dépenses spécifiques au diesel"

    def function(self, simulation, period):
        conso_totale_vp_diesel = simulation.legislation_at(period.start).imposition_indirecte.quantite_carbu_vp.diesel
        conso_totale_vp_essence = simulation.legislation_at(period.start).imposition_indirecte.quantite_carbu_vp.essence
        taille_parc_diesel = simulation.legislation_at(period.start).imposition_indirecte.parc_vp.diesel
        taille_parc_essence = simulation.legislation_at(period.start).imposition_indirecte.parc_vp.essence

        conso_moyenne_vp_diesel = conso_totale_vp_diesel / taille_parc_diesel
        conso_moyenne_vp_essence = conso_totale_vp_essence / taille_parc_essence

        nombre_vehicules_diesel = simulation.calculate('veh_diesel', period)
        nombre_vehicules_essence = simulation.calculate('veh_essence', period)
        nombre_vehicules_total = nombre_vehicules_diesel + nombre_vehicules_essence

        # to compute part_conso_diesel we need to avoid dividing by zero for those we do not have any vehicle
        # Thus, we choose arbitrarily to divide it by 1, but this choice won't affect the result as long as it is not 0
        denominateur = (
            (nombre_vehicules_diesel * conso_moyenne_vp_diesel) + (nombre_vehicules_essence * conso_moyenne_vp_essence)
            ) * (nombre_vehicules_total != 0) + 1 * (nombre_vehicules_total == 0)

        part_conso_diesel = (nombre_vehicules_diesel * conso_moyenne_vp_diesel) / denominateur

        depenses_carburants = simulation.calculate('depenses_carburants', period)

        depenses_diesel = depenses_carburants * (
            (nombre_vehicules_total == 0) * (
                conso_totale_vp_diesel / (conso_totale_vp_diesel + conso_totale_vp_essence)
                ) +
            (nombre_vehicules_total != 0) * part_conso_diesel
            )

        return period, depenses_diesel


class diesel_ticpe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le diesel"

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

        depenses_diesel = simulation.calculate('depenses_diesel', period)
        depenses_diesel_htva = depenses_diesel - tax_from_expense_including_tax(depenses_diesel, taux_plein_tva)
        montant_diesel_ticpe = tax_from_expense_including_tax(depenses_diesel_htva, taux_implicite_diesel)

        return period, montant_diesel_ticpe


class depenses_essence(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Construction par déduction des dépenses spécifiques à l'essence"

    def function(self, simulation, period):
        depenses_carburants = simulation.calculate('depenses_carburants', period)
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        depenses_essence = depenses_carburants - depenses_diesel

        return period, depenses_essence


class depenses_sp_e10(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Construction par pondération des dépenses spécifiques au sans plomb e10"

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10 = depenses_essence * part_sp_e10

        return period, depenses_sp_e10


class depenses_sp_95(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Construction par pondération des dépenses spécifiques au sans plomb 95"

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95 = depenses_essence * part_sp95

        return period, depenses_sp_95


class depenses_sp_98(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Construction par pondération des dépenses spécifiques au sans plomb 98"

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98 = depenses_essence * part_sp98

        return period, depenses_sp_98


class depenses_super_plombe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Construction par pondération des dépenses spécifiques au super plombe"

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe = depenses_essence * part_super_plombe

        return period, depenses_super_plombe


class essence_ticpe(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur toutes les essences cumulées"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        sp95_ticpe = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe = simulation.calculate('sp98_ticpe', period)
        super_plombe_ticpe = simulation.calculate('super_plombe_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe + super_plombe_ticpe)
        return period, essence_ticpe

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        sp95_ticpe = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe = simulation.calculate('sp98_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe)
        return period, essence_ticpe

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        sp95_ticpe = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe = simulation.calculate('sp98_ticpe', period)
        sp_e10_ticpe = simulation.calculate('sp_e10_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe + sp_e10_ticpe)
        return period, essence_ticpe


class fioul_domestique_ticpe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le fioul domestique"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        accise_fioul_ticpe = (
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.gazole_fioul_domestique_hectolitre / 100
            )

        prix_fioul_ttc = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
        taux_implicite_fioul = (
            (accise_fioul_ticpe * (1 + taux_plein_tva)) /
            (prix_fioul_ttc - accise_fioul_ticpe * (1 + taux_plein_tva))
            )

        depenses_fioul = simulation.calculate('poste_coicop_453', period)
        depenses_fioul_htva = depenses_fioul - tax_from_expense_including_tax(depenses_fioul, taux_plein_tva)
        montant_fioul_ticpe = tax_from_expense_including_tax(depenses_fioul_htva, taux_implicite_fioul)

        return period, montant_fioul_ticpe


class sp_e10_ticpe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le SP E10"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
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
        depenses_sp_e10 = simulation.calculate('depenses_sp_e10', period)
        depenses_sp_e10_htva = \
            depenses_sp_e10 - tax_from_expense_including_tax(depenses_sp_e10, taux_plein_tva)
        montant_sp_e10_ticpe = \
            tax_from_expense_including_tax(depenses_sp_e10_htva, taux_implicite_sp_e10)

        return period, montant_sp_e10_ticpe


class sp95_ticpe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_95"

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
        depenses_sp_95 = simulation.calculate('depenses_sp_95', period)
        depenses_sp_95_htva = depenses_sp_95 - tax_from_expense_including_tax(depenses_sp_95, taux_plein_tva)
        montant_sp95_ticpe = tax_from_expense_including_tax(depenses_sp_95_htva, taux_implicite_sp95)

        return period, montant_sp95_ticpe


class sp98_ticpe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_98"

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
        depenses_sp_98 = simulation.calculate('depenses_sp_98', period)
        depenses_sp_98_htva = depenses_sp_98 - tax_from_expense_including_tax(depenses_sp_98, taux_plein_tva)
        montant_sp98_ticpe = tax_from_expense_including_tax(depenses_sp_98_htva, taux_implicite_sp98)

        return period, montant_sp98_ticpe


class super_plombe_ticpe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le super plombé"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        taux_implicite_super_plombe = (
            (accise_super_plombe_ticpe * (1 + taux_plein_tva)) /
            (super_plombe_ttc - accise_super_plombe_ticpe * (1 + taux_plein_tva))
            )
        depenses_super_plombe = simulation.calculate('depenses_super_plombe', period)
        depenses_super_plombe_htva = \
            depenses_super_plombe - tax_from_expense_including_tax(depenses_super_plombe, taux_plein_tva)
        montant_super_plombe_ticpe = \
            tax_from_expense_including_tax(depenses_super_plombe_htva, taux_implicite_super_plombe)

        return period, montant_super_plombe_ticpe


class ticpe_totale(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur tous les carburants cumulés"

    def function(self, simulation, period):
        essence_ticpe = simulation.calculate('essence_ticpe', period)
        diesel_ticpe = simulation.calculate('diesel_ticpe', period)
        ticpe_totale = diesel_ticpe + essence_ticpe

        return period, ticpe_totale


class total_taxes_energies(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant des taxes sur l'énergie, sauf électricité et gaz"

    def function(self, simulation, period):
        essence_ticpe = simulation.calculate('essence_ticpe', period)
        diesel_ticpe = simulation.calculate('diesel_ticpe', period)
        fioul_domestique_ticpe = simulation.calculate('fioul_domestique_ticpe', period)
        total = diesel_ticpe + essence_ticpe + fioul_domestique_ticpe

        return period, total
