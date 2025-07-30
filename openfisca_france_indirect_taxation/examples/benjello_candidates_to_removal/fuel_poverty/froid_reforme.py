# -*- coding: utf-8 -*-


import statsmodels.formula.api as smf


from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy


stock_variables = [
    # 'agepr',
    'aides_logement',
    # 'brde_m2_depenses_tot',
    'combustibles_liquides',
    'depenses_combustibles_liquides',
    'depenses_electricite',
    'depenses_energies_logement',
    'depenses_gaz_ville',
    'depenses_tot',
    'dip14pr',
    'electricite',
    'gaz_ville',
    'nactifs',
    # 'nenfants',
    'ocde10',
    'ouest_sud',
    'paris',
    'petite_ville',
    'pondmen',
    'rev_disp_loyerimput',
    'rural',
    'surfhab_d',
    # 'tee_10_3_deciles_depenses_tot',
    ]

simulated_variables = stock_variables + ['niveau_vie_decile',
   'froid_4_criteres_3_deciles', 'precarite_energetique_depenses_tot',
   'total_taxes_energies']

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])


survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    year = year,
    data_year = data_year
    )

indiv_df_reference = survey_scenario.create_data_frame_by_entity(simulated_variables,
    use_baseline =True, period = year)

menages_reference = indiv_df_reference['menage']
# menages_reference =menages_reference.query('niveau_vie_decile < 4')
menages_reference['froid_4_criteres_3_deciles'] = \
    menages_reference['froid_4_criteres_3_deciles'].astype(int)

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

        regression = smf.ols(formula = 'froid_4_criteres_3_deciles ~ {}'.format(regressors),
            data = menages_reference).fit()
        rsquared_adj = regression.rsquared_adj
        max_rsquared_adj = max(max_rsquared_adj, rsquared_adj)
        if rsquared_adj == max_rsquared_adj:
            variable_to_include = variable
        else:
            continue

regression = regression.summary()

print(regression)

# A partir des coefficients estimés, calculer la probabilité de précarité de chaque ménage
# Remplacer par 1 pour ceux déjà précaires via le TEE ou le BRDE
# Calculer le nombre moyen de précaires en agrégeant les probas
# Faire de même après la réforme
# Comparer avant/après
