# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division


from datetime import date

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


for coicop12_index in range(1, 13):
    name = u'coicop12_{}'.format(coicop12_index)
    # Trick to create a class with a dynamic name.
    type(name.encode('utf-8'), (Variable,), dict(
        column = FloatCol,
        entity_class = Menages,
        label = u"Poste coicop {} de la nomenclature aggrégée à 12 niveaux".format(coicop12_index),
        ))


class depenses_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de ticpe"

    def function(self, simulation, period):
        return period, simulation.calculate('depenses_ticpe', period)


class depenses_ticpe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de ticpe"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return period, simulation.calculate('depenses_ht_ticpe', period) * (1 + taux_plein_tva)


class depenses_essence_recalculees(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence recalculées à partir du prix ht"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_sp_e10_ht = simulation.calculate('depenses_sp_e10_ht', period)
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_super_plombe_ht = simulation.calculate('depenses_super_plombe_ht', period)


class depenses_totales(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation totale du ménage"

    def function(self, simulation, period):
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
    entity_class = Menages
    label = u"Quantité de diesel consommée (en hecto-litres)"


class quantite_supercarburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantité de supercarburants (super 95, super98 et superE10) consommée (en hecto-litres)"


class somme_coicop12(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Somme des postes coicop12"

    def function(self, simulation, period):
        return period, sum(
            simulation.calculate('coicop12_{}'.format(idx), period)
            for idx in xrange(1, 13)
            )


class somme_coicop12_conso(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Somme des postes coicop12 de 1 à 8"

    def function(self, simulation, period):
        return period, sum(
            simulation.calculate('coicop12_{}'.format(idx), period)
            for idx in xrange(1, 9)
            )
