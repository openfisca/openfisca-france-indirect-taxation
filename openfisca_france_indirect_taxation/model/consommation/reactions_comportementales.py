# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 10:56:52 2016

@author: thomas.douenne
"""

from __future__ import division


from ..base import * # noqa analysis:ignore


class carburants_elasticite_prix(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Elasticite prix carburants"


class depenses_essence_ajustees(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence après réaction à la réforme des prix"

    def function(menage, period, parameters):
        depenses_essence = menage('depenses_essence', period)
        super_95_ttc = parameters(period).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = 30
        # parameters(period).imposition_indirecte.prix_carburants.reforme_essence
        carburants_elasticite_prix = menage('carburants_elasticite_prix')
        depenses_essence_ajustees = \
            depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence / super_95_ttc)
        return period, depenses_essence_ajustees


class depenses_diesel_ajustees(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en diesel après réaction à la réforme des prix"

    def function(menage, period, parameters):
        depenses_diesel = menage('depenses_diesel', period)
        diesel_ttc = parameters(period).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = parameters(period).imposition_indirecte.prix_carburants.reforme_diesel
        carburants_elasticite_prix = menage('carburants_elasticite_prix')
        depenses_essence_ajustees = \
            depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)
        return period, depenses_essence_ajustees
