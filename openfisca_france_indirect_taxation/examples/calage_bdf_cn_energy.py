# -*- coding: utf-8 -*-

from __future__ import division

import os
import pkg_resources
import csv

import pandas
from pandas import concat

from openfisca_france_indirect_taxation.examples.utils_example import get_input_data_frame
from openfisca_france_indirect_taxation.build_survey_data.utils import find_nearest_inferior


data_years = [2000, 2005, 2011]


def get_bdf_aggregates_energy(data_year = None):
    assert data_year is not None

    depenses = get_input_data_frame(data_year)
    
    # Construct depenses_tot for total consumption
    liste_variables = depenses.columns.tolist()
    postes_agreges = ['poste_{}'.format(index) for index in
        ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12"]]
    depenses['depenses_tot'] = 0
    for element in liste_variables:
        for poste in postes_agreges:
            if element[:8] == poste:
                depenses['depenses_tot'] += depenses[element]

    depenses_energie = pandas.DataFrame()
    variables_energie = ['poste_04_5_1_1_1_a', 'poste_04_5_1_1_1_b', 'poste_04_5_2_1_1',
        'poste_04_5_3_1_1', 'poste_04_5_4_1_1', 'poste_07_2_2_1_1',
        'rev_disponible', 'loyer_impute', 'rev_disp_loyerimput', 'depenses_tot']
    for energie in variables_energie:
        if depenses_energie is None:
            depenses_energie = depenses['{}'.format(energie)]
        else:
            depenses_energie = concat([depenses_energie, depenses['{}'.format(energie)]], axis = 1)

    depenses_energie = concat([depenses_energie, depenses['pondmen']], axis = 1)

    depenses_energie['factures_jointes_electricite_gaz'] = \
        (depenses_energie['poste_04_5_1_1_1_b'] * depenses_energie['poste_04_5_2_1_1']) > 0
    depenses_energie['depenses_electricite_factures_jointes'] = (
        depenses_energie.query('factures_jointes_electricite_gaz == 1')['poste_04_5_1_1_1_b'].mean() /
        (depenses_energie.query('factures_jointes_electricite_gaz == 1')['poste_04_5_1_1_1_b'].mean() +
        depenses_energie.query('factures_jointes_electricite_gaz == 1')['poste_04_5_2_1_1'].mean())
        ) * depenses_energie['poste_04_5_1_1_1_a']
    depenses_energie['depenses_electricite'] = (
        depenses_energie['poste_04_5_1_1_1_b'] + depenses_energie['depenses_electricite_factures_jointes']
        )

    depenses_energie['depenses_gaz_ville'] = (
        depenses_energie['poste_04_5_2_1_1'] +
        depenses_energie['poste_04_5_1_1_1_a'] -
        depenses_energie['depenses_electricite_factures_jointes']
        )

    depenses_energie.rename(
        columns = {
            'poste_04_5_3_1_1': 'depenses_combustibles_liquides',
            'poste_04_5_4_1_1': 'depenses_combustibles_solides',
            'poste_07_2_2_1_1': 'depenses_carburants'
            },
        inplace = True
        )

    variables_to_inflate = ['depenses_carburants', 'depenses_combustibles_liquides',
        'depenses_combustibles_solides', 'depenses_electricite','depenses_gaz_ville',
        'depenses_tot', 'loyer_impute', 'rev_disponible', 'rev_disp_loyerimput']
    
    bdf_aggregates_by_energie = pandas.DataFrame()
    for energie in variables_to_inflate:
        bdf_aggregates_by_energie.loc[energie, 'bdf_aggregates'] = (
            depenses_energie[energie] * depenses_energie['pondmen']
            ).sum()

    return bdf_aggregates_by_energie


def get_cn_aggregates_energy(target_year = None):
    assert target_year is not None
    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    parametres_fiscalite_file_path = os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'legislation',
        'conso-eff-fonction.xls'
        )

    masses_cn_data_frame = pandas.read_excel(parametres_fiscalite_file_path, sheetname = u"M€cour")
    masses_cn_data_frame.columns = masses_cn_data_frame.iloc[2]
    masses_cn_data_frame = masses_cn_data_frame.loc[:, ['Code', target_year]].copy()

    masses_cn_data_frame['poste'] = '0'
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            04.5.1', 'poste'] = 'depenses_electricite'
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            04.5.2', 'poste'] = 'depenses_gaz_ville'
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            04.5.3', 'poste'] = 'depenses_combustibles_liquides'
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            04.5.4', 'poste'] = 'depenses_combustibles_solides'
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == '            07.2.2', 'poste'] = 'depenses_carburants'
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == u'01..12+15 (HS)', 'poste'] = \
        'depenses_tot'
    masses_cn_energie = masses_cn_data_frame[masses_cn_data_frame.poste != '0']
    del masses_cn_energie['Code']

    masses_cn_energie.rename(
        columns = {
            target_year: 'conso_CN_{}'.format(target_year),
            },
        inplace = True,
        )

    masses_cn_energie.set_index('poste', inplace = True)
    masses_cn_energie = masses_cn_energie * 1e6

    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    parametres_fiscalite_file_path = os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'legislation',
        'Parametres fiscalite indirecte.xls'
        )


    masses_cn_revenus_data_frame = pandas.read_excel(parametres_fiscalite_file_path, sheetname = "revenus_CN")
    masses_cn_revenus_data_frame.rename(
        columns = {
            'annee': 'year',
            'Revenu disponible brut': 'rev_disponible',
            'Loyers imputes': 'loyer_impute'
            },
        inplace = True
        )
    masses_cn_revenus_data_frame = masses_cn_revenus_data_frame[masses_cn_revenus_data_frame.year == target_year]
    revenus_cn = masses_cn_revenus_data_frame[['loyer_impute'] + ['rev_disponible']].copy()
    # On redéfinie le revenu disponible de la compta nat en enlevant le loyer imputé pour faire concorder la définition
    # avec BdF.
    revenus_cn['rev_disp_loyerimput'] = revenus_cn['rev_disponible'].copy()
    revenus_cn['rev_disponible'] = revenus_cn['rev_disponible'] - revenus_cn['loyer_impute']
    revenus_cn = pandas.melt(revenus_cn)
    revenus_cn = revenus_cn.set_index('variable')
    revenus_cn.rename(columns = {'value': 'conso_CN_{}'.format(target_year)}, inplace = True)
    revenus_cn = revenus_cn * 1e9

    masses_cn = pandas.concat([masses_cn_energie, revenus_cn])

    return masses_cn


def get_inflators_bdf_to_cn_energy(data_year):
    '''
    Calcule les ratios de calage (bdf sur cn pour année de données)
    à partir des masses de comptabilité nationale et des masses de consommation de bdf.
    '''
    data_cn = get_cn_aggregates_energy(data_year)
    data_bdf = get_bdf_aggregates_energy(data_year)
    masses = data_cn.merge(
        data_bdf, left_index = True, right_index = True
        )
    masses.rename(columns = {'bdf_aggregates': 'conso_BDF_{}'.format(data_year)}, inplace = True)
    return (
        masses['conso_CN_{}'.format(data_year)] / masses['conso_BDF_{}'.format(data_year)]
        ).to_dict()


def get_inflators_cn_to_cn_energy(target_year):
    '''
        Calcule l'inflateur de vieillissement à partir des masses de comptabilité nationale.
    '''
    data_year = find_nearest_inferior(data_years, target_year)
    data_year_cn_aggregates = get_cn_aggregates_energy(data_year)['conso_CN_{}'.format(data_year)].to_dict()
    target_year_cn_aggregates = get_cn_aggregates_energy(target_year)['conso_CN_{}'.format(target_year)].to_dict()

    return dict(
        (key, target_year_cn_aggregates[key] / data_year_cn_aggregates[key])
        for key in data_year_cn_aggregates.keys()
        )


def get_inflators_energy(target_year):
    '''
    Fonction qui calcule les ratios de calage (bdf sur cn pour année de données) et de vieillissement
    à partir des masses de comptabilité nationale et des masses de consommation de bdf.
    '''
    data_year = find_nearest_inferior(data_years, target_year)
    inflators_bdf_to_cn = get_inflators_bdf_to_cn_energy(data_year)
    inflators_cn_to_cn = get_inflators_cn_to_cn_energy(target_year)

    ratio_by_variable = dict()
    for key in inflators_cn_to_cn.keys():
        ratio_by_variable[key] = inflators_bdf_to_cn[key] * inflators_cn_to_cn[key]
    ratio_by_variable['depenses_gaz_liquefie'] = ratio_by_variable['depenses_gaz_ville']

    return ratio_by_variable


def get_inflators_by_year_energy(rebuild = False):
    assets_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
        )
    if rebuild is not False:
        inflators_by_year = dict()
        for target_year in range(2000, 2015):
            inflators = get_inflators_energy(target_year)
            inflators_by_year[target_year] = inflators

        writer_inflators = csv.writer(open(os.path.join(assets_directory, 'openfisca_france_indirect_taxation',
            'assets', 'inflateurs', 'inflators_by_year_wip.csv'), 'wb'))
        for year in range(2000, 2015):
            for key, value in inflators_by_year[year].items():
                writer_inflators.writerow([key, value, year])

        return inflators_by_year

    else:
        re_build_inflators = dict()
        inflators_from_csv = pandas.DataFrame.from_csv(os.path.join(assets_directory,
            'openfisca_france_indirect_taxation', 'assets', 'inflateurs', 'inflators_by_year_wip.csv'),
            header = -1)
        for year in range(2000, 2015):
            inflators_from_csv_by_year = inflators_from_csv[inflators_from_csv[2] == year]
            inflators_to_dict = pandas.DataFrame.to_dict(inflators_from_csv_by_year)
            inflators = inflators_to_dict[1]
            re_build_inflators[year] = inflators

        return re_build_inflators
