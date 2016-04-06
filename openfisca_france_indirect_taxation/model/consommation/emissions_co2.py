# -*- coding: utf-8 -*-

from __future__ import division


from ..base import * # noqa analysis:ignore


class emissions_CO2_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation de carburants, en kg de CO2"

    def function(self, simulation, period):
        quantites_diesel = simulation.calculate('quantites_diesel', period)
        quantites_essence = simulation.calculate('quantites_essence', period)
        emissions_diesel = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
        emissions_essence = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
        emissions = quantites_diesel * emissions_diesel + quantites_essence * emissions_essence  # Source : Ademe

        return period, emissions


class emissions_CO2_gaz(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation de gaz, en kg de CO2"

    def function(self, simulation, period):
        quantites_gaz = simulation.calculate('quantites_gaz_contrat_optimal', period)
        emissions_gaz = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_gaz
        emissions = quantites_gaz * emissions_gaz

        return period, emissions


class emissions_CO2_electricite(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation d'électricité, en kg de CO2"

    def function(self, simulation, period):
        quantites_eletricite = simulation.calculate('quantites_electricite_selon_compteur', period)
        emissions_electricite = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_electricite
        emissions = quantites_eletricite * emissions_electricite

        return period, emissions
