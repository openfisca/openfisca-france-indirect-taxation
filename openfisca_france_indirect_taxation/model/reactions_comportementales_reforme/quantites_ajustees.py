# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class quantites_diesel_ajustees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités de diesel consommées après la réforme des prix"

    def formula(menage, period, parameters):
        depenses_diesel_ajustees = menage('depenses_diesel_ajustees', period)
        diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
        reforme_diesel = parameters(period.start).rattrapage_diesel.diesel
        quantites_diesel_ajustees = depenses_diesel_ajustees / (diesel_ttc + reforme_diesel) * 100

        return quantites_diesel_ajustees


class quantites_gaz_ajustees_taxe_carbone(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités de gaz consommées après la réforme - taxe carbone"

    def formula(menage, period, parameters):
        depenses_gaz_ajustees_taxe_carbone = menage('depenses_gaz_ajustees_taxe_carbone', period)
        depenses_gaz_tarif_fixe = menage('depenses_gaz_tarif_fixe', period)
        depenses_gaz_ajustees_variables = depenses_gaz_ajustees_taxe_carbone - depenses_gaz_tarif_fixe

        depenses_gaz_prix_unitaire = menage('depenses_gaz_prix_unitaire', period)
        reforme_gaz = parameters(period.start).taxe_carbone.gaz

        quantites_gaz_ajustees = depenses_gaz_ajustees_variables / (depenses_gaz_prix_unitaire + reforme_gaz)

        return quantites_gaz_ajustees


class quantites_electricite_ajustees_taxe_carbone(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités d'électricité consommées après la réforme - taxe carbone"

    def formula(menage, period, parameters):
        depenses_electricite_ajustees_taxe_carbone = \
            menage('depenses_electricite_ajustees_taxe_carbone', period)
        depenses_electricite_tarif_fixe = menage('depenses_electricite_tarif_fixe', period)
        depenses_electricite_ajustees_variables = \
            depenses_electricite_ajustees_taxe_carbone - depenses_electricite_tarif_fixe

        depenses_electricite_prix_unitaire = menage('depenses_electricite_prix_unitaire', period)
        reforme_electricite = parameters(period.start).taxe_carbone.electricite

        quantites_electricite_ajustees = \
            depenses_electricite_ajustees_variables / (depenses_electricite_prix_unitaire + reforme_electricite)

        quantites_electricite_avant_reforme = menage('quantites_electricite_selon_compteur', period)
        quantites_electricite_ajustees = (
            quantites_electricite_ajustees * (quantites_electricite_avant_reforme > 0)
            )

        return quantites_electricite_ajustees


class quantites_sp_e10_ajustees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités consommées de sans plomb e10 par les ménages après réforme"

    def formula(menage, period, parameters):
        depenses_essence_ajustees = menage('depenses_essence_ajustees', period)
        part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10_ajustees = depenses_essence_ajustees * part_sp_e10
        super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
        reforme_essence = parameters(period.start).rattrapage_diesel.essence
        quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

        return quantite_sp_e10


class quantites_sp95_ajustees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités consommées de sans plomb 95 par les ménages après réforme"

    def formula(menage, period, parameters):
        depenses_essence_ajustees = menage('depenses_essence_ajustees', period)
        part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp95_ajustees = depenses_essence_ajustees * part_sp95
        super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
        reforme_essence = parameters(period.start).rattrapage_diesel.essence
        quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

        return quantites_sp95_ajustees


class quantites_sp98_ajustees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités consommées de sans plomb 98 par les ménages"

    def formula(menage, period, parameters):
        depenses_essence_ajustees = menage('depenses_essence_ajustees', period)
        part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp98_ajustees = depenses_essence_ajustees * part_sp98
        super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
        reforme_essence = parameters(period.start).rattrapage_diesel.essence
        quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

        return quantites_sp98_ajustees


class quantites_super_plombe_ajustees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités consommées de super plombé par les ménages après réforme"

    def formula(menage, period, parameters):
        depenses_essence_ajustees = menage('depenses_essence_ajustees', period)
        part_super_plombe = \
            parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees * part_super_plombe
        super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
        reforme_essence = parameters(period.start).rattrapage_diesel.essence
        quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

        return quantites_super_plombe_ajustees


class quantites_essence_ajustees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités d'essence consommées par les ménages après réforme"

    def formula_1990(menage, period):
        quantites_sp95_ajustees = menage('quantites_sp95_ajustees', period)
        quantites_sp98_ajustees = menage('quantites_sp98_ajustees', period)
        quantites_super_plombe_ajustees = menage('quantites_super_plombe_ajustees', period)
        quantites_essence_ajustees = (
            quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
            )
        return quantites_essence_ajustees

    def formula_2007(menage, period):
        quantites_sp95_ajustees = menage('quantites_sp95_ajustees', period)
        quantites_sp98_ajustees = menage('quantites_sp98_ajustees', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
        return quantites_essence_ajustees

    def formula_2009(menage, period):
        quantites_sp95_ajustees = menage('quantites_sp95_ajustees', period)
        quantites_sp98_ajustees = menage('quantites_sp98_ajustees', period)
        quantites_sp_e10_ajustees = menage('quantites_sp_e10_ajustees', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
        return quantites_essence_ajustees
