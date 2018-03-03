# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division


from ..base import *  # noqa analysis:ignore


class taxes_indirectes_total(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant total de taxes indirectes payées"

    def function(menage, period, parameters):
        tva_total = menage('tva_total', period)
        taxes_indirectes_total_hors_tva = menage('taxes_indirectes_total_hors_tva', period)
        return period, (
            tva_total +
            taxes_indirectes_total_hors_tva
            )


class taxes_indirectes_total_hors_tva(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant total de taxes indirectes payées sans compter la TVA"

    def function(menage, period, parameters):
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
        return period, (
            vin_droit_d_accise +
            biere_droit_d_accise +
            alcools_forts_droit_d_accise +
            cigarette_droit_d_accise +
            cigares_droit_d_accise +
            tabac_a_rouler_droit_d_accise +
            assurance_transport_taxe +
            assurance_sante_taxe +
            autres_assurances_taxe +
            ticpe
            )
