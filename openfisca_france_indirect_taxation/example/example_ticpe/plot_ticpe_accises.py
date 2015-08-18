# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 15:48:31 2015

@author: thomas.douenne
"""


from openfisca_france_indirect_taxation.example.utils_example import graph_builder_bar_list
from openfisca_france_indirect_taxation.model.get_dataframe_from_legislation.get_accises import get_accises_carburants

liste = ['ticpe_gazole', 'ticpe_super9598', 'super_plombe_ticpe']
df_accises = get_accises_carburants(liste)

graph_builder_bar_list(df_accises['accise ticpe gazole'])
graph_builder_bar_list(df_accises['accise ticpe super9598'])
graph_builder_bar_list(df_accises['accise super plombe ticpe'])
