# -*- coding: utf-8 -*-

from __future__ import division


from ..base import * # noqa analysis:ignore


class depenses_essence_ajustees(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence après réaction à la réforme des prix"

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        # simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.reforme_essence
        carburants_elasticite_prix = simulation.calculate('elas_price_1_1')
        depenses_essence_ajustees = \
            depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence / super_95_ttc)

        return period, depenses_essence_ajustees


class depenses_diesel_ajustees(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en diesel après réaction à la réforme des prix"

    def function(self, simulation, period):
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = simulation.legislation_at(period.start).taxes_carburants.diesel
        carburants_elasticite_prix = simulation.calculate('elas_price_1_1')
        depenses_diesel_ajustees = \
            depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

        return period, depenses_diesel_ajustees


class depenses_gaz_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en gaz après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_gaz_variables = simulation.calculate('depenses_gaz_variables', period)
        depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
        reforme_gaz = simulation.legislation_at(period.start).taxe_carbone.gaz
        gaz_elasticite_prix = simulation.calculate('elas_price_2_2')
        depenses_gaz_ajustees_variable = \
            depenses_gaz_variables * (1 + (1 + gaz_elasticite_prix) * reforme_gaz / depenses_gaz_prix_unitaire)
        depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
        depenses_gaz_ajustees = depenses_gaz_ajustees_variable + depenses_gaz_tarif_fixe

        return period, depenses_gaz_ajustees
