# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 15:43:49 2015

@author: germainmarchand
"""

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

from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, \
    graph_builder_bar


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Liste des coicop agrégées en 12 postes
    list_coicop12 = []
    for coicop12_index in range(1, 13):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))
    # Liste des variables que l'on veut simuler
    simulated_variables = [
        'pondmen',
        'decuc',
        'niveau_vie_decile',
        ]
    # Merge des deux listes
    simulated_variables += list_coicop12

    p = dict()
    df_to_graph = None
    for year in [2000, 2005, 2011]:
        # Constition d'une base de données agrégée par décile (= collapse en stata)
        simulation_data_frame = simulate(simulated_variables = simulated_variables, year = year)
        if year == 2011:
            simulation_data_frame.niveau_vie_decile[simulation_data_frame.decuc == 10] = 10
        simulation_data_frame['depenses_tot'] = 0
        for i in range(1, 13):
            simulation_data_frame['depenses_tot'] += simulation_data_frame['coicop12_{}'.format(i)]
        var_to_concat = list_coicop12 + ['depenses_tot']
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame,
            groupe = 'niveau_vie_decile', varlist = var_to_concat)

        for i in range(1, 13):
            aggregates_data_frame['part_coicop12_{}'.format(i)] = \
                aggregates_data_frame['coicop12_{}'.format(i)] / aggregates_data_frame['depenses_tot']

        appendable = aggregates_data_frame[['part_coicop12_{}'.format(i) for i in range(1, 13)]]

        graph_builder_bar(appendable)
