# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 17:52:53 2015

@author: thomas.douenne
"""


from __future__ import division

import numpy as np

from openfisca_france_indirect_taxation.example.utils_example import simulate_df


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Liste des variables que l'on veut simuler
    var_to_be_simulated_with_e10 = [
        'pondmen',
        'sp_e10_ticpe',
        'sp95_ticpe',
        'sp98_ticpe',
        'super_plombe_ticpe',
        'diesel_ticpe'
        ]

    var_to_be_simulated_without_e10 = [
        'pondmen',
        'sp95_ticpe',
        'sp98_ticpe',
        'super_plombe_ticpe',
        'diesel_ticpe'
        ]

    depenses_ticpe_totales = dict()
    depenses_ticpe_diesel = dict()
    depenses_ticpe_essence = dict()
    for year in [2000, 2005, 2011]:
        try:
            data_simulation = simulate_df(var_to_be_simulated = var_to_be_simulated_with_e10, year = year)
            data_simulation['diesel_ticpe_ponderee'] = data_simulation['diesel_ticpe'] * data_simulation['pondmen']
            data_simulation['sp95_ticpe_ponderee'] = data_simulation['sp95_ticpe'] * data_simulation['pondmen']
            data_simulation['sp98_ticpe_ponderee'] = data_simulation['sp98_ticpe'] * data_simulation['pondmen']
            data_simulation['sp_e10_ticpe_ponderee'] = data_simulation['sp_e10_ticpe'] * data_simulation['pondmen']
            data_simulation['super_plombe_ticpe_ponderee'] = \
                data_simulation['super_plombe_ticpe'] * data_simulation['pondmen']
        except:
            data_simulation = simulate_df(var_to_be_simulated = var_to_be_simulated_without_e10, year = year)
            data_simulation['diesel_ticpe_ponderee'] = data_simulation['diesel_ticpe'] * data_simulation['pondmen']
            data_simulation['sp95_ticpe_ponderee'] = data_simulation['sp95_ticpe'] * data_simulation['pondmen']
            data_simulation['sp98_ticpe_ponderee'] = data_simulation['sp98_ticpe'] * data_simulation['pondmen']
            data_simulation['sp_e10_ticpe_ponderee'] = 0
            data_simulation['super_plombe_ticpe_ponderee'] = \
                data_simulation['super_plombe_ticpe'] * data_simulation['pondmen']

        depenses_diesel_ticpe = data_simulation['diesel_ticpe_ponderee'].sum()
        depenses_sp95_ticpe = data_simulation['sp95_ticpe_ponderee'].sum()
        depenses_sp98_ticpe = data_simulation['sp98_ticpe_ponderee'].sum()
        depenses_sp_e10_ticpe = data_simulation['sp_e10_ticpe_ponderee'].sum()
        depenses_super_plombe_ticpe = data_simulation['super_plombe_ticpe_ponderee'].sum()

        if year < 2007:
            depenses_essence_ticpe = (
                depenses_sp95_ticpe +
                depenses_sp98_ticpe +
                depenses_sp_e10_ticpe +
                depenses_super_plombe_ticpe
                )
        else:
            depenses_essence_ticpe = (
                depenses_sp95_ticpe +
                depenses_sp98_ticpe +
                depenses_sp_e10_ticpe
                )

        depenses_ticpe = depenses_diesel_ticpe + depenses_essence_ticpe
        depenses_ticpe_totales['en millions d euros en {}'.format(year)] = depenses_ticpe / 1000000
        depenses_ticpe_diesel['en millions d euros en {}'.format(year)] = depenses_diesel_ticpe / 1000000
        depenses_ticpe_essence['en millions d euros en {}'.format(year)] = depenses_essence_ticpe / 1000000
