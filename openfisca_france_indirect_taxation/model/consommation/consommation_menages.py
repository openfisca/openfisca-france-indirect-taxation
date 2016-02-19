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

from ..base import *  # noqa analysis:ignore


for coicop12_index in range(1, 13):
    name = u'coicop12_{}'.format(coicop12_index)
    # Trick to create a class with a dynamic name.
    type(name.encode('utf-8'), (Variable,), dict(
        column = FloatCol,
        entity_class = Menages,
        label = u"Poste coicop {} de la nomenclature aggrégée à 12 niveaux".format(coicop12_index),
        ))


class depenses_alcools_forts(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'alcools forts"

    def function(self, simulation, period):
        categorie_fiscale_10 = simulation.calculate('categorie_fiscale_10', period)
        return period, categorie_fiscale_10


class depenses_assurance_sante(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'assurance santé"

    def function(self, simulation, period):
        categorie_fiscale_16 = simulation.calculate('categorie_fiscale_16', period)
        return period, categorie_fiscale_16


class depenses_assurance_transport(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'assurance transport"

    def function(self, simulation, period):
        categorie_fiscale_15 = simulation.calculate('categorie_fiscale_15', period)
        return period, categorie_fiscale_15


class depenses_autres_assurances(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'autres assurances"

    def function(self, simulation, period):
        categorie_fiscale_17 = simulation.calculate('categorie_fiscale_17', period)
        return period, categorie_fiscale_17


class depenses_biere(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de bière"

    def function(self, simulation, period):
        categorie_fiscale_13 = simulation.calculate('categorie_fiscale_13', period)
        return period, categorie_fiscale_13


class depenses_cigares(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de cigares"

    def function(self, simulation, period):
        categorie_fiscale_8 = simulation.calculate('categorie_fiscale_8', period)
        return period, categorie_fiscale_8


class depenses_cigarettes(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de cigarettes"

    def function(self, simulation, period):
        categorie_fiscale_7 = simulation.calculate('categorie_fiscale_7', period)
        return period, categorie_fiscale_7


class depenses_tabac_a_rouler(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de tabac à rouler"

    def function(self, simulation, period):
        categorie_fiscale_9 = simulation.calculate('categorie_fiscale_9', period)
        return period, categorie_fiscale_9


class depenses_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de ticpe"

    def function(self, simulation, period):
        categorie_fiscale_14 = simulation.calculate('categorie_fiscale_14', period)
        return period, categorie_fiscale_14


class depenses_diesel_htva(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en diesel htva (mais incluant toujours la TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        depenses_diesel_htva = depenses_diesel - tax_from_expense_including_tax(depenses_diesel, taux_plein_tva)

        return period, depenses_diesel_htva


class depenses_diesel_ht(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en diesel ht (prix brut sans TVA ni TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        taux_implicite_diesel = (
            (accise_diesel_ticpe * (1 + taux_plein_tva)) /
            (prix_diesel_ttc - accise_diesel_ticpe * (1 + taux_plein_tva))
            )

        depenses_diesel_htva = simulation.calculate('depenses_diesel_htva', period)
        depenses_diesel_ht = \
            depenses_diesel_htva - tax_from_expense_including_tax(depenses_diesel_htva, taux_implicite_diesel)

        return period, depenses_diesel_ht


class depenses_diesel_recalculees(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en diesel recalculées à partir du prix ht"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_diesel_ht = simulation.calculate('depenses_diesel_ht', period)

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        taux_implicite_diesel = (
            (accise_diesel_ticpe * (1 + taux_plein_tva)) /
            (prix_diesel_ttc - accise_diesel_ticpe * (1 + taux_plein_tva))
            )

        depenses_diesel_recalculees = depenses_diesel_ht * (1 + taux_plein_tva) * (1 + taux_implicite_diesel)

        return period, depenses_diesel_recalculees


class depenses_sp_e10_ht(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence sans plomb e10 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10 = depenses_essence * part_sp_e10
        depenses_sp_e10_htva = depenses_sp_e10 - tax_from_expense_including_tax(depenses_sp_e10, taux_plein_tva)

        try:
            accise_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10
            majoration_ticpe_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
        except:
            accise_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10

        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        taux_implicite_sp_e10 = (
            (accise_ticpe_super_e10 * (1 + taux_plein_tva)) /
            (super_95_e10_ttc - accise_ticpe_super_e10 * (1 + taux_plein_tva))
            )
        depenses_sp_e10_ht = \
            depenses_sp_e10_htva - tax_from_expense_including_tax(depenses_sp_e10_htva, taux_implicite_sp_e10)

        return period, depenses_sp_e10_ht


class depenses_sp_95_ht(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence sans plomb 95 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        taux_implicite_sp95 = (
            (accise_ticpe_super95 * (1 + taux_plein_tva)) /
            (super_95_ttc - accise_ticpe_super95 * (1 + taux_plein_tva))
            )
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95 = depenses_essence * part_sp95
        depenses_sp_95_htva = depenses_sp_95 - tax_from_expense_including_tax(depenses_sp_95, taux_plein_tva)
        depenses_sp_95_ht = \
            depenses_sp_95_htva - tax_from_expense_including_tax(depenses_sp_95_htva, taux_implicite_sp95)

        return period, depenses_sp_95_ht


class depenses_sp_98_ht(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence sans plomb 98 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        taux_implicite_sp98 = (
            (accise_ticpe_super98 * (1 + taux_plein_tva)) /
            (super_98_ttc - accise_ticpe_super98 * (1 + taux_plein_tva))
            )
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98 = depenses_essence * part_sp98
        depenses_sp_98_htva = depenses_sp_98 - tax_from_expense_including_tax(depenses_sp_98, taux_plein_tva)
        depenses_sp_98_ht = \
            depenses_sp_98_htva - tax_from_expense_including_tax(depenses_sp_98_htva, taux_implicite_sp98)

        return period, depenses_sp_98_ht


class depenses_super_plombe_ht(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence super plombée hors taxes (HT, i.e. sans TVA ni TICPE)"

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        taux_implicite_super_plombe = (
            (accise_super_plombe_ticpe * (1 + taux_plein_tva)) /
            (super_plombe_ttc - accise_super_plombe_ticpe * (1 + taux_plein_tva))
            )
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe = depenses_essence * part_super_plombe
        depenses_super_plombe_htva = \
            depenses_super_plombe - tax_from_expense_including_tax(depenses_super_plombe, taux_plein_tva)
        depenses_super_plombe_ht = (depenses_super_plombe_htva -
            tax_from_expense_including_tax(depenses_super_plombe_htva, taux_implicite_super_plombe))

        return period, depenses_super_plombe_ht


class depenses_essence_ht(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en essence hors taxes (HT, i.e. sans TVA ni TICPE)"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_super_plombe_ht = simulation.calculate('depenses_super_plombe_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht + depenses_super_plombe_ht)
        return period, depenses_essence_ht

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht)
        return period, depenses_essence_ht

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_sp_e10_ht = simulation.calculate('depenses_sp_e10_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht + depenses_sp_e10_ht)
        return period, depenses_essence_ht


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


class depenses_tva_taux_intermediaire(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux intermédiaire"

    def function(self, simulation, period):
        categorie_fiscale_4 = simulation.calculate('categorie_fiscale_4', period)
        return period, categorie_fiscale_4


class depenses_tva_taux_plein(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux plein"

    def function(self, simulation, period):
        categorie_fiscale_3 = simulation.calculate('categorie_fiscale_3', period)
        try:
            categorie_fiscale_11 = simulation.calculate('categorie_fiscale_11', period)
        except:
            categorie_fiscale_11 = 0
        return period, categorie_fiscale_3 + categorie_fiscale_11


class depenses_tva_taux_reduit(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux réduit"

    def function(self, simulation, period):
        categorie_fiscale_2 = simulation.calculate('categorie_fiscale_2', period)
        return period, categorie_fiscale_2


class depenses_tva_taux_super_reduit(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux super réduit"

    def function(self, simulation, period):
        categorie_fiscale_1 = simulation.calculate('categorie_fiscale_1', period)
        return period, categorie_fiscale_1


class depenses_vin(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de vin"

    def function(self, simulation, period):
        categorie_fiscale_12 = simulation.calculate('categorie_fiscale_12', period)
        return period, categorie_fiscale_12


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
