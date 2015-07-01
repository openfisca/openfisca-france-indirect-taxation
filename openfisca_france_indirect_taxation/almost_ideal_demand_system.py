from __future__ import division

import pandas
import numpy as np
from pandas import concat
import datetime as dt
import statsmodels.formula.api as smf

from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame

import os
from ConfigParser import SafeConfigParser
from openfisca_france_data import default_config_files_directory as config_files_directory

# We want top obtain prices from the Excel file:

parser = SafeConfigParser()
config_local_ini = os.path.join(config_files_directory, 'config_local.ini')
config_ini = os.path.join(config_files_directory, 'config.ini')
parser.read([config_ini, config_local_ini])

directory_path = os.path.normpath(
    parser.get("openfisca_france_indirect_taxation", "assets")
    )
indice_prix_mensuel_98_2015 = pandas.read_csv(os.path.join(directory_path, "indice_prix_mensuel_98_2015.csv"),
    sep =';', decimal = ',')

# We build a dataframe :

aggregates_data_frame = get_input_data_frame(2005)
print aggregates_data_frame['decuc'].mean()
aggregates_data_frame['depenses_tot'] = 0
for i in range(1, 13):
    aggregates_data_frame['depenses_tot'] += aggregates_data_frame['coicop12_{}'.format(i)]

produits = [column for column in aggregates_data_frame.columns if column.isdigit()]


data = aggregates_data_frame[produits + ['vag']].copy()

data.index.name = 'ident_men'
data.reset_index(inplace = True)
df = pandas.melt(data, id_vars = ['vag', 'ident_men'], value_vars=produits,
    value_name = 'depense_bien', var_name = 'bien')

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
indice_prix_mensuel_98_2015['_10200'] = indice_prix_mensuel_98_2015['_10100']
indice_prix_mensuel_98_2015['_10400'] = indice_prix_mensuel_98_2015['_10100']
indice_prix_mensuel_98_2015['_10500'] = indice_prix_mensuel_98_2015['_10100']
indice_prix_mensuel_98_2015['_11113'] = indice_prix_mensuel_98_2015['_11112']
indice_prix_mensuel_98_2015['_12200'] = indice_prix_mensuel_98_2015['_12000']
indice_prix_mensuel_98_2015['_12510'] = indice_prix_mensuel_98_2015['_12500']
indice_prix_mensuel_98_2015['_12550'] = indice_prix_mensuel_98_2015['_12500']
indice_prix_mensuel_98_2015['_12620'] = indice_prix_mensuel_98_2015['_12610']
indice_prix_mensuel_98_2015['_12910'] = indice_prix_mensuel_98_2015['_12000']

indice_prix_mensuel_98_2015['date'] = indice_prix_mensuel_98_2015[u'Annee'] + '_' + indice_prix_mensuel_98_2015[u'Mois']
del indice_prix_mensuel_98_2015[u'Annee']
del indice_prix_mensuel_98_2015[u'Mois']
produits = list(indice_prix_mensuel_98_2015.columns[:-1])
df2 = pandas.melt(indice_prix_mensuel_98_2015, id_vars = ['date'], value_vars=produits,
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
df2 = df2[['indice_prix_produit'] + ['prix']]

df['vag'] = df['vag'].astype(str)
df['indice_prix_produit'] = df['vag'] + '_' + df['bien']
df['indice_prix_produit'] = df['indice_prix_produit'].str.replace('_0', '')
df['indice_prix_produit'] = df['indice_prix_produit'].str.replace('_', '')
df['coicop_12_numero'] = df['bien'].str[:2]
df = df[['ident_men'] + ['coicop_12_numero'] + ['indice_prix_produit'] + ['depense_bien']]

df = pandas.merge(df, df2, on = 'indice_prix_produit')

# Construct the price index by coicop:

df['coicop_12_numero'] = df['coicop_12_numero'].astype(int)  # Goal : transform 1.0 into 1 to merge with same id.
df = df.astype(str)
df['id'] = df['coicop_12_numero'] + '_' + df['ident_men']

df_depense_coicop = None
for i in range(1, 13):
    if df_depense_coicop is not None:
        df_depense_coicop = concat([df_depense_coicop, aggregates_data_frame['coicop12_{}'.format(i)]], axis = 1)
    else:
        df_depense_coicop = aggregates_data_frame['coicop12_{}'.format(i)]

list_coicop12 = [column for column in df_depense_coicop.columns]
df_depense_coicop.index.name = 'ident_men'
df_depense_coicop.reset_index(inplace = True)
df_depense_coicop = pandas.melt(df_depense_coicop, id_vars = ['ident_men'], value_vars = list_coicop12)
df_depense_coicop.rename(columns = {'value': 'depense_par_coicop'}, inplace = True)
df_depense_coicop.rename(columns = {'variable': 'numero_coicop'}, inplace = True)
df_depense_coicop['numero_coicop'] = df_depense_coicop['numero_coicop'].str.split('coicop12_').str[1]

df_depense_coicop = df_depense_coicop.astype(str)
df_depense_coicop['id'] = df_depense_coicop['numero_coicop'] + '_' + df_depense_coicop['ident_men']
df_to_merge = df_depense_coicop[['id'] + ['depense_par_coicop']]

df = pandas.merge(df, df_to_merge, on = 'id')

df[['prix'] + ['depense_bien'] + ['depense_par_coicop']] = (
    df[['prix'] + ['depense_bien'] + ['depense_par_coicop']].astype(float)
    )
df['ln_prix'] = np.log(df['prix'])
del df['prix']

df['part_bien_coicop'] = df['depense_bien'] / df['depense_par_coicop']
df.fillna(0, inplace=True)
df['indice_prix_pondere'] = df['part_bien_coicop'] * df['ln_prix']

df.sort(['id'])
grouped = df['indice_prix_pondere'].groupby(df['id'])
grouped = grouped.aggregate(np.sum)
grouped.index.name = 'id'
grouped = grouped.reset_index()

df_info_menage = aggregates_data_frame[['ocde10'] + ['depenses_tot'] + ['vag']]
df_info_menage.index.name = 'ident_men'
df_info_menage.reset_index(inplace = True)
df_info_menage['ident_men'] = df_info_menage['ident_men'].astype(str)

data_frame = pandas.merge(df_depense_coicop, df_info_menage, on = 'ident_men')

data_frame = pandas.merge(data_frame, grouped, on = 'id')
data_frame[['depenses_tot'] + ['depense_par_coicop']] = (
    data_frame[['depenses_tot'] + ['depense_par_coicop']].astype(float)
    )
data_frame['wi'] = data_frame['depense_par_coicop'] / data_frame['depenses_tot']
data_frame = data_frame.astype(str)

# Those who don't consume in coicop_i have a price index of 0 for this coicop.
# We replace it with the price index of the whole coicop at the same vag.
data_frame['indice_prix_produit'] = data_frame['vag'] + data_frame['numero_coicop'] + '000'

df2['prix'] = df2['prix'].astype(float)
df2['ln_prix_coicop'] = np.log(df2['prix'])
del df2['prix']

data_frame = pandas.merge(data_frame, df2, on = 'indice_prix_produit')

data_frame['indice_prix_pondere'] = data_frame['indice_prix_pondere'].astype(float)
data_frame['ln_prix_coicop'] = data_frame['ln_prix_coicop'].astype(float)
data_frame.loc[data_frame['indice_prix_pondere'] == 0, 'indice_prix_pondere'] = \
    data_frame.loc[data_frame['indice_prix_pondere'] == 0, 'ln_prix_coicop']
data_frame = data_frame.drop(['ln_prix_coicop', 'vag', 'indice_prix_produit'], axis = 1)

# Reshape the dataframe to have the price index of each coicop as a variable

data_frame_prix = data_frame[['numero_coicop'] + ['ident_men'] + ['indice_prix_pondere']]
data_frame_prix.index.name = 'ident_men'
data_frame_prix = pandas.pivot_table(data_frame_prix, index='ident_men', columns='numero_coicop',
    values='indice_prix_pondere')
data_frame_prix.reset_index(inplace = True)
data_frame = pandas.merge(data_frame, data_frame_prix, on = 'ident_men')
for i in range(1, 13):
    data_frame.rename(columns = {'{}'.format(i): 'ln_p{}'.format(i)}, inplace = True)

# Construct a linear approximation of the global price index P

df_indice_prix_global = data_frame[['ident_men'] + ['wi'] + ['indice_prix_pondere']]
df_indice_prix_global = df_indice_prix_global.astype(float)
df_indice_prix_global['ln_P'] = \
    df_indice_prix_global['wi'] * df_indice_prix_global['indice_prix_pondere']
df_indice_prix_global = df_indice_prix_global['ln_P'].groupby(df_indice_prix_global['ident_men'])
df_indice_prix_global = df_indice_prix_global.aggregate(np.sum)
df_indice_prix_global.index.name = 'ident_men'
df_indice_prix_global = df_indice_prix_global.reset_index()
del data_frame['id']
data_frame = data_frame.astype(float)

data_frame = pandas.merge(data_frame, df_indice_prix_global, on = 'ident_men')
data_frame['depenses_reelles'] = data_frame['depenses_tot'] / data_frame['ocde10']
data_frame['ln_depenses_reelles'] = np.log(data_frame['depenses_reelles'])
del data_frame['depenses_reelles']
data_frame['ln_depenses_reelles'] = data_frame['ln_depenses_reelles'] - data_frame['ln_P']

# Build the regression

for i in range(1, 13):
    small_df = data_frame[data_frame['numero_coicop'] == i]
    mod = smf.ols(formula='wi ~ ln_p1 + ln_p2 + ln_p3 + ln_p4 + ln_p5 + ln_p6 + ln_p7 + ln_p8 + ln_p9 + \
        ln_p10 + ln_p11 + ln_p12 + ln_depenses_reelles', data = small_df)
    res = mod.fit()
    print '---------------------------'
    print 'Estimation w{}'.format(i)
    print res.summary()
