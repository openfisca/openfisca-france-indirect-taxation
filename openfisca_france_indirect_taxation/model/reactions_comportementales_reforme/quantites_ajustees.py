# -*- coding: utf-8 -*-

from __future__ import division


from datetime import date
import numpy

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class quantites_diesel_ajustees(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Quantités de diesel consommées après la réforme des prix"

    def function(self, simulation, period):
        depenses_diesel_ajustees = simulation.calculate('depenses_diesel_ajustees', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = simulation.legislation_at(period.start).taxes_carburants.diesel
        quantites_diesel_ajustees = depenses_diesel_ajustees / (diesel_ttc + reforme_diesel) * 100

        return period, quantites_diesel_ajustees


class quantites_gaz_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Quantités de gaz consommées après la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_gaz_ajustees_taxe_carbone = simulation.calculate('depenses_gaz_ajustees_taxe_carbone', period)
        depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
        depenses_gaz_ajustees_variables = depenses_gaz_ajustees_taxe_carbone - depenses_gaz_tarif_fixe

        depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
        reforme_gaz = simulation.legislation_at(period.start).taxe_carbone.gaz

        quantites_gaz_ajustees = depenses_gaz_ajustees_variables / (depenses_gaz_prix_unitaire + reforme_gaz)

        return period, quantites_gaz_ajustees


class quantites_electricite_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Quantités d'électricité consommées après la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_electricite_ajustees_taxe_carbone = \
            simulation.calculate('depenses_electricite_ajustees_taxe_carbone', period)
        depenses_electricite_tarif_fixe = simulation.calculate('depenses_electricite_tarif_fixe', period)
        depenses_electricite_ajustees_variables = \
            depenses_electricite_ajustees_taxe_carbone - depenses_electricite_tarif_fixe

        depenses_electricite_prix_unitaire = simulation.calculate('depenses_electricite_prix_unitaire', period)
        reforme_electricite = simulation.legislation_at(period.start).taxe_carbone.electricite

        quantites_electricite_ajustees = \
            depenses_electricite_ajustees_variables / (depenses_electricite_prix_unitaire + reforme_electricite)

        quantites_electricite_avant_reforme = simulation.calculate('quantites_electricite_selon_compteur', period)
        quantites_electricite_ajustees = (
            quantites_electricite_ajustees * (quantites_electricite_avant_reforme > 0)
            )

        return period, quantites_electricite_ajustees


class quantites_sp_e10_ajustees(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Quantités consommées de sans plomb e10 par les ménages après réforme"

    def function(self, simulation, period):
        depenses_essence_ajustees = simulation.calculate('depenses_essence_ajustees', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10_ajustees = depenses_essence_ajustees * part_sp_e10
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

        return period, quantite_sp_e10


class quantites_sp95_ajustees(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Quantités consommées de sans plomb 95 par les ménages après réforme"

    def function(self, simulation, period):
        depenses_essence_ajustees = simulation.calculate('depenses_essence_ajustees', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp95_ajustees = depenses_essence_ajustees * part_sp95
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

        return period, quantites_sp95_ajustees


class quantites_sp98_ajustees(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Quantités consommées de sans plomb 98 par les ménages"

    def function(self, simulation, period):
        depenses_essence_ajustees = simulation.calculate('depenses_essence_ajustees', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp98_ajustees = depenses_essence_ajustees * part_sp98
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

        return period, quantites_sp98_ajustees


class quantites_super_plombe_ajustees(Variable):
    column = FloatCol
    entity_class = Menage
    label = u"Quantités consommées de super plombé par les ménages après réforme"

    def function(self, simulation, period):
        depenses_essence_ajustees = simulation.calculate('depenses_essence_ajustees', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees * part_super_plombe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

        return period, quantites_super_plombe_ajustees


class quantites_essence_ajustees(DatedVariable):
    column = FloatCol
    entity_class = Menage
    label = u"Quantités d'essence consommées par les ménages après réforme"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees', period)
        quantites_super_plombe_ajustees = simulation.calculate('quantites_super_plombe_ajustees', period)
        quantites_essence_ajustees = (
            quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
            )
        return period, quantites_essence_ajustees

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
        return period, quantites_essence_ajustees

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees', period)
        quantites_sp_e10_ajustees = simulation.calculate('quantites_sp_e10_ajustees', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
        return period, quantites_essence_ajustees
