# -*- coding: utf-8 -*-


from __future__ import division

import os
import pandas as pd
import pkg_resources


legislation_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'legislation',
    )


sub_levels = ['divisions', 'groupes', 'classes', 'sous_classes', 'postes']


def build_coicop_level_nomenclature(level):
    assert level in sub_levels
    data_frame = pd.DataFrame.from_csv(
        os.path.join(legislation_directory, 'nomenclature_coicop_source_by_{}.csv'.format(level)),
        sep = ';',
        header = -1,
        )
    data_frame.reset_index(inplace = True)
    data_frame.rename(columns = {0: 'code_coicop', 1: 'label_{}'.format(level[:-1])}, inplace = True)
    data_frame = data_frame.ix[2:].copy()

    # Problème dû au fichier Excel, nous devons changer le contenu d'une case:
    if level == 'sous_classes':
        data_frame.loc[data_frame['code_coicop'] == '01.1.4.4', 'code_coicop'] = "'01.1.4.4"

    index, stop = 1, False
    for sub_level in sub_levels:
        if stop:
            continue
        if sub_level == 'divisions':
            data_frame[sub_level] = data_frame['code_coicop'].str[index:index + 2].astype(int)
            index = index + 3
        else:
            data_frame[sub_level] = data_frame['code_coicop'].str[index:index + 1].astype(int)
            index = index + 2

        if level == sub_level:
            stop = True

    if level == 'postes':
        data_frame['code_coicop'] = data_frame['code_coicop'].str[1:].copy()
    else:
        del data_frame['code_coicop']

    data_frame.reset_index(inplace = True, drop = True)
    data_frame.to_csv(
        os.path.join(legislation_directory, 'nomenclature_coicop_by_{}.csv'.format(level)),
        sep = ';',
        )

    return data_frame


def build_coicop_nomenclature():
    for index in range(len(sub_levels) - 1):
        level = sub_levels[index]
        next_level = sub_levels[index + 1]
        on = sub_levels[:index + 1]
        print index, level, next_level
        if index == 0:
            coicop_nomenclature = pd.merge(
                build_coicop_level_nomenclature(level), build_coicop_level_nomenclature(next_level),
                on = on, left_index = False, right_index = False)
        else:
            coicop_nomenclature = pd.merge(coicop_nomenclature, build_coicop_level_nomenclature(next_level), on = on)

    coicop_nomenclature = coicop_nomenclature[
        ['code_coicop'] +
        ['label_{}'.format(sub_level[:-1]) for sub_level in sub_levels] +
        sub_levels
        ].copy()

    coicop_nomenclature.to_csv(
        os.path.join(legislation_directory, 'nomenclature_coicop.csv'),
        sep = ';',
        )
    return coicop_nomenclature


def get_dominant_and_exceptions(division):
    assert division in ['0{}'.format(i) for i in range(1, 10)] + [11, 12]  # TODO: fix this
    parametres_fiscalite_file_path = os.path.join(legislation_directory, 'coicop_to_categorie_fiscale.csv')
    parametres_fiscalite_data_frame = pd.read_csv(
        parametres_fiscalite_file_path,
        sep = ';',
        converters = {'posteCOICOP': str}
        )
    parametres_fiscalite_data_frame['division'] = parametres_fiscalite_data_frame['posteCOICOP'].str[:2].copy()

    division_dataframe = parametres_fiscalite_data_frame.query('division == @division')
    dominant_fiscal_category = division_dataframe.categoriefiscale.value_counts().argmax()
    exceptions_dataframe = division_dataframe.query('categoriefiscale != @dominant_fiscal_category')

    return dict(dominant_fiscal_category = dominant_fiscal_category, exceptions_dataframe = exceptions_dataframe)

# TODO:
# - Get the correct poste coicop usinf desciption and nomenclature coicop
# - Format exceptions as year_min, year_max, value. Should use http://stackoverflow.com/questions/26121668/slice-pandas-dataframe-in-groups-of-consecutive-values
# - Deal with the postes that are not in nomenclature coicop (see TODO in get_domiant_and_exceptions)
# - Try to find the legislative reference for the changes in fiscal category of products

