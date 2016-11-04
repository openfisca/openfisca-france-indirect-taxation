# -*- coding: utf-8 -*-

from __future__ import division


from openfisca_france_indirect_taxation.model.base import * # noqa analysis:ignore


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


class emissions_CO2_energies(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation d'énergies (sans combustibles solides), en kg de CO2"

    def function(self, simulation, period):
        emissions_carburants = simulation.calculate('emissions_CO2_carburants', period)
        emissions_electricite = simulation.calculate('emissions_CO2_electricite', period)
        emissions_fioul_domestique = simulation.calculate('emissions_CO2_fioul_domestique', period)
        emissions_gaz = simulation.calculate('emissions_CO2_gaz', period)

        emissions_energies = (
            emissions_carburants + emissions_electricite + emissions_fioul_domestique + emissions_gaz
            )
        return period, emissions_energies


class emissions_CO2_energies_logement(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation d'énergies pour le logement, en kg de CO2"

    def function(self, simulation, period):
        emissions_electricite = simulation.calculate('emissions_CO2_electricite', period)
        emissions_fioul_domestique = simulation.calculate('emissions_CO2_fioul_domestique', period)
        emissions_gaz = simulation.calculate('emissions_CO2_gaz', period)

        emissions_energies = (
            emissions_electricite + emissions_fioul_domestique + emissions_gaz
            )
        return period, emissions_energies


class emissions_CO2_fioul_domestique(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation de fioul domestique, en kg de CO2"

    def function(self, simulation, period):
        quantites_fioul = simulation.calculate('quantites_fioul_domestique', period)
        emissions_fioul = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_fioul_domestique
        emissions = quantites_fioul * emissions_fioul

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
