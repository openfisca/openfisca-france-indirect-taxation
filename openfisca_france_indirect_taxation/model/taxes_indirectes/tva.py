# -*- coding: utf-8 -*-

from __future__ import division


import datetime

from ..base import *  # noqa analysis:ignore


class tva_taux_intermediaire(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux intermediaire"

    @dated_function(start = datetime.date(2012, 1, 1))
    def function(self, simulation, period):
        depenses_tva_taux_intermediaire = simulation.calculate('depenses_tva_taux_intermediaire')
        taux_intermediaire = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
        return period, tax_from_expense_including_tax(depenses_tva_taux_intermediaire, taux_intermediaire)


class tva_taux_plein(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux plein"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return period, tax_from_expense_including_tax(depenses_tva_taux_plein, taux_plein)


class tva_taux_reduit(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux reduit"

    def function(self, simulation, period):
        depenses_tva_taux_reduit = simulation.calculate('depenses_tva_taux_reduit', period)
        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        return period, tax_from_expense_including_tax(depenses_tva_taux_reduit, taux_reduit)


class tva_taux_super_reduit(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux super reduit"

    def function(self, simulation, period):
        depenses_tva_taux_super_reduit = simulation.calculate('depenses_tva_taux_super_reduit', period)
        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        return period, tax_from_expense_including_tax(depenses_tva_taux_super_reduit, taux_super_reduit)


class tva_total(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée"

    def function(self, simulation, period):
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
