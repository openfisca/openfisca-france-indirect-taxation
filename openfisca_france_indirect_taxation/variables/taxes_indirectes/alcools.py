# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class alcools_forts_droit_d_accise(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des droits d'accises sur les alcools forts"

    def formula(menage, period, parameters):
        depenses_ht_alcools_forts = menage('depenses_ht_alcools_forts', period)
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        depenses_alcools_forts = depenses_ht_alcools_forts * (1 + taux_plein_tva)
        alcool_conso_et_vin = parameters(period.start).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.alcools_forts.droit_cn_alcools_total
        consommation_cn = alcool_conso_et_vin.alcools_forts.masse_conso_cn_alcools
        return droit_d_accise(depenses_alcools_forts, droit_cn, consommation_cn, taux_plein_tva)


class depenses_alcools_forts(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses d'alcools forts'"

    def formula(menage, period, parameters):
        depenses_ht_alcools_forts = menage('depenses_ht_alcools_forts', period)
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        return depenses_ht_alcools_forts * (1 + taux_plein_tva)


class biere_droit_d_accise(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des droits d'accises sur la bière"

    def formula(menage, period, parameters):
        depenses_ht_biere = menage('depenses_ht_biere', period)
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        depenses_biere = depenses_ht_biere * (1 + taux_plein_tva)
        alcool_conso_et_vin = parameters(period.start).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.biere.droit_cn_biere
        consommation_cn = alcool_conso_et_vin.biere.masse_conso_cn_biere
        return droit_d_accise(depenses_biere, droit_cn, consommation_cn, taux_plein_tva)


class depenses_biere(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Dépenses de bière'

    def formula(menage, period, parameters):
        depenses_ht_biere = menage('depenses_ht_biere', period)
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        return depenses_ht_biere * (1 + taux_plein_tva)


class total_alcool_droit_d_accise(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des droits d'accises sur l'alcool"

    def formula(menage, period):
        vin_droit_d_accise = menage('vin_droit_d_accise', period)
        biere_droit_d_accise = menage('biere_droit_d_accise', period)
        alcools_forts_droit_d_accise = menage('alcools_forts_droit_d_accise', period)
        return vin_droit_d_accise + biere_droit_d_accise + alcools_forts_droit_d_accise


class vin_droit_d_accise(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des droits d'accises sur le vin"

    def formula(menage, period, parameters):
        depenses_vin = menage('depenses_vin', period)
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        alcool_conso_et_vin = parameters(period.start).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.vin.droit_cn_vin
        consommation_cn = alcool_conso_et_vin.vin.masse_conso_cn_vin
        return droit_d_accise(depenses_vin, droit_cn, consommation_cn, taux_plein_tva)


class depenses_vin(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Dépenses de vin'

    def formula(menage, period, parameters):
        depenses_ht_vin = menage('depenses_ht_vin', period)
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        return depenses_ht_vin * (1 + taux_plein_tva)
