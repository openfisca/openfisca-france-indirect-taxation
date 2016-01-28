# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 14:17:46 2015

@author: thomas.douenne
"""

from __future__ import division

import logging
import os
import pkg_resources

import pandas
from pandas import concat

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.build_survey_data.utils import ident_men_dtype


log = logging.getLogger(__name__)


def get_bdf_data_frames(depenses, year_data = None):
    assert year_data is not None
    '''
    Récupère les dépenses de budget des familles et les agrège par poste
    (en tenant compte des poids respectifs des ménages)
    '''
    depenses_by_grosposte = pandas.DataFrame()
    for grosposte in range(1, 13):
        if depenses_by_grosposte is None:
            depenses_by_grosposte = depenses['coicop12_{}'.format(grosposte)]
        else:
            depenses_by_grosposte = concat([depenses_by_grosposte, depenses['coicop12_{}'.format(grosposte)]], axis = 1)
    depenses_by_grosposte = concat([depenses_by_grosposte, depenses['pondmen']], axis = 1)
    grospostes_list = set(depenses_by_grosposte.columns)
    grospostes_list.remove('pondmen')

    dict_bdf_weighted_sum_by_grosposte = {}
    for grosposte in grospostes_list:
        depenses_by_grosposte['{}pond'.format(grosposte)] = (
            depenses_by_grosposte[grosposte] * depenses_by_grosposte['pondmen']
            )
        dict_bdf_weighted_sum_by_grosposte[grosposte] = depenses_by_grosposte['{}pond'.format(grosposte)].sum()
    df_bdf_weighted_sum_by_grosposte = pandas.DataFrame(
        pandas.Series(
            data = dict_bdf_weighted_sum_by_grosposte,
            index = dict_bdf_weighted_sum_by_grosposte.keys()
            )
        )
    return df_bdf_weighted_sum_by_grosposte


def get_cn_data_frames(year_data = None, year_calage = None):
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

    masses_cn_data_frame = pandas.read_excel(parametres_fiscalite_file_path, sheetname = "consommation_CN")
    if year_data != year_calage:
        masses_cn_12postes_data_frame = masses_cn_data_frame.loc[:, ['Code', year_data, year_calage]]
    else:
        masses_cn_12postes_data_frame = masses_cn_data_frame.loc[:, ['Code', year_data]]

    masses_cn_12postes_data_frame['code_unicode'] = masses_cn_12postes_data_frame.Code.astype(unicode)
    masses_cn_12postes_data_frame['len_code'] = masses_cn_12postes_data_frame['code_unicode'].apply(lambda x: len(x))

    # On ne garde que les 12 postes sur lesquels on cale:
    masses_cn_12postes_data_frame = masses_cn_12postes_data_frame[masses_cn_12postes_data_frame['len_code'] == 6]
    masses_cn_12postes_data_frame['code'] = masses_cn_12postes_data_frame.Code.astype(int)
    masses_cn_12postes_data_frame = masses_cn_12postes_data_frame.drop(['len_code', 'code_unicode', 'Code'], 1)
    if year_calage != year_data:
        masses_cn_12postes_data_frame.rename(
            columns = {
                year_data: 'consoCN_COICOP_{}'.format(year_data),
                year_calage: 'consoCN_COICOP_{}'.format(year_calage),
                'code': 'poste'
                },
            inplace = True,
            )
    else:
        masses_cn_12postes_data_frame.rename(
            columns = {
                year_data: 'consoCN_COICOP_{}'.format(year_data),
                'code': 'poste'
                },
            inplace = True,
            )
    masses_cn_12postes_data_frame['poste'] = masses_cn_12postes_data_frame['poste'].astype(str)
    for element in masses_cn_12postes_data_frame['poste']:
        masses_cn_12postes_data_frame['poste'] = \
            masses_cn_12postes_data_frame['poste'].replace(element, 'coicop12_{}'.format(element))
    masses_cn_12postes_data_frame.set_index('poste', inplace = True)
    return masses_cn_12postes_data_frame


def calcul_ratios_calage(year_data, year_calage, data_bdf, data_cn):
    '''
    Fonction qui calcule les ratios de calage (bdf sur cn pour année de données) et de vieillissement
    à partir des masses de comptabilité nationale et des masses de consommation de bdf.
    '''
    masses = data_cn.merge(
        data_bdf, left_index = True, right_index = True
        )
    masses.rename(columns = {0: 'conso_bdf{}'.format(year_data)}, inplace = True)
    if year_calage != year_data:
        masses['ratio_cn{}_cn{}'.format(year_data, year_calage)] = (
            masses['consoCN_COICOP_{}'.format(year_calage)] / masses['consoCN_COICOP_{}'.format(year_data)]
            )
    if year_calage == year_data:
        masses['ratio_cn{}_cn{}'.format(year_data, year_calage)] = 1

    masses['ratio_bdf{}_cn{}'.format(year_data, year_data)] = (
        1e6 * masses['consoCN_COICOP_{}'.format(year_data)] / masses['conso_bdf{}'.format(year_data)]
        )

    return masses


def build_dict_ratios_calage():
    ratios = None
    for year in [2000, 2005, 2011]:
        # Masses de calage provenant de la comptabilité nationale
        masses_cn_12postes_data_frame = get_cn_data_frames(year_data = year, year_calage = year)
        # Enquête agrégée au niveau des gros postes de COICOP (12)
        df_bdf_weighted_sum_by_grosposte = get_bdf_data_frames(depenses = depenses, year_data = year)

        # Calcul des ratios de calage :
        masses = calcul_ratios_calage(
            year,
            year,
            data_bdf = df_bdf_weighted_sum_by_grosposte,
            data_cn = masses_cn_12postes_data_frame
            )
        ratios_bdf_cn = masses['ratio_bdf{}_cn{}'.format(year, year)]
        if ratios is None:
            ratios = ratios_bdf_cn
        else:
            ratios = pandas.concat([ratios, ratios_bdf_cn], axis = 1)

    return ratios


targets_by_year = dict()
inflators_by_year = dict()
inflators_vieillissement_by_year = dict()
for year in [2000, 2005, 2011]:
    # Masses de calage provenant de la comptabilité nationale
    masses_cn_12postes_data_frame = get_cn_data_frames(year_data = year, year_calage = year)
    # Enquête agrégée au niveau des gros postes de COICOP (12)
    df_bdf_weighted_sum_by_grosposte = get_bdf_data_frames(depenses = depenses, year_data = year)
    masses = calcul_ratios_calage(
        year,
        year,
        data_bdf = df_bdf_weighted_sum_by_grosposte,
        data_cn = masses_cn_12postes_data_frame
        )
    inflator_by_variable = masses['ratio_bdf{}_cn{}'.format(year, year)].to_dict()
    inflators_by_year['for_{}'.format(year)] = inflator_by_variable

    target = get_cn_data_frames(year, year) * 1e6
    target_by_variable = target['consoCN_COICOP_{}'.format(year)].to_dict()
    del target_by_variable['coicop12_15']
    targets_by_year['for_{}'.format(year)] = target_by_variable


for year in range(2000, 2005):
    # Masses de calage provenant de la comptabilité nationale
    masses_cn_12postes_data_frame = get_cn_data_frames(year_data = 2000, year_calage = year)
    # Enquête agrégée au niveau des gros postes de COICOP (12)
    df_bdf_weighted_sum_by_grosposte = get_bdf_data_frames(depenses = depenses, year_data = 2000)
    masses = calcul_ratios_calage(
        2000,
        year,
        data_bdf = df_bdf_weighted_sum_by_grosposte,
        data_cn = masses_cn_12postes_data_frame
        )
    inflator_vieillissement = masses['ratio_cn{}_cn{}'.format(2000, year)].to_dict()
    inflators_vieillissement_by_year['from_2000_to_{}'.format(year)] = inflator_vieillissement

for year in range(2005, 2011):
    # Masses de calage provenant de la comptabilité nationale
    masses_cn_12postes_data_frame = get_cn_data_frames(year_data = 2005, year_calage = year)
    # Enquête agrégée au niveau des gros postes de COICOP (12)
    df_bdf_weighted_sum_by_grosposte = get_bdf_data_frames(depenses = depenses, year_data = 2005)
    masses = calcul_ratios_calage(
        2005,
        year,
        data_bdf = df_bdf_weighted_sum_by_grosposte,
        data_cn = masses_cn_12postes_data_frame
        )
    inflator_vieillissement = masses['ratio_cn{}_cn{}'.format(2005, year)].to_dict()
    inflators_vieillissement_by_year['from_2005_to_{}'.format(year)] = inflator_vieillissement


for year in range(2011, 2015):
    # Masses de calage provenant de la comptabilité nationale
    masses_cn_12postes_data_frame = get_cn_data_frames(year_data = 2011, year_calage = year)
    # Enquête agrégée au niveau des gros postes de COICOP (12)
    df_bdf_weighted_sum_by_grosposte = get_bdf_data_frames(depenses = depenses, year_data = 2011)
    masses = calcul_ratios_calage(
        2011,
        year,
        data_bdf = df_bdf_weighted_sum_by_grosposte,
        data_cn = masses_cn_12postes_data_frame
        )
    inflator_vieillissement = masses['ratio_cn{}_cn{}'.format(2011, year)].to_dict()
    inflators_vieillissement_by_year['from_2011_to_{}'.format(year)] = inflator_vieillissement
