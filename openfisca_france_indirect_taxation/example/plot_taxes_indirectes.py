# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:25:34 2015

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

from openfisca_france_indirect_taxation.example.utils_example import simulate, df_weighted_average_grouped, \
    graph_builder_bar


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    simulated_variables = [
        'pondmen',
        'decuc',
        'niveau_vie_decile',
        'vin_droit_d_accise',
        'biere_droit_d_accise',
        'alcools_forts_droit_d_accise',
        'cigarette_droit_d_accise',
        'cigares_droit_d_accise',
        'tabac_a_rouler_droit_d_accise',
        'assurance_transport_taxe',
        'assurance_sante_taxe',
        'autres_assurances_taxe',
        'ticpe',
        'tva_total',
        'total_taxes_indirectes',
        'total_taxes_indirectes_sans_tva'
        ]

    p = dict()
    df_to_graph = None
    for year in [2000, 2005, 2011]:
        simulation_data_frame = simulate(simulated_variables = simulated_variables, year = year)
        annee = simulation_data_frame.apply(lambda row: year, axis = 1)
        simulation_data_frame["year"] = annee
        if year == 2011:
            simulation_data_frame.niveau_vie_decile[simulation_data_frame.decuc == 10] = 10

        var_to_concat = simulated_variables
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame,
            groupe = 'year', varlist = var_to_concat)

        aggregates_data_frame['taxe_1'] = aggregates_data_frame['vin_droit_d_accise']
        aggregates_data_frame['taxe_2'] = aggregates_data_frame['biere_droit_d_accise']
        aggregates_data_frame['taxe_3'] = aggregates_data_frame['alcools_forts_droit_d_accise']
        aggregates_data_frame['taxe_4'] = aggregates_data_frame['cigarette_droit_d_accise']
        aggregates_data_frame['taxe_5'] = aggregates_data_frame['cigares_droit_d_accise']
        aggregates_data_frame['taxe_6'] = aggregates_data_frame['tabac_a_rouler_droit_d_accise']
        aggregates_data_frame['taxe_7'] = aggregates_data_frame['assurance_transport_taxe']
        aggregates_data_frame['taxe_8'] = aggregates_data_frame['assurance_sante_taxe']
        aggregates_data_frame['taxe_9'] = aggregates_data_frame['autres_assurances_taxe']
        aggregates_data_frame['taxe_10'] = aggregates_data_frame['ticpe']
        aggregates_data_frame['taxe_11'] = aggregates_data_frame['tva_total']

        list_taxes = []
        for i in range(1, 12):
            aggregates_data_frame['part_{}'.format(i).format(year)] = \
                aggregates_data_frame['taxe_{}'.format(i)] / aggregates_data_frame['total_taxes_indirectes']
            'list_taxes_{}'.format(i)
            list_taxes.append('part_{}'.format(i))

        appendable = aggregates_data_frame[list_taxes]
        if df_to_graph is not None:
            df_to_graph = concat([df_to_graph, appendable])
        else:
            df_to_graph = appendable

    graph_builder_bar(df_to_graph)
