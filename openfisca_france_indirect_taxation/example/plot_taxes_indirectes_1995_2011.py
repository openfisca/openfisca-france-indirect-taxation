# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:10:49 2015

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

from pandas import concat

from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, \
    graph_builder_line_percent


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    list_coicop12 = []
    for coicop12_index in range(1, 13):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))

    simulated_variables = [
        'decuc',
        'tva_total',
        'ticpe',
        'vin_droit_d_accise',
        'biere_droit_d_accise',
        'alcools_forts_droit_d_accise',
        'cigarette_droit_d_accise',
        'cigares_droit_d_accise',
        'tabac_a_rouler_droit_d_accise',
        'assurance_transport_taxe',
        'assurance_sante_taxe',
        'autres_assurances_taxe',
        'niveau_vie_decile',
        'pondmen',
        'somme_coicop12',
        'rev_disponible'
        ]

    simulated_variables += list_coicop12

    p = dict()
    df_to_graph1 = None
    df_to_graph2 = None
    for year in [2000, 2005, 2011]:
        simulation_data_frame = simulate(simulated_variables = simulated_variables, year = year)
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame,
            groupe = 'niveau_vie_decile', varlist = simulated_variables)
        aggregates_data_frame['taxe_1'] = aggregates_data_frame['tva_total']
        aggregates_data_frame['taxe_2'] = aggregates_data_frame['ticpe']
        aggregates_data_frame['taxe_3'] = (
            aggregates_data_frame['assurance_sante_taxe'] +
            aggregates_data_frame['assurance_transport_taxe'] +
            aggregates_data_frame['autres_assurances_taxe']
            )
        aggregates_data_frame['taxe_4'] = (
            aggregates_data_frame['vin_droit_d_accise'] +
            aggregates_data_frame['biere_droit_d_accise'] +
            aggregates_data_frame['alcools_forts_droit_d_accise']
            )
        aggregates_data_frame['taxe_5'] = (
            aggregates_data_frame['cigares_droit_d_accise'] +
            aggregates_data_frame['cigarette_droit_d_accise'] +
            aggregates_data_frame['tabac_a_rouler_droit_d_accise']
            )

        aggregates_data_frame['total'] = (
            aggregates_data_frame['taxe_{}'.format(1)] +
            aggregates_data_frame['taxe_{}'.format(2)] +
            aggregates_data_frame['taxe_{}'.format(3)] +
            aggregates_data_frame['taxe_{}'.format(4)] +
            aggregates_data_frame['taxe_{}'.format(5)]
            )
        appendable1 = aggregates_data_frame['total'] / (
            aggregates_data_frame['somme_coicop12'] - aggregates_data_frame['coicop12_{}'.format(4)]
            )
        if df_to_graph1 is not None:
            df_to_graph1 = concat([df_to_graph1, appendable1], axis = 1)
        else:
            df_to_graph1 = appendable1

        appendable2 = \
            aggregates_data_frame['total'] / aggregates_data_frame['rev_disponible']

        if df_to_graph2 is not None:
            df_to_graph2 = concat([df_to_graph2, appendable2], axis = 1)
        else:
            df_to_graph2 = appendable2

    graph_builder_line_percent(df_to_graph1)
    graph_builder_line_percent(df_to_graph2)
