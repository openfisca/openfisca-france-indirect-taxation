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


data_years = [2000, 2005, 2011]


def get_bdf_aggregates(data_year = None):
    assert data_year is not None

    depenses = get_input_data_frame(data_year)
    depenses_energie = pandas.DataFrame()
    variables_energie = ['poste_coicop_722', 'poste_coicop_451', 'poste_coicop_452']
    for energie in variables_energie:
        if depenses_energie is None:
            depenses_energie = depenses['{}'.format(energie)]
        else:
            depenses_energie = concat([depenses_energie, depenses['{}'.format(energie)]], axis = 1)

    depenses_energie = concat([depenses_energie, depenses['pondmen']], axis = 1)
    bdf_aggregates_by_energie = pandas.DataFrame()
    for energie in variables_energie:
        bdf_aggregates_by_energie.loc[energie, 'bdf_aggregates'] = (
            depenses_energie[energie] * depenses_energie['pondmen']
            ).sum()

    return bdf_aggregates_by_energie


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
    masses_cn_data_frame = masses_cn_data_frame.loc[:, ['Code', target_year]].copy()

    masses_cn_data_frame['poste'] = 0
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            04.5.1', 'poste'] = 451
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            04.5.2', 'poste'] = 452
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            07.2.2', 'poste'] = 722
    masses_cn_energie = masses_cn_data_frame.query('poste > 0')
    del masses_cn_energie['Code']

    masses_cn_energie.rename(
        columns = {
            target_year: 'conso_CN_{}'.format(target_year),
            },
        inplace = True,
        )


    masses_cn_energie.set_index('poste', inplace = True)

    return masses_cn_energie * 1e6


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
        masses['conso_CN_{}'.format(data_year)] / masses['conso_bdf{}'.format(data_year)]
        ).to_dict()


def get_inflators_cn_to_cn(target_year):
    '''
        Calcule l'inflateur de vieillissement à partir des masses de comptabilité nationale.
    '''
    data_year = find_nearest_inferior(data_years, target_year)
    data_year_cn_aggregates = get_cn_aggregates(data_year)['conso_CN_{}'.format(data_year)].to_dict()
    target_year_cn_aggregates = get_cn_aggregates(target_year)['conso_CN_{}'.format(target_year)].to_dict()

    return dict(
        (key, target_year_cn_aggregates[key] / data_year_cn_aggregates[key])
        for key in data_year_cn_aggregates.keys()
        )



def get_inflators_energy(dataframe, year_calage = None, year_data = None):
    for year_calage in range(2000, 2015):

        assert year_data is not None
        if year_calage is None:
            year_calage = year_data

        default_config_files_directory = os.path.join(
            pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
        parametres_fiscalite_file_path = os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'legislation',
            'Parametres fiscalite indirecte.xls'
            )

        dataframe = get_input_data_frame(year_data)

        masses_cn_data_frame = pandas.read_excel(parametres_fiscalite_file_path, sheetname = "consommation_CN")
        if year_data != year_calage:
            masses_cn_data_frame = masses_cn_data_frame.loc[:, ['Code', year_data, year_calage]].copy()
        else:
            masses_cn_data_frame = masses_cn_data_frame.loc[:, ['Code', year_data]].copy()

        masses_cn_poste_coicop_722 = int(
            masses_cn_data_frame[year_calage][masses_cn_data_frame['Code'] == '            07.2.2' | \
                masses_cn_data_frame['Code'] == '            04.5.1'| \
                masses_cn_data_frame['Code'] == '            04.5.2'].values
            )
        masses_bdf_poste_coicop_722 = (dataframe['poste_coicop_722'] * dataframe['pondmen']).sum() / 1e6
        masses_cn_poste_coicop_451 = int(
            masses_cn_data_frame[year_calage][masses_cn_data_frame['Code'] == '            04.5.1'].values
            )
        masses_bdf_poste_coicop_451 = (dataframe['poste_coicop_451'] * dataframe['pondmen']).sum() / 1e6
        masses_cn_poste_coicop_452 = int(
            masses_cn_data_frame[year_calage][masses_cn_data_frame['Code'] == '            04.5.2'].values
            )
        masses_bdf_poste_coicop_452 = (dataframe['poste_coicop_452'] * dataframe['pondmen']).sum() / 1e6

        ratio_poste_coicop_722 = masses_cn_poste_coicop_722 / masses_bdf_poste_coicop_722
        ratio_poste_coicop_451 = masses_cn_poste_coicop_451 / masses_bdf_poste_coicop_451
        ratio_poste_coicop_452 = masses_cn_poste_coicop_452 / masses_bdf_poste_coicop_452

        ratio_by_variable = dict()
        ratio_by_variable['poste_coicop_722'] = ratio_poste_coicop_722
        ratio_by_variable['poste_coicop_451'] = ratio_poste_coicop_451
        ratio_by_variable['poste_coicop_452'] = ratio_poste_coicop_452


    return dataframe_calee
