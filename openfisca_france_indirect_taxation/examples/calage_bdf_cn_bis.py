# -*- coding: utf-8 -*-


from __future__ import division

import logging
import os
import pkg_resources
import csv

import pandas
from pandas import concat

from openfisca_france_indirect_taxation.examples.utils_example import get_input_data_frame
from openfisca_france_indirect_taxation.build_survey_data.utils import find_nearest_inferior


log = logging.getLogger(__name__)


data_years = [2000, 2005, 2011]


def get_bdf_aggregates(data_year = None):
    assert data_year is not None

    depenses = get_input_data_frame(data_year)
    depenses_by_grosposte = pandas.DataFrame()
    for grosposte in range(1, 13):
        if depenses_by_grosposte is None:
            depenses_by_grosposte = depenses['coicop12_{}'.format(grosposte)]
        else:
            depenses_by_grosposte = concat([depenses_by_grosposte, depenses['coicop12_{}'.format(grosposte)]], axis = 1)

    depenses_by_grosposte = concat([depenses_by_grosposte, depenses['pondmen']], axis = 1)
    grospostes = set(depenses_by_grosposte.columns)
    grospostes.remove('pondmen')
    bdf_aggregates_by_grosposte = pandas.DataFrame()
    for grosposte in grospostes:
        bdf_aggregates_by_grosposte.loc[grosposte, 'bdf_aggregates'] = (
            depenses_by_grosposte[grosposte] * depenses_by_grosposte['pondmen']
            ).sum()

    return bdf_aggregates_by_grosposte


def get_cn_aggregates(target_year = None):
    assert target_year is not None
    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    parametres_fiscalite_file_path = os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'legislation',
        'Parametres fiscalite indirecte.xls'
        )
    masses_cn_data_frame = pandas.read_excel(parametres_fiscalite_file_path, sheetname = "consommation_CN")
    masses_cn_12postes_data_frame = masses_cn_data_frame.loc[:, ['Code', target_year]]
    masses_cn_12postes_data_frame['code_unicode'] = masses_cn_12postes_data_frame.Code.astype(unicode)
    masses_cn_12postes_data_frame['len_code'] = masses_cn_12postes_data_frame['code_unicode'].apply(lambda x: len(x))

    masses_cn_12postes_data_frame = masses_cn_12postes_data_frame[masses_cn_12postes_data_frame['len_code'] == 6]
    masses_cn_12postes_data_frame['code'] = masses_cn_12postes_data_frame.Code.astype(int)
    masses_cn_12postes_data_frame = masses_cn_12postes_data_frame.drop(['len_code', 'code_unicode', 'Code'], 1)

    masses_cn_12postes_data_frame.rename(
        columns = {
            target_year: 'consoCN_COICOP_{}'.format(target_year),
            'code': 'poste'
            },
        inplace = True,
        )
    masses_cn_12postes_data_frame['poste'] = masses_cn_12postes_data_frame['poste'].astype(str)
    masses_cn_12postes_data_frame = masses_cn_12postes_data_frame[masses_cn_12postes_data_frame['poste'] != '15']
    for element in masses_cn_12postes_data_frame['poste']:
        masses_cn_12postes_data_frame['poste'] = \
            masses_cn_12postes_data_frame['poste'].replace(element, 'coicop12_{}'.format(element))
    masses_cn_12postes_data_frame.set_index('poste', inplace = True)
    return masses_cn_12postes_data_frame * 1e6


def get_inflators_bdf_to_cn(data_year):
    '''
    Calcule les ratios de calage (bdf sur cn pour année de données)
    à partir des masses de comptabilité nationale et des masses de consommation de bdf.
    '''
    data_cn = get_cn_aggregates(data_year)
    data_bdf = get_bdf_aggregates(data_year)
    masses = data_cn.merge(
        data_bdf, left_index = True, right_index = True
        )
    masses.rename(columns = {'bdf_aggregates': 'conso_bdf{}'.format(data_year)}, inplace = True)
    return (
        masses['consoCN_COICOP_{}'.format(data_year)] / masses['conso_bdf{}'.format(data_year)]
        ).to_dict()


def get_inflators_cn_to_cn(target_year):
    '''
        Calcule l'inflateur de vieillissement à partir des masses de comptabilité nationale.
    '''
    data_year = find_nearest_inferior(data_years, target_year)
    data_year_cn_aggregates = get_cn_aggregates(data_year)['consoCN_COICOP_{}'.format(data_year)].to_dict()
    target_year_cn_aggregates = get_cn_aggregates(target_year)['consoCN_COICOP_{}'.format(target_year)].to_dict()

    return dict(
        (key, target_year_cn_aggregates[key] / data_year_cn_aggregates[key])
        for key in data_year_cn_aggregates.keys()
        )


def get_inflators(target_year):
    '''
    Fonction qui calcule les ratios de calage (bdf sur cn pour année de données) et de vieillissement
    à partir des masses de comptabilité nationale et des masses de consommation de bdf.
    '''
    data_year = find_nearest_inferior(data_years, target_year)
    inflators_bdf_to_cn = get_inflators_bdf_to_cn(data_year)
    inflators_cn_to_cn = get_inflators_cn_to_cn(target_year)

    ratio_by_variable = dict()
    for key in inflators_cn_to_cn.keys():
        ratio_by_variable[key] = inflators_bdf_to_cn[key] * inflators_cn_to_cn[key]

    return ratio_by_variable


def get_inflators_by_year(rebuild = False):
    assets_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
        )
    if rebuild is not False:
        inflators_by_year = dict()
        for target_year in range(2000, 2015):
            inflators = get_inflators(target_year)
            inflators_by_year[target_year] = inflators

        for year in range(2000, 2015):
            writer_inflators = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation',
                'assets', 'inflateurs', 'inflators_by_year_{}.csv'.format(year)), 'wb'))
            for key, value in inflators_by_year[year].items():
                writer_inflators.writerow([key, value])

        return inflators_by_year

    else:
        re_build_inflators = dict()
        for year in range(2000, 2015):
            inflators_from_csv = pandas.DataFrame.from_csv(os.path.join(assets_directory,
                'openfisca_france_indirect_taxation', 'assets', 'inflateurs', 'inflators_by_year_{}.csv'.format(year)),
                header = -1)
            inflators_to_dict = pandas.DataFrame.to_dict(inflators_from_csv)
            inflators = inflators_to_dict[1]
            re_build_inflators[year] = inflators

        return re_build_inflators


def get_aggregates_by_year():
    aggregates_by_year = dict()
    for target_year in range(2000, 2015):
        aggregates = get_cn_aggregates(target_year)['consoCN_COICOP_{}'.format(target_year)].to_dict()
        aggregates_by_year[target_year] = aggregates
