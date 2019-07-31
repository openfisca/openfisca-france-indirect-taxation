# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class depenses_tva_exonere(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses TTC des biens n'acquittant pas de TVA"

    def formula(menage, period):
        return menage('depenses_', period)


class depenses_tva_taux_intermediaire(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses TTC des biens acquittant la TVA à taux intermediaire"

    def formula_2012(menage, period, parameters):
        depenses_ht_tva_taux_intermediaire = menage('depenses_ht_tva_taux_intermediaire', period)
        taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
        return depenses_ht_tva_taux_intermediaire * (1 + taux_intermediaire)


class depenses_tva_taux_plein(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses TTC des biens acquittant la TVA acquitée à taux plein"

    def formula(menage, period, parameters):
        depenses_ht_tva_taux_plein = menage('depenses_ht_tva_taux_plein', period)
        taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        return depenses_ht_tva_taux_plein * (1 + taux_plein)


class depenses_tva_taux_reduit(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses TTC des biens acquittant la TVA acquitée à taux reduit"

    def formula(menage, period, parameters):
        depenses_ht_tva_taux_reduit = menage('depenses_ht_tva_taux_reduit', period)
        taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
        return depenses_ht_tva_taux_reduit * (1 + taux_reduit)


class depenses_tva_taux_super_reduit(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses TTC des biens acquittant à taux super reduit"

    def formula(menage, period, parameters):
        depenses_ht_tva_taux_super_reduit = menage('depenses_ht_tva_taux_super_reduit', period)
        taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
        return depenses_ht_tva_taux_super_reduit * (1 + taux_super_reduit)


class tva_taux_intermediaire(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant de la TVA acquitée à taux intermediaire"

    def formula_2012(menage, period, parameters):
        depenses_ht_tva_taux_intermediaire = menage('depenses_ht_tva_taux_intermediaire', period)
        taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
        return depenses_ht_tva_taux_intermediaire * taux_intermediaire
        # tax_from_expense_including_tax(depenses_tva_taux_intermediaire, taux_intermediaire)


class tva_taux_plein(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant de la TVA acquitée à taux plein"

    def formula(menage, period, parameters):
        depenses_ht_tva_taux_plein = menage('depenses_ht_tva_taux_plein', period)
        taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        return depenses_ht_tva_taux_plein * taux_plein
        # tax_from_expense_including_tax(depenses_tva_taux_plein, taux_plein)


class tva_taux_reduit(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant de la TVA acquitée à taux reduit"

    def formula(menage, period, parameters):
        depenses_ht_tva_taux_reduit = menage('depenses_ht_tva_taux_reduit', period)
        taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
        return depenses_ht_tva_taux_reduit * taux_reduit
        # tax_from_expense_including_tax(depenses_tva_taux_reduit, taux_reduit)


class tva_taux_super_reduit(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant de la TVA acquitée à taux super reduit"

    def formula(menage, period, parameters):
        depenses_ht_tva_taux_super_reduit = menage('depenses_ht_tva_taux_super_reduit', period)
        taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
        return depenses_ht_tva_taux_super_reduit * taux_super_reduit
        # tax_from_expense_including_tax(depenses_tva_taux_super_reduit, taux_super_reduit)


class tva_total(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant de la TVA acquitée"

    def formula(menage, period):
        tva_taux_super_reduit = menage('tva_taux_super_reduit', period)
        tva_taux_reduit = menage('tva_taux_reduit', period)
        tva_taux_intermediaire = menage('tva_taux_intermediaire', period)
        tva_taux_plein = menage('tva_taux_plein', period)
        return (
            tva_taux_super_reduit
            + tva_taux_reduit
            + tva_taux_intermediaire
            + tva_taux_plein
            )
