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

from pandas import DataFrame, concat
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, percent_formatter

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
    var_to_be_simulated = [
        'ident_men',
        'pondmen',
        'decuc',
        'age',
        'decile',
        'revtot',
        'somme_coicop12',
        'ocde10',
        'niveau_de_vie',
        ]
    # Merge des deux listes
    var_to_be_simulated += list_coicop12

    p = dict()
    for year in [2000, 2005, 2011]:
        simulation_data_frame = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        annee = simulation_data_frame.apply(lambda row: year, axis = 1)
        simulation_data_frame["year"] = annee
        if year == 2011:
            simulation_data_frame.decile[simulation_data_frame.decuc == 10] = 10
        var_to_concat = list_coicop12 + ['somme_coicop12']
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame, groupe = 'year', varlist = var_to_concat)

        list_part_coicop12 = []
        for i in range(1, 13):
            aggregates_data_frame['part_coicop12_{}'.format(i)] = aggregates_data_frame['coicop12_{}'.format(i)] / aggregates_data_frame['somme_coicop12']
            'list_part_coicop12_{}'.format(i)
            list_part_coicop12.append('part_coicop12_{}'.format(i))
            df_to_graph = concat([aggregates_data_frame[list_part_coicop12]])

        df_to_graph.columns = [
            'Alimentaire', 'Alcool + Tabac', 'Habits', 'Logement', 'Meubles', u'Santé',
            'Transport', 'Communication', 'Loisirs', 'Education', 'Hotels', 'Divers'
            ]

        axes = df_to_graph.plot(
            kind = 'bar',
            stacked = True,
            color = ['#FF0000', '#006600', '#660066', '#0000FF', '#FFFF00', '#999966', '#FF6699', '#00FFFF',
                     '#CC3300', '#990033', '#3366CC', '#000000']
            )
        plt.axhline(0, color = 'k')

            # TODO utiliser format et corriger également ici
            # https://github.com/openfisca/openfisca-matplotlib/blob/master/openfisca_matplotlib/graphs.py#L123
        axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
        axes.set_xticklabels([year], rotation=0);
        # Supprimer la légende du graphique
        axes.legend(
            bbox_to_anchor = (1.4, 1.05),
            ) # TODO: supprimer la légende pour les lignes pointillées et continues
    plt.show()

#    # Supprimer la légende du graphique
#    ax=plt.subplot(111)
#    ax.legend_.remove()
