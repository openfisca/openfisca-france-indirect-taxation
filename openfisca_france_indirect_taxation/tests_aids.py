# -*- coding: utf-8 -*-
"""
Created on Fri Jul 03 16:45:31 2015

@author: thomas.douenne
"""

import numpy as np
import pandas as pd

from openfisca_france_indirect_taxation.aids_dataframe_builder_new_categ import aggregates_data_frame, df2, produits, \
    data_frame, data_frame_for_reg


""" Check if depenses_tot is equal to the sum of all expenses """

aggregates_data_frame['dep_tot'] = 0
for i in range(1, 13):
    aggregates_data_frame['dep_tot'] += aggregates_data_frame['coicop12_{}'.format(i)]
aggregates_data_frame['diff'] = aggregates_data_frame['dep_tot'] - aggregates_data_frame['depenses_tot']
assert (aggregates_data_frame['diff'] < 0.0001).any()[(aggregates_data_frame['diff'] < 0.0001).any()], \
    'Issue in depenses_tot calculation'


""" Check if the dataframe used for the regression has the right number of observations, i.e.
one per person and per category of good for each year """

assert (len(data_frame_for_reg) == (10305 + 10240 + 15797) * 9), \
    'Dataframe does not have the good shape'


""" Check that for any observation indice_prix_pondere is equal to ln_pi if numero_categ == i """

for i in range(1, 10):
    small_df = data_frame_for_reg[data_frame_for_reg['numero_categ'] == i]
    small_df['diff_prix'] = small_df['indice_prix_pondere'] - small_df['ln_p{}'.format(i)]
    assert ((small_df['diff_prix'] == 0).any()[(small_df['diff_prix'] == 0).any()]), \
        'Indice_prix_pondere and ln_pi do not match for some numero_categ'


""" Check if the sum of the shares of all categories of expenses are equal to 1 for everyone """

menage = data_frame[['ident_men'] + ['wi']]
menage.sort(['ident_men'])
menage = menage['wi'].groupby(menage['ident_men'])
menage = menage.aggregate(np.sum)
assert (menage == 1).any()[(menage == 1).any()], \
    'The sum of the shares of the all categories is equal to 1 for everyone'


""" Check if the price index of all goods in aggregate_data_frame is filled in indice_prix_mensuel_98_15
If this was not the case, we would have issues in the calculation of the price index for some people """

df_bien = df2[['bien']]
df_bien = df_bien.astype(int)
df_bien = df_bien.drop_duplicates(cols = 'bien', take_last = True)
df_bien_to_merge = aggregates_data_frame[produits][:1]
df_bien_to_merge = pd.melt(df_bien_to_merge)
df_bien_to_merge = df_bien_to_merge.astype(int)
df_bien_to_merge.rename(columns = {'variable': 'bien'}, inplace = True)
df_bien = pd.merge(df_bien, df_bien_to_merge, on = 'bien')
assert len(df_bien) == len(df_bien_to_merge), \
    'The price indexes is not filled for some goods in df2 (or before)'
