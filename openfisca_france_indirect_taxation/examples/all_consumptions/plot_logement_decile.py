# -*- coding: utf-8 -*-

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

from openfisca_france_indirect_taxation.examples.utils_example import simulate, df_weighted_average_grouped, \
    graph_builder_line_percent


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    postes_agreges = ['poste_agrege_{}'.format(index) for index in
        ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12"]
        ]

    simulated_variables = [
        'pondmen',
        'niveau_vie_decile'
        ]

    simulated_variables += postes_agreges

    p = dict()
    df_to_graph = None
    for year in [2005]:
        simulation_data_frame = simulate(simulated_variables = simulated_variables, year = year)
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame,
            groupe = 'niveau_vie_decile', varlist = simulated_variables)

        aggregates_data_frame['depenses_tot'] = aggregates_data_frame[postes_agreges].sum(axis = 1)
        aggregates_data_frame[year] = aggregates_data_frame['poste_agrege_04'] / aggregates_data_frame['depenses_tot']
        appendable = aggregates_data_frame[year]
        if df_to_graph is not None:
            df_to_graph = concat([df_to_graph, appendable], axis = 1)
        else:
            df_to_graph = appendable

    graph_builder_line_percent(df_to_graph)
