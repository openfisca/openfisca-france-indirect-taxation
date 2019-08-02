# -*- coding: utf-8 -*-

import pandas

from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_dataframe_builder_energy import \
    aggregates_data_frame, df, df_depenses_prix, data_frame_for_reg
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_price_index_builder import \
    df_indice_prix_produit

""" Check if depenses_tot is equal to the sum of all expenses """

aggregates_data_frame['dep_tot'] = 0
for i in range(1, 13):
    aggregates_data_frame['dep_tot'] += aggregates_data_frame['coicop12_{}'.format(i)]
aggregates_data_frame['diff'] = aggregates_data_frame['dep_tot'] - aggregates_data_frame['depenses_tot']
assert (aggregates_data_frame['diff'] < 0.0001).any()[(aggregates_data_frame['diff'] < 0.0001).any()], \
    'Issue in depenses_tot calculation'


""" Check that the sum of the share for the four categories is 1 """

data_frame_for_reg['sum_shares'] = 0
for i in range(1, 5):
    data_frame_for_reg['sum_shares'] += data_frame_for_reg['w{}'.format(i)]
assert (data_frame_for_reg['sum_shares'] == 1).any(), 'Shares do not sum to 1 in the final dataframe'
del data_frame_for_reg['sum_shares']


""" Check that the prices do not take unlikely values """
# This test is problematic, it does not achieves its goal
for i in range(1, 5):
    assert (data_frame_for_reg['p{}'.format(i)] > 500).any(), 'Some prices seem too small'
    assert (data_frame_for_reg['p{}'.format(i)] < 200).any(), 'Some prices seem too big'


""" Check period fixed effects sum to 1 """

data_frame_for_reg['sum_vag'] = 0
for i in range(0, 30):
    if 'vag_{}'.format(i) in data_frame_for_reg.columns:
        data_frame_for_reg['sum_vag'] += data_frame_for_reg['vag_{}'.format(i)]
    else:
        pass
assert (data_frame_for_reg['sum_vag'] == 1).any(), 'Vag fixed effects do not sum to 1'


""" Check if the price index of all goods in aggregate_data_frame is filled in indice_prix_mensuel_98_15
If this was not the case, we would have issues in the calculation of the price index for some people """

df_bien = df_indice_prix_produit[['bien']]
df_bien = df_bien.drop_duplicates(subset = 'bien', take_last = True)
produits = [column for column in aggregates_data_frame.columns if column[:13] == 'poste_coicop_']
df_bien_to_merge = aggregates_data_frame[produits][:1]
df_bien_to_merge = pandas.melt(df_bien_to_merge)
df_bien_to_merge.rename(columns = {'variable': 'bien'}, inplace = True)
df_bien_to_merge['index_to_drop'] = df_bien_to_merge['bien'].str[13:15]
for i in ['13', '99']:
    df_bien_to_merge = df_bien_to_merge[df_bien_to_merge['index_to_drop'] != i]
df_bien = pandas.merge(df_bien, df_bien_to_merge, on = 'bien')
assert len(df_bien) == len(df_bien_to_merge), \
    'The price indexes is not filled for some goods in df_indice_prix_produit (or before)'


""" Check if the goods that drop from the dataframe in the match with prices are meaningful goods or not. If the test
fails, it means that some meaningful goods are not matched with any price. This test achieves the same goal as the
previous one but in a later stage of the dataframe construction """

check = df.drop_duplicates(subset = ['indice_prix_produit'], keep = 'last')
check = check['indice_prix_produit']
check2 = df_depenses_prix.drop_duplicates(subset = ['indice_prix_produit'], keep = 'last')
check2 = check2['indice_prix_produit']
common_check = [x for x in check]
common_check2 = [x for x in check2]
common = [x for x in common_check if x not in common_check2]
del check, check2, common_check, common_check2
for element in common:
    short_name = element[13:15]
    assert short_name == '99' or short_name == '13', 'Some goods are not matched with any price'
del common, short_name


""" Check if the shares of each poste in their broad category sum to 1 """

for i in range(0, 100):
    df_ident_men_0 = df_depenses_prix[df_depenses_prix['ident_men'] == '{}'.format(i)]
    df_ident_men_0_alime = df_ident_men_0[df_ident_men_0['type_bien'] == 'alime']
    assert 0.999 < df_ident_men_0_alime['part_bien_categorie'].sum() < 1.001 or \
        -0.001 < df_ident_men_0_alime['part_bien_categorie'].sum() < 0.001

    df_ident_men_0_autre = df_ident_men_0[df_ident_men_0['type_bien'] == 'autre']
    assert 0.999 < df_ident_men_0_autre['part_bien_categorie'].sum() < 1.001 or \
        -0.001 < df_ident_men_0_autre['part_bien_categorie'].sum() < 0.001

    df_ident_men_0_carbu = df_ident_men_0[df_ident_men_0['type_bien'] == 'carbu']
    assert 0.999 < df_ident_men_0_carbu['part_bien_categorie'].sum() < 1.001 or \
        -0.001 < df_ident_men_0_carbu['part_bien_categorie'].sum() < 0.001

    df_ident_men_0_carbu = df_ident_men_0[df_ident_men_0['type_bien'] == 'logem']
    assert 0.999 < df_ident_men_0_carbu['part_bien_categorie'].sum() < 1.001 or \
        -0.001 < df_ident_men_0_carbu['part_bien_categorie'].sum() < 0.001

del df_ident_men_0, df_ident_men_0_autre, df_ident_men_0_alime, df_ident_men_0_carbu, i
