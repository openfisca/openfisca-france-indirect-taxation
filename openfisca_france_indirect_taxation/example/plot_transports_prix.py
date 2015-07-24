# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:26:44 2015

@author: thomas.douenne
"""

from ipp_macro_series_parser.agregats_transports.parser_cleaner_prix_carburants import prix_mensuel_carburants_90_15
from openfisca_france_indirect_taxation.example.utils_example import graph_builder_carburants

prix_mensuel_carburants_90_15 = prix_mensuel_carburants_90_15.set_index('annee')

prix_mensuel_carburants_90_15['taux_implicite_ticpe_diesel'] = (
    (prix_mensuel_carburants_90_15['diesel_ttc'] - prix_mensuel_carburants_90_15['diesel_ht']) /
    prix_mensuel_carburants_90_15['diesel_ht']
    )
prix_mensuel_carburants_90_15['taux_implicite_ticpe_super_95'] = (
    (prix_mensuel_carburants_90_15['super_95_ttc'] - prix_mensuel_carburants_90_15['super_95_ht']) /
    prix_mensuel_carburants_90_15['super_95_ht']
    )

print 'Evolution du prix des carburants au cours du temps'
graph_builder_carburants(prix_mensuel_carburants_90_15[['diesel_ht'] + ['diesel_ttc']], 'prix_diesel')
graph_builder_carburants(prix_mensuel_carburants_90_15[['super_95_ht'] + ['super_95_ttc']], 'prix_essence')

print 'Evolution du taux implicite de taxation des carburants au cours du temps'
graph_builder_carburants(
    prix_mensuel_carburants_90_15[['taux_implicite_ticpe_super_95'] + ['taux_implicite_ticpe_diesel']],
    'taux_implicite')
