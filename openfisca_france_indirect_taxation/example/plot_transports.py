# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:26:44 2015

@author: thomas.douenne
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

from ipp_macro_series_parser.agregats_transports.parser_cleaner_prix_carburants import prix_mensuel_carburants_90_15, \
    prix_annuel_carburants_90_14

from openfisca_france_indirect_taxation.example.utils_example import graph_builder_bar, graph_builder_line, percent_formatter


def graph_builder_prix_carburants(data_frame):
    axes = data_frame.plot()
    plt.axhline(0, color = 'k')
    axes.xaxis(data_frame['annee'])
    axes.legend(
        bbox_to_anchor = (1, 1),
        )
    return plt.show()


prix_mensuel_carburants_90_15.plot(x='annee', y='diesel_ht')

data_frame_to_be_plotted = prix_mensuel_carburants_90_15[['diesel_ht'] + ['diesel_ttc'] + ['annee']]

graph_builder_prix_carburants(data_frame_to_be_plotted)
