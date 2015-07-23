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
        'somme_coicop12_conso',
        'tva_total',
        'droit_d_accise_alcool',
        'droit_d_accise_tabac',
        'taxe_assurance',
        'tipp',
        'total_taxes_indirectes'
        ]


# Taux d'effort par rapport au revenu disponible des ménages en 2005, par taxe indirecte
# et par décile de revenu disponible

    # Constition d'une base de données agrégée par décile (= collapse en stata)
    for year in [2000, 2005, 2011]:
        df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        if year == 2011:
            df.niveau_vie_decile[df.decuc == 10] = 10

        varlist = ['total_taxes_indirectes', 'tva_total', 'droit_d_accise_alcool',
                   'droit_d_accise_tabac', 'taxe_assurance', 'tipp']
        Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'niveau_vie_decile', varlist = varlist)

        # Example
        list_part = []
        Wconcat['part_tva'] = Wconcat['tva_total'] / Wconcat['total_taxes_indirectes']
        list_part.append('part_tva')

        Wconcat['part_tipp'] = Wconcat['tipp'] / Wconcat['total_taxes_indirectes']
        list_part.append('part_tipp')

        Wconcat['part_alcool'] = Wconcat['droit_d_accise_alcool'] / Wconcat['total_taxes_indirectes']
        list_part.append('part_alcool')

        Wconcat['part_tabac'] = Wconcat['droit_d_accise_tabac'] / Wconcat['total_taxes_indirectes']
        list_part.append('part_tabac')

        Wconcat['part_assurance'] = Wconcat['taxe_assurance'] / Wconcat['total_taxes_indirectes']
        list_part.append('part_assurance')

        df_to_graph = Wconcat[list_part].copy()
        df_to_graph.columns = ['TVA', 'TICPE', 'Alcool', 'Tabac', 'Assurances']

        graph_builder_bar(df_to_graph)
