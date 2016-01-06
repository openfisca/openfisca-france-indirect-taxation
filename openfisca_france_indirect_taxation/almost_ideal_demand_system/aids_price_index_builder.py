# -*- coding: utf-8 -*-
"""
Created on Tue Jul 07 09:53:33 2015

@author: thomas.douenne
"""

from __future__ import division

import pandas as pd
from pandas import concat
import datetime as dt

import os
import pkg_resources


def date_to_vag(date):
    args = date.split('_') + ['1']
    args = [int(arg) for arg in args]
    datetime = dt.datetime(*args)

    for vague in vagues:
        if vague['start'] <= datetime <= vague['end']:
            return vague['number']

    return None

# We want to obtain prices from the Excel file:

default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
indice_prix_mensuel_98_2015 = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'indice_prix_mensuel_98_2015.csv'
        ), sep =';', decimal = ','
    )



indice_prix_mensuel_98_2015 = indice_prix_mensuel_98_2015.astype(str)

# On veut que les biens prennent les mêmes noms que ceux du modèle, i.e. poste_coicop_xyz
# On doit donc changer le nom de tous les biens renseignés dans cette base de donnée
# On sépare les biens des coicop 1 à 9 des autres de manière à enlever les 0 à la fin des noms sans faire d'erreurs

coicop_one_nine = indice_prix_mensuel_98_2015.ix[:,:'_9600']

produits_rename = [column for column in coicop_one_nine.columns if len(column) == 5 and column[4:] == '0']
change_name = coicop_one_nine[produits_rename]
for element in change_name.columns:
    change_name.rename(columns={element: element[:4]}, inplace = True)

autres_produits_list = [column for column in coicop_one_nine.columns if len(column) != 5 or column[4:] != '0']
autres_produits = coicop_one_nine[autres_produits_list]

coicop_one_nine_new = pd.concat([change_name, autres_produits], axis = 1)

coicop_dix_douze = indice_prix_mensuel_98_2015.ix[:,'_10000':]
produits_rename = [column for column in coicop_dix_douze.columns if len(column) == 6 and column[5:] == '0']
change_name = coicop_dix_douze[produits_rename]
for element in change_name.columns:
    change_name.rename(columns={element: element[:5]}, inplace = True)

autres_produits_list = [column for column in coicop_dix_douze.columns if len(column) != 6 or column[5:] != '0']
autres_produits = coicop_dix_douze[autres_produits_list]

coicop_dix_douze_new = pd.concat([change_name, autres_produits], axis = 1)

indice_prix_mensuel_98_2015 = pd.concat([coicop_one_nine_new, coicop_dix_douze_new], axis = 1)
for element in indice_prix_mensuel_98_2015.columns:
    indice_prix_mensuel_98_2015.rename(columns={element: 'poste_coicop' + element}, inplace = True)
indice_prix_mensuel_98_2015.rename(
    columns={'poste_coicopAnnee': 'Annee', 'poste_coicopMois': 'Mois'}, inplace = True)

# Fixation des indices de prix non renseignés par l'Insee :

indice_prix_mensuel_98_2015['poste_coicop_1411'] = indice_prix_mensuel_98_2015['poste_coicop_100']
indice_prix_mensuel_98_2015['poste_coicop_2201'] = indice_prix_mensuel_98_2015['poste_coicop_220']
indice_prix_mensuel_98_2015['poste_coicop_2202'] = indice_prix_mensuel_98_2015['poste_coicop_220']
indice_prix_mensuel_98_2015['poste_coicop_2203'] = indice_prix_mensuel_98_2015['poste_coicop_220']
indice_prix_mensuel_98_2015['poste_coicop_230'] = indice_prix_mensuel_98_2015['poste_coicop_200']
indice_prix_mensuel_98_2015['poste_coicop_2411'] = indice_prix_mensuel_98_2015['poste_coicop_200']
indice_prix_mensuel_98_2015['poste_coicop_322'] = indice_prix_mensuel_98_2015['poste_coicop_321']
indice_prix_mensuel_98_2015['poste_coicop_412'] = indice_prix_mensuel_98_2015['poste_coicop_411']
indice_prix_mensuel_98_2015['poste_coicop_421'] = indice_prix_mensuel_98_2015['poste_coicop_411']
indice_prix_mensuel_98_2015['poste_coicop_444'] = indice_prix_mensuel_98_2015['poste_coicop_4414']
indice_prix_mensuel_98_2015['poste_coicop_442'] = indice_prix_mensuel_98_2015['poste_coicop_4412']
indice_prix_mensuel_98_2015['poste_coicop_4552'] = indice_prix_mensuel_98_2015['poste_coicop_4551']
indice_prix_mensuel_98_2015['poste_coicop_513'] = indice_prix_mensuel_98_2015['poste_coicop_5115']
indice_prix_mensuel_98_2015['poste_coicop_552'] = indice_prix_mensuel_98_2015['poste_coicop_551']
indice_prix_mensuel_98_2015['poste_coicop_5711'] = indice_prix_mensuel_98_2015['poste_coicop_500']
indice_prix_mensuel_98_2015['poste_coicop_5712'] = indice_prix_mensuel_98_2015['poste_coicop_500']
indice_prix_mensuel_98_2015['poste_coicop_612'] = indice_prix_mensuel_98_2015['poste_coicop_611']
indice_prix_mensuel_98_2015['poste_coicop_613'] = indice_prix_mensuel_98_2015['poste_coicop_611']
indice_prix_mensuel_98_2015['poste_coicop_630'] = indice_prix_mensuel_98_2015['poste_coicop_600']
indice_prix_mensuel_98_2015['poste_coicop_6412'] = indice_prix_mensuel_98_2015['poste_coicop_600']
indice_prix_mensuel_98_2015['poste_coicop_713'] = indice_prix_mensuel_98_2015['poste_coicop_712']
indice_prix_mensuel_98_2015['poste_coicop_734'] = indice_prix_mensuel_98_2015['poste_coicop_735']
indice_prix_mensuel_98_2015['poste_coicop_831'] = indice_prix_mensuel_98_2015['poste_coicop_812']
indice_prix_mensuel_98_2015['poste_coicop_832'] = indice_prix_mensuel_98_2015['poste_coicop_812']
indice_prix_mensuel_98_2015['poste_coicop_8141'] = indice_prix_mensuel_98_2015['poste_coicop_800']
indice_prix_mensuel_98_2015['poste_coicop_9122'] = indice_prix_mensuel_98_2015['poste_coicop_912']
indice_prix_mensuel_98_2015['poste_coicop_922'] = indice_prix_mensuel_98_2015['poste_coicop_921']
indice_prix_mensuel_98_2015['poste_coicop_923'] = indice_prix_mensuel_98_2015['poste_coicop_921']
indice_prix_mensuel_98_2015['poste_coicop_935'] = indice_prix_mensuel_98_2015['poste_coicop_934']
indice_prix_mensuel_98_2015['poste_coicop_943'] = indice_prix_mensuel_98_2015['poste_coicop_931']
indice_prix_mensuel_98_2015['poste_coicop_954'] = indice_prix_mensuel_98_2015['poste_coicop_953']
indice_prix_mensuel_98_2015['poste_coicop_10151'] = indice_prix_mensuel_98_2015['poste_coicop_1010']
indice_prix_mensuel_98_2015['poste_coicop_10152'] = indice_prix_mensuel_98_2015['poste_coicop_1010']
indice_prix_mensuel_98_2015['poste_coicop_1020'] = indice_prix_mensuel_98_2015['poste_coicop_1010']
indice_prix_mensuel_98_2015['poste_coicop_1040'] = indice_prix_mensuel_98_2015['poste_coicop_1010']
indice_prix_mensuel_98_2015['poste_coicop_1050'] = indice_prix_mensuel_98_2015['poste_coicop_1010']
indice_prix_mensuel_98_2015['poste_coicop_11113'] = indice_prix_mensuel_98_2015['poste_coicop_11112']
indice_prix_mensuel_98_2015['poste_coicop_1212'] = indice_prix_mensuel_98_2015['poste_coicop_1213']
indice_prix_mensuel_98_2015['poste_coicop_1220'] = indice_prix_mensuel_98_2015['poste_coicop_1200']
indice_prix_mensuel_98_2015['poste_coicop_1251'] = indice_prix_mensuel_98_2015['poste_coicop_1250']
indice_prix_mensuel_98_2015['poste_coicop_1255'] = indice_prix_mensuel_98_2015['poste_coicop_1250']
indice_prix_mensuel_98_2015['poste_coicop_1262'] = indice_prix_mensuel_98_2015['poste_coicop_1261']
indice_prix_mensuel_98_2015['poste_coicop_1291'] = indice_prix_mensuel_98_2015['poste_coicop_1200']


indice_prix_mensuel_98_2015['date'] = indice_prix_mensuel_98_2015[u'Annee'] + '_' + indice_prix_mensuel_98_2015[u'Mois']
indice_prix_mensuel_98_2015[[u'Annee'] + [u'Mois']] = indice_prix_mensuel_98_2015[[u'Annee'] + [u'Mois']].astype(float)
indice_prix_mensuel_98_2015['temps'] = \
    ((indice_prix_mensuel_98_2015[u'Annee'] - 1998) * 12) + indice_prix_mensuel_98_2015[u'Mois']
del indice_prix_mensuel_98_2015[u'Annee']
indice_prix_mensuel_98_2015['mois'] = indice_prix_mensuel_98_2015[u'Mois'].copy()
del indice_prix_mensuel_98_2015[u'Mois']

produits = list(column for column in indice_prix_mensuel_98_2015.columns if column[:13] == 'poste_coicop_')

df_indice_prix_produit = pd.melt(indice_prix_mensuel_98_2015, id_vars = ['date', 'temps', 'mois'], value_vars=produits,
    value_name = 'prix', var_name = 'bien')
# df_indice_prix_produit.bien = df_indice_prix_produit.bien.str.split('_').str[1]

vagues = [
    dict(
        number = 9,
        start = dt.datetime(2000, 5, 9),
        end = dt.datetime(2000, 6, 18),
        ),
    dict(
        number = 10,
        start = dt.datetime(2000, 6, 19),
        end = dt.datetime(2000, 7, 30),
        ),
    dict(
        number = 11,
        start = dt.datetime(2000, 8, 14),
        end = dt.datetime(2000, 9, 24),
        ),
    dict(
        number = 12,
        start = dt.datetime(2000, 9, 25),
        end = dt.datetime(2000, 11, 5),
        ),
    dict(
        number = 13,
        start = dt.datetime(2000, 11, 6),
        end = dt.datetime(2000, 12, 17),
        ),
    dict(
        number = 14,
        start = dt.datetime(2001, 1, 2),
        end = dt.datetime(2001, 2, 11),
        ),
    dict(
        number = 15,
        start = dt.datetime(2001, 2, 12),
        end = dt.datetime(2001, 3, 25),
        ),
    dict(
        number = 16,
        start = dt.datetime(2001, 3, 26),
        end = dt.datetime(2001, 5, 6),
        ),
    dict(
        number = 17,
        start = dt.datetime(2005, 3, 1),
        end = dt.datetime(2005, 4, 24),
        ),
    dict(
        number = 18,
        start = dt.datetime(2005, 4, 25),
        end = dt.datetime(2005, 6, 19),
        ),
    dict(
        number = 19,
        start = dt.datetime(2005, 6, 20),
        end = dt.datetime(2005, 8, 28),
        ),
    dict(
        number = 20,
        start = dt.datetime(2005, 8, 29),
        end = dt.datetime(2005, 10, 23),
        ),
    dict(
        number = 21,
        start = dt.datetime(2005, 10, 24),
        end = dt.datetime(2005, 12, 18),
        ),
    dict(
        number = 22,
        start = dt.datetime(2006, 1, 2),
        end = dt.datetime(2006, 2, 27),
        ),
    dict(
        number = 23,
        start = dt.datetime(2010, 10, 4),
        end = dt.datetime(2010, 11, 27),
        ),
    dict(
        number = 24,
        start = dt.datetime(2010, 11, 29),
        end = dt.datetime(2011, 1, 29),
        ),
    dict(
        number = 25,
        start = dt.datetime(2011, 1, 31),
        end = dt.datetime(2011, 3, 26),
        ),
    dict(
        number = 26,
        start = dt.datetime(2011, 3, 28),
        end = dt.datetime(2011, 5, 21),
        ),
    dict(
        number = 27,
        start = dt.datetime(2011, 5, 23),
        end = dt.datetime(2011, 7, 23),
        ),
    dict(
        number = 28,
        start = dt.datetime(2011, 8, 1),
        end = dt.datetime(2011, 10, 1),
        ),
    ]

df_indice_prix_produit['vag'] = df_indice_prix_produit['date'].map(date_to_vag)
df_indice_prix_produit = df_indice_prix_produit.dropna()
df_indice_prix_produit['vag'] = df_indice_prix_produit['vag'].astype(int)  # delete the .0 after each number
df_indice_prix_produit['vag'] = df_indice_prix_produit['vag'].astype(str)
df_indice_prix_produit['indice_prix_produit'] = df_indice_prix_produit['bien'] + '_' + df_indice_prix_produit['vag']
df_indice_prix_produit = df_indice_prix_produit.drop_duplicates(
    subset = ['indice_prix_produit'], keep = 'last')
