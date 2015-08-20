# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 15:18:46 2015

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

depenses_transports_totales = pd.DataFrame.from_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets',
        'depenses_transports_totales_bdf.csv'), sep = ',', header = -1)
depenses_transports_totales.rename(columns = {1: 'transports bdf'}, inplace = True)
depenses_transports_totales.index = depenses_transports_totales.index.str.replace('en ', '')
depenses_transports_totales = depenses_transports_totales.sort_index()

depenses_carburants_totales = pd.DataFrame.from_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets',
        'depenses_carburants_totales_bdf.csv'), sep = ',', header = -1)
depenses_carburants_totales.rename(columns = {1: 'carburants bdf'}, inplace = True)
depenses_carburants_totales.index = depenses_carburants_totales.index.str.replace('en ', '')
depenses_carburants_totales = depenses_carburants_totales.sort_index()

depenses_diesel_totales = pd.DataFrame.from_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets',
        'depenses_diesel_totales_bdf.csv'), sep = ',', header = -1)
depenses_diesel_totales.rename(columns = {1: 'diesel bdf'}, inplace = True)
depenses_diesel_totales.index = depenses_diesel_totales.index.str.replace('en ', '')
depenses_diesel_totales = depenses_diesel_totales.sort_index()

depenses_essence_totales = pd.DataFrame.from_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets',
        'depenses_essence_totales_bdf.csv'), sep = ',', header = -1)
depenses_essence_totales.rename(columns = {1: 'essence bdf'}, inplace = True)
depenses_essence_totales.index = depenses_essence_totales.index.str.replace('en ', '')
depenses_essence_totales = depenses_essence_totales.sort_index()

comparaison_bdf_agregats = concat([depenses_transports_totales, depenses_carburants_totales, depenses_diesel_totales,
    depenses_essence_totales], axis = 1)
comparaison_bdf_agregats.index = comparaison_bdf_agregats.index.astype(int)

parametres_fiscalite_file_path = os.path.join(
    assets_directory,
    'openfisca_france_indirect_taxation',
    'assets',
    'Parametres fiscalite indirecte.xls'
    )
masses_cn_data_frame = pd.read_excel(parametres_fiscalite_file_path, sheetname = "consommation_CN")

masses_cn_carburants = masses_cn_data_frame[masses_cn_data_frame['Fonction'] == 'Carburants et lubrifiants']
masses_cn_carburants = masses_cn_carburants.transpose()
masses_cn_carburants.rename(columns = {76: 'carburants agregat'}, inplace = True)

masses_cn_transports = masses_cn_data_frame[masses_cn_data_frame['Fonction'] == 'Transports']
masses_cn_transports = masses_cn_transports.transpose()
masses_cn_transports.rename(columns = {69: 'transports agregat'}, inplace = True)

comparaison_bdf_agregats = concat([comparaison_bdf_agregats, masses_cn_carburants, masses_cn_transports], axis = 1)
comparaison_bdf_agregats = comparaison_bdf_agregats.dropna()

graph_builder_line(comparaison_bdf_agregats[['carburants agregat'] + ['carburants bdf']])
graph_builder_line(comparaison_bdf_agregats[['transports agregat'] + ['transports bdf']])
