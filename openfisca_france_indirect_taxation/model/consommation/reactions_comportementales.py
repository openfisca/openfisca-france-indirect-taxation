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

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = 30
        # simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.reforme_essence
        carburants_elasticite_prix = simulation.calculate('carburants_elasticite_prix')
        depenses_essence_ajustees = \
            depenses_essence * (1 + (carburants_elasticite_prix * reforme_essence / super_95_ttc))
        return period, depenses_essence_ajustees


class depenses_diesel_ajustees(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en diesel après réaction à la réforme des prix"

    def function(self, simulation, period):
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.reforme_diesel
        carburants_elasticite_prix = simulation.calculate('carburants_elasticite_prix')
        depenses_essence_ajustees = depenses_diesel * (1 + (carburants_elasticite_prix * reforme_diesel / diesel_ttc))
        return period, depenses_essence_ajustees
