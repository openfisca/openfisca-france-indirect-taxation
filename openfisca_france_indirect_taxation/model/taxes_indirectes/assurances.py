# -*- coding: utf-8 -*-

from __future__ import division


from datetime import date

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class assurance_sante_taxe(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant des taxes sur l'assurance santé"

    def formula(self, simulation, period):
        depenses_assurance_sante = simulation.calculate('depenses_assurance_sante', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances[
            'contrats_d_assurance_maladie_individuelles_et_collectives_cas_general_2_ter']
        # To do: use datedformula and change the computation method when other taxes play a role.
        return period, tax_from_expense_including_tax(depenses_assurance_sante, taux)


class assurance_transport_taxe(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant des taxes sur l'assurance transport"

    def formula_1984(self, simulation, period):
        depenses_assurance_transport = simulation.calculate('depenses_assurance_transport', period)
        taux_assurance_vtm = \
            simulation.legislation_at(period.start).imposition_indirecte.taux_assurances[
                'assurance_pour_les_vehicules_terrestres_a_moteurs_pour_les_particuliers']
        taux = taux_assurance_vtm
        return period, tax_from_expense_including_tax(depenses_assurance_transport, taux)

    def formula_2002(self, simulation, period):
        depenses_assurance_transport = simulation.calculate('depenses_assurance_transport', period)
        taux_assurance_vtm = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances[
            'assurance_pour_les_vehicules_terrestres_a_moteurs_pour_les_particuliers']
        taux_contrib_secu_vtm = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances[
            'contribution_secu_assurances_automobiles']
        taux = taux_assurance_vtm + taux_contrib_secu_vtm
        return period, tax_from_expense_including_tax(depenses_assurance_transport, taux)

    def formula_2004(self, simulation, period):
        depenses_assurance_transport = simulation.calculate('depenses_assurance_transport', period)
        taux_assurance_vtm = \
            simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.assurance_pour_les_vehicules_terrestres_a_moteurs_pour_les_particuliers
        taux_contrib_secu_vtm = \
            simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.contribution_secu_assurances_automobiles
        taux_contrib_fgao = \
            simulation.legislation_at(period.start).imposition_indirecte.fgao.contribution_des_assures_en_pourcentage_des_primes
        taux = taux_assurance_vtm + taux_contrib_secu_vtm + taux_contrib_fgao
        return period, tax_from_expense_including_tax(depenses_assurance_transport, taux)


class autres_assurances_taxe(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant des taxes sur les autres assurances"

    def formula(self, simulation, period):
        depenses_autres_assurances = simulation.calculate('depenses_autres_assurances', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.autres_assurances
        return period, tax_from_expense_including_tax(depenses_autres_assurances, taux)


class total_assurances_taxe(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant des taxes sur les assurances"

    def formula(self, simulation, period):
        assurance_transport_taxe = simulation.calculate('assurance_transport_taxe', period)
        assurance_sante_taxe = simulation.calculate('assurance_sante_taxe', period)
        autres_assurances_taxe = simulation.calculate('autres_assurances_taxe', period)
        return period, assurance_transport_taxe + assurance_sante_taxe + autres_assurances_taxe
