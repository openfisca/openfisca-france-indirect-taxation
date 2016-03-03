# -*- coding: utf-8 -*-

from __future__ import division


from ..base import * # noqa analysis:ignore


class emissions_co2_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de co2 des ménages via leur consommation de carburants, en kg par litre de carburants"

    def function(self, simulation, period):
        quantites_diesel = simulation.calculate('quantites_diesel', period)
        quantites_essence = simulation.calculate('quantites_essence', period)
        emissions = quantites_diesel * 2.66 + quantites_essence * 2.42  # Source : Ademe

        return period, emissions


class emissions_co2_carburants_ajustees(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de co2 des ménages via leur consommation de carburants après réforme, en kg par litres"

    def function(self, simulation, period):
        quantites_diesel_ajustees = simulation.calculate('quantites_diesel_ajustees', period)
        quantites_essence_ajustees = simulation.calculate('quantites_essence_ajustees', period)
        emissions_ajustees = quantites_diesel_ajustees * 2.66 + quantites_essence_ajustees * 2.42  # Source : Ademe

        return period, emissions_ajustees
