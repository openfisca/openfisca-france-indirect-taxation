# -*- coding: utf-8 -*-

from __future__ import division


from datetime import date

from ..base import *  # noqa analysis:ignore


class assurance_sante_taxe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur l'assurance santé"

    def function(self, simulation, period):
        depenses_assurance_sante = simulation.calculate('depenses_assurance_sante', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.contrats_d_assurance_maladie_individuelles_et_collectives_cas_general_2_ter
        # To do: use datedformula and change the computation method when other taxes play a role.
        return period, tax_from_expense_including_tax(depenses_assurance_sante, taux)


class assurance_transport_taxe(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur l'assurance transport"

    @dated_function(start = date(1984, 1, 1), stop = date(2001, 12, 31))
    def function_84_01(self, simulation, period):
        depenses_assurance_transport = simulation.calculate('depenses_assurance_transport', period)
        taux_assurance_vtm = \
            simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.assurance_pour_les_vehicules_terrestres_a_moteurs_pour_les_particuliers
        taux = taux_assurance_vtm
        return period, tax_from_expense_including_tax(depenses_assurance_transport, taux)

    @dated_function(start = date(2002, 1, 1), stop = date(2004, 8, 4))
    def function_02_04(self, simulation, period):
        depenses_assurance_transport = simulation.calculate('depenses_assurance_transport', period)
        taux_assurance_vtm = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.assurance_pour_les_vehicules_terrestres_a_moteurs_pour_les_particuliers
        taux_contrib_secu_vtm = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.contribution_secu_assurances_automobiles
        taux = taux_assurance_vtm + taux_contrib_secu_vtm
        return period, tax_from_expense_including_tax(depenses_assurance_transport, taux)

    @dated_function(start = date(2004, 8, 5), stop = date(2015, 12, 31))
    def function_04_15(self, simulation, period):
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
    entity_class = Menages
    label = u"Montant des taxes sur les autres assurances"

    def function(self, simulation, period):
        depenses_autres_assurances = simulation.calculate('depenses_autres_assurances', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.taux_assurances.autres_assurances
        return period, tax_from_expense_including_tax(depenses_autres_assurances, taux)


class total_assurances_taxe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des taxes sur les assurances"

    def function(self, simulation, period):
        assurance_transport_taxe = simulation.calculate('assurance_transport_taxe', period)
        assurance_sante_taxe = simulation.calculate('assurance_sante_taxe', period)
        autres_assurances_taxe = simulation.calculate('autres_assurances_taxe', period)
        return period, assurance_transport_taxe + assurance_sante_taxe + autres_assurances_taxe
