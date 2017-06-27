# -*- coding: utf-8 -*-


from __future__ import division


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


for coicop12_index in range(1, 13):
    name = u'coicop12_{}'.format(coicop12_index)
    # Trick to create a class with a dynamic name.
    type(name.encode('utf-8'), (Variable,), dict(
        column = FloatCol,
        entity = Menage,
        label = u"Poste coicop {} de la nomenclature aggrégée à 12 niveaux".format(coicop12_index),
        ))


class depenses_carburants(Variable):
    column = FloatCol
    entity = Menage
    label = u"Consommation de ticpe"

    def formula(self, simulation, period):
        return period, simulation.calculate('depenses_ticpe', period)


class depenses_ticpe(Variable):
    column = FloatCol
    entity = Menage
    label = u"Consommation de ticpe"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return period, simulation.calculate('depenses_ht_ticpe', period) * (1 + taux_plein_tva)


class depenses_essence_recalculees(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en essence recalculées à partir du prix ht"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_sp_e10_ht = simulation.calculate('depenses_sp_e10_ht', period)
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_super_plombe_ht = simulation.calculate('depenses_super_plombe_ht', period)


class depenses_totales(Variable):
    column = FloatCol
    entity = Menage
    label = u"Consommation totale du ménage"

    def formula(self, simulation, period):
        depenses_tva_taux_super_reduit = simulation.calculate('depenses_tva_taux_super_reduit', period)
        depenses_tva_taux_reduit = simulation.calculate('depenses_tva_taux_reduit', period)
        depenses_tva_taux_intermediaire = simulation.calculate('depenses_tva_taux_intermediaire', period)
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        return period, (
            depenses_tva_taux_super_reduit +
            depenses_tva_taux_reduit +
            depenses_tva_taux_intermediaire +
            depenses_tva_taux_plein
            )


class quantite_diesel(Variable):
    column = FloatCol
    entity = Menage
    label = u"Quantité de diesel consommée (en hecto-litres)"


class quantite_supercarburants(Variable):
    column = FloatCol
    entity = Menage
    label = u"Quantité de supercarburants (super 95, super98 et superE10) consommée (en hecto-litres)"


class somme_coicop12(Variable):
    column = FloatCol
    entity = Menage
    label = u"Somme des postes coicop12"

    def formula(self, simulation, period):
        return period, sum(
            simulation.calculate('coicop12_{}'.format(idx), period)
            for idx in xrange(1, 13)
            )


class somme_coicop12_conso(Variable):
    column = FloatCol
    entity = Menage
    label = u"Somme des postes coicop12 de 1 à 8"

    def formula(self, simulation, period):
        return period, sum(
            simulation.calculate('coicop12_{}'.format(idx), period)
            for idx in xrange(1, 9)
            )
