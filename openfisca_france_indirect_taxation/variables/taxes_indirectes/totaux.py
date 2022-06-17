# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class taxes_indirectes_total(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Montant total de taxes indirectes payées'

    def formula(menage, period):
        tva_total = menage('tva_total', period)
        taxes_indirectes_total_hors_tva = menage('taxes_indirectes_total_hors_tva', period)
        return (
            tva_total
            + taxes_indirectes_total_hors_tva
            )


class taxes_indirectes_total_hors_tva(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Montant total de taxes indirectes payées sans compter la TVA'

    def formula(menage, period):
        vin_droit_d_accise = menage('vin_droit_d_accise', period)
        biere_droit_d_accise = menage('biere_droit_d_accise', period)
        alcools_forts_droit_d_accise = menage('alcools_forts_droit_d_accise', period)
        cigarette_droit_d_accise = menage('cigarette_droit_d_accise', period)
        cigares_droit_d_accise = menage('cigares_droit_d_accise', period)
        tabac_a_rouler_droit_d_accise = menage('tabac_a_rouler_droit_d_accise', period)
        assurance_transport_taxe = menage('assurance_transport_taxe', period)
        assurance_sante_taxe = menage('assurance_sante_taxe', period)
        autres_assurances_taxe = menage('autres_assurances_taxe', period)
        ticpe = menage('ticpe_totale', period)
        return (
            vin_droit_d_accise
            + biere_droit_d_accise
            + alcools_forts_droit_d_accise
            + cigarette_droit_d_accise
            + cigares_droit_d_accise
            + tabac_a_rouler_droit_d_accise
            + assurance_transport_taxe
            + assurance_sante_taxe
            + autres_assurances_taxe
            + ticpe
            )
