# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:41:21 2015

@author: thomas.douenne
"""

from __future__ import division

from pandas import concat

from openfisca_france_indirect_taxation.example.utils_example import simulate_df, df_weighted_average_grouped, \
    graph_builder_line_percent

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
        'rev_disp_loyerimput',
        'ticpe_totale'
        ]

    p = dict()
    part_ticpe_revtot = None
    part_ticpe_rev_disp_loyerimput = None
    part_ticpe_depenses_totales = None
    for year in [2000, 2005, 2011]:
        data_simulation = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        if year == 2011:
            data_simulation.niveau_vie_decile[data_simulation.decuc == 10] = 10
        varlist = ['revtot', 'ticpe_totale', 'somme_coicop12_conso', 'rev_disp_loyerimput']
        part_ticpe_revtot_wip = df_weighted_average_grouped(
            dataframe = data_simulation, groupe = 'niveau_vie_decile', varlist = varlist
            )
        part_ticpe_revtot_wip['part_ticpe_revtot_{}'.format(year)] = \
            part_ticpe_revtot_wip['ticpe_totale'] / part_ticpe_revtot_wip['revtot']
        data_to_append_revtot = part_ticpe_revtot_wip['part_ticpe_revtot_{}'.format(year)]

        part_ticpe_rev_loyerimput_wip = \
            df_weighted_average_grouped(dataframe = data_simulation, groupe = 'niveau_vie_decile', varlist = varlist)
        part_ticpe_rev_loyerimput_wip['part_ticpe_rev_disp_loyerimput_{}'.format(year)] = (
            part_ticpe_rev_loyerimput_wip['ticpe_totale'] /
            part_ticpe_rev_loyerimput_wip['rev_disp_loyerimput']
            )
        data_to_append_rev_loyerimput = \
            part_ticpe_rev_loyerimput_wip['part_ticpe_rev_disp_loyerimput_{}'.format(year)]

        part_ticpe_depenses_totales_wip = \
            df_weighted_average_grouped(dataframe = data_simulation, groupe = 'niveau_vie_decile', varlist = varlist)
        part_ticpe_depenses_totales_wip['part_ticpe_depenses_totales_{}'.format(year)] = (
            part_ticpe_depenses_totales_wip['ticpe_totale'] /
            part_ticpe_depenses_totales_wip['somme_coicop12_conso']
            )
        data_to_append_depenses_totales = \
            part_ticpe_depenses_totales_wip['part_ticpe_depenses_totales_{}'.format(year)]

        if part_ticpe_revtot is not None:
            part_ticpe_revtot = concat([part_ticpe_revtot, data_to_append_revtot], axis = 1)
        else:
            part_ticpe_revtot = data_to_append_revtot

        if part_ticpe_rev_disp_loyerimput is not None:
            part_ticpe_rev_disp_loyerimput = \
                concat([part_ticpe_rev_disp_loyerimput, data_to_append_rev_loyerimput], axis = 1)
        else:
            part_ticpe_rev_disp_loyerimput = data_to_append_rev_loyerimput

        if part_ticpe_depenses_totales is not None:
            part_ticpe_depenses_totales = \
                concat([part_ticpe_depenses_totales, data_to_append_depenses_totales], axis = 1)
        else:
            part_ticpe_depenses_totales = data_to_append_depenses_totales

    graph_builder_line_percent(part_ticpe_revtot)
    graph_builder_line_percent(part_ticpe_rev_disp_loyerimput)
    graph_builder_line_percent(part_ticpe_depenses_totales)
