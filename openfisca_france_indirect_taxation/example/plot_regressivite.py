# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 17:36:56 2015

@author: Etienne
"""

# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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

from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, \
    graph_builder_bar


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    var_to_be_simulated = [
        'decuc',
        'tva_total',
        'ticpe',
        'droit_d_accise_vin',
        'droit_d_accise_biere',
        'droit_d_accise_alcools_forts',
        'droit_d_accise_cigarette',
        'droit_d_accise_cigares',
        'droit_d_accise_tabac_a_rouler',
        'taxe_assurance_transport',
        'taxe_assurance_sante',
        'taxe_autres_assurances',
        'niveau_vie_decile',
        'rev_disponible',
        'pondmen',
        ]

    for year in [2000, 2005, 2011]:
        df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        if year == 2011:
            df.niveau_vie_decile[df.decuc == 10] = 10
        Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile',
            varlist = var_to_be_simulated)

        Wconcat['taxe_1'] = Wconcat['tva_total']
        Wconcat['taxe_2'] = Wconcat['ticpe']
        Wconcat['taxe_3'] = (
            Wconcat['taxe_assurance_sante'] +
            Wconcat['taxe_assurance_transport'] +
            Wconcat['taxe_autres_assurances']
            )
        Wconcat['taxe_4'] = (
            Wconcat['droit_d_accise_vin'] +
            Wconcat['droit_d_accise_biere'] +
            Wconcat['droit_d_accise_alcools_forts']
            )
        Wconcat['taxe_5'] = (
            Wconcat['droit_d_accise_cigares'] +
            Wconcat['droit_d_accise_cigarette'] +
            Wconcat['droit_d_accise_tabac_a_rouler']
            )

        list_part_taxes = []
        for i in range(1, 6):
            Wconcat['part_taxe_{}'.format(i)] = Wconcat['taxe_{}'.format(i)] / Wconcat['rev_disponible']
            'list_part_taxes_{}'.format(i)
            list_part_taxes.append('part_taxe_{}'.format(i))

        df_to_graph = Wconcat[list_part_taxes]

        graph_builder_bar(df_to_graph)
