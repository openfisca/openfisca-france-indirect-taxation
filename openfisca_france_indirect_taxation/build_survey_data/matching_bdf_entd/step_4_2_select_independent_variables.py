# -*- coding: utf-8 -*-


"""
In this script we run a stepwise regression for the prediction of the variables
we want to match. The objective is to select the independent variables with
the largest predictive power.
"""

import statsmodels.formula.api as smf


from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_2_homogenize_variables import \
    create_niveau_vie_quantiles


data_entd = create_niveau_vie_quantiles()[0]

data_entd['niveau_vie_2'] = data_entd['niveau_vie'] ** 2
data_entd['distance'] = (
    data_entd['distance_diesel'] + data_entd['distance_essence']
    + data_entd['distance_autre_carbu']
    )

stock_variables = ['agepr', 'age_vehicule', 'age_carte_grise', 'aides_logement',
    'cataeu', 'cs42pr', 'dip14pr', 'moyenne_ville', 'nactifs', 'nb_diesel',
    'nb_essence', 'nbphab', 'nenfants', 'niveau_vie', 'niveau_vie_2', 'npers',
    'ocde10', 'paris', 'petite_ville', 'rural', 'situapr', 'typmen', 'veh_tot',
    'vp_deplacements_pro', 'vp_domicile_travail'
                   ]

for dependent_variable in ['distance', 'distance_diesel', 'distance_essence']:
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

            regression = smf.ols(formula = '{} ~ \
                {}'.format(dependent_variable, regressors),
                data = data_entd).fit()

            rsquared_adj = regression.rsquared_adj
            max_rsquared_adj = max(max_rsquared_adj, rsquared_adj)
            if rsquared_adj == max_rsquared_adj:
                variable_to_include = variable
            else:
                continue

    else:
        if dependent_variable == 'distance':
            regression_distance = regression.summary()
        if dependent_variable == 'distance_diesel':
            regression_distance_diesel = regression.summary()
        else:
            regression_distance_essence = regression.summary()


print(regression_distance)
# print regression_distance_diesel
# print regression_distance_essence

# latex = regression_distance.as_latex()
