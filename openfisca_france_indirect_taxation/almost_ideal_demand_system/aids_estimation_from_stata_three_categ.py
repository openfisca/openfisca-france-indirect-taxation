# -*- coding: utf-8 -*-

import pandas as pd
import pkg_resources
import os

# Import data_quaids to get the results of the estimation run on Stata.
resultats_elasticite_depenses = dict()
resultats_elasticite_uncomp = dict()
resultats_elasticite_comp = dict()
for year in ['energy_no_alime_all']:
    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    data_quaids = pd.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'quaids',
            'data_quaids_{}.csv'.format(year)
            ), sep =',')

    data_quaids = data_quaids.fillna(0)

    for i in range(1, 4):
        data_quaids['el_uncomp_{}'.format(i)] = (
            data_quaids['elas_price_{}_{}'.format(i, i)] *
            (data_quaids['depenses_tot'] * data_quaids['w{}'.format(i)]) /
            (data_quaids['depenses_tot'] * data_quaids['w{}'.format(i)]).sum()
            )

    for i in range(1, 4):
        resultats_elasticite_uncomp['el_uncomp_{0}_{1}'.format(i, year)] = sum(data_quaids['el_uncomp_{}'.format(i)])

    for i in range(1, 4):
        data_quaids['el_comp_{}'.format(i)] = (
            data_quaids['comp_price_{}_{}'.format(i, i)] *
            (data_quaids['depenses_tot'] * data_quaids['w{}'.format(i)]) /
            (data_quaids['depenses_tot'] * data_quaids['w{}'.format(i)]).sum()
            )

    for i in range(1, 4):
        resultats_elasticite_comp['el_comp_{0}_{1}'.format(i, year)] = sum(data_quaids['el_comp_{}'.format(i)])

    for i in range(1, 4):
        data_quaids['el_{}'.format(i)] = (
            data_quaids['elas_exp_{}'.format(i)] *
            (data_quaids['depenses_tot'] * data_quaids['w{}'.format(i)]) /
            (data_quaids['depenses_tot'] * data_quaids['w{}'.format(i)]).sum()
            )

    for i in range(1, 4):
        resultats_elasticite_depenses['el_{0}_{1}'.format(i, year)] = sum(data_quaids['el_{}'.format(i)])
