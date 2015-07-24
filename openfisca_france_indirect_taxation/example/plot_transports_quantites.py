# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 09:46:35 2015

@author: thomas.douenne
"""

from ipp_macro_series_parser.agregats_transports.transports_cleaner import a6_b, g2_1, g_3a
from openfisca_france_indirect_taxation.example.utils_example import graph_builder_carburants

recettes_ticpe = a6_b[a6_b['categorie'] == u'TICPE ( TIPP avant 2010) (1)']
recettes_ticpe = recettes_ticpe[recettes_ticpe['index'] == 'Total']

g_3a.loc[g_3a['index'] == u'Voitures particulières', 'index'] = 'to_be_used'
g_3a.loc[g_3a['index'] == u'Total VP françaises', 'index'] = 'to_be_used'
quantite_conso_vp = g_3a[g_3a['index'] == 'to_be_used']
del quantite_conso_vp['index']

taille_parc_vp = g2_1[g2_1['categorie'] == u'Voitures particulières']

recettes_ticpe.set_index(['categorie', 'index'], inplace = True)
recettes_ticpe = recettes_ticpe.transpose()
taille_parc_vp.set_index(['categorie', 'index'], inplace = True)
taille_parc_vp = taille_parc_vp.transpose()
quantite_conso_vp.set_index(['categorie'], inplace = True)
quantite_conso_vp = quantite_conso_vp.transpose()

print 'Evolution de la taille du parc automobile au cours du temps'
graph_builder_carburants(taille_parc_vp, 'taille_parc_vp')

print 'Evolution des quantités de carburants consommées par les voitures particulières françaises'
graph_builder_carburants(quantite_conso_vp, 'quantite_conso_vp')

print 'Evolution des recettes totales issues de la TICPE'
graph_builder_carburants(recettes_ticpe, 'recettes_totales_ticpe')

# (pour avoir les recettes prélevées sur les ménages, parser les barèmes et multiplier les accises par les quantités)
