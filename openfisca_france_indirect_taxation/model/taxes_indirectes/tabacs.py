# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 14:56:23 2015

@author: thomas.douenne
"""

from __future__ import division


from ..base import *  # noqa analysis:ignore


class cigares_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les cigares"

    def function(menage, period, parameters):
        depenses_cigares = menage('depenses_cigares', period)
        taux_normal_cigare = parameters(period).imposition_indirecte.tabac.taux_normal.cigares
        return period, tax_from_expense_including_tax(depenses_cigares, taux_normal_cigare)


class cigarette_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les cigarettes"

    def function(menage, period, parameters):
        depenses_cigarettes = menage('depenses_cigarettes', period)
        taux_normal_cigarette = \
            parameters(period).imposition_indirecte.tabac.taux_normal.cigarettes
        return period, tax_from_expense_including_tax(depenses_cigarettes, taux_normal_cigarette)


class tabac_a_rouler_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur le tabac à rouler"

    def function(menage, period, parameters):
        depenses_tabac_a_rouler = menage('depenses_tabac_a_rouler', period)
        taux_normal_tabac_a_rouler = \
            parameters(period).imposition_indirecte.tabac.taux_normal.tabac_a_rouler
        return period, tax_from_expense_including_tax(depenses_tabac_a_rouler, taux_normal_tabac_a_rouler)


class total_tabac_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur le tabac "

    def function(menage, period, parameters):
        cigarette_droit_d_accise = menage('cigarette_droit_d_accise', period)
        cigares_droit_d_accise = menage('cigares_droit_d_accise', period)
        tabac_a_rouler_droit_d_accise = menage('tabac_a_rouler_droit_d_accise', period)
        return period, cigarette_droit_d_accise + cigares_droit_d_accise + tabac_a_rouler_droit_d_accise
