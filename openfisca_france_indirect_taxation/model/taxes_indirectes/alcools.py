# -*- coding: utf-8 -*-


from __future__ import division


from ..base import *  # noqa analysis:ignore


class alcools_forts_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les alcools forts"

    def function(menage, period, parameters):
        depenses_alcools_forts = menage('depenses_alcools_forts', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_plein
        alcool_conso_et_vin = parameters(period).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.alcools_forts.droit_cn_alcools_total
        consommation_cn = alcool_conso_et_vin.alcools_forts.masse_conso_cn_alcools
        return period, droit_d_accise(depenses_alcools_forts, droit_cn, consommation_cn, taux_plein_tva)


class biere_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur la bière"

    def function(menage, period, parameters):
        depenses_biere = menage('depenses_biere', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_plein
        alcool_conso_et_vin = parameters(period).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.biere.droit_cn_biere
        consommation_cn = alcool_conso_et_vin.biere.masse_conso_cn_biere
        return period, droit_d_accise(depenses_biere, droit_cn, consommation_cn, taux_plein_tva)


class total_alcool_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur l'alcool"

    def function(menage, period, parameters):
        vin_droit_d_accise = menage('vin_droit_d_accise', period)
        biere_droit_d_accise = menage('biere_droit_d_accise', period)
        alcools_forts_droit_d_accise = menage('alcools_forts_droit_d_accise', period)
        return period, vin_droit_d_accise + biere_droit_d_accise + alcools_forts_droit_d_accise


class vin_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur le vin"

    def function(menage, period, parameters):
        depenses_vin = menage('depenses_vin', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_plein
        alcool_conso_et_vin = parameters(period).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.vin.droit_cn_vin
        consommation_cn = alcool_conso_et_vin.vin.masse_conso_cn_vin
        return period, droit_d_accise(depenses_vin, droit_cn, consommation_cn, taux_plein_tva)
