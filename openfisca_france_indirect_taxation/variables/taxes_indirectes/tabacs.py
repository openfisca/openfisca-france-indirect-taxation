# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class cigares_droit_d_accise(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des droits d'accises sur les cigares"

    def formula(menage, period, parameters):
        depenses_cigares = menage('depenses_cigares', period)
        taux_normal_cigare = parameters(period.start).imposition_indirecte.taxes_tabacs.taux_normaux_tabac.taux_normal.cigares
        return tax_from_expense_including_tax(depenses_cigares, taux_normal_cigare)


class cigarette_droit_d_accise(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des droits d'accises sur les cigarettes"

    def formula(menage, period, parameters):
        depenses_cigarettes = menage('depenses_cigarettes', period, options = [ADD])
        taux_normal_cigarette = \
            parameters(period.start).imposition_indirecte.taxes_tabacs.taux_normaux_tabac.taux_normal.cigarettes
        return tax_from_expense_including_tax(depenses_cigarettes, taux_normal_cigarette)


class depenses_cigares(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses de cigares"

    def formula(menage, period):
        return menage('poste_02_2_2', period)


class depenses_cigarettes(Variable):
    value_type = float
    entity = Menage
    label = "Dépenses de cigarettes"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(menage, period):
        return menage('poste_02_2_1', period, options = [DIVIDE])


class depenses_tabac_a_rouler(Variable):
    value_type = float
    entity = Menage
    label = "Dépenses de tabac à rouler et autres tabacs"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(menage, period):
        return menage('poste_02_2_3', period, options = [DIVIDE])


class depenses_tabac(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses totales de tabac (tous types)"

    def formula(menage, period):
        return (
            menage('depenses_cigares', period)
            + menage('depenses_cigarettes', period, options = [ADD])
            + menage('depenses_tabac_a_rouler', period, options = [ADD])
            )


class tabac_a_rouler_droit_d_accise(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des droits d'accises sur le tabac à rouler"

    def formula(menage, period, parameters):
        depenses_tabac_a_rouler = menage('depenses_tabac_a_rouler', period, options = [ADD])
        taux_normal_tabac_a_rouler = \
            parameters(period.start).imposition_indirecte.taxes_tabacs.taux_normaux_tabac.taux_normal.tabac_a_rouler
        return tax_from_expense_including_tax(depenses_tabac_a_rouler, taux_normal_tabac_a_rouler)


class total_tabac_droit_d_accise(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des droits d'accises sur le tabac "

    def formula(menage, period):
        cigarette_droit_d_accise = menage('cigarette_droit_d_accise', period)
        cigares_droit_d_accise = menage('cigares_droit_d_accise', period)
        tabac_a_rouler_droit_d_accise = menage('tabac_a_rouler_droit_d_accise', period)
        return cigarette_droit_d_accise + cigares_droit_d_accise + tabac_a_rouler_droit_d_accise
