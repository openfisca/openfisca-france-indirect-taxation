# -*- coding: utf-8 -*-

from __future__ import division


import itertools
import numpy as np
import os
import pandas
import pkg_resources

try:
    from openfisca_survey_manager.survey_collections import SurveyCollection
    from openfisca_survey_manager import default_config_files_directory as config_files_directory
    from openfisca_survey_manager.statshelpers import mark_weighted_percentiles, weighted_quantiles
except ImportError:
    SurveyCollection, config_files_directory, mark_weighted_percentiles, weighted_quantiles = None, None, None, None

from openfisca_france_indirect_taxation.utils import get_input_data_frame
from openfisca_france_indirect_taxation.scripts.build_coicop_bdf import bdf


assets_path = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'aliss',
    )


def detect_null(data_frame):
    isnull_columns = list()
    global_null = None
    for column in data_frame.columns:
        null = data_frame[column].isnull()
        if null.any():
            isnull_columns.append(column)
            global_null = (global_null | null) if global_null is not None else null
    return data_frame.loc[global_null].copy()


def build_clean_aliss_data_frame():
    year = 2011
    aliss_survey_collection = SurveyCollection.load(
        collection = 'aliss', config_files_directory = config_files_directory
        )
    survey = aliss_survey_collection.get_survey('aliss_{}'.format(year))

    aliss = survey.get_values(table = 'Base_ALISS_2011')

    errors = detect_null(aliss)
    errors.to_csv('aliss_errors.csv')

    # Removing products with missing nomf
    aliss = aliss.query('nomf != "nan"').copy()

    # Setting null nomk consumption to zéro
    aliss.fillna(
        dict(qt_k = 0, dt_k = 0, qm_k = 0, dm_k =0, pm_k = 0, qt_c = 0, dt_c = 0, qm_c = 0, dm_c = 0, pm_c = 0),
        inplace = True
        )

    aliss = aliss.loc[aliss.nomf.notnull()].copy()

    aliss['age'] = 99
    aliss['revenus'] = 99

    triplets = [
        ('1 : Jeune/Ais', 0, 3),
        ('2 : Jeune/MoyenSup', 0, 2),
        ('3 : Jeune/MoyenInf', 0, 1),
        ('4 : Jeune/Modeste', 0, 0),
        ('5 : Age Moyen/Ais', 1, 3),
        ('6 : Age Moyen/MoyenSup', 1, 2),
        ('7 : Age Moyen/MoyenInf', 1, 1),
        ('8 : Age Moyen/Modeste', 1, 0),
        ('9 : Age Sup/Ais', 2, 3),
        ('10 : Age Sup/MoyenSup', 2, 2),
        ('11 : Age Sup/MoyenInf', 2, 1),
        ('12 : Age Sup/Modeste', 2, 0),
        ('13 : Vieux/Ais', 3, 3),
        ('14 : Vieux/MoyenSup', 3, 2),
        ('15 : Vieux/MoyenInf', 3, 1),
        ('16 : Vieux/Modeste', 3, 0),
        ]

    for household_type, age, revenus in triplets:
        # print household_type, age, revenus
        selection = aliss.type.str.startswith(household_type)
        aliss.loc[selection, 'age'] = age
        aliss.loc[selection, 'revenus'] = revenus

    assert aliss.age.isin(range(4)).all()
    assert aliss.revenus.isin(range(4)).all()
    del aliss['type']

    assert aliss.notnull().all().all()

    return aliss


def add_poste_coicop(aliss):
    year = 2011
    aliss = aliss.copy()
    aliss['poste_bdf'] = 'c0' + aliss.nomc.str[:4]
    coicop_poste_bdf = bdf(year = year)[['code_bdf', 'code_coicop']].copy()
    assert not set(aliss.poste_bdf).difference(set(coicop_poste_bdf.code_bdf))
    coicop_poste_bdf['formatted_poste'] = u'poste_' + coicop_poste_bdf.code_coicop.str.replace('.', u'_')
    formatted_poste_by_poste_bdf = coicop_poste_bdf.dropna().set_index('code_bdf').to_dict()['formatted_poste']
    aliss['poste_coicop'] = aliss.poste_bdf.copy()
    aliss.replace(to_replace = dict(poste_coicop = formatted_poste_by_poste_bdf), inplace = True)
    return aliss


def compute_expenses(drop_dom = False):
    # aliss/kantar data
    aliss = build_clean_aliss_data_frame()

    print aliss.groupby('age')['tpoids'].sum() / aliss.tpoids.sum()

    aliss = add_poste_coicop(aliss)
    kept_variables = ['age', 'dt_c', 'dt_k', 'nomk', 'nomc', 'poste_coicop', 'tpoids', 'revenus']
    aliss = aliss[kept_variables].copy()
    depenses_aliss = aliss.groupby(
        ['age', 'revenus', 'poste_coicop', 'nomc', 'nomk']).apply(
            lambda df: (df.tpoids * df.dt_k).sum()
            ).reset_index()
    depenses_aliss.rename(columns = {0: "depenses_kantar"}, inplace = True)

    # BDF data
    year = 2011
    input_data_frame = get_input_data_frame(year)
    print input_data_frame.zeat.value_counts()
    if drop_dom:
        input_data_frame = input_data_frame.query('zeat != 0').copy()


    input_data_frame.eval("age = 0 + (agepr > 30) + (agepr > 45) + (agepr > 60)",
    #    inplace = True,  # Remove comment for pandas 0.18
        )
    print input_data_frame.groupby('age')['pondmen'].sum() / input_data_frame.pondmen.sum()

    input_data_frame['revenus_kantar'] = (
        input_data_frame.rev_disponible.astype('float') / input_data_frame.ocde10_old.astype('float')
    #    inplace = True,
        )
    labels = np.arange(0, 20)
    input_data_frame['vingtile'], values = weighted_quantiles(input_data_frame.revenus_kantar.astype('float'), labels,
        input_data_frame.pondmen.astype('float'), return_quantiles = True)

    print values
    input_data_frame['revenus'] = (
        0 +
        (input_data_frame.revenus_kantar >= values[3 - 1]).astype('int') +
        (input_data_frame.revenus_kantar >= values[11 - 1]).astype('int') +
        (input_data_frame.revenus_kantar >= values[17 - 1]).astype('int')
        )
    print input_data_frame.vingtile.value_counts(dropna = False)
    print input_data_frame.revenus.value_counts(dropna = False)
    print input_data_frame.groupby('revenus')['pondmen'].sum() / input_data_frame.pondmen.sum()

    assert input_data_frame.revenus.isin([0, 1, 2, 3]).all()
    assert input_data_frame.age.isin([0, 1, 2, 3]).all()
    assert input_data_frame.age.notnull().all()
    kept_postes = list(aliss.poste_coicop.unique())
    input_data_frame = input_data_frame[kept_postes + ['age', 'pondmen', 'revenus']].copy()
    melted_input_data_frame = pandas.melt(input_data_frame,
        id_vars= ['age', 'pondmen', 'revenus'], value_vars = kept_postes)
    depenses_input = melted_input_data_frame.groupby(
        ['age', 'revenus', 'variable']).apply(
            lambda df: (df.pondmen * df.value).sum()
            ).reset_index()
    depenses_input.rename(columns = {"variable": "poste_coicop", 0: "depenses_bdf"}, inplace = True)

    depenses = depenses_aliss.merge(depenses_input)

    grouped_depenses_kantar = depenses.groupby(['age', 'revenus', 'poste_coicop'])['depenses_kantar'].agg(
        {'depenses_agregees_kantar': np.sum}
        )
    depenses = depenses.set_index(
        ['age', 'revenus', 'poste_coicop']
        ).combine_first(
            grouped_depenses_kantar
            ).reset_index()
    depenses['kantar_to_bdf'] = depenses.depenses_bdf / depenses.depenses_agregees_kantar

    depenses.to_csv(os.path.join(assets_path, 'expenses.csv'), index = False)
    return depenses


def compute_kantar_elasticities(compute = False):
    aliss = build_clean_aliss_data_frame()
    kantar_cross_price_elasticities_path = os.path.join(
        assets_path,
        'kantar_cross_price_elasticities.csv',
        )

    if not compute:
        if os.path.exists(kantar_cross_price_elasticities_path):
          nomk_cross_price_elasticity = pandas.read_csv(kantar_cross_price_elasticities_path)
          return nomk_cross_price_elasticity.set_index(['age', 'revenus', 'nomk'])

    nomf_by_dirty_nomf = {
        '1 : Juices': 'Juic',
        '2 : Alcohol': 'Alc',
        '3 : Soft drinks': 'SD',
        '4 : Bottled water': 'Wat',
        '5 : Coffee and tea': 'Cof',
        '6 : Fresh fruits and vegetables': 'FFV',
        '7 : Spices': 'Spices',
        '8 : Plant-based foods high in fats': 'PBF',
        '9 : Plant-based dishes': 'PBD',
        '10 : Plant-based foods high in sugar': 'PBS',
        '11 : Starchy foods': 'Starch',
        '12 : Processed fruits and vegetables': 'PFV',
        '13 : Beef': 'Beef',
        '14 : Other meats': 'OM',
        '15 : Cooked meats': 'CM',
        '16 : Animal-based foods high in fats': 'ABF',
        '17 : Cheese': 'Cheese',
        '18 : Fish and seafoods': 'Fish',
        '19 : Dairy products': 'Dairy',
        '20 : Prepared mixed meals': 'PrepM',
        '21 : Prepared desserts': 'PrepD',
        }

    assert (aliss.nomf != 'nan').all()
    assert aliss.nomf.notnull().all()

    nomf_nomk = aliss.query('age == 0 & revenus == 0')[['nomf', 'nomk']]

    (nomf_nomk.nomk.value_counts() == 1).all()
    nomf_by_nomk = nomf_nomk.set_index('nomk').to_dict()['nomf']

    print nomf_nomk.nomf.value_counts(dropna = False)

    nomks_by_nomf = dict(
        (nomf_by_dirty_nomf.get(nomf), nomf_nomk.query('nomf == @nomf')['nomk'].unique())
        for nomf in nomf_nomk.nomf.unique()
        )
    assert len(nomks_by_nomf.keys()) == 21

    # budget shares
    budget_share_path = os.path.join(assets_path, 'budget_share.csv')
    if os.path.exists(budget_share_path) and not compute:
        kantar_budget_share = pandas.read_csv(budget_share_path)
    else:
        kantar_budget_share = pandas.DataFrame()
        for age, revenus, nomf in itertools.product(aliss.age.unique(), aliss.revenus.unique(), aliss.nomf.unique()):

            extract = aliss.query(
                'nomf == @nomf & age == @age & revenus == @revenus'
                )[
                    ['age', 'revenus', 'nomk', 'dm_k', 'dm_f']
                ]

            assert len(extract.dm_f.unique()) == 1
            extract['budget_share_kf'] = extract.dm_k / extract.dm_f
            extract['nomf'] = nomf_by_dirty_nomf.get(nomf)

            kantar_budget_share = kantar_budget_share.append(extract)

        kantar_budget_share.fillna(0, inplace = True) # TODO
        kantar_budget_share.to_csv(budget_share_path)

    assert (kantar_budget_share.nomf != 'nan').all()
    assert kantar_budget_share.notnull().all().all()

    csv_path_name = os.path.join(
        assets_path,
        'cross_price_elasticities.csv',
        )
    nomf_cross_price_elasticities = pandas.read_csv(csv_path_name)

    assert nomf_cross_price_elasticities.notnull().all().all()

    nomks = aliss.nomk.unique()

    iterables = [range(4), range(4), nomks]
    index = pandas.MultiIndex.from_product(iterables, names=['age', 'revenus', 'nomk'])
    nomk_cross_price_elasticity = pandas.DataFrame(
        index = index,
        columns = nomks,
        )

    # TODO save by age, revenus
    for age, revenus in itertools.product(aliss.age.unique(), aliss.revenus.unique()):
        temp_nomk_cross_price_elasticity = pandas.DataFrame(
            index = nomks,
            columns = list(nomks),
            )

        nomf_cross_price_elasticity = nomf_cross_price_elasticities.query(
            'age == @age & revenus == @revenus').set_index('product')
        nomf_cross_price_elasticity.drop(['age', 'revenus'], axis = 1, inplace = True)
        nomfs = nomf_cross_price_elasticity.index.unique()

        for f, fprime in itertools.product(nomfs, nomfs):
            elasticity_ffprime = nomf_cross_price_elasticity.loc[f, fprime]
            elasticity_kkprime = pandas.DataFrame(
                index = nomks_by_nomf[f],
                columns = nomks_by_nomf[fprime],
                )
            nomks_for_fprime = nomks_by_nomf[fprime]
            budget_share = kantar_budget_share.query(
                'age == @age & revenus == @revenus & nomk in @nomks_for_fprime & nomf == @fprime'
                )[['nomk', 'budget_share_kf']].set_index(('nomk'))
            assert budget_share.notnull().all().all()
            transposed_elasticity_kkprime = elasticity_kkprime.T
            transposed_elasticity_kkprime.loc[nomks_for_fprime] = budget_share * elasticity_ffprime
            assert transposed_elasticity_kkprime.notnull().all().all()

            elasticity_kkprime = transposed_elasticity_kkprime.T
            assert elasticity_kkprime.notnull().all().all(), \
                'elasticity_kkprime: age={}, revenus={}, f={}, fprime={}'.format(age, revenus, f, fprime)

            temp_nomk_cross_price_elasticity = temp_nomk_cross_price_elasticity.combine_first(elasticity_kkprime)

        temp_nomk_cross_price_elasticity['age'] = age
        temp_nomk_cross_price_elasticity['revenus'] = revenus
        temp_nomk_cross_price_elasticity.index.name = 'nomk'
        temp_nomk_cross_price_elasticity = temp_nomk_cross_price_elasticity.reset_index()
        temp_nomk_cross_price_elasticity = temp_nomk_cross_price_elasticity.set_index(['age', 'revenus', 'nomk'])
        nomk_cross_price_elasticity = nomk_cross_price_elasticity.combine_first(temp_nomk_cross_price_elasticity)

    # Some k-kprime elasticities are not found
    print "{} k-kprime elasticities are not found".format(nomk_cross_price_elasticity.isnull().sum().sum())
    nomk_cross_price_elasticity.fillna(0, inplace = True)

    nomk_cross_price_elasticity.to_csv(kantar_cross_price_elasticities_path)
    return nomk_cross_price_elasticity


def compute_expenses_coefficient(taux_reforme = None, reform = None):
    from openfisca_france_indirect_taxation.reforms.aliss import build_aliss_reform

    assert reform in ['sante', 'environnement', 'tva_sociale']
    aliss_uncomplete = build_clean_aliss_data_frame()
    aliss = add_poste_coicop(aliss_uncomplete)
    aliss_extract = aliss[['nomf', 'nomk', 'poste_bdf', 'poste_coicop']].copy()
    aliss_extract.drop_duplicates(inplace = True)
    year = 2011

    legislation_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
        'openfisca_france_indirect_taxation',
        'assets',
        'legislation',
        )
    codes_coicop_data_frame = pandas.read_csv(
        os.path.join(legislation_directory, 'coicop_legislation.csv'),
        )
    legislation = codes_coicop_data_frame[['code_bdf', 'categorie_fiscale']].copy()
    legislation.rename(columns = {'code_bdf': 'poste_bdf'}, inplace = True)
    correction = aliss_extract.merge(legislation)
    correction = correction[['nomf', 'nomk', 'poste_bdf', 'categorie_fiscale']].drop_duplicates().copy()
    # load reforms and add taux
    taux_by_categorie_fiscale = {
        'tva_taux_super_reduit': .021,
        'tva_taux_reduit': .055,
        'tva_taux_intermediaire': .1,
        'tva_taux_plein': .2,
        }

    aliss_reform = build_aliss_reform()
    columns = ['nomf', 'nomc', 'code_bdf', 'categorie_fiscale'] + [reform]
    reform_extract = aliss_reform[columns].copy()
    reform_extract.rename(columns = {reform: 'reform_categorie_fiscale'}, inplace = True)

    # TODO gérér les catégories fiscales

    correction = correction.merge(
        reform_extract[['nomf', 'reform_categorie_fiscale']].drop_duplicates().copy(), on = 'nomf', how = 'outer')

    correction['taux'] = correction.categorie_fiscale.apply(
        lambda x: taux_by_categorie_fiscale.get(x, 0))

    correction['taux_reforme'] = correction.reform_categorie_fiscale.apply(
        lambda x: taux_by_categorie_fiscale.get(x))

    correction.loc[correction.reform_categorie_fiscale.isnull(), 'taux_reforme'] = \
        correction.loc[correction.reform_categorie_fiscale.isnull(), 'taux'].values
    correction['elasticity_factor'] = (correction.taux_reforme - correction.taux) / (1 + correction.taux)

    kantar_elasticities_indexed = compute_kantar_elasticities(compute = False)
    kantar_elasticities = kantar_elasticities_indexed.reset_index(['age', 'revenus'])
    assert sorted(kantar_elasticities.age.value_counts(dropna = False).index) == sorted(range(4))
    assert sorted(kantar_elasticities.revenus.value_counts(dropna = False).index) == sorted(range(4))
    assert kantar_elasticities.age.notnull().all()
    assert kantar_elasticities.revenus.notnull().all()

    iterables = [range(4), range(4), sorted(correction.nomk.unique())]
    index = pandas.MultiIndex.from_product(iterables, names=['age', 'revenus', 'nomk'])
    final_corrections = pandas.DataFrame(
        index = index,
        columns = sorted(correction.nomk.unique()),
        )

    nomk_len = len(correction.nomk)
    for age, revenus in itertools.product(kantar_elasticities.age.unique(), kantar_elasticities.revenus.unique()):
        correction['age'] = age
        correction['revenus'] = revenus
        matrix = kantar_elasticities.query('age == @age & revenus == @revenus').drop(['age', 'revenus'], axis =1)
        matrix.fillna(0, inplace = True)
        assert sorted(matrix.index.tolist()) == sorted(correction.nomk), \
            "Problem at age={} and revenus={}\n {}, {}".format(
                age, revenus, len(matrix.index.tolist()), len(correction.nomk))
        assert matrix.shape == (nomk_len, nomk_len)
        expense_factor = (
            (1 + correction.taux_reforme) / (1 + correction.taux) * (1 + np.dot(matrix, correction.elasticity_factor))
            )
        assert len(expense_factor) == nomk_len
        correction['expense_factor'] = expense_factor
        correction['inelastic_expense_factor'] = (1 + correction.taux_reforme) / (1 + correction.taux)

        final_corrections = final_corrections.combine_first(correction.set_index(['age', 'revenus', 'nomk']))

    return final_corrections.reset_index()


if __name__ == '__main__':
    # correction = compute_expenses_coefficient(reform = 'tva_sociale')
    depenses = compute_expenses(drop_dom = True)
