# -*- coding: utf-8 -*-

import pandas as pd
import os

from openfisca_france_indirect_taxation.utils import assets_directory


# Import data_quaids to get the results of the estimation run on Stata.
selection_elasticites = dict()
resultats_elasticite_depenses = dict()
resultats_elasticite_uncomp = dict()
resultats_elasticite_comp = dict()
for year in ['energy_no_alime_all']:
    data_quaids = pd.read_csv(
        os.path.join(
            assets_directory,
            'quaids',
            'data_quaids_{}.csv'.format(year)
            ), sep =',')

    data_quaids = data_quaids.fillna(0)
    df = data_quaids.query('year == 2011')

    # positive_elas = df.query('elect_only == 0').query('elas_price_2_2 > 0')['pondmen'].sum()
    # sum_pop = df.query('elect_only == 0')['pondmen'].sum()
    # ratio_positive_elas = positive_elas / sum_pop

    # Set upper and lower bounds for elasticities : [-2;0]
    for j in range(1, 4):
        selection_elasticites['elas_price_{0}_{0} - (0)'.format(j)] = \
            float(len(df.query('elas_price_{0}_{0} > 0'.format(j)))) / len(df)
        selection_elasticites['elas_price_{0}_{0} - (-2)'.format(j)] = \
            float(len(df.query('elas_price_{0}_{0} < -2'.format(j)))) / len(df)
        df['elas_price_{0}_{0}'.format(j)] = \
            (df['elas_price_{0}_{0}'.format(j)] < 0) * df['elas_price_{0}_{0}'.format(j)]
        df['elas_price_{0}_{0}'.format(j)] = (
            (df['elas_price_{0}_{0}'.format(j)] > -2) * df['elas_price_{0}_{0}'.format(j)]
            + (df['elas_price_{0}_{0}'.format(j)] < -2) * (-2)
            )

    for i in range(1, 4):
        df['el_uncomp_{}'.format(i)] = (
            df['elas_price_{}_{}'.format(i, i)]
            * (df['depenses_tot'] * df['w{}'.format(i)])
            / (df['depenses_tot'] * df['w{}'.format(i)]).sum()
            )

    for i in range(1, 4):
        resultats_elasticite_uncomp['el_uncomp_{0}_{1}'.format(i, year)] = sum(df['el_uncomp_{}'.format(i)])

    for i in range(1, 4):
        df['el_comp_{}'.format(i)] = (
            df['comp_price_{}_{}'.format(i, i)]
            * (df['depenses_tot'] * df['w{}'.format(i)])
            / (df['depenses_tot'] * df['w{}'.format(i)]).sum()
            )

    for i in range(1, 4):
        resultats_elasticite_comp['el_comp_{0}_{1}'.format(i, year)] = sum(df['el_comp_{}'.format(i)])

    for i in range(1, 4):
        df['el_{}'.format(i)] = (
            df['elas_exp_{}'.format(i)]
            * (df['depenses_tot'] * df['w{}'.format(i)])
            / (df['depenses_tot'] * df['w{}'.format(i)]).sum()
            )

    for i in range(1, 4):
        resultats_elasticite_depenses['el_{0}_{1}'.format(i, year)] = sum(df['el_{}'.format(i)])
