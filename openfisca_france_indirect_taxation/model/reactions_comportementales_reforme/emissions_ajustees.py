# -*- coding: utf-8 -*-

from __future__ import division


from ..base import * # noqa analysis:ignore


class difference_emissions_CO2_carburants_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Variation des émissions de CO2 des ménages via leur conso de carburants après taxe carbu, en kg de CO2"

    def function(self, simulation, period):
        emissions_carburants = simulation.calculate('emissions_CO2_carburants', period)
        emissions_carburants_ajustees = \
            simulation.calculate('emissions_CO2_carburants_ajustees_taxes_carburants', period)
        difference_emissions = emissions_carburants - emissions_carburants_ajustees

        return period, difference_emissions


class difference_emissions_CO2_energies_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Variation des émissions de CO2 des ménages via leur conso d'énergies après hausse cce 14-15, en kg de CO2"

    def function(self, simulation, period):
        emissions_energies = simulation.calculate('emissions_CO2_energies', period)
        emissions_energies_ajustees = \
            simulation.calculate('emissions_CO2_energies_ajustees_cce_2014_2015', period)
        difference_emissions = emissions_energies - emissions_energies_ajustees

        return period, difference_emissions


class difference_emissions_CO2_energies_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Variation des émissions de CO2 des ménages via leur conso d'énergies après hausse cce 14-16, en kg de CO2"

    def function(self, simulation, period):
        emissions_energies = simulation.calculate('emissions_CO2_energies', period)
        emissions_energies_ajustees = \
            simulation.calculate('emissions_CO2_energies_ajustees_cce_2014_2016', period)
        difference_emissions = emissions_energies - emissions_energies_ajustees

        return period, difference_emissions


class difference_emissions_CO2_energies_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Variation des émissions de CO2 des ménages via leur conso d'énergies après taxe carbone, en kg de CO2"

    def function(self, simulation, period):
        emissions_energies = simulation.calculate('emissions_CO2_energies', period)
        emissions_energies_ajustees = \
            simulation.calculate('emissions_CO2_energies_ajustees_taxe_carbone', period)
        difference_emissions = emissions_energies - emissions_energies_ajustees

        return period, difference_emissions


class emissions_CO2_carburants_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur conso de carburants après réforme - cce 2014-2015 - en kg de CO2"

    def function(self, simulation, period):
        quantites_diesel_ajustees = simulation.calculate('quantites_diesel_ajustees_cce_2014_2015', period)
        quantites_essence_ajustees = simulation.calculate('quantites_essence_ajustees_cce_2014_2015', period)
        emissions_diesel = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
        emissions_essence = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
        emissions_ajustees = (
            (quantites_diesel_ajustees * emissions_diesel) +
            (quantites_essence_ajustees * emissions_essence)
            )  # Source : Ademe

        return period, emissions_ajustees


class emissions_CO2_carburants_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur conso de carburants après réforme - cce 2014-2016 - en kg de CO2"

    def function(self, simulation, period):
        quantites_diesel_ajustees = simulation.calculate('quantites_diesel_ajustees_cce_2014_2016', period)
        quantites_essence_ajustees = simulation.calculate('quantites_essence_ajustees_cce_2014_2016', period)
        emissions_diesel = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
        emissions_essence = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
        emissions_ajustees = (
            (quantites_diesel_ajustees * emissions_diesel) +
            (quantites_essence_ajustees * emissions_essence)
            )  # Source : Ademe

        return period, emissions_ajustees


class emissions_CO2_carburants_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation de carburants après réforme, en kg de CO2"

    def function(self, simulation, period):
        quantites_diesel_ajustees = simulation.calculate('quantites_diesel_ajustees_taxe_carbone', period)
        quantites_essence_ajustees = simulation.calculate('quantites_essence_ajustees_taxe_carbone', period)
        emissions_diesel = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
        emissions_essence = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
        emissions_ajustees = (
            (quantites_diesel_ajustees * emissions_diesel) +
            (quantites_essence_ajustees * emissions_essence)
            )  # Source : Ademe

        return period, emissions_ajustees


class emissions_CO2_carburants_ajustees_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation de carburants après réforme, en kg de CO2"

    def function(self, simulation, period):
        quantites_diesel_ajustees = simulation.calculate('quantites_diesel_ajustees_taxes_carburants', period)
        quantites_essence_ajustees = simulation.calculate('quantites_essence_ajustees_taxes_carburants', period)
        emissions_diesel = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
        emissions_essence = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
        emissions_ajustees = (
            (quantites_diesel_ajustees * emissions_diesel) +
            (quantites_essence_ajustees * emissions_essence)
            )  # Source : Ademe

        return period, emissions_ajustees


class emissions_CO2_energies_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur conso d'énergies après hausse cce 14-15, en kg de CO2"

    def function(self, simulation, period):
        emissions_carburants_ajustees = simulation.calculate('emissions_CO2_carburants_ajustees_cce_2014_2015', period)
        emissions_electricite_ajustees = simulation.calculate('emissions_CO2_electricite', period)
        emissions_fioul_domestique_ajustees = \
            simulation.calculate('emissions_CO2_fioul_domestique_ajustees_cce_2014_2015', period)
        emissions_gaz_ajustees = simulation.calculate('emissions_CO2_gaz_ajustees_cce_2014_2015', period)

        emissions_energies_ajustees = (
            emissions_carburants_ajustees + emissions_electricite_ajustees +
            emissions_fioul_domestique_ajustees + emissions_gaz_ajustees
            )
        return period, emissions_energies_ajustees


class emissions_CO2_energies_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur conso d'énergies après hausse cce 14-16, en kg de CO2"

    def function(self, simulation, period):
        emissions_carburants_ajustees = simulation.calculate('emissions_CO2_carburants_ajustees_cce_2014_2016', period)
        emissions_electricite_ajustees = simulation.calculate('emissions_CO2_electricite', period)
        emissions_fioul_domestique_ajustees = \
            simulation.calculate('emissions_CO2_fioul_domestique_ajustees_cce_2014_2016', period)
        emissions_gaz_ajustees = simulation.calculate('emissions_CO2_gaz_ajustees_cce_2014_2016', period)

        emissions_energies_ajustees = (
            emissions_carburants_ajustees + emissions_electricite_ajustees +
            emissions_fioul_domestique_ajustees + emissions_gaz_ajustees
            )
        return period, emissions_energies_ajustees


class emissions_CO2_energies_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur conso d'énergies après taxe carbone, en kg de CO2"

    def function(self, simulation, period):
        emissions_carburants_ajustees = simulation.calculate('emissions_CO2_carburants_ajustees_taxe_carbone', period)
        emissions_electricite_ajustees = simulation.calculate('emissions_CO2_electricite_ajustees_taxe_carbone', period)
        emissions_fioul_domestique_ajustees = \
            simulation.calculate('emissions_CO2_fioul_domestique_ajustees_taxe_carbone', period)
        emissions_gaz_ajustees = simulation.calculate('emissions_CO2_gaz_ajustees_taxe_carbone', period)

        emissions_energies_ajustees = (
            emissions_carburants_ajustees + emissions_electricite_ajustees +
            emissions_fioul_domestique_ajustees + emissions_gaz_ajustees
            )
        return period, emissions_energies_ajustees


class emissions_CO2_electricite_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation d'électricité après réforme, en kg de CO2"

    def function(self, simulation, period):
        quantites_electricite_ajustees = simulation.calculate('quantites_electricite_ajustees_taxe_carbone', period)
        emissions_eletricite = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_electricite
        emissions_ajustees = quantites_electricite_ajustees * emissions_eletricite

        return period, emissions_ajustees


class emissions_CO2_fioul_domestique_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur conso de fioul après réforme - hausse cce 2014-2015 - en kg de CO2"

    def function(self, simulation, period):
        quantites_fioul_ajustees = simulation.calculate('quantites_fioul_domestique_ajustees_cce_2014_2015', period)
        emissions_fioul = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_fioul_domestique
        emissions_ajustees = quantites_fioul_ajustees * emissions_fioul

        return period, emissions_ajustees


class emissions_CO2_fioul_domestique_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur conso de fioul après réforme - hausse cce 2014-2016 - en kg de CO2"

    def function(self, simulation, period):
        quantites_fioul_ajustees = simulation.calculate('quantites_fioul_domestique_ajustees_cce_2014_2016', period)
        emissions_fioul = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_fioul_domestique
        emissions_ajustees = quantites_fioul_ajustees * emissions_fioul

        return period, emissions_ajustees


class emissions_CO2_fioul_domestique_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation de fioul après réforme, en kg de CO2"

    def function(self, simulation, period):
        quantites_fioul_ajustees = simulation.calculate('quantites_fioul_domestique_ajustees_taxe_carbone', period)
        emissions_fioul = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_fioul_domestique
        emissions_ajustees = quantites_fioul_ajustees * emissions_fioul

        return period, emissions_ajustees


class emissions_CO2_gaz_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur conso de gaz après réforme - hausse cce 2014-2015 - en kg de CO2"

    def function(self, simulation, period):
        quantites_gaz_ajustees = simulation.calculate('quantites_gaz_ajustees_cce_2014_2015', period)
        emissions_gaz = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_gaz
        emissions_ajustees = quantites_gaz_ajustees * emissions_gaz

        return period, emissions_ajustees


class emissions_CO2_gaz_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur conso de gaz après réforme - hausse cce 2014-2016 - en kg de CO2"

    def function(self, simulation, period):
        quantites_gaz_ajustees = simulation.calculate('quantites_gaz_ajustees_cce_2014_2016', period)
        emissions_gaz = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_gaz
        emissions_ajustees = quantites_gaz_ajustees * emissions_gaz

        return period, emissions_ajustees


class emissions_CO2_gaz_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Emissions de CO2 des ménages via leur consommation de gaz après réforme, en kg de CO2"

    def function(self, simulation, period):
        quantites_gaz_ajustees = simulation.calculate('quantites_gaz_ajustees_taxe_carbone', period)
        emissions_gaz = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_gaz
        emissions_ajustees = quantites_gaz_ajustees * emissions_gaz

        return period, emissions_ajustees
