# -*- coding: utf-8 -*-
"""
Created on Tue Jul 04 16:36:58 2017

@author: Thomas
"""

import statsmodels.formula.api as smf


from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_4_clean_data import \
    clean_data


data_enl = clean_data()[0]



data_enl['froid'] = 0
data_enl['froid'].loc[data_enl['gchauf_n'] != 0] = 1

data_enl['froid_cout'] = 0
data_enl['froid_cout'].loc[data_enl['gchauf_3'] == 1] = 1

data_enl['aides_logement'] = 0
data_enl['aides_logement'].loc[data_enl['aba'] == 1] = 1

data_enl['rural'] = 0
data_enl['com_5000'] = 0
data_enl['com_10000'] = 0
data_enl['com_20000'] = 0
data_enl['com_50000'] = 0
data_enl['com_100000'] = 0
data_enl['com_200000'] = 0
data_enl['com_2000000'] = 0
data_enl['paris'] = 0

data_enl.loc[data_enl['tuu'] == 0, 'rural'] = 1
data_enl.loc[data_enl['tuu'] == 1, 'com_5000'] = 1
data_enl.loc[data_enl['tuu'] == 2, 'com_10000'] = 1
data_enl.loc[data_enl['tuu'] == 3, 'com_20000'] = 1
data_enl.loc[data_enl['tuu'] == 4, 'com_50000'] = 1
data_enl.loc[data_enl['tuu'] == 5, 'com_100000'] = 1
data_enl.loc[data_enl['tuu'] == 6, 'com_200000'] = 1
data_enl.loc[data_enl['tuu'] == 7, 'com_2000000'] = 1
data_enl.loc[data_enl['tuu'] == 8, 'paris'] = 1



data_enl['reg_paris'] = 0
data_enl['bass_paris'] = 0
data_enl['nord'] = 0
data_enl['est'] = 0
data_enl['ouest'] = 0
data_enl['sud_ouest'] = 0
data_enl['centre_est'] = 0
data_enl['medi'] = 0

data_enl.loc[data_enl['zeat'] == 1, 'reg_paris'] = 1
data_enl.loc[data_enl['zeat'] == 2, 'bass_paris'] = 1
data_enl.loc[data_enl['zeat'] == 3, 'nord'] = 1
data_enl.loc[data_enl['zeat'] == 4, 'est'] = 1
data_enl.loc[data_enl['zeat'] == 5, 'ouest'] = 1
data_enl.loc[data_enl['zeat'] == 7, 'sud_ouest'] = 1
data_enl.loc[data_enl['zeat'] == 8, 'centre_est'] = 1
data_enl.loc[data_enl['zeat'] == 9, 'medi'] = 1


"""
Predict froid
"""


regression = smf.ols(formula = 'froid_cout ~ \
    aides_logement + agepr + \
    com_5000 + com_10000 + com_20000 + com_50000 + com_100000 + com_200000 + \
    com_2000000 + revtot + rural + ocde10 + part_energies_revtot_after + \
    reg_paris + bass_paris + nord + est + ouest + sud_ouest + centre_est + medi + \
    surfhab_d + zeat',
    data = data_enl).fit()
print regression.summary()


"""
Predict froid_cout
"""


regression = smf.ols(formula = 'froid ~ \
    aides_logement + agepr + \
    com_5000 + com_10000 + com_20000 + com_50000 + com_100000 + com_200000 + \
    com_2000000 + revtot + rural + ocde10 + part_energies_revtot_after + \
    reg_paris + bass_paris + nord + est + ouest + sud_ouest + centre_est + medi + \
    surfhab_d + zeat',
    data = data_enl).fit()
print regression.summary()


