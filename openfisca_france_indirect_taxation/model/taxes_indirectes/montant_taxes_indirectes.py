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


import datetime

from ..base import *  # noqa analysis:ignore


@reference_formula
class droit_d_accise_alcool(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur l'alcool"

    def function(self, simulation, period):
        droit_d_accise_vin = simulation.calculate('droit_d_accise_vin', period)
        droit_d_accise_biere = simulation.calculate('droit_d_accise_biere', period)
        droit_d_accise_alcools_forts = simulation.calculate('droit_d_accise_alcools_forts', period)
        return period, droit_d_accise_vin + droit_d_accise_biere + droit_d_accise_alcools_forts


@reference_formula
class droit_d_accise_alcools_forts(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les alcools forts"

    def function(self, simulation, period):
        consommation_alcools_forts = simulation.calculate('consommation_alcools_forts', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        droit_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.alcools_forts.droit_cn_alcools_total
        consommation_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.alcools_forts.masse_conso_cn_alcools
        return period, droit_d_accise(consommation_alcools_forts, droit_cn, consommation_cn, taux_plein_tva)


@reference_formula
class taxe_assurance(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur les assurances"

    def function(self, simulation, period):
        taxe_assurance_transport = simulation.calculate('taxe_assurance_transport', period)
        taxe_assurance_sante = simulation.calculate('taxe_assurance_sante', period)
        taxe_autres_assurances = simulation.calculate('taxe_autres_assurances', period)
        return period, taxe_assurance_transport + taxe_assurance_sante + taxe_autres_assurances


@reference_formula
class taxe_assurance_sante(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur l'assurance santé"

    def function(self, simulation, period):
        consommation_assurance_sante = simulation.calculate('consommation_assurance_sante', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.taux_assurances_sante
        return period, tax_from_expense_including_tax(consommation_assurance_sante, taux)


@reference_formula
class taxe_assurance_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur l'assurance transport"

    def function(self, simulation, period):
        consommation_assurance_transport = simulation.calculate('consommation_assurance_transport', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.taux_assur_transport
        return period, tax_from_expense_including_tax(consommation_assurance_transport, taux)


@reference_formula
class taxe_autres_assurances(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur les autres assurances"

    def function(self, simulation, period):
        consommation_autres_assurances = simulation.calculate('consommation_autres_assurances', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.taux_assurances_autres
        return period, tax_from_expense_including_tax(consommation_autres_assurances, taux)


@reference_formula
class droit_d_accise_biere(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur la bière"

    def function(self, simulation, period):
        consommation_biere = simulation.calculate('consommation_biere', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        droit_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.biere.droit_cn_biere
        consommation_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.biere.masse_conso_cn_biere
        return period, droit_d_accise(consommation_biere, droit_cn, consommation_cn, taux_plein_tva)


@reference_formula
class droit_d_accise_cigares(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les cigares"

    def function(self, simulation, period):
        consommation_cigares = simulation.calculate('consommation_cigares', period)
        taux_normal_cigare = simulation.legislation_at(period.start).imposition_indirecte.tabac.cigares.taux_normal_cigare
        return period, tax_from_expense_including_tax(consommation_cigares, taux_normal_cigare)


@reference_formula
class droit_d_accise_cigarette(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les cigarettes"

    def function(self, simulation, period):
        consommation_cigarette = simulation.calculate('consommation_cigarette', period)
        taux_normal_cigarette = simulation.legislation_at(period.start).imposition_indirecte.tabac.cigarettes.taux_normal_cigarette
        return period, tax_from_expense_including_tax(consommation_cigarette, taux_normal_cigarette)


@reference_formula
class droit_d_accise_vin(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur le vin"

    def function(self, simulation, period):
        consommation_vin = simulation.calculate('consommation_vin', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        droit_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.vin.droit_cn_vin
        consommation_cn = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin.vin.masse_conso_cn_vin
        return period, droit_d_accise(consommation_vin, droit_cn, consommation_cn, taux_plein_tva)


@reference_formula
class droit_d_accise_tabac(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur le tabac "

    def function(self, simulation, period):
        droit_d_accise_cigarette = simulation.calculate('droit_d_accise_cigarette', period)
        droit_d_accise_cigares = simulation.calculate('droit_d_accise_cigares', period)
        droit_d_accise_tabac_a_rouler = simulation.calculate('droit_d_accise_tabac_a_rouler', period)
        return period, droit_d_accise_cigarette + droit_d_accise_cigares + droit_d_accise_tabac_a_rouler


@reference_formula
class droit_d_accise_tabac_a_rouler(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur le tabac à rouler"

    def function(self, simulation, period):
        consommation_tabac_a_rouler = simulation.calculate('consommation_tabac_a_rouler', period)
        taux_normal_tabac_a_rouler = simulation.legislation_at(period.start).imposition_indirecte.tabac.tabac_a_rouler.taux_normal_tabac_a_rouler
        return period, tax_from_expense_including_tax(consommation_tabac_a_rouler, taux_normal_tabac_a_rouler)


@reference_formula
class ticpe_diesel(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Taxe intérieur sur la consommation des produits énergétiques (diesel)"

    def function(self, simulation, period):

        diesel_quantite = simulation.calculate('diesel_quantite', period)
        # accise_ticpe_diesel = simulation.legislation_at(period.start).ticpe.diesel
        # 46.82 = accise nationale / le consommateur paie davantage
        accise_ticpe_diesel = 46.82  # €/ hl
        return period, accise_ticpe_diesel * diesel_quantite


@reference_formula
class ticpe_supercarburants(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Taxe intérieur sur la consommation des produits énergétiques (supercarburants)"

    def function(self, simulation, period):

        supercarburants_quantite = simulation.calculate('supercarburants_quantite', period)
        # accise_ticpe_supercarburants = simulation.legislation_at(period.start).ticpe.supercarburants
        accise_ticpe_supercarburants = 62.41  # € / hl
        return period, accise_ticpe_supercarburants * supercarburants_quantite


@reference_formula
class ticpe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la ticpe"

    def function(self, simulation, period):
        pourcentage_vehicule_essence = simulation.calculate('pourcentage_vehicule_essence', period)
        consommation_ticpe = simulation.calculate('consommation_ticpe', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        consommation_ticpe_ht = consommation_ticpe - tax_from_expense_including_tax(consommation_ticpe, taux_plein_tva)

        ticpe_super9598 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
        ticpe_gazole = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        prix_super_ttc = (super_95_ttc + super_98_ttc) / 2

        prix_ttc_gazole = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc

        taux_implicite_super9598 = ticpe_super9598 * (1 + taux_plein_tva) / (prix_super_ttc - ticpe_super9598 * (1 + taux_plein_tva))
        taux_implicite_diesel = ticpe_gazole * (1 + taux_plein_tva) / (prix_ttc_gazole - ticpe_gazole * (1 + taux_plein_tva))

        taux_implicite_ticpe = taux_implicite_diesel * (1 - pourcentage_vehicule_essence) + taux_implicite_super9598 * pourcentage_vehicule_essence

        return period, tax_from_expense_including_tax(consommation_ticpe_ht, taux_implicite_ticpe)


@reference_formula
class total_taxes_indirectes(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant total de taxes indirectes payées"

    def function(self, simulation, period):
        tva_total = simulation.calculate('tva_total', period)
        droit_d_accise_vin = simulation.calculate('droit_d_accise_vin', period)
        droit_d_accise_biere = simulation.calculate('droit_d_accise_biere', period)
        droit_d_accise_alcools_forts = simulation.calculate('droit_d_accise_alcools_forts', period)
        droit_d_accise_cigarette = simulation.calculate('droit_d_accise_cigarette', period)
        droit_d_accise_cigares = simulation.calculate('droit_d_accise_cigares', period)
        droit_d_accise_tabac_a_rouler = simulation.calculate('droit_d_accise_tabac_a_rouler', period)
        taxe_assurance_transport = simulation.calculate('taxe_assurance_transport', period)
        taxe_assurance_sante = simulation.calculate('taxe_assurance_sante', period)
        taxe_autres_assurances = simulation.calculate('taxe_autres_assurances', period)
        ticpe = simulation.calculate('ticpe', period)
        return period, (
            tva_total +
            droit_d_accise_vin +
            droit_d_accise_biere +
            droit_d_accise_alcools_forts +
            droit_d_accise_cigarette +
            droit_d_accise_cigares +
            droit_d_accise_tabac_a_rouler +
            taxe_assurance_transport +
            taxe_assurance_sante +
            taxe_autres_assurances +
            ticpe
            )


@reference_formula
class total_taxes_indirectes_sans_tva(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant total de taxes indirectes payées sans compter la TVA"

    def function(self, simulation, period):
        droit_d_accise_vin = simulation.calculate('droit_d_accise_vin', period)
        droit_d_accise_biere = simulation.calculate('droit_d_accise_biere', period)
        droit_d_accise_alcools_forts = simulation.calculate('droit_d_accise_alcools_forts', period)
        droit_d_accise_cigarette = simulation.calculate('droit_d_accise_cigarette', period)
        droit_d_accise_cigares = simulation.calculate('droit_d_accise_cigares', period)
        droit_d_accise_tabac_a_rouler = simulation.calculate('droit_d_accise_tabac_a_rouler', period)
        taxe_assurance_transport = simulation.calculate('taxe_assurance_transport', period)
        taxe_assurance_sante = simulation.calculate('taxe_assurance_sante', period)
        taxe_autres_assurances = simulation.calculate('taxe_autres_assurances', period)
        ticpe = simulation.calculate('ticpe', period)
        return period, (
            droit_d_accise_vin +
            droit_d_accise_biere +
            droit_d_accise_alcools_forts +
            droit_d_accise_cigarette +
            droit_d_accise_cigares +
            droit_d_accise_tabac_a_rouler +
            taxe_assurance_transport +
            taxe_assurance_sante +
            taxe_autres_assurances +
            ticpe
            )


@reference_formula
class tva_taux_intermediaire(DatedFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux intermediaire"

    @dated_function(start = datetime.date(2012, 1, 1))
    def function(self, simulation, period):
        consommation_tva_taux_intermediaire = simulation.calculate('consommation_tva_taux_intermediaire')
        taux_intermediaire = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
        return period, tax_from_expense_including_tax(consommation_tva_taux_intermediaire, taux_intermediaire)


@reference_formula
class tva_taux_plein(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux plein"

    def function(self, simulation, period):
        consommation_tva_taux_plein = simulation.calculate('consommation_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return period, tax_from_expense_including_tax(consommation_tva_taux_plein, taux_plein)


@reference_formula
class tva_taux_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux reduit"

    def function(self, simulation, period):
        consommation_tva_taux_reduit = simulation.calculate('consommation_tva_taux_reduit', period)
        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        return period, tax_from_expense_including_tax(consommation_tva_taux_reduit, taux_reduit)


@reference_formula
class tva_taux_super_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux super reduit"

    def function(self, simulation, period):
        consommation_tva_taux_super_reduit = simulation.calculate('consommation_tva_taux_super_reduit', period)
        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        return period, tax_from_expense_including_tax(consommation_tva_taux_super_reduit, taux_super_reduit)


@reference_formula
class tva_total(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée"

    def function(self, simulation, period):
        tva_taux_super_reduit = simulation.calculate('tva_taux_super_reduit', period)
        tva_taux_reduit = simulation.calculate('tva_taux_reduit', period)
        tva_taux_intermediaire = simulation.calculate('tva_taux_intermediaire', period)
        tva_taux_plein = simulation.calculate('tva_taux_plein', period)
        return period, (
            tva_taux_super_reduit +
            tva_taux_reduit +
            tva_taux_intermediaire +
            tva_taux_plein
            )


#@referene_formula
#class ticpe_super95 (SimpleFormulaColumn):
#    column = FloatCol
#    entity_class = Menages
#    label = u"Taxe intérieur sur la consommation des produits énergétiques (supercarburant : super95)"
#
#    def function(self, simulation, period):
#
#        #Attention, besoin d'ajuster en pondérant, données pour supercarburants et non super95
#        super95_quantite = simulation.calculate('super95_quantite', period)
#        # accise_ticpe_super95 = simulation.legislation_at(period.start).ticpe.super95
#        accise_ticpe_super95 = 62.41 # € / hl
#        return period, accise_ticpe_super95 * super95_quantite
#
#@referene_formula
#class ticpe_super98 (SimpleFormulaColumn):
#    column = FloatCol
#    entity_class = Menages
#    label = u"Taxe intérieur sur la consommation des produits énergétiques (supercarburant : super98)"
#
#    def function(self, simulation, period):
#
#        #Attention, besoin d'ajuster en pondérant, données pour supercarburants et non super98
#        super98_quantite = simulation.calculate('super98_quantite', period)
#        # accise_ticpe_super98 = simulation.legislation_at(period.start).ticpe.super98
#        accise_ticpe_super98 = 62.41 # ��� / hl
#        return period, accise_ticpe_super98 * super98_quantite
#
#@referene_formula
#class ticpe_superE10 (SimpleFormulaColumn):
#    column = FloatCol
#    entity_class = Menages
#    label = u"Taxe intérieur sur la consommation des produits énergétiques (supercarburant - superE10)"
#
#    def function(self, simulation, period):
#
#        #Attention, besoin d'ajuster en pondérant, données pour supercarburants et non superE10
#        superE10_quantite = simulation.calculate('superE10_quantite', period)
#        # accise_ticpe_superE10 = simulation.legislation_at(period.start).ticpe.superE10
#        accise_ticpe_superE10 = 62.41 # € / hl
#        return period, accise_ticpe_superE10 * superE10_quantite
#
