# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 18:09:46 2015

@author: thomas.douenne
"""

import pandas as pd
from pandas import concat

import openfisca_france_indirect_taxation

TaxBenefitSystem = openfisca_france_indirect_taxation.init_country()
tax_benefit_system = TaxBenefitSystem()
legislation_json = tax_benefit_system.legislation_json


def get_accises_carburants(liste_carburants):
    accises_carburants = None
    for element in liste_carburants:
        accise_dict = \
            legislation_json['children']['imposition_indirecte']['children']['ticpe']['children'][element]
        df_accise = pd.DataFrame.from_dict(accise_dict['values'])

        df_accise['start'] = df_accise['start'].str[:4]
        del df_accise['stop']
        df_accise = df_accise.set_index('start')
        df_accise = df_accise.transpose()

        for year in range(1993, 2017):
            try:
                df_accise['{}'.format(year)]
            except:
                df_accise['{}'.format(year)] = df_accise['{}'.format(year - 1)]

        df_accise = df_accise.transpose()
        df_accise.rename(columns = {'value': 'accise ' + element.replace('_', ' ')}, inplace = True)
        df_accise = df_accise.sort_index()

        if accises_carburants is not None:
            accises_carburants = concat([accises_carburants, df_accise], axis=1)
        else:
            accises_carburants = df_accise

    return accises_carburants
