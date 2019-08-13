# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class assurance_sante_taxe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des taxes sur l'assurance santé"

    def formula(menage, period, parameters):
        depenses_assurance_sante = menage('depenses_assurance_sante', period)
        taxes_assurances = parameters(period.start).imposition_indirecte.taxes_assurances
        taux = taxes_assurances.tsca.contrats_assurance_maladie_individuelles_collectives_cas_general_2_ter
        # To do: change date and change the computation method when other taxes play a role.
        return tax_from_expense_including_tax(depenses_assurance_sante, taux)


class assurance_transport_taxe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des taxes sur l'assurance transport"

    def formula_1984(menage, period, parameters):
        depenses_assurance_transport = menage('depenses_assurance_transport', period)
        taxes_assurances = parameters(period.start).imposition_indirecte.taxes_assurances
        taux_assurance_vtm = taxes_assurances.tsca.assurance_vehicules_terrestres_moteurs_particuliers
        return tax_from_expense_including_tax(depenses_assurance_transport, taux_assurance_vtm)

    def formula_2002(menage, period, parameters):
        depenses_assurance_transport = menage('depenses_assurance_transport', period)
        taxes_assurances = parameters(period.start).imposition_indirecte.taxes_assurances
        taux_assurance_vtm = taxes_assurances.tsca.assurance_vehicules_terrestres_moteurs_particuliers
        taux_contrib_secu_vtm = taxes_assurances.tsca.contribution_secu_assurances_automobiles
        return tax_from_expense_including_tax(depenses_assurance_transport, taux_assurance_vtm + taux_contrib_secu_vtm)

    def formula_2004(menage, period, parameters):
        depenses_assurance_transport = menage('depenses_assurance_transport', period)
        taxes_assurances = parameters(period.start).imposition_indirecte.taxes_assurances
        taux_assurance_vtm = taxes_assurances.tsca.assurance_vehicules_terrestres_moteurs_particuliers
        taux_contrib_secu_vtm = taxes_assurances.tsca.contribution_secu_assurances_automobiles
        taux_contrib_fgao = \
            parameters(period.start).imposition_indirecte.taxes_assurances.fgao.contribution_assures_en_pourcentage_primes
        taux = taux_assurance_vtm + taux_contrib_secu_vtm + taux_contrib_fgao
        return tax_from_expense_including_tax(depenses_assurance_transport, taux)


class autres_assurances_taxe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des taxes sur les autres assurances"

    def formula(menage, period, parameters):
        depenses_autres_assurances = menage('depenses_autres_assurances', period)
        taux = parameters(period.start).imposition_indirecte.taxes_assurances.tsca.autres_assurances
        return tax_from_expense_including_tax(depenses_autres_assurances, taux)


class total_assurances_taxe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des taxes sur les assurances"

    def formula(menage, period):
        assurance_transport_taxe = menage('assurance_transport_taxe', period)
        assurance_sante_taxe = menage('assurance_sante_taxe', period)
        autres_assurances_taxe = menage('autres_assurances_taxe', period)
        return assurance_transport_taxe + assurance_sante_taxe + autres_assurances_taxe
