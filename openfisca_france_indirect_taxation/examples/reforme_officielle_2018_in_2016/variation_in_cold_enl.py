# -*- coding: utf-8 -*-

# In this script we estimate from the data ENL the probability for an household
# to be cold according to several of his characteristics.
# The aime will then be to compute the effect of the reform on the likelihood of being cold

# Import general modules
from __future__ import division

import statsmodels.formula.api as smf

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_2_homogenize_variables import \
    create_niveau_vie_quantiles

def estimate_froid():
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
        ]
        
    data_enl = data_enl.query('niveau_vie_decile < 4')
    data_enl['froid_4_criteres_3_deciles'] = (
        data_enl['froid_cout'] + data_enl['froid_isolation'] + data_enl['froid_impaye'] + data_enl['froid_installation']
        )
    data_enl['froid_4_criteres_3_deciles'] = 1 * (data_enl['froid_4_criteres_3_deciles'] > 0)
    
    data_enl = data_enl.query('revtot > 0')
    data_enl['revtot_2'] = data_enl['revtot'] ** 2
    
    data_enl['part_energies_revtot'] = data_enl['depenses_energies'] / data_enl['revtot']
    
    
    # OLS regression
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

    # Logistic regression
    regressors = ['part_energies_revtot', 'revtot', 'revtot_2', 'depenses_combustibles_liquides',
                  'depenses_electricite', 'depenses_gaz_ville'] + variables_kept
    regression_logit = smf.Logit(data_enl['froid_4_criteres_3_deciles'], data_enl[regressors]).fit()
    
    return regression_ols, regression_logit


if __name__ == "__main__":
    estimations = estimate_froid()
    regression_ols = estimations[0]
    regression_logit = estimations[1]

    print regression_ols.summary()
    print regression_logit.summary()
