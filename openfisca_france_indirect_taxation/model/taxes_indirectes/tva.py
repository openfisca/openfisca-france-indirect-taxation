# -*- coding: utf-8 -*-

from __future__ import division


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class depenses_tva_exonere(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses TTC des biens n'acquittant pas de TVA"

    def formula(self, simulation, period):
        return period, simulation.calculate('depenses_', period)


class depenses_tva_taux_intermediaire(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses TTC des biens acquittant la TVA à taux intermediaire"

    def formula_2012(self, simulation, period):
        depenses_ht_tva_taux_intermediaire = simulation.calculate('depenses_ht_tva_taux_intermediaire')
        taux_intermediaire = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
        return period, depenses_ht_tva_taux_intermediaire * (1 + taux_intermediaire)


class depenses_tva_taux_plein(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses TTC des biens acquittant la TVA acquitée à taux plein"

    def formula(self, simulation, period):
        depenses_ht_tva_taux_plein = simulation.calculate('depenses_ht_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return period, depenses_ht_tva_taux_plein * (1 + taux_plein)


class depenses_tva_taux_reduit(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses TTC des biens acquittant la TVA acquitée à taux reduit"

    def formula(self, simulation, period):
        depenses_ht_tva_taux_reduit = simulation.calculate('depenses_ht_tva_taux_reduit', period)
        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        return period, depenses_ht_tva_taux_reduit * (1 + taux_reduit)


class depenses_tva_taux_super_reduit(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses TTC des biens acquittant à taux super reduit"

    def formula(self, simulation, period):
        depenses_ht_tva_taux_super_reduit = simulation.calculate('depenses_ht_tva_taux_super_reduit', period)
        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        return period, depenses_ht_tva_taux_super_reduit * (1 + taux_super_reduit)


class tva_taux_intermediaire(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant de la TVA acquitée à taux intermediaire"

    def formula_2012(self, simulation, period):
        depenses_ht_tva_taux_intermediaire = simulation.calculate('depenses_ht_tva_taux_intermediaire')
        taux_intermediaire = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
        return period, depenses_ht_tva_taux_intermediaire * taux_intermediaire
        # tax_from_expense_including_tax(depenses_tva_taux_intermediaire, taux_intermediaire)


class tva_taux_plein(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant de la TVA acquitée à taux plein"

    def formula(self, simulation, period):
        depenses_ht_tva_taux_plein = simulation.calculate('depenses_ht_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return period, depenses_ht_tva_taux_plein * taux_plein
        # tax_from_expense_including_tax(depenses_tva_taux_plein, taux_plein)


class tva_taux_reduit(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant de la TVA acquitée à taux reduit"

    def formula(self, simulation, period):
        depenses_ht_tva_taux_reduit = simulation.calculate('depenses_ht_tva_taux_reduit', period)
        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        return period, depenses_ht_tva_taux_reduit * taux_reduit
        # tax_from_expense_including_tax(depenses_tva_taux_reduit, taux_reduit)


class tva_taux_super_reduit(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant de la TVA acquitée à taux super reduit"

    def formula(self, simulation, period):
        depenses_ht_tva_taux_super_reduit = simulation.calculate('depenses_ht_tva_taux_super_reduit', period)
        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        return period, depenses_ht_tva_taux_super_reduit * taux_super_reduit
        # tax_from_expense_including_tax(depenses_tva_taux_super_reduit, taux_super_reduit)


class tva_total(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant de la TVA acquitée"

    def formula(self, simulation, period):
        tva_taux_super_reduit = simulation.calculate('tva_taux_super_reduit', period)
        tva_taux_reduit = simulation.calculate('tva_taux_reduit', period)
        tva_taux_intermediaire = simulation.calculate('tva_taux_intermediaire', period)
        tva_taux_plein = simulation.calculate('tva_taux_plein', period)
        return period, (
            tva_taux_super_reduit +
            tva_taux_reduit +
            tva_taux_intermediaire +
            tva_taux_plein
            )
