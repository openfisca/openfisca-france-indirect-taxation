# -*- coding: utf-8 -*-

from __future__ import division


from datetime import date

from ..base import *  # noqa analysis:ignore


class contributions_additionnelles_gaz_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Recettes de la hausse de cce 2014-2015 sur la consommation de gaz - ceteris paribus"
    # On considère que les contributions sur les taxes précédentes ne sont pas affectées

    def function(self, simulation, period):
        quantites_gaz_ajustees = simulation.calculate('quantites_gaz_ajustees_cce_2014_2015', period)
        reforme_gaz = simulation.legislation_at(period.start).contribution_climat_energie_reforme.gaz_2014_2015
        recettes_gaz = quantites_gaz_ajustees * reforme_gaz

        return period, recettes_gaz


class contribution_tva_taux_plein_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Contribution sur la TVA à taux plein après réaction à la réforme - cce 2014-2015"

    def function(self, simulation, period):
        depenses_tva_taux_plein_ajustees = \
            simulation.calculate('depenses_tva_taux_plein_ajustees_cce_2014_2015', period)

        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = (
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_plein_2014_2015
            )
        nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

        return period, tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)


class contribution_tva_taux_plein_bis_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Contribution sur la TVA à taux plein après réaction à la réforme - cce 2014-2015"

    def function(self, simulation, period):
        depenses_tva_taux_plein_ajustees = \
            simulation.calculate('depenses_tva_taux_plein_bis_ajustees_cce_2014_2015', period)

        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = (
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_plein_bis_2014_2015
            )
        nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

        return period, tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)


class contribution_tva_taux_reduit_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Contribution sur la TVA à taux reduit après réaction à la réforme - cce 2014-2015"

    def function(self, simulation, period):
        depenses_tva_taux_reduit_ajustees = \
            simulation.calculate('depenses_tva_taux_reduit_ajustees_cce_2014_2015', period)

        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        abaissement_tva_taux_reduit = \
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_reduit_2014_2015
        nouveau_taux_reduit = taux_reduit - abaissement_tva_taux_reduit

        return period, tax_from_expense_including_tax(depenses_tva_taux_reduit_ajustees, nouveau_taux_reduit)


class contribution_tva_taux_super_reduit_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Contribution sur la TVA à taux super reduit après réaction à la réforme - cce 2014-2015"

    def function(self, simulation, period):
        depenses_tva_taux_super_reduit_ajustees = \
            simulation.calculate('depenses_tva_taux_super_reduit_ajustees_cce_2014_2015', period)

        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        abaissement_tva_taux_super_reduit = \
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_super_reduit_2014_2015
        nouveau_taux_super_reduit = taux_super_reduit - abaissement_tva_taux_super_reduit

        return period, \
            tax_from_expense_including_tax(depenses_tva_taux_super_reduit_ajustees, nouveau_taux_super_reduit)


class diesel_ticpe_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le diesel après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        reforme_diesel = simulation.legislation_at(period.start).contribution_climat_energie_reforme.diesel_2014_2015
        accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
        taux_implicite_diesel_ajuste = (
            (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
            (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
            )

        depenses_diesel_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_diesel_ajustees_cce_2014_2015', period)
        depenses_diesel_htva_ajustees = (
            depenses_diesel_ajustees_cce_2014_2015 -
            tax_from_expense_including_tax(depenses_diesel_ajustees_cce_2014_2015, taux_plein_tva)
            )
        montant_diesel_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
            )

        return period, montant_diesel_ticpe_ajuste


class difference_contribution_energie_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions aux taxes sur l'énergie après la hausse cce 2014-2015"

    def function(self, simulation, period):
        contribution_diesel = simulation.calculate('difference_ticpe_diesel_cce_2014_2015', period)
        contribution_essence = simulation.calculate('difference_ticpe_essence_cce_2014_2015', period)
        contribution_gaz = simulation.calculate('contributions_additionnelles_gaz_cce_2014_2015', period)
        ticpe_fioul_domestique_ajustee = simulation.calculate('fioul_domestique_ticpe_ajustees_cce_2014_2015', period)
        ticpe_fioul_domestique = simulation.calculate('fioul_domestique_ticpe', period)
        contribution_fioul = ticpe_fioul_domestique_ajustee - ticpe_fioul_domestique

        total = contribution_diesel + contribution_essence + contribution_fioul + contribution_gaz

        return period, total


class difference_contribution_totale_cce_2014_2015_tva_plein(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence de contribution totale après réaction à la réforme et redistribution - cce 2014-2015"

    def function(self, simulation, period):
        contribution = simulation.calculate('difference_contribution_energie_cce_2014_2015', period)
        redistribution = simulation.calculate('difference_contribution_tva_taux_plein_cce_2014_2015', period)
        difference = redistribution - contribution

        return period, difference


class difference_contribution_totale_cce_2014_2015_tva_plein_reduit_super_reduit(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence de contribution totale après réaction à la réforme et redistribution - cce 2014-2015"

    def function(self, simulation, period):
        contribution = simulation.calculate('difference_contribution_energie_cce_2014_2015', period)
        redistribution = \
            simulation.calculate('difference_contribution_tva_plein_reduit_super_reduit_cce_2014_2015', period)
        difference = redistribution - contribution

        return period, difference


class difference_contribution_tva_taux_plein_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence de contribution sur la TVA à taux plein après réaction à la réforme - cce 2014-2015"

    def function(self, simulation, period):
        contribution = simulation.calculate('tva_taux_plein', period)
        contribution_ajustee = simulation.calculate('contribution_tva_taux_plein_ajustee_cce_2014_2015', period)
        difference = contribution - contribution_ajustee

        return period, difference


class difference_contribution_tva_plein_reduit_super_reduit_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence de contribution sur la TVA après réaction à la réforme - cce 2014-2015"

    def function(self, simulation, period):
        contribution_plein = simulation.calculate('tva_taux_plein', period)
        contribution_reduit = simulation.calculate('tva_taux_reduit', period)
        contribution_super_reduit = simulation.calculate('tva_taux_super_reduit', period)
        contribution_plein_ajustee = \
            simulation.calculate('contribution_tva_taux_plein_bis_ajustee_cce_2014_2015', period)
        contribution_reduit_ajustee = \
            simulation.calculate('contribution_tva_taux_reduit_ajustee_cce_2014_2015', period)
        contribution_super_reduit_ajustee = \
            simulation.calculate('contribution_tva_taux_super_reduit_ajustee_cce_2014_2015', period)
        difference = (
            (contribution_plein + contribution_reduit + contribution_super_reduit) -
            (contribution_plein_ajustee + contribution_reduit_ajustee + contribution_super_reduit_ajustee)
            )

        return period, difference


class difference_ticpe_diesel_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE sur le diesel avant et après la réforme"

    def function(self, simulation, period):
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee_cce_2014_2015', period)
        diesel_ticpe = simulation.calculate('diesel_ticpe', period)
        difference = diesel_ticpe_ajustee - diesel_ticpe

        return period, difference


class difference_ticpe_essence_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Différence entre les contributions à la TICPE sur l'essence avant et après la réforme"

    def function(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee_cce_2014_2015', period)
        essence_ticpe = simulation.calculate('essence_ticpe', period)
        difference = essence_ticpe_ajustee - essence_ticpe

        return period, difference


class essence_ticpe_ajustee_cce_2014_2015(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_cce_2014_2015', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_cce_2014_2015', period)
        super_plombe_ticpe_ajustee = simulation.calculate('super_plombe_ticpe_ajustee_cce_2014_2015', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_cce_2014_2015', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_cce_2014_2015', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe_ajustee_cce_2014_2015', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe_ajustee_cce_2014_2015', period)
        sp_e10_ticpe_ajustee = simulation.calculate('sp_e10_ticpe_ajustee_cce_2014_2015', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
        return period, essence_ticpe_ajustee


class fioul_domestique_ticpe_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le fioul domestique après réforme - hausse cce 2014-2015"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        accise_fioul_ticpe = (
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.gazole_fioul_domestique_hectolitre / 100
            )
        reforme_fioul = \
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.fioul_domestique_2014_2015
        accise_fioul_ajustee = accise_fioul_ticpe + reforme_fioul
        prix_fioul_ttc = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
        prix_fioul_ttc_ajuste = prix_fioul_ttc + reforme_fioul

        taux_implicite_fioul_ajuste = (
            (accise_fioul_ajustee * (1 + taux_plein_tva)) /
            (prix_fioul_ttc_ajuste - accise_fioul_ajustee * (1 + taux_plein_tva))
            )

        depenses_fioul_ajustees = simulation.calculate('depenses_fioul_domestique_ajustees_cce_2014_2015', period)
        depenses_fioul_ajustees_htva = \
            depenses_fioul_ajustees - tax_from_expense_including_tax(depenses_fioul_ajustees, taux_plein_tva)
        montant_fioul_ticpe_ajuste = \
            tax_from_expense_including_tax(depenses_fioul_ajustees_htva, taux_implicite_fioul_ajuste)

        return period, montant_fioul_ticpe_ajuste


class sp_e10_ticpe_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le SP E10 après réforme"

    def function(self, simulation, period):
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

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
        taux_implicite_sp_e10_ajuste = (
            (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva)) /
            (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        sp_e10_depenses_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_sp_e10
        sp_e10_depenses_htva_ajustees = \
            sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
        montant_sp_e10_ticpe_ajuste = \
            tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

        return period, montant_sp_e10_ticpe_ajuste


class sp95_ticpe_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_95 après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        super_95_ttc_ajuste = super_95_ttc + reforme_essence
        taux_implicite_sp95_ajuste = (
            (accise_ticpe_super95_ajustee * (1 + taux_plein_tva)) /
            (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_sp95
        depenses_sp_95_htva_ajustees = (
            depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
            )
        montant_sp95_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
            )

        return period, montant_sp95_ticpe_ajuste


class sp98_ticpe_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de TICPE sur le sp_98 après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        super_98_ttc_ajuste = super_98_ttc + reforme_essence
        taux_implicite_sp98_ajuste = (
            (accise_ticpe_super98_ajustee * (1 + taux_plein_tva)) /
            (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_sp98
        depenses_sp_98_htva_ajustees = (
            depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
            )
        montant_sp98_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
            )

        return period, montant_sp98_ticpe_ajuste


class super_plombe_ticpe_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur le super plombé après réforme"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
        taux_implicite_super_plombe_ajuste = (
            (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva)) /
            (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_super_plombe
        depenses_super_plombe_htva_ajustees = (
            depenses_super_plombe_ajustees -
            tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
            )
        montant_super_plombe_ticpe_ajuste = \
            tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

        return period, montant_super_plombe_ticpe_ajuste


class ticpe_totale_ajustee_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

    def function(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe_ajustee_cce_2014_2015', period)
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe_ajustee_cce_2014_2015', period)
        ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

        return period, ticpe_totale_ajustee
