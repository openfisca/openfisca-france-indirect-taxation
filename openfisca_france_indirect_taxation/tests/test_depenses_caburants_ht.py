# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 18:40:27 2016

@author: thomas.douenne
"""


from openfisca_france_indirect_taxation.examples.utils_example import simulate

simulated_variables = [
    'pondmen',
    'decuc',
    'depenses_diesel_ht',
    'depenses_diesel_htva',
    'diesel_ticpe',
    'depenses_diesel',
    'depenses_diesel_recalculees'
    ]
# Merge des deux listes

for year in [2000]:
    # Constition d'une base de données agrégée par décile (= collapse en stata)
    df = simulate(simulated_variables = simulated_variables, year = year)
    df['check_diesel_ht'] = df['depenses_diesel_ht'] - (df['depenses_diesel_htva'] - df['diesel_ticpe'])
    assert (df['check_diesel_ht'] == 0).any()
    df['check_diesel_recalcule'] = df['depenses_diesel'] - df['depenses_diesel_recalculees']
    assert (df['check_diesel_recalcule'] == 0).any()
