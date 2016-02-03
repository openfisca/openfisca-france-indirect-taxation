# -*- coding: utf-8 -*-
"""
Created on Mon Feb 01 16:31:53 2016

@author: thomas.douenne
"""

from __future__ import division

import os
import pkg_resources
import pandas as pd


def indices_prix_carbus(year):
    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    prix_carbu = pd.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'prix',
            'prix_mensuel_carbu_match_to_vag.csv'
            ), sep =';', decimal = ','
        )
    prix_carbu = prix_carbu[['diesel_ttc'] + ['super_95_ttc'] + ['vag']].astype(float)

    quantite_carbu_vp_france = pd.read_csv(os.path.join(default_config_files_directory,
            'openfisca_france_indirect_taxation', 'assets', 'quantites',
            'quantite_carbu_vp_france.csv'), sep = ';')
    quantite_carbu_vp_france.rename(columns = {'Unnamed: 0': 'annee'}, inplace = True)

    quantite_carbu_vp_france['part_conso_ess'] = \
        quantite_carbu_vp_france['essence'] / (quantite_carbu_vp_france['essence'] + quantite_carbu_vp_france['diesel'])
    quantite_carbu_vp_france = quantite_carbu_vp_france[quantite_carbu_vp_france['annee'] == year]
    part_conso_ess = quantite_carbu_vp_france['part_conso_ess'].min()

    prix_carbu['indice_ess'] = prix_carbu['super_95_ttc'] / (prix_carbu['super_95_ttc'] * part_conso_ess +
        prix_carbu['diesel_ttc'] * (1 - part_conso_ess))
    prix_carbu['indice_die'] = prix_carbu['indice_ess'] * (prix_carbu['diesel_ttc'] / prix_carbu['super_95_ttc'])

    return prix_carbu[['indice_ess'] + ['indice_die'] + ['vag']]


def add_area_dummy(dataframe):
    areas = ['rural', 'villes_petites', 'villes_moyennes', 'villes_grandes', 'agglo_paris']
    for area in areas:
        dataframe[area] = 0
    dataframe.loc[dataframe['strate'] == 0, 'rural'] = 1
    dataframe.loc[dataframe['strate'] == 1, 'villes_petites'] = 1
    dataframe.loc[dataframe['strate'] == 2, 'villes_moyennes'] = 1
    dataframe.loc[dataframe['strate'] == 3, 'villes_grandes'] = 1
    dataframe.loc[dataframe['strate'] == 4, 'agglo_paris'] = 1
    return dataframe


def add_vag_dummy(dataframe):
    first_vag = dataframe['vag'].min()
    last_vag = dataframe['vag'].max()
    for vag in range(first_vag, last_vag + 1):
        dataframe['vag_{}'.format(vag)] = 0
        dataframe.loc[dataframe['vag'] == vag, 'vag_{}'.format(vag)] = 1
    return dataframe


# On veut construire des indices de prix plus précis pour les carburants, en prenant en compte le type de voitures
# dont disposent les ménages. On pondère donc en utilisant un indice de prix qui dépend de la part de véhicules essences
# de chaque ménage. On estime que si 1/2 véhicule est essence, on affecte pour 1/2 l'indice du prix de l'essence,
# et sur 1/2 celui du diesel. On ne prend donc pas en compte les distances parcourus avec chaque véhicule.
def price_carbu_pond(dataframe):
    dataframe['veh_tot'] = dataframe['veh_essence'] + dataframe['veh_diesel']
    dataframe['part_veh_essence'] = 0.5
    dispose_de_vehicule = dataframe['veh_tot'] != 0
    dataframe.loc[dispose_de_vehicule, 'part_veh_essence'] = \
        dataframe.loc[dispose_de_vehicule, 'veh_essence'] / dataframe.loc[dispose_de_vehicule, 'veh_tot']
    dataframe['prix_carbu'] = dataframe['prix_carbu'] * (dataframe['part_veh_essence'] * dataframe['indice_ess'] +
        (1 - dataframe['part_veh_essence']) * dataframe['indice_die'])
    return dataframe
