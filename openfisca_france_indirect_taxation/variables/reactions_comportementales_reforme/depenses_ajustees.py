# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore

import numpy


class depenses_essence_ajustees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en essence après réaction à la réforme des prix"

    def formula(menage, period, parameters):
        depenses_essence = menage('depenses_essence', period)
        super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
        reforme_essence = parameters(period.start).rattrapage_diesel.essence
        carburants_elasticite_prix = menage('elas_price_1_1', period)
        depenses_essence_ajustees = \
            depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence / super_95_ttc)

        return depenses_essence_ajustees


class depenses_diesel_ajustees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en diesel après réaction à la réforme des prix"

    def formula(menage, period, parameters):
        depenses_diesel = menage('depenses_diesel', period)
        diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
        reforme_diesel = parameters(period.start).rattrapage_diesel.diesel
        carburants_elasticite_prix = menage('elas_price_1_1', period)
        depenses_diesel_ajustees = \
            depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

        return depenses_diesel_ajustees


class depenses_gaz_ville_ajustees_taxe_carbone(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en gaz après réaction à la réforme - taxe carbone"

    def formula(menage, period, parameters):
        depenses_gaz_variables = menage('depenses_gaz_variables', period)
        depenses_gaz_prix_unitaire = menage('depenses_gaz_prix_unitaire', period)
        reforme_gaz = parameters(period.start).taxe_carbone.gaz
        gaz_elasticite_prix = menage('elas_price_2_2', period)
        depenses_gaz_ajustees_variables = \
            depenses_gaz_variables * (1 + (1 + gaz_elasticite_prix) * reforme_gaz / depenses_gaz_prix_unitaire)
        depenses_gaz_tarif_fixe = menage('depenses_gaz_tarif_fixe', period)
        depenses_gaz_ajustees = depenses_gaz_ajustees_variables + depenses_gaz_tarif_fixe
        depenses_gaz_ajustees[numpy.isnan(depenses_gaz_ajustees)] = 0
        depenses_gaz_ajustees[numpy.isinf(depenses_gaz_ajustees)] = 0

        return depenses_gaz_ajustees


class depenses_electricite_ajustees_taxe_carbone(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en électricité après réaction à la réforme - taxe carbone"

    def formula(menage, period, parameters):
        depenses_electricite_variables = menage('depenses_electricite_variables', period)
        depenses_electricite_prix_unitaire = menage('depenses_electricite_prix_unitaire', period)
        reforme_electricite = parameters(period.start).taxe_carbone.electricite
        electricite_elasticite_prix = menage('elas_price_2_2', period)
        depenses_electricite_ajustees_variables = (
            depenses_electricite_variables
            * (1 + (1 + electricite_elasticite_prix) * reforme_electricite / depenses_electricite_prix_unitaire)
            )
        depenses_electricite_tarif_fixe = menage('depenses_electricite_tarif_fixe', period)
        min_tarif_fixe = depenses_electricite_tarif_fixe.min()
        depenses_electricite_ajustees = depenses_electricite_ajustees_variables + depenses_electricite_tarif_fixe

        # We do not want to input the expenditure of the contract for those who consume nothing
        depenses_elec = menage('depenses_electricite', period)
        depenses_electricite_ajustees = (
            depenses_electricite_ajustees * (depenses_elec > min_tarif_fixe)
            + depenses_elec * (depenses_elec < min_tarif_fixe)
            )

        return depenses_electricite_ajustees
