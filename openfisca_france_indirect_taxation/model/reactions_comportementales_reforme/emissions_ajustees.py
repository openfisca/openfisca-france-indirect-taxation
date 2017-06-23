# -*- coding: utf-8 -*-

from __future__ import division


from openfisca_france_indirect_taxation.model.base import * # noqa analysis:ignore


class emissions_CO2_carburants_ajustees(Variable):
    column = FloatCol
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation de carburants après réforme, en kg de CO2"

    def formula(self, simulation, period):
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


class emissions_CO2_electricite_ajustees(Variable):
    column = FloatCol
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation d'électricité après réforme, en kg de CO2"

    def formula(self, simulation, period):
        quantites_electricite_ajustees = simulation.calculate('quantites_electricite_ajustees_taxe_carbone', period)
        emissions_eletricite = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_electricite
        emissions_ajustees = quantites_electricite_ajustees * emissions_eletricite

        return period, emissions_ajustees


class emissions_CO2_gaz_ajustees(Variable):
    column = FloatCol
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation de gaz après réforme, en kg de CO2"

    def formula(self, simulation, period):
        quantites_gaz_ajustees = simulation.calculate('quantites_gaz_ajustees_taxe_carbone', period)
        emissions_gaz = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_gaz
        emissions_ajustees = quantites_gaz_ajustees * emissions_gaz

        return period, emissions_ajustees
