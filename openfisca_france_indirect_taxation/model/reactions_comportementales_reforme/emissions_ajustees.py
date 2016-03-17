# -*- coding: utf-8 -*-

from __future__ import division


from ..base import * # noqa analysis:ignore


class emissions_CO2_carburants_ajustees(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation de carburants après réforme, en kg de CO2"

    def function(self, simulation, period):
        quantites_diesel_ajustees = simulation.calculate('quantites_diesel_ajustees', period)
        quantites_essence_ajustees = simulation.calculate('quantites_essence_ajustees', period)
        emissions_diesel = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
        emissions_essence = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
        emissions_ajustees = (
            (quantites_diesel_ajustees * emissions_diesel) +
            (quantites_essence_ajustees * emissions_essence)
            )  # Source : Ademe

        return period, emissions_ajustees
