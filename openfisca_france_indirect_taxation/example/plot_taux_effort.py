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

from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, \
    graph_builder_line_percent, save_dataframe_to_graph

# On va dans ce fichier créer les graphiques permettant de voir les taux d'effort selon trois définition du revenu:
# - revenu total
# - revenu disponible
# - revenu disponible et loyer imputé

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Liste des variables que l'on veut simuler
    var_to_be_simulated = [
        'pondmen',
        'decuc',
        'niveau_vie_decile',
        'revtot',
        'somme_coicop12_conso',
        'rev_disponible',
        'rev_disp_loyerimput',
        'total_taxes_indirectes'
        ]

# 1 calcul taux d'effort sur le revenu total
    # Constition d'une base de données agrégée par décile (= collapse en stata)
    p = dict()
    df_taux_effort_revtot = None
    df_taux_effort_rev_disponible = None
    df_taux_effort_rev_disp_loyerimput = None
    for year in [2000, 2005, 2011]:
        df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        if year == 2011:
            df.niveau_vie_decile[df.decuc == 10] = 10
        varlist = ['revtot', 'total_taxes_indirectes', 'rev_disponible', 'rev_disp_loyerimput']
        Wconcat1 = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = varlist)
        Wconcat1['taux_d_effort_revtot_{}'.format(year)] = \
            Wconcat1['total_taxes_indirectes'] / Wconcat1['revtot']
        appendable1 = Wconcat1['taux_d_effort_revtot_{}'.format(year)]

        df.rev_disponible = df.rev_disponible * 1.33
        Wconcat2 = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = varlist)
        Wconcat2['taux_d_effort_rev_disponible_{}'.format(year)] = \
            Wconcat2['total_taxes_indirectes'] / Wconcat2['rev_disponible']
        appendable2 = Wconcat2['taux_d_effort_rev_disponible_{}'.format(year)]

        Wconcat3 = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = varlist)
        Wconcat3['taux_d_effort_rev_disp_loyerimput_{}'.format(year)] = \
            Wconcat3['total_taxes_indirectes'] / Wconcat3['rev_disp_loyerimput']
        appendable3 = Wconcat3['taux_d_effort_rev_disp_loyerimput_{}'.format(year)]

        if df_taux_effort_revtot is not None:
            df_taux_effort_revtot = concat([df_taux_effort_revtot, appendable1], axis = 1)
        else:
            df_taux_effort_revtot = appendable1

        if df_taux_effort_rev_disponible is not None:
            df_taux_effort_rev_disponible = concat([df_taux_effort_rev_disponible, appendable2], axis = 1)
        else:
            df_taux_effort_rev_disponible = appendable2

        if df_taux_effort_rev_disp_loyerimput is not None:
            df_taux_effort_rev_disp_loyerimput = concat([df_taux_effort_rev_disp_loyerimput, appendable3], axis = 1)
        else:
            df_taux_effort_rev_disp_loyerimput = appendable3

    graph_builder_line_percent(df_taux_effort_revtot, 1, 1)
    graph_builder_line_percent(df_taux_effort_rev_disponible, 1, 1)
    graph_builder_line_percent(df_taux_effort_rev_disp_loyerimput, 1, 1)

    save_dataframe_to_graph(df_taux_effort_revtot, 'taux_d_effort_revtot.csv')
    save_dataframe_to_graph(df_taux_effort_rev_disponible, 'taux_d_effort_rev_disponible.csv')
    save_dataframe_to_graph(df_taux_effort_rev_disp_loyerimput, 'taux_d_effort_rev_disp_loyerimput.csv')
