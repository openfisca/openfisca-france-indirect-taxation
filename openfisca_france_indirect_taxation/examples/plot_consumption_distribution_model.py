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

from pandas import concat

from openfisca_france_indirect_taxation.examples.utils_example import simulate, df_weighted_average_grouped, \
    graph_builder_bar

# Le but est ici de voir l'évolution de la distribution selon les 8 postes agrégés
# des coicop12 qui nous intéressent de 2005 à 2010
# Par la suite nous ferons cette étude de 1995 à 2011 (comme de 2006 à 2010 les données sont calées sur 2005
# nous savons par avance que cette distribution sera constante).
# Ce document sert donc de structure.


# On cherche donc tout d'abord à importer nos données de 2005 à 2010

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)


# Exemple: graphe par décile de revenu par uc de la ventilation de la consommation selon les postes agrégés de la CN
    # Lite des coicop agrégées en 12 postes
    list_coicop12 = []
    for coicop12_index in range(1, 13):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))
    # Liste des variables que l'on veut simuler
    simulated_variables = [
        'pondmen',
        'niveau_vie_decile',
        'somme_coicop12',
        ]
    # Merge des deux listes
    simulated_variables += list_coicop12

    p = dict()
    df_to_graph = None
    for year in [2000, 2005, 2011]:
        simulation_data_frame = simulate(simulated_variables = simulated_variables, year = year)
        annee = simulation_data_frame.apply(lambda row: year, axis = 1)
        simulation_data_frame["year"] = annee
        var_to_concat = list_coicop12 + ['somme_coicop12']
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame, groupe = 'year',
            varlist = var_to_concat)

        for i in range(1, 13):
            aggregates_data_frame['part_coicop12_{}'.format(i)] = \
                aggregates_data_frame['coicop12_{}'.format(i)] / aggregates_data_frame['somme_coicop12']

        appendable = aggregates_data_frame[['part_coicop12_{}'.format(i) for i in range(1, 13)]]
        if df_to_graph is not None:
            df_to_graph = concat([df_to_graph, appendable])
        else:
            df_to_graph = appendable

    graph_builder_bar(df_to_graph)
