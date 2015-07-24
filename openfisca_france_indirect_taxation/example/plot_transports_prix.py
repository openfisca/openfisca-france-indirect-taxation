# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:26:44 2015

@author: thomas.douenne
"""

import matplotlib.pyplot as plt

from ipp_macro_series_parser.agregats_transports.parser_cleaner_prix_carburants import prix_mensuel_carburants_90_15


def graph_builder_prix_carburants(data_frame):
    axes = data_frame.plot(color = ['#FF0000', '#0000FF'])
    plt.axhline(0, color = 'k')
    # axes.xaxis(data_frame['annee'])
    axes.legend(
        bbox_to_anchor = (1, 1.23),
        )
    return plt.show()

prix_mensuel_carburants_90_15 = prix_mensuel_carburants_90_15.set_index('annee')

prix_mensuel_carburants_90_15['taux_implicite_ticpe_diesel'] = (
    (prix_mensuel_carburants_90_15['diesel_ttc'] - prix_mensuel_carburants_90_15['diesel_ht']) /
    prix_mensuel_carburants_90_15['diesel_ht']
    )
prix_mensuel_carburants_90_15['taux_implicite_ticpe_super_95'] = (
    (prix_mensuel_carburants_90_15['super_95_ttc'] - prix_mensuel_carburants_90_15['super_95_ht']) /
    prix_mensuel_carburants_90_15['super_95_ht']
    )

# Evolution du prix au cours du temps :

graph_builder_prix_carburants(prix_mensuel_carburants_90_15[['diesel_ht'] + ['diesel_ttc']])
graph_builder_prix_carburants(prix_mensuel_carburants_90_15[['super_95_ht'] + ['super_95_ttc']])

# Evolution du taux implicite au cours du temps :

graph_builder_prix_carburants(
    prix_mensuel_carburants_90_15[['taux_implicite_ticpe_super_95'] + ['taux_implicite_ticpe_diesel']]
    )
