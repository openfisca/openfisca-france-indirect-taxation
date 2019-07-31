# -*- coding: utf-8 -*-
"""
Created on Tue Jul 04 16:36:58 2017

@author: Thomas
"""

import statsmodels.formula.api as smf


from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_4_clean_data import \
    clean_data


data_enl = clean_data()[0]


data_enl['froid'] = 0
data_enl['froid'].loc[data_enl['gchauf_n'] != 0] = 1

data_enl['froid_cout'] = 0
data_enl['froid_cout'].loc[data_enl['gchauf_3'] == 1] = 1

data_enl['aides_logement'] = 0
data_enl['aides_logement'].loc[data_enl['aba'] == 1] = 1

data_enl['revtot_2'] = data_enl['revtot'] ** 2

"""
Predict froid
"""

regression = smf.ols(formula = 'froid ~ \
    aides_logement + agepr + bat_av_49 + bat_49_74 + log_indiv + \
     ocde10 + ouest_sud + part_energies_revtot + revtot + revtot_2 + rural + \
    surfhab_d',
    data = data_enl).fit()
print(regression.summary())

variables = ['aides_logement', 'agepr', 'bat_av_49', 'bat_49_74', 'log_indiv',
    'ocde10', 'ouest_sud', 'part_energies_revtot', 'revtot', 'revtot_2', 'rural',
    'surfhab_d']

logit = smf.Logit(data_enl['froid'], data_enl[variables]).fit()
print(logit.summary())

probit = smf.Probit(data_enl['froid'], data_enl[variables]).fit()
print(probit.summary())


"""
Predict froid_cout
"""

regression = smf.ols(formula = 'froid_cout ~ \
    aides_logement + agepr + bat_av_49 + bat_49_74 + log_indiv + \
     ocde10 + ouest_sud + part_energies_revtot + revtot + revtot_2 + rural + \
    surfhab_d',
    data = data_enl).fit()
print(regression.summary())

variables = ['aides_logement', 'agepr', 'bat_av_49', 'bat_49_74', 'log_indiv',
    'ocde10', 'ouest_sud', 'part_energies_revtot', 'revtot', 'revtot_2', 'rural',
    'surfhab_d']

logit = smf.Logit(data_enl['froid_cout'], data_enl[variables]).fit()
print(logit.summary())
