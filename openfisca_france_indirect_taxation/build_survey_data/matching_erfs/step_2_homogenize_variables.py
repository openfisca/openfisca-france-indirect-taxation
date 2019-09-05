# -*- coding: utf-8 -*-

# Dans ce script les variables qui ont des différences de définition sont reconstruites
# sur le modèle de l'enquête BdF (ou ENL dans certains cas où la nomenclature ENL a plus de sens)
# de manière à avoir des définitions identiques.
# Les noms de variables sont aussi alignés.


from openfisca_france_indirect_taxation.build_survey_data.matching_erfs.step_1_build_dataframes import \
    load_data_bdf_erfs


def homogenize_definitions():
    data_erfs, data_bdf = load_data_bdf_erfs()

    data_erfs = data_erfs.query('metrodom == 1')
    del data_erfs['metrodom']

    data_erfs.loc[data_erfs.typmen7 == 6, 'typmen7'] = 5
    data_erfs.loc[data_erfs.typmen7 == 9, 'typmen7'] = 5

    data_erfs.rename(
        columns = {
            'wprm': 'pondmen',
            'ageprm': 'agepr',
            'catau2010': 'cataeu',
            'cstotprm': 'cs42pr',
            'm_rsa_actm': 'rsa_act',
            'nb_uci': 'ocde10',
            'nbactif': 'nactifs',
            'nbactop': 'nactoccup',
            'nbind': 'npers',
            'revdispm': 'rev_disponible',
            'sexeprm': '',
            'so': 'stalog',
            'tau2010': 'tau',
            'th': 'mhab_d',
            'tuu2010': 'tuu',
            'typmen7': 'typmen',
            },
        inplace = True,
        )

    data_bdf.rename(
        columns = {
            'rev502': 'rev_valeurs_mobilieres_bruts',
            },
        inplace = True,
        )

    data_erfs = data_erfs.astype(object)

    return data_erfs, data_bdf


if __name__ == "__main__":
    data_erfs, data_bdf = homogenize_definitions()
