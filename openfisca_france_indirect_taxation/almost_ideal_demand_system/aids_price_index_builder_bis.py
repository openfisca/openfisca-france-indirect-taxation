# -*- coding: utf-8 -*-

from __future__ import division

import pandas as pd
from pandas import concat
import datetime as dt

import os
import pkg_resources


from openfisca_france_indirect_taxation.utils import get_input_data_frame


def date_to_vag(date):
    args = date.split('_') + ['1']
    args = [int(arg) for arg in args]
    datetime = dt.datetime(*args)

    for vague in vagues:
        if vague['start'] <= datetime <= vague['end']:
            return vague['number']

    return None

# We want to obtain prices from the Excel file:

    
df = get_input_data_frame(2011)
colonnes_df = [column for column in df.columns if column[:6] == 'poste_']

    
default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
indice_prix_mensuel_98_2015 = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'prix',
        'indice_prix_mensuel_98_2015.csv'
        ), sep =';', decimal = ','
    )

indice_prix_mensuel_98_2015 = indice_prix_mensuel_98_2015.astype(str)

# On veut que les biens prennent les mêmes noms que ceux du modèle, i.e. poste_x_y_z
# On doit donc changer le nom de tous les biens renseignés dans cette base de donnée
# On sépare les biens des coicop 1 à 9 des autres de manière à enlever les 0 à la fin des noms sans faire d'erreurs

coicop_un_neuf = indice_prix_mensuel_98_2015.ix[:,:'_9600']

produits_rename = [column for column in coicop_un_neuf.columns if len(column) == 5 and column[4:] == '0']
change_name = coicop_un_neuf[produits_rename]
for element in change_name.columns:
    change_name.rename(columns={element: element[:4]}, inplace = True)

autres_produits_list = [column for column in coicop_un_neuf.columns if len(column) != 5 or column[4:] != '0']
autres_produits = coicop_un_neuf[autres_produits_list]

coicop_un_neuf_new = pd.concat([change_name, autres_produits], axis = 1)

for col in coicop_un_neuf_new.columns.tolist():
    if col[:1] == '_':
        coicop_un_neuf_new.rename(columns={col:'poste_0{}_'.format(col[1]) + col[2:]}, inplace = True)        
            
coicop_dix_douze = indice_prix_mensuel_98_2015.ix[:,'_10000':]
produits_rename = [column for column in coicop_dix_douze.columns if len(column) == 6 and column[5:] == '0']
change_name = coicop_dix_douze[produits_rename]
for element in change_name.columns:
    change_name.rename(columns={element: element[:5]}, inplace = True)

autres_produits_list = [column for column in coicop_dix_douze.columns if len(column) != 6 or column[5:] != '0']
autres_produits = coicop_dix_douze[autres_produits_list]

coicop_dix_douze_new = pd.concat([change_name, autres_produits], axis = 1)

for col in coicop_dix_douze_new.columns.tolist():
    if col[:1] == '_':
        coicop_dix_douze_new.rename(columns={col:'poste_{}_'.format(col[1:3]) + col[3:]}, inplace = True)        

indice_prix_mensuel_98_2015 = pd.concat([coicop_un_neuf_new, coicop_dix_douze_new], axis = 1)

colonnes_prix = indice_prix_mensuel_98_2015.columns.tolist()

# Associer toutes ces variabes à un code de BdF
# Pour les variables de BdF n'ayant pas de prix correspondant, en imputer un manuellement
# Pour ce faire, utiliser les informations reliant ces indices à des biens


# Fixation des indices de prix non renseignés par l'Insee :

indice_prix_mensuel_98_2015['poste_1411'] = indice_prix_mensuel_98_2015['poste_100']
indice_prix_mensuel_98_2015['poste_2201'] = indice_prix_mensuel_98_2015['poste_220']
indice_prix_mensuel_98_2015['poste_2202'] = indice_prix_mensuel_98_2015['poste_220']
indice_prix_mensuel_98_2015['poste_2203'] = indice_prix_mensuel_98_2015['poste_220']
indice_prix_mensuel_98_2015['poste_230'] = indice_prix_mensuel_98_2015['poste_200']
indice_prix_mensuel_98_2015['poste_2411'] = indice_prix_mensuel_98_2015['poste_200']
indice_prix_mensuel_98_2015['poste_322'] = indice_prix_mensuel_98_2015['poste_321']
indice_prix_mensuel_98_2015['poste_412'] = indice_prix_mensuel_98_2015['poste_411']
indice_prix_mensuel_98_2015['poste_421'] = indice_prix_mensuel_98_2015['poste_411']
indice_prix_mensuel_98_2015['poste_444'] = indice_prix_mensuel_98_2015['poste_4414']
indice_prix_mensuel_98_2015['poste_442'] = indice_prix_mensuel_98_2015['poste_4412']
indice_prix_mensuel_98_2015['poste_4552'] = indice_prix_mensuel_98_2015['poste_4551']
indice_prix_mensuel_98_2015['poste_513'] = indice_prix_mensuel_98_2015['poste_5115']
indice_prix_mensuel_98_2015['poste_552'] = indice_prix_mensuel_98_2015['poste_551']
indice_prix_mensuel_98_2015['poste_5711'] = indice_prix_mensuel_98_2015['poste_500']
indice_prix_mensuel_98_2015['poste_5712'] = indice_prix_mensuel_98_2015['poste_500']
indice_prix_mensuel_98_2015['poste_612'] = indice_prix_mensuel_98_2015['poste_611']
indice_prix_mensuel_98_2015['poste_613'] = indice_prix_mensuel_98_2015['poste_611']
indice_prix_mensuel_98_2015['poste_630'] = indice_prix_mensuel_98_2015['poste_600']
indice_prix_mensuel_98_2015['poste_6412'] = indice_prix_mensuel_98_2015['poste_600']
indice_prix_mensuel_98_2015['poste_713'] = indice_prix_mensuel_98_2015['poste_712']
indice_prix_mensuel_98_2015['poste_734'] = indice_prix_mensuel_98_2015['poste_735']
indice_prix_mensuel_98_2015['poste_831'] = indice_prix_mensuel_98_2015['poste_812']
indice_prix_mensuel_98_2015['poste_832'] = indice_prix_mensuel_98_2015['poste_812']
indice_prix_mensuel_98_2015['poste_8141'] = indice_prix_mensuel_98_2015['poste_800']
indice_prix_mensuel_98_2015['poste_9122'] = indice_prix_mensuel_98_2015['poste_912']
indice_prix_mensuel_98_2015['poste_922'] = indice_prix_mensuel_98_2015['poste_921']
indice_prix_mensuel_98_2015['poste_923'] = indice_prix_mensuel_98_2015['poste_921']
indice_prix_mensuel_98_2015['poste_935'] = indice_prix_mensuel_98_2015['poste_934']
indice_prix_mensuel_98_2015['poste_943'] = indice_prix_mensuel_98_2015['poste_931']
indice_prix_mensuel_98_2015['poste_954'] = indice_prix_mensuel_98_2015['poste_953']
indice_prix_mensuel_98_2015['poste_10151'] = indice_prix_mensuel_98_2015['poste_1010']
indice_prix_mensuel_98_2015['poste_10152'] = indice_prix_mensuel_98_2015['poste_1010']
indice_prix_mensuel_98_2015['poste_1020'] = indice_prix_mensuel_98_2015['poste_1010']
indice_prix_mensuel_98_2015['poste_1040'] = indice_prix_mensuel_98_2015['poste_1010']
indice_prix_mensuel_98_2015['poste_1050'] = indice_prix_mensuel_98_2015['poste_1010']
indice_prix_mensuel_98_2015['poste_11113'] = indice_prix_mensuel_98_2015['poste_11112']
indice_prix_mensuel_98_2015['poste_1212'] = indice_prix_mensuel_98_2015['poste_1213']
indice_prix_mensuel_98_2015['poste_1220'] = indice_prix_mensuel_98_2015['poste_1200']
indice_prix_mensuel_98_2015['poste_1251'] = indice_prix_mensuel_98_2015['poste_1250']
indice_prix_mensuel_98_2015['poste_1255'] = indice_prix_mensuel_98_2015['poste_1250']
indice_prix_mensuel_98_2015['poste_1262'] = indice_prix_mensuel_98_2015['poste_1261']
indice_prix_mensuel_98_2015['poste_1291'] = indice_prix_mensuel_98_2015['poste_1200']






indice_prix_mensuel_98_2015['date'] = indice_prix_mensuel_98_2015[u'Annee'] + '_' + indice_prix_mensuel_98_2015[u'Mois']
indice_prix_mensuel_98_2015[[u'Annee'] + [u'Mois']] = indice_prix_mensuel_98_2015[[u'Annee'] + [u'Mois']].astype(float)
indice_prix_mensuel_98_2015['temps'] = \
    ((indice_prix_mensuel_98_2015[u'Annee'] - 1998) * 12) + indice_prix_mensuel_98_2015[u'Mois']
del indice_prix_mensuel_98_2015[u'Annee']
indice_prix_mensuel_98_2015['mois'] = indice_prix_mensuel_98_2015[u'Mois'].copy()
del indice_prix_mensuel_98_2015[u'Mois']

produits = list(column for column in indice_prix_mensuel_98_2015.columns if column[:13] == 'poste_')

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
