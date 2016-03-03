# -*- coding: utf-8 -*-

import pandas as pd
from pandas import concat

import openfisca_france_indirect_taxation

TaxBenefitSystem = openfisca_france_indirect_taxation.init_country()
tax_benefit_system = TaxBenefitSystem()
legislation_json = tax_benefit_system.legislation_json


# To do: integrate "majoration regionale ticpe" to reflect the real excise taxes applied
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


def get_majoration_ticpe(liste_carburants):
    majoration_carburants = None
    for element in liste_carburants:
        majoration_dict = \
            legislation_json['children']['imposition_indirecte']['children'][element]['children']['alsace']
        df_majoration = pd.DataFrame.from_dict(majoration_dict['values'])
        df_majoration['start'] = df_majoration['start'].str[:4]
        del df_majoration['stop']
        df_majoration = df_majoration.set_index('start')
        df_majoration = df_majoration.transpose()

        for year in range(2007, 2021):
            try:
                df_majoration['{}'.format(year)]
            except:
                df_majoration['{}'.format(year)] = df_majoration['{}'.format(year - 1)]
        df_majoration = df_majoration.transpose()
        df_majoration.rename(columns = {'value': element.replace('_', ' ')}, inplace = True)
        df_majoration = df_majoration.sort_index()

        if majoration_carburants is not None:
            majoration_carburants = concat([majoration_carburants, df_majoration], axis = 1)
        else:
            majoration_carburants = df_majoration

    return majoration_carburants


def get_accise_ticpe_majoree():
    accise_nationale = get_accises_carburants(['ticpe_gazole', 'ticpe_super9598', 'super_plombe_ticpe'])
    majoration_regionale = get_majoration_ticpe(['major_regionale_ticpe_gazole', 'major_regionale_ticpe_super'])
    accise_totale = concat([accise_nationale, majoration_regionale], axis = 1)
    accise_totale = accise_totale.fillna(0)
    accise_totale['accise majoree sans plomb'] = (
        accise_totale['accise ticpe super9598'] + accise_totale['major regionale ticpe super']
        )
    accise_totale['accise majoree super plombe'] = (
        accise_totale['accise super plombe ticpe'] + accise_totale['major regionale ticpe super']
        )
    accise_totale['accise majoree diesel'] = (
        accise_totale['accise ticpe gazole'] + accise_totale['major regionale ticpe gazole']
        )
    accise_totale = accise_totale[
        ['accise majoree sans plomb'] + ['accise majoree super plombe'] + ['accise majoree diesel']
        ].copy()
    accise_totale = accise_totale[accise_totale['accise majoree sans plomb'] != 2.5].copy()

    return accise_totale
