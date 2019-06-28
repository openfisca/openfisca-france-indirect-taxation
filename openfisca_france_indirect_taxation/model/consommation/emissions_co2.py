# -*- coding: utf-8 -*-

from __future__ import division


from openfisca_france_indirect_taxation.model.base import * # noqa analysis:ignore


# Source : Ademe, Documentation des facteurs d'émissions de la Base Carbone
# http://www.bilans-ges.ademe.fr/static/documents/[Base%20Carbone]%20Documentation%20g%C3%A9n%C3%A9rale%20v11.0.pdf

class emissions_CO2_carburants(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation de carburants, en kg de CO2"

    def formula(self, simulation, period):
        quantites_diesel = menage('quantites_diesel', period)
        quantites_essence = menage('quantites_essence', period)
        emissions_diesel = \
            parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
        emissions_essence = \
            parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
        emissions = quantites_diesel * emissions_diesel + quantites_essence * emissions_essence  # Source : Ademe

        return emissions


class emissions_CO2_combustibles_liquides(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation de combustibles liquides, en kg de CO2"

    def formula(self, simulation, period):
        quantite_combustibles_liquides = menage('quantites_combustibles_liquides', period)
        emissions_combustibles_liquidies = \
            parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_combustibles_liquides
        emissions = quantite_combustibles_liquides * emissions_combustibles_liquidies

        return emissions


class emissions_CO2_diesel(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation de diesel, en kg de CO2"

    def formula(self, simulation, period):
        quantites_diesel = menage('quantites_diesel', period)
        emissions_diesel = \
            parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
        emissions_co2 = quantites_diesel * emissions_diesel

        return emissions_co2


class emissions_CO2_electricite(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation d'électricité, en kg de CO2"

    def formula(self, simulation, period):
        quantites_eletricite = menage('quantites_electricite_selon_compteur', period)
        emissions_electricite = \
            parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_electricite
        emissions = quantites_eletricite * emissions_electricite

        return emissions


class emissions_CO2_energies_logement(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation d'énergies dans leur logement, en kg de CO2"

    def formula(self, simulation, period):
        emissions_electricite = menage('emissions_CO2_electricite', period)
        emissions_gaz_ville = menage('emissions_CO2_gaz_ville', period)
        emissions_gaz_liquefie = menage('emissions_CO2_gaz_liquefie', period)
        emissions_combustibles_liquides = menage('emissions_CO2_combustibles_liquides', period)
        emissions = emissions_electricite + emissions_gaz_ville + emissions_gaz_liquefie + emissions_combustibles_liquides  # Source : Ademe

        return emissions


class emissions_CO2_energies_totales(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation d'énergies totale, en kg de CO2"

    def formula(self, simulation, period):
        emissions_energies_logement = menage('emissions_CO2_energies_logement', period)
        emissions_carburants = menage('emissions_CO2_carburants', period)
        emissions = emissions_energies_logement + emissions_carburants

        return emissions


class emissions_CO2_essence(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation de carburants, en kg de CO2"

    def formula(self, simulation, period):
        quantites_essence = menage('quantites_essence', period)
        emissions_essence = \
            parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
        emissions_co2 = quantites_essence * emissions_essence

        return emissions_co2


class emissions_CO2_gaz_liquefie(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation de gaz, en kg de CO2"

    def formula(self, simulation, period):
        quantites_gaz = menage('quantites_gaz_liquefie', period)
        emissions_gaz = \
            parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_gaz_liquefie
        emissions = quantites_gaz * emissions_gaz

        return emissions


class emissions_CO2_gaz_ville(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Emissions de CO2 des ménages via leur consommation de gaz, en kg de CO2"

    def formula(self, simulation, period):
        quantites_gaz = menage('quantites_gaz_final', period)
        emissions_gaz = \
            parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_gaz_ville
        emissions = quantites_gaz * emissions_gaz

        return emissions
