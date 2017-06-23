# -*- coding: utf-8 -*-

from __future__ import division


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class depenses_diesel(Variable):
    column = FloatCol
    entity = Menage
    label = u"Construction par pondération des dépenses spécifiques au diesel"

    def formula(self, simulation, period):
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
    entity = Menage
    label = u"Calcul du montant de TICPE sur le diesel"

    def formula(self, simulation, period):
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


class diesel_ticpe_ajustee(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de TICPE sur le diesel après réforme"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        reforme_diesel = simulation.legislation_at(period.start).taxes_carburants.diesel
        accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
        taux_implicite_diesel_ajuste = (
            (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
            (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
            )

        depenses_diesel_ajustees = simulation.calculate('depenses_diesel_ajustees', period)
        depenses_diesel_htva_ajustees = (
            depenses_diesel_ajustees - tax_from_expense_including_tax(depenses_diesel_ajustees, taux_plein_tva)
            )
        montant_diesel_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
            )

        return period, montant_diesel_ticpe_ajuste


class depenses_essence(Variable):
    column = FloatCol
    entity = Menage
    label = u"Construction par déduction des dépenses spécifiques à l'essence"

    def formula(self, simulation, period):
        depenses_carburants = simulation.calculate('depenses_carburants', period)
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        depenses_essence = depenses_carburants - depenses_diesel

        return period, depenses_essence


class depenses_sp_e10(Variable):
    column = FloatCol
    entity = Menage
    label = u"Construction par pondération des dépenses spécifiques au sans plomb e10"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10 = depenses_essence * part_sp_e10

        return period, depenses_sp_e10


class depenses_sp_95(Variable):
    column = FloatCol
    entity = Menage
    label = u"Construction par pondération des dépenses spécifiques au sans plomb 95"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95 = depenses_essence * part_sp95

        return period, depenses_sp_95


class depenses_sp_98(Variable):
    column = FloatCol
    entity = Menage
    label = u"Construction par pondération des dépenses spécifiques au sans plomb 98"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98 = depenses_essence * part_sp98

        return period, depenses_sp_98


class depenses_super_plombe(Variable):
    column = FloatCol
    entity = Menage
    label = u"Construction par pondération des dépenses spécifiques au super plombe"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe = depenses_essence * part_super_plombe

        return period, depenses_super_plombe


class essence_ticpe(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de la TICPE sur toutes les essences cumulées"

    def formula_1990(self, simulation, period):
        sp95_ticpe = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe = simulation.calculate('sp98_ticpe', period)
        super_plombe_ticpe = simulation.calculate('super_plombe_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe + super_plombe_ticpe)
        return period, essence_ticpe

    def formula_2007(self, simulation, period):
        sp95_ticpe = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe = simulation.calculate('sp98_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe)
        return period, essence_ticpe

    def formula_2009(self, simulation, period):
        sp95_ticpe = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe = simulation.calculate('sp98_ticpe', period)
        sp_e10_ticpe = simulation.calculate('sp_e10_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe + sp_e10_ticpe)
        return period, essence_ticpe


class essence_ticpe_ajustee(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"

    def formula_1990(self, simulation, period):
        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee', period)
        super_plombe_ticpe_ajustee = simulation.calculate('super_plombe_ticpe_ajustee', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    def formula_2007(self, simulation, period):
        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    def formula_2009(self, simulation, period):
        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee', period)
        sp_e10_ticpe_ajustee = simulation.calculate('sp_e10_ticpe_ajustee', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
        return period, essence_ticpe_ajustee


class sp_e10_ticpe(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de la TICPE sur le SP E10"

    def formula(self, simulation, period):
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


class sp_e10_ticpe_ajustee(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de la TICPE sur le SP E10 après réforme"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        try:
            accise_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10
            majoration_ticpe_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
        except:
            accise_ticpe_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10

        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
        taux_implicite_sp_e10_ajuste = (
            (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva)) /
            (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees = simulation.calculate('depenses_essence_ajustees', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        sp_e10_depenses_ajustees = depenses_essence_ajustees * part_sp_e10
        sp_e10_depenses_htva_ajustees = \
            sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
        montant_sp_e10_ticpe_ajuste = \
            tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

        return period, montant_sp_e10_ticpe_ajuste


class sp95_ticpe(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de TICPE sur le sp_95"

    def formula(self, simulation, period):
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


class sp95_ticpe_ajustee(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de TICPE sur le sp_95 après réforme"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        super_95_ttc_ajuste = super_95_ttc + reforme_essence
        taux_implicite_sp95_ajuste = (
            (accise_ticpe_super95_ajustee * (1 + taux_plein_tva)) /
            (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees = simulation.calculate('depenses_essence_ajustees', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95_ajustees = depenses_essence_ajustees * part_sp95
        depenses_sp_95_htva_ajustees = (
            depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
            )
        montant_sp95_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
            )

        return period, montant_sp95_ticpe_ajuste


class sp98_ticpe(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de TICPE sur le sp_98"

    def formula(self, simulation, period):
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


class sp98_ticpe_ajustee(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de TICPE sur le sp_98 après réforme"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        super_98_ttc_ajuste = super_98_ttc + reforme_essence
        taux_implicite_sp98_ajuste = (
            (accise_ticpe_super98_ajustee * (1 + taux_plein_tva)) /
            (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees = simulation.calculate('depenses_essence_ajustees', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98_ajustees = depenses_essence_ajustees * part_sp98
        depenses_sp_98_htva_ajustees = (
            depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
            )
        montant_sp98_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
            )

        return period, montant_sp98_ticpe_ajuste


class super_plombe_ticpe(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de la TICPE sur le super plombé"

    def formula(self, simulation, period):
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


class super_plombe_ticpe_ajustee(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de la TICPE sur le super plombé après réforme"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
        taux_implicite_super_plombe_ajuste = (
            (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva)) /
            (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees = simulation.calculate('depenses_essence_ajustees', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees * part_super_plombe
        depenses_super_plombe_htva_ajustees = (
            depenses_super_plombe_ajustees -
            tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
            )
        montant_super_plombe_ticpe_ajuste = \
            tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

        return period, montant_super_plombe_ticpe_ajuste


class ticpe_totale(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de la TICPE sur tous les carburants cumulés"

    def formula(self, simulation, period):
        essence_ticpe = simulation.calculate('essence_ticpe', period)
        diesel_ticpe = simulation.calculate('diesel_ticpe', period)
        ticpe_totale = diesel_ticpe + essence_ticpe

        return period, ticpe_totale


class ticpe_totale_ajustee(Variable):
    column = FloatCol
    entity = Menage
    label = u"Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

    def formula(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee', period)
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee', period)
        ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

        return period, ticpe_totale_ajustee


class difference_ticpe_diesel_reforme(Variable):
    column = FloatCol
    entity = Menage
    label = u"Différence entre les contributions à la TICPE sur le diesel avant et après la réforme"

    def formula(self, simulation, period):
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee', period)
        diesel_ticpe = simulation.calculate('diesel_ticpe', period)
        difference = diesel_ticpe_ajustee - diesel_ticpe

        return period, difference


class difference_ticpe_essence_reforme(Variable):
    column = FloatCol
    entity = Menage
    label = u"Différence entre les contributions à la TICPE sur l'essence avant et après la réforme"

    def formula(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee', period)
        essence_ticpe = simulation.calculate('essence_ticpe', period)
        difference = essence_ticpe_ajustee - essence_ticpe

        return period, difference


class difference_ticpe_totale_reforme(Variable):
    column = FloatCol
    entity = Menage
    label = u"Différence entre les contributions à la TICPE avant et après la réforme"

    def formula(self, simulation, period):
        ticpe_totale_ajustee = simulation.calculate('ticpe_totale_ajustee', period)
        ticpe_totale = simulation.calculate('ticpe_totale', period)
        difference = ticpe_totale_ajustee - ticpe_totale

        return period, difference
