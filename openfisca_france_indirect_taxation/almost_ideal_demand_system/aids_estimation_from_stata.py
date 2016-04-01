# -*- coding: utf-8 -*-

from __future__ import division


import pandas as pd
import pkg_resources
import os


def get_elasticities(year):
    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    data_quaids = pd.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'quaids',
            'data_quaids_energy_no_alime_all.csv'.format(year)
            ), sep =',')
    data_quaids = data_quaids.query('year == @year')
    liste_elasticities = [column for column in data_quaids.columns if column[:4] == 'elas']
    data_quaids[liste_elasticities] = data_quaids[liste_elasticities].astype('float32')
    dataframe = data_quaids[liste_elasticities + ['ident_men', 'year']].copy()

    dataframe = dataframe.fillna(0)
    # We block the elasticities of housing energy to some value found in the literature (Clerc and Marcus, 2009)
    dataframe['elas_price_2_2'] = -0.1

    assert not dataframe.ident_men.duplicated().any(), 'Some housholds are duplicated'

    return dataframe


def test():
    # Import data_quaids to get the results of the estimation run on Stata.
    resultats_elasticite_depenses = dict()
    resultats_elasticite_uncomp = dict()
    borne_inferieure_el_dep = dict()
    borne_superieure_el_dep = dict()
    for year in ['all', 'all_no_elect_only']:
        default_config_files_directory = os.path.join(
            pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
        data_quaids = pd.read_csv(
            os.path.join(
                default_config_files_directory,
                'openfisca_france_indirect_taxation',
                'assets',
                'quaids',
                'data_quaids_{}.csv'.format(year)
                ),
            sep =',')

        # Compute a weighted average of the elasticity of each household
        # weights are the share of the household in total consumption
        data_quaids['part_depenses_tot'] = data_quaids['depenses_tot'] / data_quaids['depenses_tot'].sum()
        data_quaids.fillna(0, inplace=True)
        assert 0.999 < sum(data_quaids['part_depenses_tot']) < 1.001, "the sum of the shares is not equal to 1"

        for i in range(1, 5):
            data_quaids['el_{}'.format(i)] = \
                data_quaids['elas_exp_{}'.format(i)] * data_quaids['part_depenses_tot']

        # Compute the estimation of the income elasticities of consumption
        for i in range(1, 5):
            resultats_elasticite_depenses['el_{0}_{1}'.format(i, year)] = data_quaids['el_{}'.format(i)].sum()

        # Compute the 95% confidence interval for those elasticities
        for i in range(1, 5):
            borne_superieure_el_dep['borne_sup_{0}_{1}'.format(i, year)] = (
                resultats_elasticite_depenses['el_{0}_{1}'.format(i, year)] + 1.96 *
                (data_quaids['elas_exp_{}'.format(i)].describe()['std'] /
                len(data_quaids['elas_exp_{}'.format(i)]) ** 0.5)
                )
            borne_inferieure_el_dep['borne_inf_{0}_{1}'.format(i, year)] = (
                resultats_elasticite_depenses['el_{0}_{1}'.format(i, year)] - 1.96 *
                (data_quaids['elas_exp_{}'.format(i)].describe()['std'] /
                len(data_quaids['elas_exp_{}'.format(i)]) ** 0.5)
                )

        for i in range(1, 5):
            data_quaids['el_uncomp_{}'.format(i)] = \
                data_quaids['elas_price_{}_{}'.format(i, i)] * data_quaids['part_depenses_tot']

        # Compute the estimation of the uncompensated price elasticities of consumption
        for i in range(1, 5):
            resultats_elasticite_uncomp['el_uncomp_{0}_{1}'.format(i, year)] = sum(data_quaids['el_uncomp_{}'.format(i)])


if __name__ =="__main__":
    year = 2011
    df = get_elasticities(year)
    print df.dtypes