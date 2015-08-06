# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:26:44 2015

@author: thomas.douenne
"""

from ipp_macro_series_parser.agregats_transports.parser_cleaner_prix_carburants import prix_mensuel_carburants_90_15
from openfisca_france_indirect_taxation.example.utils_example import graph_builder_carburants

prix_mensuel_carburants_90_15[['annee'] + ['mois']] = prix_mensuel_carburants_90_15[['annee'] + ['mois']].astype(str)
prix_mensuel_carburants_90_15['date'] = prix_mensuel_carburants_90_15['annee'] + '_' + prix_mensuel_carburants_90_15['mois']
prix_mensuel_carburants_90_15 = prix_mensuel_carburants_90_15.set_index('date')

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

print 'Evolution du prix des carburants entre 1990 et 2015'
graph_builder_carburants(
    prix_mensuel_carburants_90_15[['prix SP95 ttc'] + ['prix diesel ttc'] + ['prix SP95 ht'] + ['prix diesel ht']],
    'prix carburants', 0.39, 1.025, 'darkgreen', 'darkred', 'lawngreen', 'orangered')

print 'Evolution du taux implicite de taxation (incluant la TVA) des carburants entre 1990 et 2015'
graph_builder_carburants(
    prix_mensuel_carburants_90_15[['taux implicite diesel'] + ['taux implicite super 95']],
    'taux implicite ticpe', 1, 1, 'darkred', 'darkgreen', None, None)
