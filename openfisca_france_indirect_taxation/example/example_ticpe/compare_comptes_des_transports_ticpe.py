# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 11:47:11 2015

@author: thomas.douenne
"""

from __future__ import division

from pandas import concat
import pkg_resources
import os
import pandas as pd

from ipp_macro_series_parser.agregats_transports.transports_cleaner import g_3a
from openfisca_france_indirect_taxation.get_dataframe_from_legislation.get_accises import \
    get_accise_ticpe_majoree

"""Ici on applique aux quantités de carburants consommées par des véhicules autres que les ménages
la ticpe à taux plein. En réalité, un certain nombre d'exonération s'appliquent pour les professionels.
On calcul donc simplement une borne supérieure des recettes engendrées"""

assets_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )

depenses_ticpe_totales_bdf = pd.DataFrame.from_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets',
        'depenses_ticpe_totales_bdf.csv'), sep = ',', header = -1)
depenses_ticpe_totales_bdf.rename(columns = {1: 'total bdf'}, inplace = True)
depenses_ticpe_totales_bdf.index = depenses_ticpe_totales_bdf.index.str.replace('en millions d euros en ', '')
depenses_ticpe_totales_bdf = depenses_ticpe_totales_bdf.sort_index()
depenses_ticpe_totales_bdf.index = depenses_ticpe_totales_bdf.index.astype(int)

depenses_ticpe_diesel_bdf = pd.DataFrame.from_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets',
        'depenses_ticpe_diesel_bdf.csv'), sep = ',', header = -1)
depenses_ticpe_diesel_bdf.rename(columns = {1: 'diesel bdf'}, inplace = True)
depenses_ticpe_diesel_bdf.index = depenses_ticpe_diesel_bdf.index.str.replace('en millions d euros en ', '')
depenses_ticpe_diesel_bdf = depenses_ticpe_diesel_bdf.sort_index()
depenses_ticpe_diesel_bdf.index = depenses_ticpe_diesel_bdf.index.astype(int)


depenses_ticpe_essence_bdf = pd.DataFrame.from_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets',
        'depenses_ticpe_essence_bdf.csv'), sep = ',', header = -1)
depenses_ticpe_essence_bdf.rename(columns = {1: 'essence bdf'}, inplace = True)
depenses_ticpe_essence_bdf.index = depenses_ticpe_essence_bdf.index.str.replace('en millions d euros en ', '')
depenses_ticpe_essence_bdf = depenses_ticpe_essence_bdf.sort_index()
depenses_ticpe_essence_bdf.index = depenses_ticpe_essence_bdf.index.astype(int)


accises = get_accise_ticpe_majoree()
accises.index = accises.index.astype(int)

nombre_essence = g_3a[g_3a['categorie'] == 'ESSENCE']
del nombre_essence['categorie']
nombre_essence = nombre_essence.set_index('index')
nombre_essence = nombre_essence.transpose()
consommation_essence = nombre_essence[[u'Voitures particulières'] + [u'Livraisons CPDP (1)']].copy()
consommation_essence['vehicules essence non particuliers'] = (
    consommation_essence[u'Livraisons CPDP (1)'] - consommation_essence[u'Voitures particulières']
    )

nombre_diesel = g_3a[g_3a['categorie'] == 'GAZOLE']
del nombre_diesel['categorie']
nombre_diesel = nombre_diesel.set_index('index')
nombre_diesel = nombre_diesel.transpose()
consommation_diesel = nombre_diesel[[u'Voitures particulières'] + [u'Livraisons CPDP (1)']].copy()
consommation_diesel['vehicules diesel non particuliers'] = (
    consommation_diesel[u'Livraisons CPDP (1)'] - consommation_diesel[u'Voitures particulières']
    )

recettes_ticpe_non_vp = concat(
    [consommation_essence['vehicules essence non particuliers'],
    consommation_diesel['vehicules diesel non particuliers'], accises],
    axis = 1)

recettes_ticpe_non_vp['recettes essence'] = (
    recettes_ticpe_non_vp['vehicules essence non particuliers'] *
    recettes_ticpe_non_vp['accise majoree sans plomb'] / 100
    )

recettes_ticpe_non_vp['recettes diesel'] = (
    recettes_ticpe_non_vp['vehicules diesel non particuliers'] *
    recettes_ticpe_non_vp['accise majoree diesel'] / 100
    )

recettes_ticpe_non_vp['recettes totales non vp'] = (
    recettes_ticpe_non_vp['recettes diesel'] + recettes_ticpe_non_vp['recettes essence'])

recettes_ticpe_totale = concat([recettes_ticpe_non_vp[['recettes totales non vp'] +
    ['recettes diesel'] + ['recettes essence']], depenses_ticpe_totales_bdf, depenses_ticpe_diesel_bdf,
    depenses_ticpe_essence_bdf], axis = 1)

recettes_ticpe_totale = recettes_ticpe_totale.dropna()
recettes_ticpe_totale['recettes totales tous carburants'] = \
    recettes_ticpe_totale['recettes totales non vp'] + recettes_ticpe_totale['total bdf']
recettes_ticpe_totale['recettes totales diesel'] = \
    recettes_ticpe_totale['recettes diesel'] + recettes_ticpe_totale['diesel bdf']
recettes_ticpe_totale['recettes totales essence'] = \
    recettes_ticpe_totale['recettes essence'] + recettes_ticpe_totale['essence bdf']

recettes_ticpe = dict()
recettes_ticpe_diesel = dict()
recettes_ticpe_essence = dict()
for year in [2000, 2005, 2011]:
    recettes_ticpe['en millions d euros en {}'.format(year)] = \
        recettes_ticpe_totale['recettes totales tous carburants'].loc[year]
    recettes_ticpe_diesel['en millions d euros en {}'.format(year)] = \
        recettes_ticpe_totale['recettes totales diesel'].loc[year]
    recettes_ticpe_essence['en millions d euros en {}'.format(year)] = \
        recettes_ticpe_totale['recettes totales essence'].loc[year]
