#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os


from ipp_macro_series_parser.agregats_transports.poids_carburants.parser_cleaner_prix_carburants import prix_annuel_carburants_90_16, \
    prix_mensuel_carburants_90_17
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_price_index_builder import date_to_vag
from openfisca_france_indirect_taxation.utils import assets_directory


# We will create three csv files. One for annual data, two other for monthly data.
# The one match_to_vag will match prices to vagues.

prix_mensuel_carbu_match_to_vag = prix_mensuel_carburants_90_17.copy()

prix_annuel_carburants_90_16['Date'] = prix_annuel_carburants_90_16['Date'].astype(int)
prix_annuel_carburants_90_16 = prix_annuel_carburants_90_16.set_index('Date')

prix_mensuel_carburants_90_17[['annee', 'mois']] = prix_mensuel_carburants_90_17[['annee', 'mois']].astype(str)
prix_mensuel_carburants_90_17['Date'] = \
    prix_mensuel_carburants_90_17['annee'] + '/' + prix_mensuel_carburants_90_17['mois']
prix_mensuel_carburants_90_17 = prix_mensuel_carburants_90_17.drop(['annee', 'mois'], axis = 1)
prix_mensuel_carburants_90_17 = prix_mensuel_carburants_90_17.set_index('Date')

prix_mensuel_carbu_match_to_vag[['annee', 'mois']] = \
    prix_mensuel_carbu_match_to_vag[['annee', 'mois']].astype(str)
prix_mensuel_carbu_match_to_vag['date'] = \
    prix_mensuel_carbu_match_to_vag['annee'] + '_' + prix_mensuel_carbu_match_to_vag['mois']
prix_mensuel_carbu_match_to_vag['vag'] = prix_mensuel_carbu_match_to_vag['date'].map(date_to_vag)
prix_mensuel_carbu_match_to_vag = prix_mensuel_carbu_match_to_vag[prix_mensuel_carbu_match_to_vag['vag'] < 29]
prix_mensuel_carbu_match_to_vag = prix_mensuel_carbu_match_to_vag.drop_duplicates('vag')
prix_mensuel_carbu_match_to_vag['vag'] = prix_mensuel_carbu_match_to_vag['vag'].astype(int)
prix_mensuel_carbu_match_to_vag = prix_mensuel_carbu_match_to_vag.set_index('vag')
prix_mensuel_carbu_match_to_vag = prix_mensuel_carbu_match_to_vag.drop(['annee', 'mois', 'date'], axis = 1)


prix_annuel_carburants_90_16.to_csv(os.path.join(assets_directory, 'prix', 'prix_annuel_carburants.csv'), sep = ',')
prix_mensuel_carburants_90_17.to_csv(os.path.join(assets_directory, 'prix', 'prix_mensuel_carburants.csv'), sep = ',')
prix_mensuel_carbu_match_to_vag.to_csv(os.path.join(assets_directory, 'prix', 'prix_mensuel_carbu_match_to_vag.csv'), sep = ',')
