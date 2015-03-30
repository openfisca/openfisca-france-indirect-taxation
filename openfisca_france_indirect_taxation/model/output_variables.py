# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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

import datetime
import numpy

from . base import *  # noq analysis:ignore


from openfisca_france_indirect_taxation.param.param import ( # noq analysis:ignore
    # P_tva_taux_plein, P_tva_taux_intermediaire, P_tva_taux_reduit,
    # P_tva_taux_super_reduit,
    P_alcool_0211, P_alcool_0212, P_alcool_0213
    )
# TODO: supprimer les P_alcool ?


@reference_formula
class age(SimpleFormulaColumn):
    column = AgeCol
    entity_class = Individus
    label = u"Age de l'individu"

    def function(self, simulation, period):
        birth = simulation.calculate('birth', period)
        return period, (numpy.datetime64(period.date) - birth).astype('timedelta64[Y]')


@reference_formula
class consommation_tva_taux_super_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux super réduit"

    def function(self, simulation, period):
        categorie_fiscale_1 = simulation.calculate('categorie_fiscale_1', period)
        return period, categorie_fiscale_1


@reference_formula
class consommation_tva_taux_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux réduit"

    def function(self, simulation, period):
        categorie_fiscale_2 = simulation.calculate('categorie_fiscale_2', period)
        return period, categorie_fiscale_2


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
class consommation_tva_taux_intermediaire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux intermédiaire"

    def function(self, simulation, period):
        categorie_fiscale_4 = simulation.calculate('categorie_fiscale_4', period)
        return period, categorie_fiscale_4


@reference_formula
class consommation_cigarette(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de cigarettes"

    def function(self, simulation, period):
        categorie_fiscale_7 = simulation.calculate('categorie_fiscale_7', period)
        return period, categorie_fiscale_7


@reference_formula
class consommation_cigares(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de cigares"

    def function(self, simulation, period):
        categorie_fiscale_8 = simulation.calculate('categorie_fiscale_8', period)
        return period, categorie_fiscale_8


@reference_formula
class consommation_tabac_a_rouler(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de tabac à rouler"

    def function(self, simulation, period):
        categorie_fiscale_9 = simulation.calculate('categorie_fiscale_9', period)
        return period, categorie_fiscale_9


@reference_formula
class consommation_alcools_forts(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'alcools forts"

    def function(self, simulation, period):
        categorie_fiscale_10 = simulation.calculate('categorie_fiscale_10', period)
        return period, categorie_fiscale_10


@reference_formula
class consommation_vin(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de vin"

    def function(self, simulation, period):
        categorie_fiscale_12 = simulation.calculate('categorie_fiscale_12', period)
        return period, categorie_fiscale_12


@reference_formula
class consommation_biere(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de bière"

    def function(self, simulation, period):
        categorie_fiscale_13 = simulation.calculate('categorie_fiscale_13', period)
        return period, categorie_fiscale_13


@reference_formula
class consommation_tipp(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation de tipp"

    def function(self, simulation, period):
        categorie_fiscale_14 = simulation.calculate('categorie_fiscale_14', period)
        return period, categorie_fiscale_14


@reference_formula
class consommation_assurance_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'assurance transport"

    def function(self, simulation, period):
        categorie_fiscale_15 = simulation.calculate('categorie_fiscale_15', period)
        return period, categorie_fiscale_15


@reference_formula
class consommation_assurance_sante(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'assurance santé"

    def function(self, simulation, period):
        categorie_fiscale_16 = simulation.calculate('categorie_fiscale_16', period)
        return period, categorie_fiscale_16


@reference_formula
class consommation_autres_assurances(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation d'autres assurances"

    def function(self, simulation, period):
        categorie_fiscale_17 = simulation.calculate('categorie_fiscale_17', period)
        return period, categorie_fiscale_17


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


@reference_formula
class decile(SimpleFormulaColumn):
    column = EnumCol(
        enum = Enum([
            u"Hors champ"
            u"1er décile",
            u"2nd décile",
            u"3e décile",
            u"4e décile",
            u"5e décile",
            u"6e décile",
            u"7e décile",
            u"8e décile",
            u"9e décile",
            u"10e décile"
            ])
        )

    entity_class = Menages
    label = u"Décile de niveau de vie"

    def function(self, simulation, period):
        niveau_de_vie = simulation.calculate('niveau_de_vie', period)
        pondmen = simulation.calculate('pondmen', period)
        labels = numpy.arange(1, 11)
        method = 2
        decile, values = mark_weighted_percentiles(niveau_de_vie, labels, pondmen, method, return_quantiles = True)
        del values
        return period, decile


@reference_formula
class montant_tva_taux_plein(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux plein"

    def function(self, simulation, period):
        consommation_tva_taux_plein = simulation.calculate('consommation_tva_taux_plein', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return period, tax_from_expense_including_tax(consommation_tva_taux_plein, taux)


@reference_formula
class montant_tva_taux_intermediaire(DatedFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux intermediaire"

    @dated_function(start = datetime.date(2012, 1, 1))
    def function(self, simulation, period):
        consommation_tva_taux_intermediaire = simulation.calculate('consommation_tva_taux_intermediaire')
        taux = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
        return period, tax_from_expense_including_tax(consommation_tva_taux_intermediaire, taux)


@reference_formula
class montant_tva_taux_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux reduit"

    def function(self, simulation, period):
        consommation_tva_taux_reduit = simulation.calculate('consommation_tva_taux_reduit', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        return period, tax_from_expense_including_tax(consommation_tva_taux_reduit, taux)


@reference_formula
class montant_tva_taux_super_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux super reduit"

    def function(self, simulation, period):
        consommation_tva_taux_super_reduit = simulation.calculate('consommation_tva_taux_super_reduit', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        return period, tax_from_expense_including_tax(consommation_tva_taux_super_reduit, taux)


@reference_formula
class montant_tva_total(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée"

    def function(self, simulation, period):
        montant_tva_taux_super_reduit = simulation.calculate('montant_tva_taux_super_reduit', period)
        montant_tva_taux_reduit = simulation.calculate('montant_tva_taux_reduit', period)
        montant_tva_taux_intermediaire = simulation.calculate('montant_tva_taux_intermediaire', period)
        montant_tva_taux_plein = simulation.calculate('montant_tva_taux_plein', period)
        return period, (
            montant_tva_taux_super_reduit +
            montant_tva_taux_reduit +
            montant_tva_taux_intermediaire +
            montant_tva_taux_plein
            )


@reference_formula
class montant_droit_d_accise_vin(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur le vin"

    def function(self, simulation, period):
        consommation_vin = simulation.calculate('consommation_vin', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        droit_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.vin.droit_cn_vin
        consommation_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.vin.masse_conso_cn_vin
        return period, montant_droit_d_accise(consommation_vin, droit_cn, consommation_cn, taux_plein_tva)


@reference_formula
class montant_droit_d_accise_biere(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur la bière"

    def function(self, simulation, period):
        consommation_biere = simulation.calculate('consommation_biere', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        droit_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.vin.droit_cn_biere
        consommation_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.vin.masse_conso_cn_biere
        return period, montant_droit_d_accise(consommation_biere, droit_cn, consommation_cn, taux_plein_tva)


@reference_formula
class montant_droit_d_accise_alcools_forts(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les alcools forts"

    def function(self, simulation, period):
        consommation_alcools_forts = simulation.calculate('consommation_alcools_forts', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        droit_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.vin.droit_cn_alcools
        consommation_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.vin.masse_conso_cn_alcools
        return period, montant_droit_d_accise(consommation_alcools_forts, droit_cn, consommation_cn, taux_plein_tva)


@reference_formula
class montant_droit_d_accise_cigarette(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les cigarettes"

    def function(self, simulation, period):
        consommation_cigarette = simulation.calculate('consommation_cigarette', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        droit_cn = simulation.legislation_at(period.start).imposition_indirecte.taux_normal_cigarette
        consommation_cn = simulation.legislation_at(period.start).imposition_indirecte.taux_specifique_cigarette
        return period, montant_droit_d_accise(consommation_cigarette, droit_cn, consommation_cn, taux_plein_tva)


@reference_formula
class montant_droit_d_accise_cigares(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les cigares"

    def function(self, simulation, period):
        consommation_cigares = simulation.calculate('consommation_cigares', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        droit_cn = simulation.legislation_at(period.start).imposition_indirecte.taux_normal_cigar
        consommation_cn = simulation.legislation_at(period.start).imposition_indirecte.taux_specifique_cigare
        return period, montant_droit_d_accise(consommation_cigares, droit_cn, consommation_cn, taux_plein_tva)


@reference_formula
class montant_droit_d_accise_tabac_a_rouler(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur le tabac à rouler"

    def function(self, simulation, period):
        consommation_tabac_a_rouler = simulation.calculate('consommation_tabac_a_rouler', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        droit_cn = simulation.legislation_at(period.start).imposition_indirecte.taux_normal_tabac_a_rouler
        consommation_cn = simulation.legislation_at(period.start).imposition_indirecte.taux_specifique_tabac_a_rouler
        return period, montant_droit_d_accise(consommation_tabac_a_rouler, droit_cn, consommation_cn, taux_plein_tva)


@reference_formula
class montant_taxe_assurance_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur l'assurance transport"

    def function(self, simulation, period):
        consommation_assurance_transport = simulation.calculate('consommation_assurance_transport', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.taux_assur_transport
        return period, tax_from_expense_including_tax(consommation_assurance_transport, taux)


@reference_formula
class montant_taxe_assurance_sante(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur l'assurance santé"

    def function(self, simulation, period):
        consommation_assurance_sante = simulation.calculate('consommation_assurance_sante', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.taux_assurances_sante
        return period, tax_from_expense_including_tax(consommation_assurance_sante, taux)


@reference_formula
class montant_taxe_autres_assurances(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur les autres assurances"

    def function(self, simulation, period):
        consommation_autres_assurances = simulation.calculate('consommation_autres_assurances', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.taux_assurances_autres
        return period, tax_from_expense_including_tax(consommation_autres_assurances, taux)


@reference_formula
class montant_tipp(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la tipp"

    def function(self, simulation, period):

        return period,  # TODO:


@reference_formula
class niveau_de_vie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Revenus disponibles divisés par ocde10 soit le nombre d'unités de consommation du ménage"

    def function(self, simulation, period):
        rev_disponible = simulation.calculate('rev_disponible', period)
        ocde10 = simulation.calculate('ocde10', period)
        return period, rev_disponible / ocde10
