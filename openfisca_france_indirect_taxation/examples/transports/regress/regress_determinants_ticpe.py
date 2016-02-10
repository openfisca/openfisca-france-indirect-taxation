# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 09:47:41 2015

@author: thomas.douenne
"""

from __future__ import division

import statsmodels.formula.api as smf

from openfisca_france_indirect_taxation.examples.utils_example import simulate_df_calee_by_grosposte

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    simulated_variables = [
        'pondmen',
        'revtot',
        'rev_disp_loyerimput',
        'depenses_carburants',
        'depenses_essence',
        'depenses_diesel',
        'strate',
        'nenfants',
        'nadultes',
        'situacj',
        'situapr',
        'niveau_vie_decile'
        ]

    for year in [2005]:
        data_for_reg = simulate_df_calee_by_grosposte(simulated_variables = simulated_variables, year = year)

    # In 2005 3 people consume fuel while their rev_disp_loyerimput is 0. Creates inf number in part_carburants
    data_for_reg = data_for_reg[data_for_reg['rev_disp_loyerimput'] > 0]
    data_for_reg['rev_disp_loyerimput_2'] = data_for_reg['rev_disp_loyerimput'] ** 2
    data_for_reg['part_carburants'] = data_for_reg['depenses_carburants'] / data_for_reg['rev_disp_loyerimput']
    data_for_reg['part_diesel'] = data_for_reg['depenses_diesel'] / data_for_reg['rev_disp_loyerimput']
    data_for_reg['part_essence'] = data_for_reg['depenses_essence'] / data_for_reg['rev_disp_loyerimput']

    data_for_reg['rural'] = 0
    data_for_reg['petite_villes'] = 0
    data_for_reg['villes_moyennes'] = 0
    data_for_reg['grandes_villes'] = 0
    data_for_reg['agglo_paris'] = 0

    data_for_reg.loc[data_for_reg['strate'] == 0, 'rural'] = 1
    data_for_reg.loc[data_for_reg['strate'] == 1, 'petite_villes'] = 1
    data_for_reg.loc[data_for_reg['strate'] == 2, 'villes_moyennes'] = 1
    data_for_reg.loc[data_for_reg['strate'] == 3, 'grandes_villes'] = 1
    data_for_reg.loc[data_for_reg['strate'] == 4, 'agglo_paris'] = 1

    deciles = ['decile_1', 'decile_2', 'decile_3', 'decile_4', 'decile_5', 'decile_6', 'decile_7', 'decile_8',
               'decile_9', 'decile_10']

    for decile in deciles:
        data_for_reg[decile] = 0
        number = decile.replace('decile_', '')
        data_for_reg.loc[data_for_reg['niveau_vie_decile'] == int(number), decile] = 1
    # Situation vis-à-vis de l'emploi :
    # Travaille : emploi, stage, étudiant
    # Autres : chômeurs, retraités, personnes au foyer, autres
    data_for_reg['cj_travaille'] = 0
    data_for_reg['pr_travaille'] = 0
    data_for_reg.loc[data_for_reg['situacj'] < 4, 'cj_travaille'] = 1
    data_for_reg.loc[data_for_reg['situacj'] == 0, 'cj_travaille'] = 0
    data_for_reg.loc[data_for_reg['situapr'] < 4, 'pr_travaille'] = 1
    data_for_reg['travaille'] = data_for_reg['cj_travaille'] + data_for_reg['pr_travaille']

    regression_carburants = smf.ols(formula = 'part_carburants ~ \
        decile_1 + decile_2 + decile_3 + decile_4 + decile_5 + decile_6 + decile_7 + decile_8 + decile_9 + \
        rural + petite_villes + grandes_villes + agglo_paris + \
        nenfants + nadultes + travaille',
        data = data_for_reg).fit()
    print regression_carburants.summary()

    regression_diesel = smf.ols(formula = 'part_diesel ~ \
        decile_1 + decile_2 + decile_3 + decile_4 + decile_5 + decile_6 + decile_7 + decile_8 + decile_9 + \
        rural + petite_villes + grandes_villes + agglo_paris + \
        nenfants + nadultes + travaille',
        data = data_for_reg).fit()
    print regression_diesel.summary()

    regression_essence = smf.ols(formula = 'part_essence ~ \
        decile_1 + decile_2 + decile_3 + decile_4 + decile_5 + decile_6 + decile_7 + decile_8 + decile_9 + \
        rural + petite_villes + grandes_villes + agglo_paris + \
        nenfants + nadultes + travaille',
        data = data_for_reg).fit()
    print regression_essence.summary()

# It is tempting to add a variable 'vehicule'. However, I think it is a case of bad control. It captures part
# of the effect we actually want to estimate.
