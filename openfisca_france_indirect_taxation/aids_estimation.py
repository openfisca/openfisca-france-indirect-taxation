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
for i in range(1, 13):
    small_df = data_frame_for_reg[data_frame_for_reg['numero_coicop'] == i]
    results = smf.ols(formula = 'wi ~ ln_p1 + ln_p2 + ln_p3 + ln_p4 + ln_p5 + ln_p6 + ln_p7 + ln_p8 + ln_p9 + \
        ln_p10 + ln_p11 + ln_p12 + ln_depenses_reelles + vag + typmen + niveau_vie_decile', data = small_df).fit()
    print '---------------------------'
    print 'Estimation w{}'.format(i)
    print results.summary()
    elasticite_depense['ed_{}'.format(i)] = calcul_elasticite_depense()
    elasticite_prix['ep_{}'.format(i)] = calcul_elasticite_prix_compensee()
print 'Elasticite depense :'
for element in elasticite_depense.items():
    print element
print 'Elasticite prix :'
for element in elasticite_prix.items():
    print element
