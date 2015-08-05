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

prix_mensuel_carburants_90_15.rename(columns = {'diesel_ht': 'prix diesel ht', 'diesel_ttc': 'prix diesel ttc',
    'super_95_ht': 'prix SP95 ht', 'super_95_ttc': 'prix SP95 ttc',
    'taux_implicite_ticpe_diesel': 'taux implicite diesel', 'taux_implicite_ticpe_super_95': 'taux implicite super 95'},
    inplace = True)

print 'Evolution du prix des carburants au cours du temps'
graph_builder_carburants(
    prix_mensuel_carburants_90_15[['prix diesel ttc'] + ['prix diesel ht']], 'prix diesel', 0.42, 1, 'darkred',
    'orangered', 'yellow')
graph_builder_carburants(
    prix_mensuel_carburants_90_15[['prix super 95 ttc'] + ['prix super 95 ht']], 'prix essence', 0.48, 1, 'darkgreen',
    'lawngreen', 'yellow')

print 'Evolution du taux implicite de taxation des carburants au cours du temps'
graph_builder_carburants(
    prix_mensuel_carburants_90_15[['taux implicite diesel'] + ['taux implicite super 95']],
    'taux implicite ticpe', 1, 1, 'darkred', 'darkgreen', 'yellow')
