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

from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, \
    graph_builder_bar


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    var_to_be_simulated = [
        'pondmen',
        'decuc',
        'niveau_vie_decile',
        'droit_d_accise_vin',
        'droit_d_accise_biere',
        'droit_d_accise_alcools_forts',
        'droit_d_accise_cigarette',
        'droit_d_accise_cigares',
        'droit_d_accise_tabac_a_rouler',
        'taxe_assurance_transport',
        'taxe_assurance_sante',
        'taxe_autres_assurances',
        'tipp',
        'tva_total',
        'total_taxes_indirectes',
        'total_taxes_indirectes_sans_tva'
        ]

    p = dict()
    df_to_graph = None
    for year in [2000, 2005, 2011]:
        simulation_data_frame = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        annee = simulation_data_frame.apply(lambda row: year, axis = 1)
        simulation_data_frame["year"] = annee
        if year == 2011:
            simulation_data_frame.niveau_vie_decile[simulation_data_frame.decuc == 10] = 10

        var_to_concat = var_to_be_simulated
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame,
            groupe = 'year', varlist = var_to_concat)

        aggregates_data_frame['taxe_1'] = aggregates_data_frame['droit_d_accise_vin']
        aggregates_data_frame['taxe_2'] = aggregates_data_frame['droit_d_accise_biere']
        aggregates_data_frame['taxe_3'] = aggregates_data_frame['droit_d_accise_alcools_forts']
        aggregates_data_frame['taxe_4'] = aggregates_data_frame['droit_d_accise_cigarette']
        aggregates_data_frame['taxe_5'] = aggregates_data_frame['droit_d_accise_cigares']
        aggregates_data_frame['taxe_6'] = aggregates_data_frame['droit_d_accise_tabac_a_rouler']
        aggregates_data_frame['taxe_7'] = aggregates_data_frame['taxe_assurance_transport']
        aggregates_data_frame['taxe_8'] = aggregates_data_frame['taxe_assurance_sante']
        aggregates_data_frame['taxe_9'] = aggregates_data_frame['taxe_autres_assurances']
        aggregates_data_frame['taxe_10'] = aggregates_data_frame['tipp']
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
