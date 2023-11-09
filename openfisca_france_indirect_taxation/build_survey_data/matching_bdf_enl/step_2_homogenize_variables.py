# -*- coding: utf-8 -*-

# Dans ce script les variables qui ont des différences de définition sont reconstruites
# sur le modèle de l'enquête BdF (ou ENL dans certains cas où la nomenclature ENL a plus de sens)
# de manière à avoir des définitions identiques.
# Les noms de variables sont aussi alignés.

import numpy as np

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_1_build_dataframes import \
    load_data_bdf_enl
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy


def inflate_energy_consumption(data_enl, data_bdf):
    inflators = get_inflators_by_year_energy()  # Inflate BdF to year of the ENL, 2013
    inflators_bdf = inflators[2013]
    inflators_enl = dict()
    inflators_bdf['depenses_gaz_liquefie'] = inflators_bdf['depenses_gaz_ville']
    for energie in ['depenses_electricite', 'depenses_gaz_ville', 'depenses_gaz_liquefie',
            'depenses_combustibles_liquides', 'depenses_combustibles_solides']:
        data_bdf[energie] = data_bdf[energie] * inflators_bdf[energie]
        inflators_enl[energie] = (
            (data_bdf.pondmen * data_bdf[energie]).sum() / data_bdf.pondmen.sum()
            ) / (
            (data_enl.pondmen * data_enl[energie]).sum() / data_bdf.pondmen.sum()
            )
        data_enl[energie] = data_enl[energie] * inflators_enl[energie]

    return data_enl, data_bdf


def homogenize_variables_definition_bdf_enl(year_data):

    enl_provisoire = False
    data_enl, data_bdf = load_data_bdf_enl(year_data)
    # Vérification que les données ENL ne contiennent pas les DOM
    assert (data_enl['dom'] == 2).any()
    del data_enl['dom']
    assert (data_bdf['zeat'] != 0).any()

    # Aides au logement : séparation propriétaire/locataire dans BdF -> création d'une unique variable
    check = data_bdf.query('aidlog1 != 0').copy()
    assert (check['aidlog2'] == 0).any()

    data_bdf['aba'] = data_bdf['aidlog1'] + data_bdf['aidlog2']
    del check

    # Montant des aides au logement : séparation propriétaire/locataire dans BdF -> création d'une unique variable
    for i in [1, 2]:
        data_bdf['mall{}'.format(i)] = data_bdf['mall{}'.format(i)].fillna(0)
        check = data_bdf.query('aidlog{} != 1'.format(i)).copy()
        assert (check['mall{}'.format(i)] == 0).any()

    data_bdf['amr'] = data_bdf['mall1'] + data_bdf['mall2']

    del data_bdf['aidlog1'], data_bdf['aidlog2'], data_bdf['mall1'], data_bdf['mall2'], check

    # Définition du statut du logement
    data_enl['stalog'] = 0
    data_enl.loc[data_enl.soc == 0, 'stalog'] = 1
    data_enl.loc[data_enl.soc == 1, 'stalog'] = 2
    data_enl.loc[data_enl.soc == 2, 'stalog'] = 3
    data_enl.loc[data_enl.soc == 3, 'stalog'] = 4

    # Les définitions du ménage dans BdF et ENL sont différentes :
    # on exclut les catégories absentes de BdF (logements-foyers pour personnes âgées
    # et chambre d'hôtels)
    for i in [4, 6]:
        data_enl = data_enl.query('htl != {}'.format(i)).copy()

    # Changement nomenclature variable année de construction du batiment:
    # ENL 2006 et ENL 2013 provisoire
    # iaat annee d'achevement de la construction
    # 1  Avant 1871
    # 2  De 1871 à 1914
    # 3  De 1915 à 1948
    # 4  De 1949 à 1961
    # 5  De 1962 à 1967
    # 6  De 1968 à 1974
    # 7  De 1975 à 1981
    # 8  De 1982 à 1989
    # 9  De 1990 à 1998
    # 10 En 1999 ou après

    # ENL 2013 définitive
    # iaatr
    # 1 Avant 1949
    # 2 De 1949 à 1974
    # 3 De 1975 à 1981
    # 4 De 1982 à 1989
    # 5 De 1990 à 1998
    # 6 1999 ou après

    # BDF 2011
    # ancons année d'achèvement de l'immeuble
    # 1 En 1948 ou avant
    # 2 De 1949 à 1961
    # 3 De 1962 à 1967
    # 4 De 1968 à 1974
    # 5 De 1975 à 1981
    # 6 De 1982 à 1989
    # 7 De 1990 à 1998
    # 8 De 1999 à 2003
    # 9 En 2004 et après
    # 10 En construction
    if enl_provisoire:
        data_enl['ancons'] = 0
        data_enl.loc[data_enl.iaat < 4, 'ancons'] = 1
        data_enl.loc[data_enl.iaat == 4, 'ancons'] = 2
        data_enl.loc[data_enl.iaat == 5, 'ancons'] = 3
        data_enl.loc[data_enl.iaat == 6, 'ancons'] = 4
        data_enl.loc[data_enl.iaat == 7, 'ancons'] = 5
        data_enl.loc[data_enl.iaat == 8, 'ancons'] = 6
        data_enl.loc[data_enl.iaat == 9, 'ancons'] = 7
        # Pour après 1998 on affecte aléatoirement 8 ou 9 (99-03 ou 03-et après)
        data_enl.loc[data_enl.iaat == 10, 'ancons'] = np.random.choice(np.array([8, 9]))
    else:
        data_enl['ancons'] = 0
        data_enl.loc[data_enl.iaatr == 1, 'ancons'] = 1
        data_enl.loc[data_enl.iaatr == 2, 'ancons'] = 2  # TODO ,3,4
        data_enl.loc[data_enl.iaatr == 3, 'ancons'] = 5
        data_enl.loc[data_enl.iaatr == 4, 'ancons'] = 6
        data_enl.loc[data_enl.iaatr == 5, 'ancons'] = 7
        data_enl.loc[data_enl.iaatr == 6, 'ancons'] = 8
        data_enl.loc[(data_enl.iaatr == 6) & (data_enl.iaatcd >= 2004), 'ancons'] = 9

    # dip14pr - dans ENL les sans diplômes sont notés 0 au lieu de 71
    data_enl.loc[data_enl.ndip14 == 0, 'ndip14'] = 71

    # Situapr et Situacj vs Msitua
    data_enl['situapr'] = data_enl['msitua'].copy()
    data_enl.loc[data_enl.msitua == 8, 'situapr'] = 7
    data_enl['situacj'] = data_enl['msituac'].copy()
    data_enl.loc[data_enl.msituac == 8, 'situacj'] = 7

    del data_enl['msitua'], data_enl['msituac']

    # OCDE10 vs MUC1
    data_enl['muc1'] = data_enl['muc1'] / 10

    # Nbh1
    data_bdf['nbh1'] = data_bdf['nbh1'].fillna(0)

    # Gestion des dépenses d'énergies
    joint_data_bdf = data_bdf.query('poste_04_5_1_1_1_b > 0').query('poste_04_5_2_1_1 > 0').copy()
    part_electricite_bdf = (
        joint_data_bdf.poste_04_5_1_1_1_b.sum() / (
            joint_data_bdf.poste_04_5_1_1_1_b.sum()
            + joint_data_bdf.poste_04_5_2_1_1.sum()
            )
        )
    data_bdf['depenses_electricite'] = (
        data_bdf['poste_04_5_1_1_1_b'] + data_bdf['poste_04_5_1_1_1_a'] * part_electricite_bdf
        )
    data_bdf['depenses_gaz_ville'] = (
        data_bdf['poste_04_5_2_1_1'] + data_bdf['poste_04_5_1_1_1_a'] * (1 - part_electricite_bdf)
        )

    joint_data_enl = data_enl.query('coml11 > 0').query('coml12 > 0').copy()
    part_electricite_enl = (
        joint_data_enl['coml11'].sum()
        / (joint_data_enl['coml11'].sum() + joint_data_enl['coml12'].sum())
        )
    data_enl['depenses_electricite'] = (
        data_enl['coml11'] + data_enl['coml13'] * part_electricite_enl
        )
    data_enl['depenses_gaz_ville'] = (
        data_enl['coml12'] + data_enl['coml13'] * (1 - part_electricite_enl)
        )

    data_enl['poste_04_5_1_1_1'] = (data_enl['coml11']).copy()

    data_enl['depenses_combustibles_solides'] = (data_enl['coml41'] + data_enl['coml42']).copy()

    del data_enl['coml41'], data_enl['coml42']

    # zeat : dans BdF certains ménages ont 6 et aucun 9, alors que 6 n'existe pas
    data_bdf.loc[data_bdf.zeat == 6, 'zeat'] = 9

    # Rename
    renaming = {
        'cataeu2010': 'cataeu',
        'cceml': 'mfac_eau1_d',
        'coml': 'depenses_energies',
        'coml2': 'depenses_combustibles_liquides',
        'coml3': 'depenses_gaz_liquefie',
        'enfhod': 'nbh1',
        'gmur': 'isolation_murs',
        'gtoit2': 'isolation_toit',
        'gvit1': 'majorite_double_vitrage',
        'gvit1b': 'isolation_fenetres',
        'lchauf': 'mchof_d',
        'hnph1': 'nbphab',
        'hsh1': 'surfhab_d',
        'lmlm': 'mloy_d',
        'mag': 'agepr',
        'mcs': 'cs42pr',
        'mcsc': 'cs42cj',
        # 'mne1': 'nenfants', add back if needed
        'mpa': 'nactifs',
        'mrtota3': 'revtot',
        'muc1': 'ocde10',
        'ndip14': 'dip14pr',
        'nhab': 'npers',
        'qex': 'pondmen',
        'tau2010': 'tau',
        'tu2010': 'tuu',
        }

    assert set(renaming.keys()) < set(data_enl.columns), 'Missing {} in data_enl'.format(
        set(renaming.keys()).difference(set(data_enl.columns))
        )
    data_enl.rename(
        columns = renaming,
        inplace = True,
        )

    data_bdf.rename(
        columns = {
            'poste_04_5_2_2_1': 'depenses_gaz_liquefie',
            'poste_04_5_3_1_1': 'depenses_combustibles_liquides',
            'poste_04_5_4_1_1': 'depenses_combustibles_solides',
            },
        inplace = True,
        )

    # Pour ceux ne connaissant pas l'isolation de leurs murs (4), on impute une isolation moyenne (2)
    data_enl.loc[data_enl['isolation_murs'] == 4, 'isolation_murs'] = 2
    # Pour ceux ne connaissant pas l'isolation de leur toit (5), on impute une isolation ancienne mais suffisante (2)
    data_enl.loc[data_enl['isolation_toit'] == 5, 'isolation_murs'] = 2

    data_enl = data_enl.sort_index(axis = 1)
    data_bdf = data_bdf.sort_index(axis = 1)

    data_enl, data_bdf = inflate_energy_consumption(data_enl, data_bdf)

    return data_enl, data_bdf


def create_new_variables(year_data):
    data_enl, data_bdf = homogenize_variables_definition_bdf_enl(year_data)

    def create_new_variables_(data, option = None):
        assert option in ['enl', 'bdf']

        if option == 'bdf':
            assert 'revtot' in data

        # Dummy variable pour la consommation de fioul
        data['fioul'] = 0
        data.loc[data['depenses_combustibles_liquides'] > 0, 'fioul'] = 1

        data['gaz_ville'] = 0
        data.loc[data['depenses_gaz_ville'] > 0, 'gaz_ville'] = 1

        data['electricite'] = 0
        data.loc[data['depenses_electricite'] > 0, 'electricite'] = 1

        # Création de dummy variables pour la commune de résidence
        data['strate'] = 0
        data.loc[data['tuu'].isin([1, 2, 3]), 'strate'] = 1
        data.loc[data['tuu'].isin([4, 5, 6]), 'strate'] = 2
        data.loc[data['tuu'] == 7, 'strate'] = 3
        data.loc[data['tuu'] == 8, 'strate'] = 4

        data['rural'] = 0
        data['petite_ville'] = 0
        data['moyenne_ville'] = 0
        data['grande_ville'] = 0
        data['paris'] = 0

        data.loc[data['strate'] == 0, 'rural'] = 1
        data.loc[data['strate'] == 1, 'petite_ville'] = 1
        data.loc[data['strate'] == 2, 'moyenne_ville'] = 1
        data.loc[data['strate'] == 3, 'grande_ville'] = 1
        data.loc[data['strate'] == 4, 'paris'] = 1

        # Dummy variables pour l'ancienneté du batîment (1er norme importante sur l'isolation en 74)
        data['bat_av_49'] = 0
        data['bat_49_74'] = 0
        data['bat_ap_74'] = 0

        data.loc[data['ancons'] == 1, 'bat_av_49'] = 1
        data.loc[data['ancons'] < 5, 'bat_49_74'] = 1
        data.loc[data['ancons'] == 1, 'bat_49_74'] = 0
        data.loc[data['ancons'] > 4, 'bat_ap_74'] = 1

        # Dummy variables pour le type de logement
        data['log_indiv'] = 0
        data['log_colec'] = 1

        for j in [1, 5, 7]:
            data.loc[data['htl'] == j, 'log_indiv'] = 1
            data.loc[data['htl'] == j, 'log_colec'] = 0
        del j

        # Creation de dummy variables pour la zone climatique
        data['ouest_sud'] = 0
        data['est_nord'] = 1

        for j in [5, 7, 9]:
            data.loc[data['zeat'] == j, 'ouest_sud'] = 1
            data.loc[data['zeat'] == j, 'est_nord'] = 0
        del j

        if option == 'enl':
            data['froid'] = 0
            data.loc[data.gchauf_n != 0, 'froid'] = 1
            del data['gchauf_n']

            data['froid_installation'] = 0
            data.loc[data.gchauf_1 == 1, 'froid_installation'] = 1
            del data['gchauf_1']

            data['froid_cout'] = 0
            data.loc[data.gchauf_3 == 1, 'froid_cout'] = 1
            del data['gchauf_3']

            data['froid_isolation'] = 0
            data.loc[data.gchauf_4 == 1, 'froid_isolation'] = 1
            del data['gchauf_4']

            data['froid_impaye'] = 0
            data.loc[data.gchauf_5 == 1, 'froid_impaye'] = 1
            del data['gchauf_5']

        data['aides_logement'] = 0
        data.loc[data['aba'] == 1, 'aides_logement'] = 1

        # Création d'une variable pour la part des dépenses totales en énergies
        # On néglige l'énergie thermique de BdF car les dépenses sont absentes de l'ENL
        energie_logement = ['depenses_combustibles_liquides', 'depenses_combustibles_solides',
            'depenses_electricite', 'depenses_gaz_liquefie', 'depenses_gaz_ville']

        if option == 'bdf':
            data['depenses_energies'] = 0
            for energie in energie_logement:
                data['depenses_energies'] += data[energie]
            data['part_energies_depenses_tot'] = (
                data['depenses_energies'] / data['depenses_tot']
                )

        assert 'depenses_energies' in data
        assert 'revtot' in data

        data = data.query('revtot > 0').copy()
        data['part_energies_revtot'] = (
            data['depenses_energies'] / data['revtot']
            )
        # Suppression des outliers
        data = data.query('part_energies_revtot < 0.5').copy()

        return data

    return create_new_variables_(data_enl, option = 'enl'), create_new_variables_(data_bdf, option = 'bdf')


def create_niveau_vie_quantiles(year_data):
    data_enl, data_bdf = create_new_variables(year_data)

    def create_niveau_vie_quantiles_(data):
        data['niveau_vie'] = (data['revtot'] / data['ocde10']).copy()

        data = data.sort_values(by = ['niveau_vie'])
        data['sum_pondmen'] = data['pondmen'].cumsum()

        population_totale = data['sum_pondmen'].max()
        data['niveau_vie_decile'] = 0
        for j in range(1, 11):
            data.loc[data.sum_pondmen > population_totale * (float(j) / 10 - 0.1), 'niveau_vie_decile'] = j

        data['niveau_vie_quintile'] = 0
        for j in range(1, 6):
            data.loc[data.sum_pondmen > population_totale * (float(j) / 5 - 0.2), 'niveau_vie_quintile'] = j

        data = data.sort_index()
        del data['sum_pondmen']
        return data

    return create_niveau_vie_quantiles_(data_enl), create_niveau_vie_quantiles_(data_bdf)


if __name__ == '__main__':
    data_enl, data_bdf = create_niveau_vie_quantiles()
