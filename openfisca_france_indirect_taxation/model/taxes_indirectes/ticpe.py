# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 14:51:33 2015

@author: thomas.douenne
"""

from __future__ import division


from datetime import date

from ..base import *  # noqa analysis:ignore


class depenses_diesel(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Construction par pondération des dépenses spécifiques au diesel"

    def function(menage, period, parameters):
        conso_totale_vp_diesel = parameters(period).imposition_indirecte.quantite_carbu_vp.diesel
        conso_totale_vp_essence = parameters(period).imposition_indirecte.quantite_carbu_vp.essence
        taille_parc_diesel = parameters(period).imposition_indirecte.parc_vp.diesel
        taille_parc_essence = parameters(period).imposition_indirecte.parc_vp.essence

        conso_moyenne_vp_diesel = conso_totale_vp_diesel / taille_parc_diesel
        conso_moyenne_vp_essence = conso_totale_vp_essence / taille_parc_essence

        nombre_vehicules_diesel = menage('veh_diesel', period)
        nombre_vehicules_essence = menage('veh_essence', period)
        nombre_vehicules_total = nombre_vehicules_diesel + nombre_vehicules_essence

        # to compute part_conso_diesel we need to avoid dividing by zero for those we do not have any vehicle
        # Thus, we choose arbitrarily to divide it by 1, but this choice won't affect the result as long as it is not 0
        denominateur = (
            (nombre_vehicules_diesel * conso_moyenne_vp_diesel) + (nombre_vehicules_essence * conso_moyenne_vp_essence)
            ) * (nombre_vehicules_total != 0) + 1 * (nombre_vehicules_total == 0)

        part_conso_diesel = (nombre_vehicules_diesel * conso_moyenne_vp_diesel) / denominateur

        depenses_carburants = menage('depenses_carburants', period)

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

    def function(menage, period, parameters):
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                parameters(period).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = parameters(period).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = parameters(period).imposition_indirecte.ticpe.ticpe_gazole

        prix_diesel_ttc = parameters(period).imposition_indirecte.prix_carburants.diesel_ttc
        taux_implicite_diesel = (
            (accise_diesel_ticpe * (1 + taux_plein_tva)) /
            (prix_diesel_ttc - accise_diesel_ticpe * (1 + taux_plein_tva))
            )

        depenses_diesel = menage('depenses_diesel', period)
        depenses_diesel_htva = depenses_diesel - tax_from_expense_including_tax(depenses_diesel, taux_plein_tva)
        montant_diesel_ticpe = tax_from_expense_including_tax(depenses_diesel_htva, taux_implicite_diesel)

        return period, montant_diesel_ticpe


class depenses_essence(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Construction par pondération des dépenses spécifiques à l'essence"

    def function(menage, period, parameters):
        depenses_carburants = menage('depenses_carburants', period)
        depenses_diesel = menage('depenses_diesel', period)
        depenses_essence = depenses_carburants - depenses_diesel

        return period, depenses_essence


class essence_ticpe(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur toutes les essences cumulées"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(menage, period, parameters):

        sp95_ticpe = menage('sp95_ticpe', period)
        sp98_ticpe = menage('sp98_ticpe', period)
        super_plombe_ticpe = menage('super_plombe_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe + super_plombe_ticpe)
        return period, essence_ticpe

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(menage, period, parameters):

        sp95_ticpe = menage('sp95_ticpe', period)
        sp98_ticpe = menage('sp98_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe)
        return period, essence_ticpe

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(menage, period, parameters):

        sp95_ticpe = menage('sp95_ticpe', period)
        sp98_ticpe = menage('sp98_ticpe', period)
        sp_e10_ticpe = menage('sp_e10_ticpe', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe + sp_e10_ticpe)
        return period, essence_ticpe


class sp_e10_ticpe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le SP E10"

    def function(menage, period, parameters):
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_plein
        try:
            accise_super_e10 = \
                parameters(period).imposition_indirecte.ticpe.ticpe_super_e10
            majoration_ticpe_super_e10 = \
                parameters(period).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
        except:
            accise_super_e10 = \
                parameters(period).imposition_indirecte.ticpe.ticpe_super_e10

        super_95_e10_ttc = parameters(period).imposition_indirecte.prix_carburants.super_95_e10_ttc
        taux_implicite_sp_e10 = (
            (accise_ticpe_super_e10 * (1 + taux_plein_tva)) /
            (super_95_e10_ttc - accise_ticpe_super_e10 * (1 + taux_plein_tva))
            )
        depenses_essence = menage('depenses_essence', period)
        part_sp_e10 = parameters(period).imposition_indirecte.part_type_supercarburants.sp_e10
        sp_e10_depenses = depenses_essence * part_sp_e10
        sp_e10_depenses_htva = \
            sp_e10_depenses - tax_from_expense_including_tax(sp_e10_depenses, taux_plein_tva)
        montant_sp_e10_ticpe = \
            tax_from_expense_including_tax(sp_e10_depenses_htva, taux_implicite_sp_e10)

        return period, montant_sp_e10_ticpe


class sp95_ticpe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_95"

    def function(menage, period, parameters):
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = parameters(period).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                parameters(period).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = parameters(period).imposition_indirecte.ticpe.ticpe_super9598

        super_95_ttc = parameters(period).imposition_indirecte.prix_carburants.super_95_ttc
        taux_implicite_sp95 = (
            (accise_ticpe_super95 * (1 + taux_plein_tva)) /
            (super_95_ttc - accise_ticpe_super95 * (1 + taux_plein_tva))
            )
        depenses_essence = menage('depenses_essence', period)
        part_sp95 = parameters(period).imposition_indirecte.part_type_supercarburants.sp_95
        sp95_depenses = depenses_essence * part_sp95
        sp95_depenses_htva = sp95_depenses - tax_from_expense_including_tax(sp95_depenses, taux_plein_tva)
        montant_sp95_ticpe = tax_from_expense_including_tax(sp95_depenses_htva, taux_implicite_sp95)

        return period, montant_sp95_ticpe


class sp98_ticpe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_98"

    def function(menage, period, parameters):
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = parameters(period).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                parameters(period).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = parameters(period).imposition_indirecte.ticpe.ticpe_super9598

        super_98_ttc = parameters(period).imposition_indirecte.prix_carburants.super_98_ttc
        taux_implicite_sp98 = (
            (accise_ticpe_super98 * (1 + taux_plein_tva)) /
            (super_98_ttc - accise_ticpe_super98 * (1 + taux_plein_tva))
            )
        depenses_essence = menage('depenses_essence', period)
        part_sp98 = parameters(period).imposition_indirecte.part_type_supercarburants.sp_98
        sp98_depenses = depenses_essence * part_sp98
        sp98_depenses_htva = sp98_depenses - tax_from_expense_including_tax(sp98_depenses, taux_plein_tva)
        montant_sp98_ticpe = tax_from_expense_including_tax(sp98_depenses_htva, taux_implicite_sp98)

        return period, montant_sp98_ticpe


class super_plombe_ticpe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le super plombé"

    def function(menage, period, parameters):
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            parameters(period).imposition_indirecte.ticpe.super_plombe_ticpe
        super_plombe_ttc = parameters(period).imposition_indirecte.prix_carburants.super_plombe_ttc
        taux_implicite_super_plombe = (
            (accise_super_plombe_ticpe * (1 + taux_plein_tva)) /
            (super_plombe_ttc - accise_super_plombe_ticpe * (1 + taux_plein_tva))
            )
        depenses_essence = menage('depenses_essence', period)
        part_super_plombe = \
            parameters(period).imposition_indirecte.part_type_supercarburants.super_plombe
        super_plombe_depenses = depenses_essence * part_super_plombe
        super_plombe_depenses_htva = \
            super_plombe_depenses - tax_from_expense_including_tax(super_plombe_depenses, taux_plein_tva)
        montant_super_plombe_ticpe = \
            tax_from_expense_including_tax(super_plombe_depenses_htva, taux_implicite_super_plombe)

        return period, montant_super_plombe_ticpe


class ticpe_totale(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur tous les carburants cumulés"

    def function(menage, period, parameters):
        essence_ticpe = menage('essence_ticpe', period)
        diesel_ticpe = menage('diesel_ticpe', period)
        ticpe_totale = diesel_ticpe + essence_ticpe

        return period, ticpe_totale
