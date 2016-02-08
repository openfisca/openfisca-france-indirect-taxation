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


def build_nomenclature(level):
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


for index in range(len(sub_levels)-1):
    level = sub_levels[index]
    next_level = sub_levels[index + 1]
    on = sub_levels[:index + 1]
    if index == 0:
        nomenclature_coicop = pd.merge(build_nomenclature(level), build_nomenclature(next_level), on = on,
            left_index = False, right_index = False)
    else:
        nomenclature_coicop = pd.merge(nomenclature_coicop, build_nomenclature(next_level), on = on)


nomenclature_coicop = nomenclature_coicop[['code_coicop'] + ['label_division'] + ['label_groupe'] +
    ['label_classe'] + ['label_sous_classe'] + ['label_poste'] + ['divisions'] + ['groupes'] + ['classes'] +
    ['sous_classes'] + ['postes']].copy()


nomenclature_coicop.to_csv(
    os.path.join(legislation_directory, 'nomenclature_coicop.csv'),
    sep = ';',
    )

# On fait correspondre à chaque bien sa catégorie fiscale
nomenclature_coicop['categorie_fiscale'] = 0
nomenclature_coicop.loc[nomenclature_coicop['divisions'] == 1, 'categorie_fiscale'] = 2  # see exceptions
nomenclature_coicop.loc[nomenclature_coicop['divisions'] == 3, 'categorie_fiscale'] = 3
nomenclature_coicop.loc[nomenclature_coicop['divisions'] == 5, 'categorie_fiscale'] = 3  # see exceptions...

parametres_fiscalite_file_path = os.path.join(legislation_directory, 'coicop_to_categorie_fiscale.csv')
parametres_fiscalite_data_frame = pd.read_csv(
    parametres_fiscalite_file_path,
    sep = ';',
    converters = {'posteCOICOP': str}
    )
parametres_fiscalite_data_frame['posteCOICOP'] = parametres_fiscalite_data_frame['posteCOICOP'].astype(str)
parametres_fiscalite_data_frame['divisions'] = parametres_fiscalite_data_frame['posteCOICOP'].str[:1].copy()
