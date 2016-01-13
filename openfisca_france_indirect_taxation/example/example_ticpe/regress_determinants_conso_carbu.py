# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 14:25:36 2015

@author: thomas.douenne
"""

# The aim of this module is to understand what determines the fuel consumption of households. We want to know what are
# the determinant features, such as the effect of income or residence on fuel consumption. We could therefore try to
# estimate price and income elasticities for fuel consumption on micro data. To avoid the endogeneity of our data,
# taking into account that income may be linked to fuel consumption through other effect that what we want to capture
# in the income effect, we could instrument by the total consumption, or by the rent.

# The regression will take the following form: the explained variable will be the fuel consumption expressed not in €
# but in litres. The explanatory variables will be a set of covariates, prices and income. Then we will look at the
# results when we instrument for income.
# We must construct a dataframe with for each individual its fuel consumption, and all the determinant variables.


from __future__ import division

import statsmodels.formula.api as smf
import numpy as np
import pandas as pd
import pkg_resources
import os

from openfisca_france_indirect_taxation.example.utils_example import simulate_df_calee_on_ticpe
from openfisca_france_indirect_taxation.get_dataframe_from_legislation.get_accises import \
    get_accise_ticpe_majoree

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    simulated_variables_without_e10 = [
        'sp95_ticpe',
        'sp98_ticpe',
        'super_plombe_ticpe',
        'diesel_ticpe',
        'rev_disponible',
        'strate',
        'nenfants',
        'nadultes',
        'situacj',
        'situapr',
        'niveau_vie_decile',
        'ocde10',
        'vag',
        'poste_coicop_411',
        'poste_coicop_412',
        'poste_coicop_421'
        ]

    simulated_variables_with_e10 = simulated_variables_without_e10 + ['sp_e10_ticpe']

# First, obtain the fuel consumption of each individual:

    for year in [2005]:
        try:
            data_simulation = \
                simulate_df_calee_on_ticpe(simulated_variables = simulated_variables_with_e10, year = year)
        except:
            data_simulation = \
                simulate_df_calee_on_ticpe(simulated_variables = simulated_variables_without_e10, year = year)
            data_simulation['sp_e10_ticpe'] = 0
        del simulated_variables_with_e10, simulated_variables_without_e10

        liste_carburants_accise = get_accise_ticpe_majoree()
        value_accise_diesel = liste_carburants_accise['accise majoree diesel'].loc[u'{}'.format(year)] / 100
        value_accise_sp = liste_carburants_accise['accise majoree sans plomb'].loc[u'{}'.format(year)] / 100
        value_accise_super_plombe = \
            liste_carburants_accise['accise majoree super plombe'].loc[u'{}'.format(year)] / 100

        data_simulation['quantite_diesel'] = data_simulation['diesel_ticpe'] / (value_accise_diesel)
        data_simulation['quantite_sans_plomb'] = (data_simulation['sp95_ticpe'] + data_simulation['sp98_ticpe'] +
            data_simulation['sp_e10_ticpe']) / (value_accise_sp)
        data_simulation['quantite_super_plombe'] = data_simulation['super_plombe_ticpe'] / (value_accise_super_plombe)
        del value_accise_diesel, value_accise_sp, value_accise_super_plombe, liste_carburants_accise

        for element in data_simulation['quantite_super_plombe']:
            if element == np.nan:
                data_simulation['quantite_essence'] = (
                    data_simulation['quantite_sans_plomb'] + data_simulation['quantite_super_plombe']
                    )
            else:
                data_simulation['quantite_essence'] = data_simulation['quantite_sans_plomb']
        data_simulation['quantite_carbu'] = data_simulation['quantite_diesel'] + data_simulation['quantite_essence']

        # We transform the variable strate into 5 dummy variables, one for each type of area:

        data_simulation['rural'] = 0
        data_simulation['petite_villes'] = 0
        data_simulation['villes_moyennes'] = 0
        data_simulation['grandes_villes'] = 0
        data_simulation['agglo_paris'] = 0

        data_simulation.loc[data_simulation['strate'] == 0, 'rural'] = 1
        data_simulation.loc[data_simulation['strate'] == 1, 'petite_villes'] = 1
        data_simulation.loc[data_simulation['strate'] == 2, 'villes_moyennes'] = 1
        data_simulation.loc[data_simulation['strate'] == 3, 'grandes_villes'] = 1
        data_simulation.loc[data_simulation['strate'] == 4, 'agglo_paris'] = 1

        # For each household we now have the quantity of fuel consumed in litres. This is our dependant variable.
        # We will now construct a dataframe including the explanatory variables. We especially need prices.

        default_config_files_directory = os.path.join(
            pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
        prix_carbu = pd.read_csv(
            os.path.join(
                default_config_files_directory,
                'openfisca_france_indirect_taxation',
                'assets',
                'prix_mensuel_carbu_match_to_vag.csv'
                ), sep =';', decimal = ','
            )

        prix_carbu = prix_carbu[['diesel_ttc'] + ['super_95_ttc'] + ['vag']].astype(float)

        data_households = pd.merge(data_simulation, prix_carbu, on = 'vag')
        del data_simulation, prix_carbu

        data_households = data_households[['quantite_carbu'] + ['quantite_diesel'] + ['quantite_essence'] +
            ['diesel_ttc'] + ['super_95_ttc'] + ['rev_disponible'] + ['rural'] + ['petite_villes'] +
            ['villes_moyennes'] + ['grandes_villes'] + ['agglo_paris'] + ['nenfants'] + ['nadultes'] + ['ocde10'] +
            ['situapr'] + ['situacj'] + ['poste_coicop_411'] + ['poste_coicop_412'] + ['poste_coicop_421']
            ].astype(float)

        # data_households contains all the variables we need for the regression. We can therefore implement it

        reg_conso_carbu = smf.ols(formula = 'quantite_carbu ~ \
            diesel_ttc + super_95_ttc + rev_disponible + rural + petite_villes + grandes_villes + \
            agglo_paris + nenfants + nadultes + situacj + situapr',
            data = data_households).fit()
        # print reg_conso_carbu.summary()

        # We may want to estimate elasticities, which implies the use of log variables:
        data_log = data_households.copy()
        data_log['ln_quantite_carbu'] = np.log(data_log['quantite_carbu'])
        data_log.loc[data_log['ln_quantite_carbu'] < -10, 'ln_quantite_carbu'] = 0
        data_log['ln_diesel_ttc'] = np.log(data_log['diesel_ttc'])
        data_log['ln_super_95_ttc'] = np.log(data_log['super_95_ttc'])
        data_log['ln_rev_disponible'] = np.log(data_log['rev_disponible'])
        data_log = data_log[data_log['rev_disponible'] > 0]

        reg_conso_carbu_log = smf.ols(formula = 'ln_quantite_carbu ~ \
            ln_diesel_ttc + ln_super_95_ttc + ln_rev_disponible + rural + petite_villes + grandes_villes + \
            agglo_paris + nenfants + nadultes + situacj + situapr',
            data = data_log).fit()
        print reg_conso_carbu_log.summary()

        # We will now introduce an instrumental variable to correct for the endogeneity of expenditures.

        data_log['loyer'] = data_log['poste_coicop_411'] + data_log['poste_coicop_412'] + data_log['poste_coicop_421']
        data_log.to_csv('data_regression.csv', sep = ',')
        #model = \
        #    gmm.IV2SLS(data_log['ln_rev_disponible'], data_log['ln_quantite_carbu'], data_log['loyer']).fit()
        #print model.summary()

        # reg_gmm = statsmodels.sandbox.regression.gmm.IV2SLS('ln_rev_disponible', 'ln_quantite_carbu',
          #                                                  instrument='loyer')

# The results are equivalent for the three years concerning the income elasticity, and it is close to 1. It seems to be
# important, but not absurd. The price elasticities however are probably not well estimated, with positive price
# elasticities. This does not make sense, maybe because of the lack of variation in prices, maybe because of endogeneity

# Next step: we may use instrumental variables, we may also use bootstrap standard errors.
# A first instrument could by total expenditure (minus fuel expenditures to avoid endogeneity)
# But there is actually no reason for this instrument to be exogenous
# A more promising instrument is the rent (or imputed rent) paid by the households. This is given at the coicop
# 411 and 412, and in loyer_impute (= poste_coicop_421).

# The command to execute 2 stage least square is the following:
# statsmodels.sandbox.regression.gmm.IV2SLS(endog, exog, instrument=None)
