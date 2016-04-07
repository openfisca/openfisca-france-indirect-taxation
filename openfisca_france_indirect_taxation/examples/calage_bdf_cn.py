#! /usr/bin/env python
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Ce script comprend plusieurs fonctions, dont le but est de caler les données Budget des Familles sur des agrégats.
# L'agrégation des données BdF rendant des totaux différents de ceux de la comptabilité nationale, ces calages sont
# importants pour restaurer les bonnes quantités. Plusieurs méthodes sont proposées.

# Import de modules généraux
from __future__ import division

import logging
import os
import pkg_resources

import pandas
from pandas import concat

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.build_survey_data.utils import ident_men_dtype


log = logging.getLogger(__name__)


def calage_viellissement_depenses(year_data, year_calage, depenses, masses):
    depenses_calees = pandas.DataFrame()
    coicop_list = set(poste_coicop for poste_coicop in depenses.columns if poste_coicop[:5] == 'poste')
    for column in coicop_list:
        coicop = column.replace('poste_coicop_', '')
        if coicop[:1] != '1' and coicop[:1] != '9':
            grosposte = int(coicop[:1])
        else:
            if len(coicop) == 3:
                grosposte = int(coicop[:1])
            elif len(coicop) == 5:
                grosposte = int(coicop[:2])
            elif coicop in ['1151', '1181', '1411', '9122', '9151', '9211', '9341']:
                grosposte = int(coicop[:1])
            elif coicop[:2] == '99' or coicop[:2] == '13':
                grosposte = 99
            else:
                grosposte = int(coicop[:2])
        # RAPPEL : 12 postes CN et COICOP
        #    01 Produits alimentaires et boissons non alcoolisées
        #    02 Boissons alcoolisées et tabac
        #    03 Articles d'habillement et chaussures
        #    04 Logement, eau, gaz, électricité et autres combustibles
        #    05 Meubles, articles de ménage et entretien courant de l'habitation
        #    06 Santé
        #    07 Transports
        #    08 Communication
        #    09 Loisir et culture
        #    10 Education
        #    11 Hotels, cafés, restaurants
        #    12 Biens et services divers
        if grosposte != 99:
            grosposte = 'coicop12_{}'.format(grosposte)
            ratio_bdf_cn = masses.at[grosposte, 'ratio_bdf{}_cn{}'.format(year_data, year_data)]
            ratio_cn_cn = masses.at[grosposte, 'ratio_cn{}_cn{}'.format(year_data, year_calage)]
            depenses_calees[column] = depenses[column] * ratio_bdf_cn * ratio_cn_cn
            log.info(u'''
Pour le grosposte {}, le ratio de calage de la base bdf {} sur la cn est {},
le ratio de calage sur la cn pour l\'annee {} est {}'''.format(
                grosposte, year_data, ratio_bdf_cn, year_calage, ratio_cn_cn))
    return depenses_calees


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

#    On ne garde que les 12 postes sur lesquels on cale:
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


def build_depenses_calees(depenses, year_calage, year_data):
    # Masses de calage provenant de la comptabilité nationale
    masses_cn_12postes_data_frame = get_cn_data_frames(year_data = year_data, year_calage = year_calage)
    # Enquête agrégée au niveau des gros postes de COICOP (12)
    df_bdf_weighted_sum_by_grosposte = get_bdf_data_frames(depenses = depenses, year_data = year_data)

    # Calcul des ratios de calage :
    masses = calcul_ratios_calage(
        year_data,
        year_calage,
        data_bdf = df_bdf_weighted_sum_by_grosposte,
        data_cn = masses_cn_12postes_data_frame
        )

    # Application des ratios de calage
    depenses.index = depenses.index.astype(ident_men_dtype)
    assert depenses.index.dtype == 'object', "depenses index is not an object"
    depenses_calees = calage_viellissement_depenses(year_data, year_calage, depenses, masses)

    return depenses_calees


def build_revenus_cales(revenus, year_calage, year_data):
    # Masses de calage provenant de la comptabilité nationale
    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    parametres_fiscalite_file_path = os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'legislation',
        'Parametres fiscalite indirecte.xls',
        )

    masses_cn_revenus_data_frame = pandas.read_excel(parametres_fiscalite_file_path, sheetname = "revenus_CN")

    masses_cn_revenus_data_frame.rename(
        columns = {
            'annee': 'year',
            'Revenu disponible brut': 'rev_disponible_cn',
            'Loyers imputes': 'loyer_imput_cn'
            },
        inplace = True
        )

    masses_cn_revenus_data_frame = masses_cn_revenus_data_frame[masses_cn_revenus_data_frame.year == year_calage]

    revenus = revenus[['pondmen'] + ['loyer_impute'] + ['rev_disponible'] + ['rev_disp_loyerimput']]
    weighted_sum_revenus = (revenus.pondmen * revenus.rev_disponible).sum()

    revenus.loyer_impute = revenus.loyer_impute.astype(float)
    weighted_sum_loyer_impute = (revenus.pondmen * revenus.loyer_impute).sum()

    rev_disponible_cn = masses_cn_revenus_data_frame.rev_disponible_cn.sum()
    loyer_imput_cn = masses_cn_revenus_data_frame.loyer_imput_cn.sum()

    revenus_cales = revenus.copy()

    # Calcul des ratios de calage :
    revenus_cales['ratio_revenus'] = (rev_disponible_cn * 1e9 - loyer_imput_cn * 1e9) / weighted_sum_revenus
    revenus_cales['ratio_loyer_impute'] = loyer_imput_cn * 1e9 / weighted_sum_loyer_impute

    # Application des ratios de calage
    revenus_cales.rev_disponible = revenus.rev_disponible * revenus_cales['ratio_revenus']
    revenus_cales.loyer_impute = revenus_cales.loyer_impute * revenus_cales['ratio_loyer_impute']
    revenus_cales.rev_disp_loyerimput = revenus_cales.rev_disponible + revenus_cales.loyer_impute

    return revenus_cales


def build_df_calee_on_grospostes(dataframe, year_calage = None, year_data = None):
    assert year_data is not None
    if year_calage is None:
        year_calage = year_data
    depenses_calees = build_depenses_calees(dataframe, year_calage, year_data)
    revenus_cales = build_revenus_cales(dataframe, year_calage, year_data)
    var_list = [variable for variable in dataframe.columns if variable[:5] != 'poste' and variable != 'loyer_impute' and
        variable != 'rev_disponible' and variable != 'rev_disp_loyerimput' and variable != 'pondmen']
    autres_variables = dataframe[var_list]
    dataframe_calee = concat([depenses_calees, revenus_cales, autres_variables], axis = 1)

    return dataframe_calee


def build_df_calee_on_ticpe(dataframe, year_calage = None, year_data = None):
    assert year_data is not None
    if year_calage is None:
        year_calage = year_data
    dataframe_calee = build_df_calee_on_grospostes(dataframe, year_calage, year_data)

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

    masses_ticpe_cn = int(
        masses_cn_12postes_data_frame[year_calage][masses_cn_12postes_data_frame['Code'] == '            07.2.2'].values
        )
    masses_ticpe_bdf = (dataframe['poste_coicop_07_2_2_1_1'] * dataframe['pondmen']).sum() / 1e6
    ratio_ticpe = masses_ticpe_cn / masses_ticpe_bdf
    dataframe['poste_coicop_07_2_2_1_1'] = dataframe['poste_coicop_07_2_2_1_1'] * ratio_ticpe
    dataframe_calee['poste_coicop_07_2_2_1_1'] = dataframe['poste_coicop_07_2_2_1_1']

    return dataframe_calee
