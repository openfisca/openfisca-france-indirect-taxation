# -*- coding: utf-8 -*-


from __future__ import division


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class alcools_forts_droit_d_accise(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant des droits d'accises sur les alcools forts"

    def formula(self, simulation, period):
        depenses_ht_alcools_forts = simulation.calculate('depenses_ht_alcools_forts', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_alcools_forts = depenses_ht_alcools_forts * (1 + taux_plein_tva)
        alcool_conso_et_vin = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.alcools_forts.droit_cn_alcools_total
        consommation_cn = alcool_conso_et_vin.alcools_forts.masse_conso_cn_alcools
        return period, droit_d_accise(depenses_alcools_forts, droit_cn, consommation_cn, taux_plein_tva)


class depenses_alcools_forts(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses d'alcools forts'"

    def formula(self, simulation, period):
        depenses_ht_alcools_forts = simulation.calculate('depenses_ht_alcools_forts', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return period, depenses_ht_alcools_forts * (1 + taux_plein_tva)


class biere_droit_d_accise(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant des droits d'accises sur la bière"

    def formula(self, simulation, period):
        depenses_ht_biere = simulation.calculate('depenses_ht_biere', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_biere = depenses_ht_biere * (1 + taux_plein_tva)
        alcool_conso_et_vin = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.biere.droit_cn_biere
        consommation_cn = alcool_conso_et_vin.biere.masse_conso_cn_biere
        return period, droit_d_accise(depenses_biere, droit_cn, consommation_cn, taux_plein_tva)


class depenses_biere(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses de bière"

    def formula(self, simulation, period):
        depenses_ht_biere = simulation.calculate('depenses_ht_biere', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return period, depenses_ht_biere * (1 + taux_plein_tva)


class total_alcool_droit_d_accise(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant des droits d'accises sur l'alcool"

    def formula(self, simulation, period):
        vin_droit_d_accise = simulation.calculate('vin_droit_d_accise', period)
        biere_droit_d_accise = simulation.calculate('biere_droit_d_accise', period)
        alcools_forts_droit_d_accise = simulation.calculate('alcools_forts_droit_d_accise', period)
        return period, vin_droit_d_accise + biere_droit_d_accise + alcools_forts_droit_d_accise


class vin_droit_d_accise(Variable):
    column = FloatCol
    entity = Menage
    label = u"Montant des droits d'accises sur le vin"

    def formula(self, simulation, period):
        depenses_vin = simulation.calculate('depenses_vin', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        alcool_conso_et_vin = simulation.legislation_at(period.start).imposition_indirecte.alcool_conso_et_vin
        droit_cn = alcool_conso_et_vin.vin.droit_cn_vin
        consommation_cn = alcool_conso_et_vin.vin.masse_conso_cn_vin
        return period, droit_d_accise(depenses_vin, droit_cn, consommation_cn, taux_plein_tva)


class depenses_vin(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses de vin"

    def formula(self, simulation, period):
        depenses_ht_vin = simulation.calculate('depenses_ht_vin', period)
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return period, depenses_ht_vin * (1 + taux_plein_tva)
