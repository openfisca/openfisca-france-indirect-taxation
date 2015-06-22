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


from ..base import *  # noq analysis:ignore


from openfisca_france_indirect_taxation.param.param import ( # noq analysis:ignore
    # P_tva_taux_plein, P_tva_taux_intermediaire, P_tva_taux_reduit,
    # P_tva_taux_super_reduit,
    P_alcool_0211, P_alcool_0212, P_alcool_0213
    )


for coicop12_index in range(1, 13):
    reference_input_variable(
        column = FloatCol,
        entity_class = Menages,
        label = u"Poste coicop {} de la nomenclature aggrégée à 12 niveaux".format(coicop12_index),
        name = 'coicop12_{}'.format(coicop12_index),
        )

reference_input_variable(
    column = FloatCol,
    entity_class = Menages,
    label = u"Quantité de diesel consommée (en hecto-litres)",
    name = 'diesel_quantite',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Menages,
    label = u"Quantité de supercarburants (super 95, super98 et superE10) consommée (en hecto-litres)",
    name = 'supercarburants_quantite',
    )


@reference_formula
class consommation_alcools_forts(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'alcools forts"

    def function(self, simulation, period):
        categorie_fiscale_10 = simulation.calculate('categorie_fiscale_10', period)
        return period, categorie_fiscale_10


@reference_formula
class consommation_assurance_sante(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'assurance santé"

    def function(self, simulation, period):
        categorie_fiscale_16 = simulation.calculate('categorie_fiscale_16', period)
        return period, categorie_fiscale_16


@reference_formula
class consommation_assurance_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'assurance transport"

    def function(self, simulation, period):
        categorie_fiscale_15 = simulation.calculate('categorie_fiscale_15', period)
        return period, categorie_fiscale_15


@reference_formula
class consommation_autres_assurances(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'autres assurances"

    def function(self, simulation, period):
        categorie_fiscale_17 = simulation.calculate('categorie_fiscale_17', period)
        return period, categorie_fiscale_17


@reference_formula
class consommation_biere(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de bière"

    def function(self, simulation, period):
        categorie_fiscale_13 = simulation.calculate('categorie_fiscale_13', period)
        return period, categorie_fiscale_13


@reference_formula
class consommation_cigares(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de cigares"

    def function(self, simulation, period):
        categorie_fiscale_8 = simulation.calculate('categorie_fiscale_8', period)
        return period, categorie_fiscale_8


@reference_formula
class consommation_cigarette(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de cigarettes"

    def function(self, simulation, period):
        categorie_fiscale_7 = simulation.calculate('categorie_fiscale_7', period)
        return period, categorie_fiscale_7


@reference_formula
class consommation_tabac_a_rouler(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de tabac à rouler"

    def function(self, simulation, period):
        categorie_fiscale_9 = simulation.calculate('categorie_fiscale_9', period)
        return period, categorie_fiscale_9


@reference_formula
class consommation_tipp(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de tipp"

    def function(self, simulation, period):
        categorie_fiscale_14 = simulation.calculate('categorie_fiscale_14', period)
        return period, categorie_fiscale_14


@reference_formula
class consommation_totale(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation totale du ménage"

    def function(self, simulation, period):
        consommation_tva_taux_super_reduit = simulation.calculate('consommation_tva_taux_super_reduit', period)
        consommation_tva_taux_reduit = simulation.calculate('consommation_tva_taux_reduit', period)
        consommation_tva_taux_intermediaire = simulation.calculate('consommation_tva_taux_intermediaire', period)
        consommation_tva_taux_plein = simulation.calculate('consommation_tva_taux_plein', period)
        return period, (
            consommation_tva_taux_super_reduit +
            consommation_tva_taux_reduit +
            consommation_tva_taux_intermediaire +
            consommation_tva_taux_plein
            )


@reference_formula
class consommation_tva_taux_intermediaire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux intermédiaire"

    def function(self, simulation, period):
        categorie_fiscale_4 = simulation.calculate('categorie_fiscale_4', period)
        return period, categorie_fiscale_4


@reference_formula
class consommation_tva_taux_plein(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux plein"

    def function(self, simulation, period):
        categorie_fiscale_3 = simulation.calculate('categorie_fiscale_3', period)
        categorie_fiscale_11 = simulation.calculate('categorie_fiscale_11', period)
        return period, categorie_fiscale_3 + categorie_fiscale_11


@reference_formula
class consommation_tva_taux_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux réduit"

    def function(self, simulation, period):
        categorie_fiscale_2 = simulation.calculate('categorie_fiscale_2', period)
        return period, categorie_fiscale_2


@reference_formula
class consommation_tva_taux_super_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux super réduit"

    def function(self, simulation, period):
        categorie_fiscale_1 = simulation.calculate('categorie_fiscale_1', period)
        return period, categorie_fiscale_1


@reference_formula
class consommation_vin(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de vin"

    def function(self, simulation, period):
        categorie_fiscale_12 = simulation.calculate('categorie_fiscale_12', period)
        return period, categorie_fiscale_12


@reference_formula
class somme_coicop12(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Somme des postes coicop12"

    def function(self, simulation, period):
        coicop12_1 = simulation.calculate('coicop12_1', period)
        coicop12_2 = simulation.calculate('coicop12_2', period)
        coicop12_3 = simulation.calculate('coicop12_3', period)
        coicop12_4 = simulation.calculate('coicop12_4', period)
        coicop12_5 = simulation.calculate('coicop12_5', period)
        coicop12_6 = simulation.calculate('coicop12_6', period)
        coicop12_7 = simulation.calculate('coicop12_7', period)
        coicop12_8 = simulation.calculate('coicop12_8', period)
        coicop12_9 = simulation.calculate('coicop12_9', period)
        coicop12_10 = simulation.calculate('coicop12_10', period)
        coicop12_11 = simulation.calculate('coicop12_11', period)
        coicop12_12 = simulation.calculate('coicop12_12', period)
        return period, (
            coicop12_1 +
            coicop12_2 +
            coicop12_3 +
            coicop12_4 +
            coicop12_5 +
            coicop12_6 +
            coicop12_7 +
            coicop12_8 +
            coicop12_9 +
            coicop12_10 +
            coicop12_11 +
            coicop12_12
            )


@reference_formula
class somme_coicop12_conso(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Somme des postes coicop12 de 1 à 8"

    def function(self, simulation, period):
        coicop12_1 = simulation.calculate('coicop12_1', period)
        coicop12_2 = simulation.calculate('coicop12_2', period)
        coicop12_3 = simulation.calculate('coicop12_3', period)
        coicop12_4 = simulation.calculate('coicop12_4', period)
        coicop12_5 = simulation.calculate('coicop12_5', period)
        coicop12_6 = simulation.calculate('coicop12_6', period)
        coicop12_7 = simulation.calculate('coicop12_7', period)
        coicop12_8 = simulation.calculate('coicop12_8', period)
        return period, (
            coicop12_1 +
            coicop12_2 +
            coicop12_3 +
            coicop12_4 +
            coicop12_5 +
            coicop12_6 +
            coicop12_7 +
            coicop12_8
            )
