# -*- coding: utf-8 -*-

import pandas as pd
from pandas import concat

import openfisca_france_indirect_taxation

TaxBenefitSystem = openfisca_france_indirect_taxation.init_country()
tax_benefit_system = TaxBenefitSystem()
legislation_json = tax_benefit_system.legislation_json


def get_prix_carburants(liste_carburants):
    prix_carburants = None
    for element in liste_carburants:
        prix_dict = \
            legislation_json['children']['imposition_indirecte']['children']['prix_carburants']['children'][element]
        df_prix = pd.DataFrame.from_dict(prix_dict['values'])

        df_prix['start'] = df_prix['start'].str[:4]
        del df_prix['stop']
        df_prix = df_prix.set_index('start')
        df_prix.rename(columns = {'value': 'prix ' + element.replace('_', ' ')}, inplace = True)

        if prix_carburants is not None:
            prix_carburants = concat([prix_carburants, df_prix], axis=1)
        else:
            prix_carburants = df_prix

    return prix_carburants
