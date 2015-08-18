# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 18:06:45 2015

@author: thomas.douenne
"""

from pandas import concat

from openfisca_france_indirect_taxation.example.utils_example import graph_builder_bar_list
from openfisca_france_indirect_taxation.model.get_dataframe_from_legislation.get_accises import get_accises_carburants
from openfisca_france_indirect_taxation.model.get_dataframe_from_legislation.get_tva import get_tva_taux_plein
from openfisca_france_indirect_taxation.model.get_dataframe_from_legislation.get_prix_carburants import \
    get_prix_carburants

# Taux implicite du diesel:
ticpe_gazole = ['ticpe_gazole', 'ticpe_super9598']
accise_diesel = get_accises_carburants(ticpe_gazole)
diesel_ttc = ['diesel_ttc', 'super_95_ttc']
prix_diesel = get_prix_carburants(diesel_ttc)
tva_taux_plein = get_tva_taux_plein()

df_taux_implicite = concat([accise_diesel, prix_diesel, tva_taux_plein], axis = 1)
df_taux_implicite.rename(columns = {'value': 'taux plein tva'}, inplace = True)

df_taux_implicite['taux_implicite_diesel'] = (
    df_taux_implicite['accise ticpe gazole'] * (1 + df_taux_implicite['taux plein tva']) /
    (df_taux_implicite['prix diesel ttc'] -
    (df_taux_implicite['accise ticpe gazole'] * (1 + df_taux_implicite['taux plein tva'])))
    )

df_taux_implicite['taux_implicite_sp95'] = (
    df_taux_implicite['accise ticpe super9598'] * (1 + df_taux_implicite['taux plein tva']) /
    (df_taux_implicite['prix super 95 ttc'] -
    (df_taux_implicite['accise ticpe super9598'] * (1 + df_taux_implicite['taux plein tva'])))
    )

df_taux_implicite = df_taux_implicite.dropna()

graph_builder_bar_list(df_taux_implicite['taux_implicite_diesel'])
graph_builder_bar_list(df_taux_implicite['taux_implicite_sp95'])
