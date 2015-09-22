# -*- coding: utf-8 -*-
"""
Created on Tue Jul 07 09:53:33 2015

@author: thomas.douenne
"""

from __future__ import division

import pandas as pd
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

# Fixation des indices de prix non renseignés par l'Insee :

indice_prix_mensuel_98_2015['_1411'] = indice_prix_mensuel_98_2015['_1000']
indice_prix_mensuel_98_2015['_2201'] = indice_prix_mensuel_98_2015['_2200']
indice_prix_mensuel_98_2015['_2202'] = indice_prix_mensuel_98_2015['_2200']
indice_prix_mensuel_98_2015['_2203'] = indice_prix_mensuel_98_2015['_2200']
indice_prix_mensuel_98_2015['_2300'] = indice_prix_mensuel_98_2015['_2000']
indice_prix_mensuel_98_2015['_2411'] = indice_prix_mensuel_98_2015['_2000']
indice_prix_mensuel_98_2015['_3220'] = indice_prix_mensuel_98_2015['_3210']
indice_prix_mensuel_98_2015['_4120'] = indice_prix_mensuel_98_2015['_4110']
indice_prix_mensuel_98_2015['_421'] = indice_prix_mensuel_98_2015['_4110']
indice_prix_mensuel_98_2015['_4440'] = indice_prix_mensuel_98_2015['_4414']
indice_prix_mensuel_98_2015['_4420'] = indice_prix_mensuel_98_2015['_4412']
indice_prix_mensuel_98_2015['_4552'] = indice_prix_mensuel_98_2015['_4551']
indice_prix_mensuel_98_2015['_5130'] = indice_prix_mensuel_98_2015['_5115']
indice_prix_mensuel_98_2015['_5520'] = indice_prix_mensuel_98_2015['_5510']
indice_prix_mensuel_98_2015['_5711'] = indice_prix_mensuel_98_2015['_5000']
indice_prix_mensuel_98_2015['_5712'] = indice_prix_mensuel_98_2015['_5000']
indice_prix_mensuel_98_2015['_6120'] = indice_prix_mensuel_98_2015['_6110']
indice_prix_mensuel_98_2015['_6130'] = indice_prix_mensuel_98_2015['_6110']
indice_prix_mensuel_98_2015['_6300'] = indice_prix_mensuel_98_2015['_6000']
indice_prix_mensuel_98_2015['_6412'] = indice_prix_mensuel_98_2015['_6000']
indice_prix_mensuel_98_2015['_7130'] = indice_prix_mensuel_98_2015['_7120']
indice_prix_mensuel_98_2015['_7340'] = indice_prix_mensuel_98_2015['_7350']
indice_prix_mensuel_98_2015['_8310'] = indice_prix_mensuel_98_2015['_8120']
indice_prix_mensuel_98_2015['_8320'] = indice_prix_mensuel_98_2015['_8120']
indice_prix_mensuel_98_2015['_8141'] = indice_prix_mensuel_98_2015['_8000']
indice_prix_mensuel_98_2015['_9122'] = indice_prix_mensuel_98_2015['_9120']
indice_prix_mensuel_98_2015['_9220'] = indice_prix_mensuel_98_2015['_9210']
indice_prix_mensuel_98_2015['_9230'] = indice_prix_mensuel_98_2015['_9210']
indice_prix_mensuel_98_2015['_9350'] = indice_prix_mensuel_98_2015['_9340']
indice_prix_mensuel_98_2015['_9430'] = indice_prix_mensuel_98_2015['_9310']
indice_prix_mensuel_98_2015['_9540'] = indice_prix_mensuel_98_2015['_9530']
indice_prix_mensuel_98_2015['_10151'] = indice_prix_mensuel_98_2015['_10100']
indice_prix_mensuel_98_2015['_10152'] = indice_prix_mensuel_98_2015['_10100']
indice_prix_mensuel_98_2015['_10200'] = indice_prix_mensuel_98_2015['_10100']
indice_prix_mensuel_98_2015['_10400'] = indice_prix_mensuel_98_2015['_10100']
indice_prix_mensuel_98_2015['_10500'] = indice_prix_mensuel_98_2015['_10100']
indice_prix_mensuel_98_2015['_11113'] = indice_prix_mensuel_98_2015['_11112']
indice_prix_mensuel_98_2015['_12120'] = indice_prix_mensuel_98_2015['_12130']
indice_prix_mensuel_98_2015['_12200'] = indice_prix_mensuel_98_2015['_12000']
indice_prix_mensuel_98_2015['_12510'] = indice_prix_mensuel_98_2015['_12500']
indice_prix_mensuel_98_2015['_12550'] = indice_prix_mensuel_98_2015['_12500']
indice_prix_mensuel_98_2015['_12620'] = indice_prix_mensuel_98_2015['_12610']
indice_prix_mensuel_98_2015['_12910'] = indice_prix_mensuel_98_2015['_12000']

indice_prix_mensuel_98_2015['date'] = indice_prix_mensuel_98_2015[u'Annee'] + '_' + indice_prix_mensuel_98_2015[u'Mois']
indice_prix_mensuel_98_2015[[u'Annee'] + [u'Mois']] = indice_prix_mensuel_98_2015[[u'Annee'] + [u'Mois']].astype(float)
indice_prix_mensuel_98_2015['temps'] = \
    ((indice_prix_mensuel_98_2015[u'Annee'] - 1998) * 12) + indice_prix_mensuel_98_2015[u'Mois']
del indice_prix_mensuel_98_2015[u'Annee']
indice_prix_mensuel_98_2015['mois'] = indice_prix_mensuel_98_2015[u'Mois'].copy()
del indice_prix_mensuel_98_2015[u'Mois']
produits = list(indice_prix_mensuel_98_2015.columns[:-3])
df_indice_prix_produit = pd.melt(indice_prix_mensuel_98_2015, id_vars = ['date', 'temps', 'mois'], value_vars=produits,
    value_name = 'prix', var_name = 'bien')
df_indice_prix_produit.bien = df_indice_prix_produit.bien.str.split('_').str[1]

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
df_indice_prix_produit['vag'] = df_indice_prix_produit['vag'].astype(str)
df_indice_prix_produit['indice_prix_produit'] = df_indice_prix_produit['vag'] + '_' + df_indice_prix_produit['bien']
df_indice_prix_produit['indice_prix_produit'] = df_indice_prix_produit['indice_prix_produit'].str.replace('.0_', '')
df_indice_prix_produit = df_indice_prix_produit.drop_duplicates(cols='indice_prix_produit', take_last=True)
