# -*- coding: utf-8 -*-
"""
Created on Thu Jul 09 18:41:37 2015

@author: thomas.douenne
"""

# To do : change this test to fit with energy instead of categ

import pandas as pd

from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_dataframe_builder_categ import \
    aggregates_data_frame, df, produits, data_frame_for_reg, year, df_indice_prix_produit, df_to_merge


""" Check if depenses_tot is equal to the sum of all expenses """

aggregates_data_frame['dep_tot'] = 0
for i in range(1, 13):
    aggregates_data_frame['dep_tot'] += aggregates_data_frame['coicop12_{}'.format(i)]
aggregates_data_frame['diff'] = aggregates_data_frame['dep_tot'] - aggregates_data_frame['depenses_tot']
assert (aggregates_data_frame['diff'] < 0.0001).any()[(aggregates_data_frame['diff'] < 0.0001).any()], \
    'Issue in depenses_tot calculation'


""" Check if the dataframe used for the regression has the right number of observations, i.e.
one per person and per category of good for each year """

assert (len(data_frame_for_reg) == (10305 + 10240 + 15797)), \
    'Dataframe does not have the good shape'


""" Check if the price index of all goods in aggregate_data_frame is filled in indice_prix_mensuel_98_15
If this was not the case, we would have issues in the calculation of the price index for some people """

df_bien = df_indice_prix_produit[['bien']]
df_bien = df_bien.astype(int)
df_bien = df_bien.drop_duplicates(cols = 'bien', take_last = True)
df_bien_to_merge = aggregates_data_frame[produits][:1]
df_bien_to_merge = pd.melt(df_bien_to_merge)
df_bien_to_merge = df_bien_to_merge.astype(int)
df_bien_to_merge.rename(columns = {'variable': 'bien'}, inplace = True)
df_bien = pd.merge(df_bien, df_bien_to_merge, on = 'bien')
assert len(df_bien) == len(df_bien_to_merge), \
    'The price indexes is not filled for some goods in df_indice_prix_produit (or before)'


""" Check if indice_prix_produit has duplicates : hotherwise, this would distort our price indexes """

restricted_df = df.drop_duplicates(cols = 'indice_prix_produit', take_last = True)
if year == [2005, 2011]:
    assert len(restricted_df) == len(produits) * 6, \
        'Some price indexes are duplicates'
elif year == 2000:
    assert len(restricted_df) == len(produits) * 8, \
        'Some price indexes are duplicates'


""" Check if df_to_merge contains duplicates, to avoid mistakes in the merge with df """

restricted_df_to_merge = df_to_merge.drop_duplicates(cols = 'id', take_last = True)
assert len(restricted_df_to_merge) == len(df_to_merge), \
    'df_to_merge contains some duplicates'


""" Check if the price index for each good is the same for everyone """

limited_df = df[['ident_men'] + ['indice_prix_produit'] + ['prix'] + ['vag']]
limited_df = limited_df.astype(float)
if year == 2000:
    limited_df = limited_df[limited_df['vag'] == 9]
if year == 2005:
    limited_df = limited_df[limited_df['vag'] == 20]
if year == 2011:
    limited_df = limited_df[limited_df['vag'] == 25]
limited_df = limited_df[['ident_men'] + ['prix'] + ['indice_prix_produit']]
limited_df = pd.pivot_table(limited_df, index = 'indice_prix_produit', columns = 'ident_men')
limited_df = limited_df.T.drop_duplicates().T
assert len(limited_df.columns) == 1, \
    'Everyone does not have the same price index for some goods'


""" Check part_bien_categ """

limited_df_indice_prix_produit = df[['ident_men'] + ['part_bien_categ'] + ['numero_categ']]
limited_df_indice_prix_produit['numero_categ'] = limited_df_indice_prix_produit['numero_categ'].astype(float)
for i in range(1, 10):
    limited_df_part_bien_categ = limited_df_indice_prix_produit[limited_df_indice_prix_produit['numero_categ'] == i]
    limited_df_part_bien_categ = limited_df_part_bien_categ.groupby('ident_men').sum()
    assert (limited_df_part_bien_categ['part_bien_categ'] == 1).any()\
        [(limited_df_part_bien_categ['part_bien_categ'] == 1).any()], \
        'part_bien_categ does not sum up to 1'


""" Check if the sum of the expenditure shares wi adds up to 1 """

data_frame_for_reg['somme_wi'] = 0
for i in range(1, 10):
    data_frame_for_reg['somme_wi'] += data_frame_for_reg['w{}'.format(i)]
assert (data_frame_for_reg['somme_wi'] == 1).any(), 'The expenditure shares do not sum to 1'


""" Check if the sum of all monthly dummies adds up to 1 """

data_frame_for_reg['somme_mi'] = 0
for i in range(1, 13):
    data_frame_for_reg['somme_mi'] += data_frame_for_reg['m{}'.format(i)]
assert (data_frame_for_reg['somme_mi'] == 1).any(), 'The monthly dummies do not sum to 1'


""" | """

assert 0.999 < sum(data_frame_for_reg['part_depenses_tot']) < 1.001, \
    "The sum of the weights is not equal to 1 for depenses_tot"
for i in range(1, 10):
    assert 0.999 < sum(data_frame_for_reg['part_depenses_tot_{}'.format(i)]) < 1.001, \
        "The sum of the weights is not equal to 1 for some depenses_tot_i"
