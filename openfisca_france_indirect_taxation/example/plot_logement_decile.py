# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:00:08 2015

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
    graph_builder_line


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    list_coicop12 = []
    for coicop12_index in range(1, 13):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))

    var_to_be_simulated = [
        'pondmen',
        'niveau_vie_decile',
        'somme_coicop12',
        ]

    var_to_be_simulated += list_coicop12

    p = dict()
    df_to_graph = None
    for year in [2000, 2005, 2011]:
        simulation_data_frame = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame,
            groupe = 'niveau_vie_decile', varlist = var_to_be_simulated)

        aggregates_data_frame[year] = aggregates_data_frame['coicop12_4'] / aggregates_data_frame['somme_coicop12']
        appendable = aggregates_data_frame[year]
        if df_to_graph is not None:
            df_to_graph = concat([df_to_graph, appendable])
        else:
            df_to_graph = appendable

    graph_builder_line(df_to_graph)
