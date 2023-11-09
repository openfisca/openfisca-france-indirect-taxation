#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os

from ipp_macro_series_parser.agregats_transports.poids_carburants.poids_carburants_cleaner import consommation, parc_auto
from openfisca_france_indirect_taxation.utils import assets_directory


parc_annuel_moyen_vp = parc_auto[parc_auto['categorie'] == 'Voitures particulières']
del parc_annuel_moyen_vp['categorie']
parc_annuel_moyen_vp = parc_annuel_moyen_vp.set_index('index')
parc_annuel_moyen_vp = parc_annuel_moyen_vp.transpose()

parc_annuel_moyen_vp['check'] = \
    parc_annuel_moyen_vp['dont essence'] + parc_annuel_moyen_vp['dont Diesel'] - parc_annuel_moyen_vp['Total']
assert (parc_annuel_moyen_vp['check'] == 0).any(), 'sum of diesel and super is not equal to total'
del parc_annuel_moyen_vp['Total']
del parc_annuel_moyen_vp['check']
parc_annuel_moyen_vp.columns = ['essence', 'diesel']

quantite_carbu_vp_france = consommation[consommation['index'] == 'Voitures particulières']
del quantite_carbu_vp_france['index']
quantite_carbu_vp_france = quantite_carbu_vp_france.set_index('categorie')
quantite_carbu_vp_france = quantite_carbu_vp_france.transpose()
quantite_carbu_vp_france.columns = ['essence', 'diesel']


parc_annuel_moyen_vp.to_csv(os.path.join(assets_directory, 'quantites', 'parc_annuel_moyen_vp.csv'), sep = ',')

quantite_carbu_vp_france.to_csv(os.path.join(assets_directory, 'quantites', 'quantite_carbu_vp_france.csv'), sep = ',')
