# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 15:47:20 2015

@author: thomas.douenne
"""

from __future__ import division
import pkg_resources
import os
import pandas as pd
from pandas import concat

from openfisca_france_indirect_taxation.example.utils_example import graph_builder_line

assets_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )

quantites_carburants_consommees = pd.DataFrame.from_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets',
        'quantites_carburants_consommees_bdf.csv'), sep = ',', header = -1)
quantites_carburants_consommees.rename(columns = {1: 'carburants bdf'}, inplace = True)
quantites_carburants_consommees.index = quantites_carburants_consommees.index.str.replace('en milliers de m3 en ', '')
quantites_carburants_consommees = quantites_carburants_consommees.sort_index()

quantites_diesel_consommees = pd.DataFrame.from_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets',
        'quantites_diesel_consommees_bdf.csv'), sep = ',', header = -1)
quantites_diesel_consommees.rename(columns = {1: 'diesel bdf'}, inplace = True)
quantites_diesel_consommees.index = quantites_diesel_consommees.index.str.replace('en milliers de m3 en ', '')
quantites_diesel_consommees = quantites_diesel_consommees.sort_index()

quantites_essence_consommees = pd.DataFrame.from_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets',
        'quantites_essence_consommees_bdf.csv'), sep = ',', header = -1)
quantites_essence_consommees.rename(columns = {1: 'essence bdf'}, inplace = True)
quantites_essence_consommees.index = quantites_essence_consommees.index.str.replace('en milliers de m3 en ', '')
quantites_essence_consommees = quantites_essence_consommees.sort_index()

quantite_carbu_vp_france = pd.read_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets',
        'quantite_carbu_vp_france.csv'), sep = ';')
quantite_carbu_vp_france['Unnamed: 0'] = quantite_carbu_vp_france['Unnamed: 0'].astype(str)
quantite_carbu_vp_france = quantite_carbu_vp_france.set_index('Unnamed: 0')
quantite_carbu_vp_france.rename(columns = {'essence': 'essence agregat'}, inplace = True)
quantite_carbu_vp_france.rename(columns = {'diesel': 'diesel agregat'}, inplace = True)
quantite_carbu_vp_france['carburants agregat'] = quantite_carbu_vp_france.sum(axis = 1)

comparaison_bdf_agregats = concat([quantite_carbu_vp_france, quantites_diesel_consommees,
    quantites_essence_consommees, quantites_carburants_consommees], axis = 1)
comparaison_bdf_agregats = comparaison_bdf_agregats.dropna()

graph_builder_line(comparaison_bdf_agregats[['essence agregat'] + ['essence bdf']])
graph_builder_line(comparaison_bdf_agregats[['diesel agregat'] + ['diesel bdf']])
graph_builder_line(comparaison_bdf_agregats[['carburants agregat'] + ['carburants bdf']])
