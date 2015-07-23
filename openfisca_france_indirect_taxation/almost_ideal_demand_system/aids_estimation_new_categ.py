# -*- coding: utf-8 -*-
"""
Created on Mon Jul 06 11:22:22 2015

@author: thomas.douenne
"""

from __future__ import division

import statsmodels.formula.api as smf

from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_dataframe_builder_new_categ import \
    data_frame_for_reg


def calcul_elasticite_depense():
    return (results.params.ln_depenses_par_uc / small_df['wi'].mean()) + 1


def calcul_elasticite_prix_compensee():
    return ((results.params['ln_p{}'.format(i)] - results.params.ln_depenses_par_uc * (small_df['wi'].mean() -
    results.params.ln_depenses_par_uc * small_df['ln_depenses_par_uc'].mean())) / small_df['wi'].mean()) - 1


elasticite_depense = dict()
elasticite_prix = dict()
r_2 = dict()
for i in range(1, 10):
    small_df = data_frame_for_reg[data_frame_for_reg['numero_categ'] == i]
    small_df = small_df[small_df['depense_par_categ'] > 0]  # On estime uniquement la marge intensive et non extensive.
    results = smf.ols(formula = 'wi ~ ln_p1 + ln_p2 + ln_p3 + ln_p4 + ln_p5 + ln_p6 + ln_p7 + ln_p8 + ln_p9 + \
        ln_depenses_par_uc + typmen + fumeur', data = small_df).fit()
    print '---------------------------'
    print 'Estimation w{}'.format(i)
    print results.summary()
    elasticite_depense['ed_{}'.format(i)] = calcul_elasticite_depense()
    elasticite_prix['ep_{}'.format(i)] = calcul_elasticite_prix_compensee()
    r_2['r2_{}'.format(i)] = results.rsquared
