# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 14:59:41 2015

@author: thomas.douenne
"""

from __future__ import division


import datetime

from ..base import *  # noqa analysis:ignore


class tva_taux_intermediaire(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux intermediaire"

    @dated_function(start = datetime.date(2012, 1, 1))
    def function(menage, period, parameters):
        depenses_tva_taux_intermediaire = menage('depenses_tva_taux_intermediaire')
        taux_intermediaire = parameters(period).imposition_indirecte.tva.taux_intermediaire
        return period, tax_from_expense_including_tax(depenses_tva_taux_intermediaire, taux_intermediaire)


class tva_taux_plein(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux plein"

    def function(menage, period, parameters):
        depenses_tva_taux_plein = menage('depenses_tva_taux_plein', period)
        taux_plein = parameters(period).imposition_indirecte.tva.taux_plein
        return period, tax_from_expense_including_tax(depenses_tva_taux_plein, taux_plein)


class tva_taux_reduit(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux reduit"

    def function(menage, period, parameters):
        depenses_tva_taux_reduit = menage('depenses_tva_taux_reduit', period)
        taux_reduit = parameters(period).imposition_indirecte.tva.taux_reduit
        return period, tax_from_expense_including_tax(depenses_tva_taux_reduit, taux_reduit)


class tva_taux_super_reduit(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux super reduit"

    def function(menage, period, parameters):
        depenses_tva_taux_super_reduit = menage('depenses_tva_taux_super_reduit', period)
        taux_super_reduit = parameters(period).imposition_indirecte.tva.taux_super_reduit
        return period, tax_from_expense_including_tax(depenses_tva_taux_super_reduit, taux_super_reduit)


class tva_total(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée"

    def function(menage, period, parameters):
        tva_taux_super_reduit = menage('tva_taux_super_reduit', period)
        tva_taux_reduit = menage('tva_taux_reduit', period)
        tva_taux_intermediaire = menage('tva_taux_intermediaire', period)
        tva_taux_plein = menage('tva_taux_plein', period)
        return period, (
            tva_taux_super_reduit +
            tva_taux_reduit +
            tva_taux_intermediaire +
            tva_taux_plein
            )
