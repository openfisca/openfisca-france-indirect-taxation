# -*- coding: utf-8 -*-

from __future__ import division


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class cigares_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Montant des droits d'accises sur les cigares"

    def formula(self, simulation, period):
        depenses_cigares = simulation.calculate('depenses_cigares', period)
        taux_normal_cigare = simulation.legislation_at(period.start).imposition_indirecte.tabac.taux_normal.cigares
        return period, tax_from_expense_including_tax(depenses_cigares, taux_normal_cigare)


class cigarette_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Montant des droits d'accises sur les cigarettes"

    def formula(self, simulation, period):
        depenses_cigarettes = simulation.calculate('depenses_cigarettes', period)
        taux_normal_cigarette = \
            simulation.legislation_at(period.start).imposition_indirecte.tabac.taux_normal.cigarettes
        return period, tax_from_expense_including_tax(depenses_cigarettes, taux_normal_cigarette)


class depenses_cigares(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Dépenses de cigares"

    def formula(self, simulation, period):
        return period, simulation.calculate('poste_02_2_2', period)


class depenses_cigarettes(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Dépenses de cigarettes"

    def formula(self, simulation, period):
        return period, simulation.calculate('poste_02_2_1', period)


class depenses_tabac_a_rouler(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Dépenses de tabac à rouler et autres tabacs"

    def formula(self, simulation, period):
        return period, simulation.calculate('poste_02_2_3', period)


class tabac_a_rouler_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Montant des droits d'accises sur le tabac à rouler"

    def formula(self, simulation, period):
        depenses_tabac_a_rouler = simulation.calculate('depenses_tabac_a_rouler', period)
        taux_normal_tabac_a_rouler = \
            simulation.legislation_at(period.start).imposition_indirecte.tabac.taux_normal.tabac_a_rouler
        return period, tax_from_expense_including_tax(depenses_tabac_a_rouler, taux_normal_tabac_a_rouler)


class total_tabac_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Montant des droits d'accises sur le tabac "

    def formula(self, simulation, period):
        cigarette_droit_d_accise = simulation.calculate('cigarette_droit_d_accise', period)
        cigares_droit_d_accise = simulation.calculate('cigares_droit_d_accise', period)
        tabac_a_rouler_droit_d_accise = simulation.calculate('tabac_a_rouler_droit_d_accise', period)
        return period, cigarette_droit_d_accise + cigares_droit_d_accise + tabac_a_rouler_droit_d_accise
