# -*- coding: utf-8 -*-

import pandas

import os


# from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_dataframe_builder_energy_no_alime import \
#    aggregates_data_frame, data_frame_for_reg#, df, df_depenses_prix


from openfisca_france_indirect_taxation.utils import assets_directory


df_indice_prix_produit = pandas.read_csv(
    os.path.join(
        assets_directory,
        'prix',
        'df_indice_prix_produit.csv'
        ), sep =';', decimal = ','
    )
df_indice_prix_produit.set_index('Unnamed: 0', inplace = True)

data_frame_for_reg_2011 = pandas.read_csv(
    os.path.join(
        assets_directory,
        'quaids',
        'data_frame_energy_no_alime_2011.csv'
        ), sep =','
    )
data_frame_for_reg_2011.set_index('Unnamed: 0', inplace = True)


""" Check that the sum of the share for the four categories is 1 """

data_frame_for_reg_2011['sum_shares'] = 0
for i in range(1, 4):
    data_frame_for_reg_2011['sum_shares'] += data_frame_for_reg_2011['w{}'.format(i)]
assert (data_frame_for_reg_2011['sum_shares'] == 1).any(), 'Shares do not sum to 1 in the final dataframe'
del data_frame_for_reg_2011['sum_shares']


""" Check that the prices do not take unlikely values """
for i in range(1, 4):
    assert max(data_frame_for_reg_2011['p{}'.format(i)]) < 400, 'Some prices seem too big'
    assert min(data_frame_for_reg_2011['p{}'.format(i)]) > 10, 'Some prices seem too small'


""" Check period fixed effects sum to 1 """

data_frame_for_reg_2011['sum_vag'] = 0
for i in range(0, 30):
    if 'vag_{}'.format(i) in data_frame_for_reg_2011.columns:
        data_frame_for_reg_2011['sum_vag'] += data_frame_for_reg_2011['vag_{}'.format(i)]
    else:
        pass
assert (data_frame_for_reg_2011['sum_vag'] == 1).any(), 'Vag fixed effects do not sum to 1'
