# -*- coding: utf-8 -*-
"""
Created on Thu Jul 02 17:16:15 2015

@author: thomas.douenne
"""

from __future__ import division

import statsmodels.formula.api as smf

from openfisca_france_indirect_taxation.aids_dataframe_builder import data_frame_for_reg


def calcul_elasticite_depense():
    return (results.params.ln_depenses_reelles / small_df['wi'].mean()) + 1


def calcul_elasticite_prix_compensee():
    return ((results.params['ln_p{}'.format(i)] - results.params.ln_depenses_reelles * (small_df['wi'].mean() -
    results.params.ln_depenses_reelles * small_df['ln_depenses_reelles'].mean())) / small_df['wi'].mean()) - 1


elasticite_depense = dict()
elasticite_prix = dict()
r_2 = dict()
for i in range(1, 13):
    small_df = data_frame_for_reg[data_frame_for_reg['numero_coicop'] == i]
    small_df = small_df[small_df['depense_par_coicop'] > 0]
    results = smf.ols(formula = 'wi ~ ln_p1 + ln_p2 + ln_p3 + ln_p4 + ln_p5 + ln_p6 + ln_p7 + ln_p8 + ln_p9 + \
        ln_p10 + ln_p11 + ln_p12 + ln_depenses_reelles + vag + typmen + niveau_vie_decile + \
        fumeur', data = small_df).fit()
    print '---------------------------'
    print 'Estimation w{}'.format(i)
    print results.summary()
    elasticite_depense['ed_{}'.format(i)] = calcul_elasticite_depense()
    elasticite_prix['ep_{}'.format(i)] = calcul_elasticite_prix_compensee()
    r_2['r2_{}'.format(i)] = results.rsquared
