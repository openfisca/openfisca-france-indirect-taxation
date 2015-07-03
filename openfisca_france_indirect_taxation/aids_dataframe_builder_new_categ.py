# -*- coding: utf-8 -*-
"""
Created on Fri Jul 03 16:11:38 2015

@author: thomas.douenne
"""

from __future__ import division

import pandas as pd
import numpy as np
from pandas import concat
import datetime as dt

from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame, simulate_df

import os
from ConfigParser import SafeConfigParser
from openfisca_france_data import default_config_files_directory as config_files_directory

# We want to obtain prices from the Excel file:

parser = SafeConfigParser()
config_local_ini = os.path.join(config_files_directory, 'config_local.ini')
config_ini = os.path.join(config_files_directory, 'config.ini')
parser.read([config_ini, config_local_ini])

directory_path = os.path.normpath(
    parser.get("openfisca_france_indirect_taxation", "assets")
    )
indice_prix_mensuel_98_2015 = pd.read_csv(os.path.join(directory_path, "indice_prix_mensuel_98_2015.csv"),
    sep =';', decimal = ',')

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
df2 = pd.melt(indice_prix_mensuel_98_2015, id_vars = ['date', 'temps', 'mois'], value_vars=produits,
    value_name = 'prix', var_name = 'bien')
df2.bien = df2.bien.str.split('_').str[1]

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


def date_to_vag(date):
    args = date.split('_') + ['1']
    args = [int(arg) for arg in args]
    datetime = dt.datetime(*args)

    for vague in vagues:
        if vague['start'] <= datetime <= vague['end']:
            return vague['number']

    return None

df2['vag'] = df2['date'].map(date_to_vag)
df2.dropna(inplace = True)
df2['vag'] = df2['vag'].astype(str)
df2['indice_prix_produit'] = df2['vag'] + '_' + df2['bien']
df2['indice_prix_produit'] = df2['indice_prix_produit'].str.replace('.0_', '')
df2 = df2.drop_duplicates(cols='indice_prix_produit', take_last=True)

# Now that we have our price indexes, we construct a dataframe with the rest of the information

data_frame_for_reg = None
for year in [2011]:
    aggregates_data_frame = get_input_data_frame(year)
    aggregates_data_frame['depenses_tot'] = 0
    produits = [column for column in aggregates_data_frame.columns if column.isdigit()]
    aggregates_data_frame['depenses_tot'] = aggregates_data_frame[produits].sum(axis=1)

    data = aggregates_data_frame[produits + ['vag'] + ['depenses_tot']].copy()

    data.index.name = 'ident_men'
    data.reset_index(inplace = True)
    df = pd.melt(data, id_vars = ['ident_men', 'vag', 'depenses_tot'], value_vars = produits,
        value_name = 'depense_bien', var_name = 'bien')

    df2 = df2[['indice_prix_produit'] + ['prix'] + ['temps'] + ['mois']]

    df['vag'] = df['vag'].astype(str)
    df['indice_prix_produit'] = df['vag'] + '_' + df['bien']
    df['indice_prix_produit'] = df['indice_prix_produit'].str.replace('_0', '')
    df['indice_prix_produit'] = df['indice_prix_produit'].str.replace('_', '')
    df['coicop_12_numero'] = df['bien'].str[:2]
    df['coicop_12_numero'] = df['coicop_12_numero'].astype(float)
    df['numero_categ'] = df['coicop_12_numero']
    df['numero_categ'] = df['numero_categ'].replace(5, 3)
    df['numero_categ'] = df['numero_categ'].replace(6, 5)
    df['numero_categ'] = df['numero_categ'].replace(10, 5)
    df['numero_categ'] = df['numero_categ'].replace(7, 6)
    df['numero_categ'] = df['numero_categ'].replace(9, 7)
    df['numero_categ'] = df['numero_categ'].replace(8, 9)
    df['numero_categ'] = df['numero_categ'].replace(11, 8)
    df['numero_categ'] = df['numero_categ'].replace(12, 9)

    df = df[['ident_men'] + ['numero_categ'] + ['indice_prix_produit'] + ['depense_bien'] + ['vag']]

    df = pd.merge(df, df2, on = 'indice_prix_produit')
    df_temps = df[['vag'] + ['temps'] + ['mois']]
    df_temps['mois'] = df_temps['mois'].astype(float)
    df_temps['mois2'] = df_temps['mois'] ** 2
    df_temps = df_temps.drop_duplicates(cols='vag', take_last=True)
    df_temps = df_temps.astype(float)


    # Construct the price index by category:

    df['numero_categ'] = df['numero_categ'].astype(int)  # Goal : transform 1.0 into 1 to merge with same id.
    df = df.astype(str)
    df['id'] = df['numero_categ'] + '_' + df['ident_men']

    df_depense_categ = None
    for i in range(1, 13):
        if df_depense_categ is not None:
            df_depense_categ = concat([df_depense_categ, aggregates_data_frame['coicop12_{}'.format(i)]], axis = 1)
        else:
            df_depense_categ = aggregates_data_frame['coicop12_{}'.format(i)]
    df_depense_categ['categ_1'] = df_depense_categ['coicop12_1'].copy()
    df_depense_categ['categ_2'] = df_depense_categ['coicop12_2'].copy()
    df_depense_categ['categ_3'] = df_depense_categ['coicop12_3'] + df_depense_categ['coicop12_5']
    df_depense_categ['categ_4'] = df_depense_categ['coicop12_4'].copy()
    df_depense_categ['categ_5'] = df_depense_categ['coicop12_6'] + df_depense_categ['coicop12_10']
    df_depense_categ['categ_6'] = df_depense_categ['coicop12_7'].copy()
    df_depense_categ['categ_7'] = df_depense_categ['coicop12_9'].copy()
    df_depense_categ['categ_8'] = df_depense_categ['coicop12_11'].copy()
    df_depense_categ['categ_9'] = df_depense_categ['coicop12_8'] + df_depense_categ['coicop12_12']
    for i in range(1, 13):
        df_depense_categ = df_depense_categ.drop(['coicop12_{}'.format(i)], axis = 1)

    list_categ = [column for column in df_depense_categ.columns]
    df_depense_categ.index.name = 'ident_men'
    df_depense_categ.reset_index(inplace = True)
    df_depense_categ = pd.melt(df_depense_categ, id_vars = ['ident_men'], value_vars = list_categ)
    df_depense_categ.rename(columns = {'value': 'depense_par_categ'}, inplace = True)
    df_depense_categ.rename(columns = {'variable': 'numero_categ'}, inplace = True)
    df_depense_categ['numero_categ'] = df_depense_categ['numero_categ'].str.split('categ_').str[1]

    df_depense_categ = df_depense_categ.astype(str)
    df_depense_categ['id'] = df_depense_categ['numero_categ'] + '_' + df_depense_categ['ident_men']
    df_to_merge = df_depense_categ[['id'] + ['depense_par_categ']]

    df = pd.merge(df, df_to_merge, on = 'id')

    df[['prix'] + ['depense_bien'] + ['depense_par_categ']] = (
        df[['prix'] + ['depense_bien'] + ['depense_par_categ']].astype(float)
        )
    df['ln_prix'] = np.log(df['prix'])
    del df['prix']

    df['part_bien_categ'] = df['depense_bien'] / df['depense_par_categ']
    df.fillna(0, inplace=True)
    df['indice_prix_pondere'] = df['part_bien_categ'] * df['ln_prix']

    df.sort(['id'])
    grouped = df['indice_prix_pondere'].groupby(df['id'])
    grouped = grouped.aggregate(np.sum)
    grouped.index.name = 'id'
    grouped = grouped.reset_index()

    # Import information about households, including niveau_vie_decile
    # (To do: Obviously there are mistakes in its computation, check why).

    var_to_be_simulated = ['niveau_vie_decile']
    simulation_data_frame = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
    simulation_data_frame.index.name = 'ident_men'
    simulation_data_frame.reset_index(inplace = True)
    simulation_data_frame['ident_men'] = simulation_data_frame['ident_men'].astype(str)

    df_info_menage = aggregates_data_frame[['ocde10'] + ['depenses_tot'] + ['vag'] + ['typmen'] + ['revtot'] +
        ['02201'] + ['02202'] + ['02203']]
    df_info_menage['fumeur'] = 0
    df_info_menage[['02201'] + ['02202'] + ['02203']] = df_info_menage[['02201'] + ['02202'] + ['02203']].astype(float)
    df_info_menage['consommation_tabac'] = df_info_menage['02201'] + df_info_menage['02202'] + df_info_menage['02203']
    df_info_menage['fumeur'] = 1 * (df_info_menage['consommation_tabac'] > 0)
    df_info_menage.drop(['consommation_tabac', '02201', '02202', '02203'], inplace = True, axis = 1)
    df_info_menage.index.name = 'ident_men'
    df_info_menage.reset_index(inplace = True)
    df_info_menage['ident_men'] = df_info_menage['ident_men'].astype(str)
    df_info_menage = pd.merge(df_info_menage, simulation_data_frame, on = 'ident_men')

    data_frame = pd.merge(df_depense_categ, df_info_menage, on = 'ident_men')

    data_frame = pd.merge(data_frame, grouped, on = 'id')
    data_frame[['depenses_tot'] + ['depense_par_categ']] = (
        data_frame[['depenses_tot'] + ['depense_par_categ']].astype(float)
        )
    data_frame['wi'] = data_frame['depense_par_categ'] / data_frame['depenses_tot']
    data_frame = data_frame.astype(str)
