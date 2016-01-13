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

products = ['transports', 'carburants', 'essence', 'diesel']
depenses_bdf = pd.DataFrame()
for element in products:
    depenses = pd.DataFrame.from_csv(os.path.join(assets_directory,
            'openfisca_france_indirect_taxation', 'assets',
            'depenses_{}_totales_bdf.csv').format(element), sep = ',', header = -1)
    depenses.rename(columns = {1: '{} bdf'.format(element)}, inplace = True)
    depenses.index = depenses.index.str.replace('en ', '')
    depenses = depenses.sort_index()
    depenses_bdf = concat([depenses, depenses_bdf], axis = 1)

depenses_bdf.index = depenses_bdf.index.astype(int)

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

comparaison_bdf_agregats = concat([depenses_bdf, masses_cn_carburants, masses_cn_transports], axis = 1)
comparaison_bdf_agregats = comparaison_bdf_agregats.dropna()

graph_builder_line(comparaison_bdf_agregats[['carburants agregat'] + ['carburants bdf']])
graph_builder_line(comparaison_bdf_agregats[['transports agregat'] + ['transports bdf']])
