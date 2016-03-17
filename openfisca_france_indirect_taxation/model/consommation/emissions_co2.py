# -*- coding: utf-8 -*-

from __future__ import division


from ..base import * # noqa analysis:ignore


class emissions_CO2_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de co2 des ménages via leur consommation de carburants, en kg par litre de carburants"

    def function(self, simulation, period):
        quantites_diesel = simulation.calculate('quantites_diesel', period)
        quantites_essence = simulation.calculate('quantites_essence', period)
        emissions_diesel = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
        emissions_essence = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
        emissions = quantites_diesel * emissions_diesel + quantites_essence * emissions_essence  # Source : Ademe

        return period, emissions
