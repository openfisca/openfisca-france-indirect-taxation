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


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class taxes_indirectes_total(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant total de taxes indirectes payées"

    def function(self, simulation, period):
        tva_total = simulation.calculate('tva_total', period)
        taxes_indirectes_total_hors_tva = simulation.calculate('taxes_indirectes_total_hors_tva', period)
        return period, (
            tva_total +
            taxes_indirectes_total_hors_tva
            )


class taxes_indirectes_total_hors_tva(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Montant total de taxes indirectes payées sans compter la TVA"

    def function(self, simulation, period):
        vin_droit_d_accise = simulation.calculate('vin_droit_d_accise', period)
        biere_droit_d_accise = simulation.calculate('biere_droit_d_accise', period)
        alcools_forts_droit_d_accise = simulation.calculate('alcools_forts_droit_d_accise', period)
        cigarette_droit_d_accise = simulation.calculate('cigarette_droit_d_accise', period)
        cigares_droit_d_accise = simulation.calculate('cigares_droit_d_accise', period)
        tabac_a_rouler_droit_d_accise = simulation.calculate('tabac_a_rouler_droit_d_accise', period)
        assurance_transport_taxe = simulation.calculate('assurance_transport_taxe', period)
        assurance_sante_taxe = simulation.calculate('assurance_sante_taxe', period)
        autres_assurances_taxe = simulation.calculate('autres_assurances_taxe', period)
        ticpe = simulation.calculate('ticpe_totale', period)
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
