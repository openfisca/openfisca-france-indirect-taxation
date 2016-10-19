# -*- coding: utf-8 -*-


from __future__ import division


from openfisca_france_indirect_taxation.model.base import *


class alcools_forts_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les alcools forts"

    def function(self, simulation, period):
        depenses_alcools_forts = simulation.calculate('depenses_alcools_forts', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        alcool_conso_et_vin = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.alcools_forts.droit_cn_alcools_total
        consommation_cn = alcool_conso_et_vin.alcools_forts.masse_conso_cn_alcools
        return period, droit_d_accise(depenses_alcools_forts, droit_cn, consommation_cn, taux_plein_tva)


class biere_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur la bière"

    def function(self, simulation, period):
        depenses_biere = simulation.calculate('depenses_biere', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        alcool_conso_et_vin = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.biere.droit_cn_biere
        consommation_cn = alcool_conso_et_vin.biere.masse_conso_cn_biere
        return period, droit_d_accise(depenses_biere, droit_cn, consommation_cn, taux_plein_tva)


class total_alcool_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur l'alcool"

    def function(self, simulation, period):
        vin_droit_d_accise = simulation.calculate('vin_droit_d_accise', period)
        biere_droit_d_accise = simulation.calculate('biere_droit_d_accise', period)
        alcools_forts_droit_d_accise = simulation.calculate('alcools_forts_droit_d_accise', period)
        return period, vin_droit_d_accise + biere_droit_d_accise + alcools_forts_droit_d_accise


class vin_droit_d_accise(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur le vin"

    def function(self, simulation, period):
        depenses_vin = simulation.calculate('depenses_vin', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        alcool_conso_et_vin = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.vin.droit_cn_vin
        consommation_cn = alcool_conso_et_vin.vin.masse_conso_cn_vin
        return period, droit_d_accise(depenses_vin, droit_cn, consommation_cn, taux_plein_tva)
