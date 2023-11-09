# -*- coding: utf-8 -*-


'''
In this script we run a stepwise regression for the prediction of the variables
we want to match. The objective is to select the independent variables with
the largest predictive power.
'''

import statsmodels.formula.api as smf


from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_2_homogenize_variables import (
    create_niveau_vie_quantiles)


data_enl = create_niveau_vie_quantiles()[0]
data_enl['revtot_2'] = data_enl['revtot'] ** 2

stock_variables = [
    'agepr',
    'aides_logement',
    'bat_49_74',
    'bat_av_49',
    'cs42pr',
    'depenses_energies',
    'dip14pr',
    'electricite',
    'fioul',
    'gaz',
    'log_indiv',
    'moyenne_ville',
    'nactifs',
    'nenfants',
    'ocde10',
    'ouest_sud',
    'paris',
    'part_energies_revtot',
    'petite_ville',
    'revtot',
    'rural',
    'surfhab_d',
    ]

for dependent_variable in ['froid', 'froid_cout', 'froid_isolation']:
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

            formula = '{} ~ {}'.format(dependent_variable, regressors)
            print(formula)
            regression = smf.ols(formula = formula, data = data_enl).fit()

            rsquared_adj = regression.rsquared_adj
            max_rsquared_adj = max(max_rsquared_adj, rsquared_adj)
            if rsquared_adj == max_rsquared_adj:
                variable_to_include = variable
            else:
                continue

    else:
        if dependent_variable == 'froid':
            regression_froid = regression.summary()
        if dependent_variable == 'froid_cout':
            regression_froid_cout = regression.summary()
        else:
            regression_froid_isolation = regression.summary()


print(regression_froid)
print(regression_froid_cout)
# print regression_froid_isolation

latex = regression_froid.as_latex()
