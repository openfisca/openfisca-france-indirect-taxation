#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Thu Aug 13 13:59:49 2015

@author: thomas.douenne
"""

import pkg_resources
import os

from ipp_macro_series_parser.agregats_transports.transports_cleaner import g2_1, g_3a

parc_annuel_moyen_vp = g2_1[g2_1['categorie'] == u'Voitures particulières']
del parc_annuel_moyen_vp['categorie']
parc_annuel_moyen_vp = parc_annuel_moyen_vp.set_index('index')
parc_annuel_moyen_vp = parc_annuel_moyen_vp.transpose()

parc_annuel_moyen_vp['check'] = \
    parc_annuel_moyen_vp['dont essence'] + parc_annuel_moyen_vp['dont Diesel'] - parc_annuel_moyen_vp['Total']
assert (parc_annuel_moyen_vp['check'] == 0).any(), "sum of diesel and super is not equal to total"
del parc_annuel_moyen_vp['Total']
del parc_annuel_moyen_vp['check']
parc_annuel_moyen_vp.columns = ['essence', 'diesel']

quantite_carbu_vp_france = g_3a[g_3a['index'] == u'Voitures particulières']
del quantite_carbu_vp_france['index']
quantite_carbu_vp_france = quantite_carbu_vp_france.set_index('categorie')
quantite_carbu_vp_france = quantite_carbu_vp_france.transpose()
quantite_carbu_vp_france.columns = ['essence', 'diesel']

assets_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )

parc_annuel_moyen_vp.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
    'quantites', 'parc_annuel_moyen_vp.csv'), sep = ';')

quantite_carbu_vp_france.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
    'quantites', 'quantite_carbu_vp_france.csv'), sep = ';')
