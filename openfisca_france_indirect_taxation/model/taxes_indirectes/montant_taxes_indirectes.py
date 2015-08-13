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
from datetime import date

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
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.contrats_d_assurance_maladie_individuelles_et_collectives_cas_general_2_ter
        # To do: use datedformula and change the computation method when other taxes play a role.
        return period, tax_from_expense_including_tax(consommation_assurance_sante, taux)


@reference_formula
class taxe_assurance_transport(DatedFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur l'assurance transport"

    @dated_function(start = date(1984, 1, 1), stop = date(2001, 12, 31))
    def function(self, simulation, period):
        consommation_assurance_transport = simulation.calculate('consommation_assurance_transport', period)
        taux_assurance_vtm = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.assurance_pour_les_vehicules_terrestres_a_moteurs_pour_les_particuliers
        taux = taux_assurance_vtm
        return period, tax_from_expense_including_tax(consommation_assurance_transport, taux)

    @dated_function(start = date(2002, 1, 1), stop = date(2004, 8, 4))
    def function(self, simulation, period):
        consommation_assurance_transport = simulation.calculate('consommation_assurance_transport', period)
        taux_assurance_vtm = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.assurance_pour_les_vehicules_terrestres_a_moteurs_pour_les_particuliers
        taux_contrib_secu_vtm = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.contribution_secu_assurances_automobiles
        taux = taux_assurance_vtm + taux_contrib_secu_vtm
        return period, tax_from_expense_including_tax(consommation_assurance_transport, taux)

    @dated_function(start = date(2004, 8, 5), stop = date(2015, 12, 31))
    def function(self, simulation, period):
        consommation_assurance_transport = simulation.calculate('consommation_assurance_transport', period)
        taux_assurance_vtm = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.assurance_pour_les_vehicules_terrestres_a_moteurs_pour_les_particuliers
        taux_contrib_secu_vtm = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.contribution_secu_assurances_automobiles
        taux_contrib_fgao = simulation.legislation_at(period.start).imposition_indirecte.fgao.contribution_des_assures_en_pourcentage_des_primes
        taux = taux_assurance_vtm + taux_contrib_secu_vtm + taux_contrib_fgao
        return period, tax_from_expense_including_tax(consommation_assurance_transport, taux)


@reference_formula
class taxe_autres_assurances(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur les autres assurances"

    def function(self, simulation, period):
        consommation_autres_assurances = simulation.calculate('consommation_autres_assurances', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.autres_assurances
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
        taux_normal_cigare = simulation.legislation_at(period.start).imposition_indirecte.tabac.taux_normal.cigares
        return period, tax_from_expense_including_tax(consommation_cigares, taux_normal_cigare)


@reference_formula
class droit_d_accise_cigarette(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les cigarettes"

    def function(self, simulation, period):
        consommation_cigarette = simulation.calculate('consommation_cigarette', period)
        taux_normal_cigarette = simulation.legislation_at(period.start).imposition_indirecte.tabac.taux_normal.cigarettes
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
        taux_normal_tabac_a_rouler = simulation.legislation_at(period.start).imposition_indirecte.tabac.taux_normal.tabac_a_rouler
        return period, tax_from_expense_including_tax(consommation_tabac_a_rouler, taux_normal_tabac_a_rouler)


@reference_formula
class ticpe_carburants(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montants de la Taxe Intérieur sur la Consommation des Produits Energétiques"

    def function(self, simulation, period):

        # Get TVA at full rate
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        # Get implied tax rate for super
        accise_ticpe_super9598 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        # Need to use proxies to construct a weighted average
        prix_sp_ttc = (super_95_ttc + super_98_ttc) / 2
        taux_implicite_super9598 = (
            (accise_ticpe_super9598 * (1 + taux_plein_tva)) /
            (prix_sp_ttc - accise_ticpe_super9598 * (1 + taux_plein_tva))
            )

        # Get implied tax rate for diesel
        accise_ticpe_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        taux_implicite_diesel = (
            (accise_ticpe_diesel * (1 + taux_plein_tva)) /
            (prix_diesel_ttc - accise_ticpe_diesel * (1 + taux_plein_tva))
            )

        # Get weights to construct an approximation of consumption per type of fuel for each household
        conso_totale_vp_diesel = simulation.legislation_at(period.start).imposition_indirecte.quantite_carbu_vp.diesel
        conso_totale_vp_super = simulation.legislation_at(period.start).imposition_indirecte.quantite_carbu_vp.essence
        taille_parc_diesel = simulation.legislation_at(period.start).imposition_indirecte.parc_vp.diesel
        taille_parc_diesel = simulation.legislation_at(period.start).imposition_indirecte.parc_vp.essence

        conso_moyenne_vp_diesel = conso_totale_vp_diesel / taille_parc_diesel
        conso_moyenne_vp_super = conso_totale_vp_super / taille_parc_super

        nombre_vehicules_diesel = simulation.calculate('veh_diesel', period)
        nombre_vehicules_essence = simulation.calculate('veh_essence', period)

        part_conso_diesel = ((nombre_vehicules_diesel * conso_moyenne_vp_diesel) /
            (nombre_vehicules_essence * conso_moyenne_vp_super) + (nombre_vehicules_diesel * conso_moyenne_vp_diesel))
        part_conso_super = ((nombre_vehicules_super * conso_moyenne_vp_super) /
            (nombre_vehicules_essence * conso_moyenne_vp_super) + (nombre_vehicules_diesel * conso_moyenne_vp_diesel))

        # Get information about fuel consumption and use weights to compute expenses in ticpe
        depenses_carburants = simulation.calculate('consommation_ticpe', period)
        depenses_diesel = depenses_carburants * part_conso_diesel
        depenses_diesel_ht = depenses_diesel - tax_from_expense_including_tax(depenses_diesel, taux_plein_tva)
        depenses_super = depenses_carburants * part_conso_super
        depenses_super_ht = depenses_super - tax_from_expense_including_tax(depenses_super, taux_plein_tva)

        montant_ticpe_diesel = tax_from_expense_including_tax(depenses_diesel_ht, taux_implicite_diesel)
        montant_ticpe_super = tax_from_expense_including_tax(depenses_super_ht, taux_implicite_super9598)
        montant_ticpe_total = montant_ticpe_diesel + montant_ticpe_super


        return period, montant_ticpe_total


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
        ticpe_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        # Need to use proxies to construct a weighted average
        prix_super_ttc = (super_95_ttc + super_98_ttc) / 2

        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc

        taux_implicite_super9598 = ticpe_super9598 * (1 + taux_plein_tva) / (prix_super_ttc - ticpe_super9598 * (1 + taux_plein_tva))
        taux_implicite_diesel = ticpe_diesel * (1 + taux_plein_tva) / (prix_diesel_ttc - ticpe_diesel * (1 + taux_plein_tva))

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
        ticpe = simulation.calculate('ticpe_carburants', period)
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
        ticpe = simulation.calculate('ticpe_carburants', period)
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
