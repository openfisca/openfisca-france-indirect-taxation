# -*- coding: utf-8 -*-

import pandas as pd
from pandas import concat

import openfisca_france_indirect_taxation

tax_benefit_system = openfisca_france_indirect_taxation.FranceIndirectTaxationTaxBenefitSystem()
legislation_json = tax_benefit_system.legislation_json


def get_tva_taux_plein():
    dict_tva_taux_plein = \
        legislation_json['children']['imposition_indirecte']['children']['tva']['children']['taux_plein']
    df_tva_taux_plein = pd.DataFrame.from_dict(dict_tva_taux_plein['values'])
    df_tva_taux_plein['start'] = df_tva_taux_plein['start'].str[:4]
    del df_tva_taux_plein['stop']
    df_tva_taux_plein = df_tva_taux_plein.set_index('start')
    df_tva_taux_plein = df_tva_taux_plein.transpose()
    for year in range(1968, 2015):
        try:
            df_tva_taux_plein['{}'.format(year)]
        except:
            df_tva_taux_plein['{}'.format(year)] = df_tva_taux_plein['{}'.format(year - 1)]
    df_tva_taux_plein = df_tva_taux_plein.transpose()
    df_tva_taux_plein = df_tva_taux_plein.sort_index()

    return df_tva_taux_plein
