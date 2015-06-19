# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 10:08:25 2015

@author: malkaguillot
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


from openfisca_france_indirect_taxation.example.plot_consumption_distribution \
    import df_weighted_average_grouped, simulate_df, graph_builder_bar

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    var_to_be_simulated = [
        # Variable de déciles par uc originelle de l'enquête
        'decuc',
        'montant_tva_taux_plein',
        'montant_tva_taux_intermediaire',
        'montant_tva_taux_reduit',
        'montant_tva_taux_super_reduit',
        'montant_tva_total',
        'niveau_vie_decile',
        'rev_disponible',
        'pondmen',
        ]

    # Constition d'une base de données agrégée par décile (= collapse en stata)
    for year in [2000, 2005, 2011]:
        df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        if year == 2011:
            df.niveau_vie_decile[df.decuc == 10] = 10
        varlist = ['rev_disponible', 'montant_tva_taux_super_reduit',
                   'montant_tva_taux_reduit', 'montant_tva_taux_plein', 'montant_tva_taux_intermediaire'
                   ]
        Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = varlist)

        # Example
        Wconcat['part_tva_tx_super_reduit'] = Wconcat['montant_tva_taux_super_reduit'] / Wconcat['rev_disponible']
        Wconcat['part_tva_tx_reduit'] = Wconcat['montant_tva_taux_reduit'] / Wconcat['rev_disponible']
        Wconcat['part_tva_tx_intermediaire'] = Wconcat['montant_tva_taux_intermediaire'] / Wconcat['rev_disponible']
        Wconcat['part_tva_tx_plein'] = Wconcat['montant_tva_taux_plein'] / Wconcat['rev_disponible']

        df_to_graph = Wconcat[['part_tva_tx_plein', 'part_tva_tx_super_reduit', 'part_tva_tx_reduit',
                               'part_tva_tx_intermediaire']]

        # Graphe par décile de revenu par uc de la ventilation des taux de taxation
        graph_builder_bar(df_to_graph)
