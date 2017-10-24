# -*- coding: utf-8 -*-

# In this script we estimate from the data ENL the probability for an household
# to be cold according to several of his characteristics.
# The aime will then be to compute the effect of the reform on the likelihood of being cold

# Import general modules
from __future__ import division

import statsmodels.formula.api as smf

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_2_homogenize_variables import \
    create_niveau_vie_quantiles

data_enl = create_niveau_vie_quantiles()[0]


stock_variables = [
    'agepr',
    'aides_logement',
    'depenses_energies',
    'dip14pr',
    'electricite',
    'gaz_ville',
    'isolation_fenetres',
    'isolation_murs',
    'isolation_toit',
    'majorite_double_vitrage',
    'nactifs',
    'nenfants',
    'ocde10',
    'ouest_sud',
    'paris',
    'petite_ville',
    'revtot',
    'rural',
    'surfhab_d',
    #'tee_10_3_deciles_depenses_tot',
    ]

#simulated_variables = stock_variables + ['niveau_vie_decile',
#   'froid_4_criteres_3_deciles', 'precarite_energetique_depenses_tot',
#   'total_taxes_energies']

data_enl = data_enl.query('niveau_vie_decile < 4')
data_enl['froid_4_criteres_3_deciles'] = (
    data_enl['froid_cout'] + data_enl['froid_isolation'] + data_enl['froid_impaye'] + data_enl['froid_installation']
    )
data_enl['froid_4_criteres_3_deciles'] = 1 * (data_enl['froid_4_criteres_3_deciles'] > 0)

data_enl = data_enl.query('revtot > 0')
data_enl['revtot_2'] = data_enl['revtot'] ** 2

data_enl['part_energies_revtot'] = data_enl['depenses_energies'] / data_enl['revtot']


new_stock_variables = list(stock_variables)
max_rsquared_adj = 0.000001
current_max_rsquared_adj = 0
variable_to_include = None
variables_kept = []
while max_rsquared_adj > current_max_rsquared_adj:
    current_max_rsquared_adj = max_rsquared_adj
    if variable_to_include is not None:
        new_stock_variables.remove(variable_to_include)
        variables_kept = variables_kept + [variable_to_include]
    for variable in new_stock_variables:
        variables = variables_kept + [variable]

        regressors = ' ' 
        for element in variables:
            if regressors == ' ':
                regressors = element
            else:
                regressors = regressors + ' + {}'.format(element)

        regression_ols = smf.ols(formula = 'froid_4_criteres_3_deciles ~ part_energies_revtot + revtot + revtot_2 + \
            depenses_combustibles_liquides + depenses_electricite + depenses_gaz_ville + {}'.format(regressors),
            data = data_enl).fit()
        rsquared_adj = regression_ols.rsquared_adj
        max_rsquared_adj = max(max_rsquared_adj, rsquared_adj)
        if rsquared_adj == max_rsquared_adj:
            variable_to_include = variable
        else:
            continue

summary_ols = regression_ols.summary()

print summary_ols

regressors = ['part_energies_revtot', 'revtot', 'revtot_2', 'depenses_combustibles_liquides',
              'depenses_electricite', 'depenses_gaz_ville'] + variables_kept

# When we do the same with Logit :
logit = smf.Logit(data_enl['froid_4_criteres_3_deciles'], data_enl[regressors]).fit()

summary_logit = logit.summary()
print summary_logit

data_enl['predict_logit'] = logit.predict()
data_enl['predict_ols'] = regression_ols.predict()

print data_enl['predict_ols'].mean()
print data_enl['predict_logit'].mean()
print data_enl['froid_4_criteres_3_deciles'].mean()

print data_enl[['predict_ols'] + ['predict_logit'] + ['froid_4_criteres_3_deciles']]

# A partir des coefficients estimés, calculer la probabilité de précarité de chaque ménage
# Remplacer par 1 pour ceux déjà précaires via le TEE ou le BRDE
# Calculer le nombre moyen de précaires en agrégeant les probas
# Faire de même après la réforme
# Comparer avant/après
