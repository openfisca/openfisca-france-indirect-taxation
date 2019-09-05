# -*- coding: utf-8 -*-

# L'objectif des "compare" est d'évaluer la qualité des calages effectués. Ils comparent les dépenses ou quantités
# agrégées de Budget des Familles après calage, avec celles de la comptabilité nationale.

# Import de modules généraux


from pandas import concat
import pkg_resources
import os
import pandas as pd

# Import de modules spécifiques à Openfisca
from ipp_macro_series_parser.agregats_transports.transports_cleaner import g_3a
# Import de paramètres de la législation (montant des accises de la TICPE)
from openfisca_france_indirect_taxation.examples.dataframes_from_legislation.get_accises import \
    get_accise_ticpe_majoree

"""Ici on applique aux quantités de carburants consommées par des véhicules autres que les ménages
la ticpe à taux plein. En réalité, un certain nombre d'exonération s'appliquent pour les professionels.
On calcul donc simplement une borne supérieure des recettes engendrées"""

# Import des fichiers csv donnant les montants agrégés des dépenses en TICPE d'après les enquêtes BdF.
# Ces montants sont calculés dans compute_depenses_ticpe
assets_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )

products = ['totales', 'essence', 'diesel']
depenses_ticpe_bdf = pd.DataFrame()
for element in products:
    depenses_ticpe = pd.read_csv(
        os.path.join(
            assets_directory,
            'openfisca_france_indirect_taxation', 'assets', 'depenses',
            'depenses_ticpe_{}_bdf.csv'.format(element)),
        sep = ',',
        header = -1
        )
    depenses_ticpe.rename(columns = {1: '{} bdf'.format(element)}, inplace = True)
    depenses_ticpe.index = depenses_ticpe.index.str.replace('en millions d euros en ', '')
    depenses_ticpe = depenses_ticpe.sort_index()
    depenses_ticpe.index = depenses_ticpe.index.astype(int)
    depenses_ticpe_bdf = concat([depenses_ticpe_bdf, depenses_ticpe], axis = 1)

accises = get_accise_ticpe_majoree()
accises.index = accises.index.astype(int)

nombre_essence = g_3a[g_3a['categorie'] == 'ESSENCE']
del nombre_essence['categorie']
nombre_essence = nombre_essence.set_index('index')
nombre_essence = nombre_essence.transpose()
consommation_essence = nombre_essence[['Voitures particulières', 'Livraisons CPDP (1)']].copy()
consommation_essence['vehicules essence non particuliers'] = (
    consommation_essence['Livraisons CPDP (1)'] - consommation_essence['Voitures particulières']
    )

nombre_diesel = g_3a[g_3a['categorie'] == 'GAZOLE']
del nombre_diesel['categorie']
nombre_diesel = nombre_diesel.set_index('index')
nombre_diesel = nombre_diesel.transpose()
consommation_diesel = nombre_diesel[['Voitures particulières', 'Livraisons CPDP (1)']].copy()
consommation_diesel['vehicules diesel non particuliers'] = (
    consommation_diesel['Livraisons CPDP (1)'] - consommation_diesel['Voitures particulières']
    )

recettes_ticpe_non_vp = concat(
    [consommation_essence['vehicules essence non particuliers'],
    consommation_diesel['vehicules diesel non particuliers'], accises],
    axis = 1)

recettes_ticpe_non_vp['recettes essence'] = (
    recettes_ticpe_non_vp['vehicules essence non particuliers']
    * recettes_ticpe_non_vp['accise majoree sans plomb'] / 100
    )

recettes_ticpe_non_vp['recettes diesel'] = (
    recettes_ticpe_non_vp['vehicules diesel non particuliers']
    * recettes_ticpe_non_vp['accise majoree diesel'] / 100
    )

recettes_ticpe_non_vp['recettes totales non vp'] = (
    recettes_ticpe_non_vp['recettes diesel'] + recettes_ticpe_non_vp['recettes essence'])

recettes_ticpe_totale = concat([recettes_ticpe_non_vp[['recettes totales non vp']
+ ['recettes diesel', 'recettes essence']], depenses_ticpe_bdf], axis = 1)

recettes_ticpe_totale = recettes_ticpe_totale.dropna()
recettes_ticpe_totale['recettes totales tous carburants'] = \
    recettes_ticpe_totale['recettes totales non vp'] + recettes_ticpe_totale['totales bdf']
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
