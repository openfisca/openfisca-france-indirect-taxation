# -*- coding: utf-8 -*-


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
divisions = ['0{}'.format(i) for i in range(1, 10)] + ['11', '12']  # TODO: fix this
taxe_by_categorie_fiscale_number = {
    0: '',
    1: 'tva_taux_super_reduit',
    2: 'tva_taux_reduit',
    3: 'tva_taux_plein',
    4: 'tva_taux_intermediaire',
    7: 'cigarettes',
    8: 'cigares',
    9: 'tabac_a_rouler',
    10: 'alcools_forts',
    11: 'tva_taux_plein',
    12: 'vin',
    13: 'biere',
    14: 'ticpe',
    15: 'assurance_transport',
    16: 'assurance_sante',
    17: 'autres_assurances'
    }


def build_coicop_level_nomenclature(level, keep_code = False, to_csv = False):
    assert level in sub_levels
    data_frame = pd.read_csv(
        os.path.join(legislation_directory, 'nomenclature_coicop_source_by_{}.csv'.format(level)),
        sep = ';',
        header = -1,
        )
    data_frame.reset_index(inplace = True)
    data_frame.rename(columns = {0: 'code_coicop', 1: 'label_{}'.format(level[:-1])}, inplace = True)
    data_frame = data_frame.ix[2:].copy()

    # Problème dû au fichier Excel, nous devons changer le contenu d'une case:
    if level == 'sous_classes':
        data_frame.loc[data_frame['code_coicop'] == "01.1.4.4", 'code_coicop'] = "'01.1.4.4"

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

    if keep_code or level == 'postes':
        data_frame['code_coicop'] = data_frame['code_coicop'].str[1:].copy()
    else:
        del data_frame['code_coicop']

    data_frame.reset_index(inplace = True, drop = True)
    if to_csv:
        data_frame.to_csv(
            os.path.join(legislation_directory, 'nomenclature_coicop_by_{}.csv'.format(level)),
            )

    return data_frame


def build_raw_coicop_nomenclature():
    for index in range(len(sub_levels) - 1):
        level = sub_levels[index]
        next_level = sub_levels[index + 1]
        on = sub_levels[:index + 1]
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

    return coicop_nomenclature[['label_division', 'label_groupe', 'label_classe',
       'label_sous_classe', 'label_poste', 'code_coicop']].copy()


def build_complete_coicop_nomenclature(to_csv = True):
    coicop_nomenclature = build_raw_coicop_nomenclature()

    items = [
        ("Cigares et cigarillos", "02.2.1"),
        ("Cigarettes", "02.2.2"),
        ("Tabac sous d'autres formes et produits connexes", "02.2.3"),
        ("Stupéfiants ", "02.3"),
        ]

    for label_poste, code_coicop in items:
        label_division = "Boissons alcoolisées et tabac"
        label_groupe = "Tabac"
        label_classe = label_sous_classe = label_poste
        data = dict(
            label_division = [label_division],
            label_groupe = [label_groupe],
            label_classe = [label_classe],
            label_sous_classe = [label_sous_classe],
            label_poste = [label_poste],
            code_coicop = [code_coicop],
            )
        coicop_nomenclature = coicop_nomenclature.append(
            pd.DataFrame.from_dict(data, dtype = 'str'),
            ignore_index = True
            )
        coicop_nomenclature.sort_values("code_coicop", inplace = True)

    if to_csv:
        coicop_nomenclature.to_csv(
            os.path.join(legislation_directory, 'nomenclature_coicop.csv'),
            )

    return coicop_nomenclature[['label_division', 'label_groupe', 'label_classe',
       'label_sous_classe', 'label_poste', 'code_coicop']].copy()


if __name__ == "__main__":
    # sys.exit(main())
    coicop_nomenclature = build_complete_coicop_nomenclature()
    coicop_nomenclature.dtypes
