# -*- coding: utf-8 -*-


import itertools
import logging
import numpy as np
import os
import pandas


try:
    from openfisca_survey_manager.survey_collections import SurveyCollection
    from openfisca_survey_manager import default_config_files_directory as config_files_directory
    from openfisca_survey_manager.statshelpers import mark_weighted_percentiles, weighted_quantiles
except ImportError:
    SurveyCollection, config_files_directory, mark_weighted_percentiles, weighted_quantiles = None, None, None, None

from openfisca_france_indirect_taxation.utils import assets_directory, get_input_data_frame
from openfisca_france_indirect_taxation.scripts.build_coicop_bdf import bdf


log = logging.getLogger(__name__)


assets_path = os.path.join(
    assets_directory,
    'aliss',
    )


def build_clean_aliss_data_frame():
    year = 2011
    aliss_survey_collection = SurveyCollection.load(
        collection = 'aliss', config_files_directory = config_files_directory
        )
    survey = aliss_survey_collection.get_survey('aliss_{}'.format(year))
    aliss = survey.get_values(table = 'Base_ALISS_2011')

    assert (
        aliss.columns.tolist()
        == [
            'type', 'nomF', 'nomK', 'nomC', 'Qt_c', 'Dt_c', 'Qm_c', 'Dm_c', 'pm_c',
            'Tpoids', 'Qt_k', 'Dt_k', 'Qm_k', 'Dm_k', 'pm_k', 'Qt_f', 'Dt_f',
            'Qm_f', 'Dm_f', 'pm_f', 'nomCOICOP', 'SomTpoids', 'DT_k', 'D_a'
            ]
        )
    assert (aliss['DT_k'] == aliss['DT_k'].unique()[0]).all(), 'DT_k is not a unique total number'

    # Lower case all variables but DT_k which is translated to 'Dt_k'
    aliss.columns = list(map(str.lower, aliss.columns[:-2])) + ['Dt_k', 'd_a']
    log.info('These columns contains nans {}'.format(
        aliss.columns[aliss.isnull().any()].tolist()
        ))
    aliss.dropna(inplace = True)
    assert aliss.notnull().all().all()
    # Renaming categories
    aliss['age'] = 99
    aliss['revenus'] = 99
    triplets = [
        ('1 : Jeune/Aisé', 0, 3),
        ('2 : Jeune/MoyenSup', 0, 2),
        ('3 : Jeune/MoyenInf', 0, 1),
        ('4 : Jeune/Modeste', 0, 0),
        ('5 : Age Moyen/Aisé', 1, 3),
        ('6 : Age Moyen/MoyenSup', 1, 2),
        ('7 : Age Moyen/MoyenInf', 1, 1),
        ('8 : Age Moyen/Modeste', 1, 0),
        ('9 : Age Sup/Aisé', 2, 3),
        ('10 : Age Sup/MoyenSup', 2, 2),
        ('11 : Age Sup/MoyenInf', 2, 1),
        ('12 : Age Sup/Modeste', 2, 0),
        ('13 : Vieux/Aisé', 3, 3),
        ('14 : Vieux/MoyenSup', 3, 2),
        ('15 : Vieux/MoyenInf', 3, 1),
        ('16 : Vieux/Modeste', 3, 0),
        ]
    for household_type, age, revenus in triplets:
        selection = aliss.type.str.startswith(household_type)
        aliss.loc[selection, 'age'] = age
        aliss.loc[selection, 'revenus'] = revenus

    assert aliss.age.isin(list(range(4))).all()
    assert aliss.revenus.isin(list(range(4))).all()
    del aliss['type']
    assert aliss.notnull().all().all()

    aliss.replace(
        {
            'nomk': {
                '11471 : \x8cufs ': '11471 : Œufs ',
                '11262 : b\x9cuf pané': '11262 : bœuf pané'
                },
            },
        inplace = True,
        )
    return aliss


def add_poste_coicop(aliss):
    year = 2011
    aliss = aliss.copy()
    aliss['poste_bdf'] = 'c0' + aliss.nomc.str[:4]
    coicop_poste_bdf = bdf(year = year)[['code_bdf', 'code_coicop']].copy()
    assert not set(aliss.poste_bdf).difference(set(coicop_poste_bdf.code_bdf))
    coicop_poste_bdf['formatted_poste'] = 'poste_' + coicop_poste_bdf.code_coicop.str.replace('.', '_')
    formatted_poste_by_poste_bdf = coicop_poste_bdf.dropna().set_index('code_bdf').to_dict()['formatted_poste']
    aliss['poste_coicop'] = aliss.poste_bdf.copy()
    aliss.replace(to_replace = dict(poste_coicop = formatted_poste_by_poste_bdf), inplace = True)
    return aliss


def complete_input_data_frame(input_data_frame, drop_dom = True):
    if drop_dom:
        input_data_frame = input_data_frame.query('zeat != 0').copy()

    input_data_frame.eval(
        'age = 0 + (agepr > 30) + (agepr > 45) + (agepr > 60)',
        inplace = True,  # Remove comment for pandas 0.18
        )

    input_data_frame['revenus_kantar'] = (
        input_data_frame.rev_disponible.astype('float') / input_data_frame.ocde10_old.astype('float')
        )
    labels = np.arange(0, 20)
    input_data_frame['vingtile'], values = weighted_quantiles(input_data_frame.revenus_kantar.astype('float'), labels,
        input_data_frame.pondmen.astype('float'), return_quantiles = True)

    input_data_frame['revenus'] = (
        0
        + (input_data_frame.revenus_kantar >= values[3 - 1]).astype('int')
        + (input_data_frame.revenus_kantar >= values[11 - 1]).astype('int')
        + (input_data_frame.revenus_kantar >= values[17 - 1]).astype('int')
        )

    assert input_data_frame.revenus.isin([0, 1, 2, 3]).all()
    assert input_data_frame.age.isin([0, 1, 2, 3]).all()
    assert input_data_frame.age.notnull().all()
    return input_data_frame


def build_aggregated_shares(expenditures, kantar_prefix = 'kantar'):
    expenditures = expenditures.copy()
    grouped_kantar_expenditures = expenditures.groupby(['age', 'revenus', 'poste_coicop']).agg({
        '{}_expenditures'.format(kantar_prefix): np.sum,
        '{}_budget_share'.format(kantar_prefix): np.sum
        }).rename(columns = {
            '{}_expenditures'.format(kantar_prefix): '{}_aggregated_expenditures'.format(kantar_prefix),
            '{}_budget_share'.format(kantar_prefix): '{}_aggregated_budget_share'.format(kantar_prefix)
            })

    expenditures = expenditures.set_index(
        ['age', 'revenus', 'poste_coicop']
        ).combine_first(
            grouped_kantar_expenditures
            ).reset_index()

    if (expenditures.kantar_aggregated_expenditures == 0).sum() > 0:
        expenditures.loc[
            expenditures.kantar_aggregated_expenditures == 0,
            '{}_aggregated_expenditures'.format(kantar_prefix)
            ] = (
                expenditures.loc[expenditures.kantar_aggregated_expenditures == 0, 'bdf_expenditures']
                )
        expenditures.loc[
            expenditures.kantar_aggregated_expenditures == 0,
            '{}_aggregated_budget_share'.format(kantar_prefix)
            ] = (
                expenditures.loc[expenditures.kantar_aggregated_expenditures == 0, 'bdf_budget_share']
                )
    # TODO should renomalize
    if kantar_prefix == 'kantar':
        expenditures['{}_to_bdf'.format(kantar_prefix)] = (
            expenditures.bdf_expenditures / expenditures.kantar_aggregated_expenditures
            )
        expenditures['{}_budget_share_to_bdf'.format(kantar_prefix)] = (
            expenditures.bdf_budget_share / expenditures.kantar_aggregated_budget_share
            )

    return expenditures


def compute_population_shares(drop_dom = True, display_plot = False):
    aliss = build_clean_aliss_data_frame()
    kept_variables = ['age', 'tpoids', 'revenus']
    aliss = aliss[kept_variables].copy()
    aliss_population_shares = aliss.groupby(
        ['age', 'revenus']).apply(
            lambda df: (df.tpoids).sum()
            ).reset_index()
    aliss_population_shares.rename(columns = {0: 'aliss_population'}, inplace = True)
    aliss_population_shares['aliss_population_share'] = (
        aliss_population_shares.aliss_population / aliss_population_shares.aliss_population.sum()
        )

    year = 2011
    input_data_frame = get_input_data_frame(year)
    input_data_frame = complete_input_data_frame(input_data_frame, drop_dom = drop_dom)
    input_data_frame = input_data_frame[['age', 'pondmen', 'revenus']].copy()
    bdf_population_shares = input_data_frame.groupby(
        ['age', 'revenus']).apply(
            lambda df: (df.pondmen).sum()
            ).reset_index()
    bdf_population_shares.rename(columns = {0: 'bdf_population'}, inplace = True)
    bdf_population_shares['bdf_population_share'] = (
        bdf_population_shares.bdf_population / bdf_population_shares.bdf_population.sum()
        )

    return aliss_population_shares.merge(bdf_population_shares)


def compute_expenditures(drop_dom = True, display_plot = False):
    # aliss/kantar data
    aliss = build_clean_aliss_data_frame()
    aliss = add_poste_coicop(aliss)
    kept_variables = ['age', 'dt_c', 'dt_k', 'dt_f', 'nomk', 'nomc', 'poste_coicop', 'revenus']
    aliss = aliss[kept_variables].copy()
    aliss_expenditures = aliss.groupby(
        ['age', 'revenus', 'poste_coicop', 'nomc', 'nomk']).apply(
            lambda df: (df.dt_k).sum()
            ).reset_index()
    aliss_expenditures.rename(columns = {0: 'kantar_expenditures'}, inplace = True)

    log.info('kantar_expenditures_total:', (aliss.dt_k).sum() / 1e9)
    log.info('bdf_expenditures_total: ', (aliss.dt_c).drop_duplicates().sum() / 1e9)

    aliss_expenditures['kantar_budget_share'] = aliss_expenditures.groupby(
        ['age', 'revenus'])['kantar_expenditures'].transform(
            lambda x: x / x.sum()
            )

    # BDF data
    year = 2011
    input_data_frame = get_input_data_frame(year)
    input_data_frame = complete_input_data_frame(input_data_frame, drop_dom = drop_dom)
    kept_postes = list(aliss.poste_coicop.unique())
    input_data_frame = input_data_frame[kept_postes + ['age', 'pondmen', 'revenus']].copy()
    melted_input_data_frame = pandas.melt(input_data_frame,
        id_vars= ['age', 'pondmen', 'revenus'], value_vars = kept_postes)
    input_data_expenditures = melted_input_data_frame.groupby(
        ['age', 'revenus', 'variable']).apply(
            lambda df: (df.pondmen * df.value).sum()
            ).reset_index()
    input_data_expenditures.rename(columns = {'variable': 'poste_coicop', 0: 'bdf_expenditures'}, inplace = True)

    log.info('bdf_expenditures_total: ', input_data_expenditures.bdf_expenditures.sum() / 1e9)

    input_data_expenditures['bdf_budget_share'] = input_data_expenditures.groupby(
        ['age', 'revenus'])['bdf_expenditures'].transform(
            lambda x: x / x.sum()
            )

    expenditures = aliss_expenditures.merge(input_data_expenditures)
    expenditures = build_aggregated_shares(expenditures)

    expenditures.to_csv(os.path.join(assets_path, 'expenditures.csv'), index = False)

    if display_plot:
        plot_variables = ['bdf_budget_share', 'kantar_budget_share_to_bdf', 'kantar_aggregated_budget_share']
        expenditures[plot_variables].drop_duplicates().plot(
            x = 'bdf_budget_share', y = 'kantar_budget_share_to_bdf', kind = 'scatter', xlim = [0, .13], ylim = [0, 7],
            ).get_figure().savefig(os.path.join(assets_path, 'budget_share_ratios'))

        expenditures[plot_variables].drop_duplicates().plot(
            x = 'bdf_budget_share', y = 'kantar_aggregated_budget_share', kind = 'scatter',
            xlim = [0, .13], ylim = [0, .13],
            ).get_figure().savefig(os.path.join(assets_path, 'budget_shares'))

    return expenditures.set_index(['age', 'revenus', 'nomk'])


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
    # nomf_by_nomk = nomf_nomk.set_index('nomk').to_dict()['nomf']

    log.info(nomf_nomk.nomf.value_counts(dropna = False))

    nomks_by_nomf = dict(
        (nomf_by_dirty_nomf.get(nomf), nomf_nomk.query('nomf == @nomf')['nomk'].unique())
        for nomf in nomf_nomk.nomf.unique()
        )
    assert len(list(nomks_by_nomf.keys())) == 21

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

            assert len(extract.dm_f.unique()) == 1, f'Problem when extracting budget share for age = {age} and revenu = {revenus}'
            extract['budget_share_kf'] = extract.dm_k / extract.dm_f
            extract['nomf'] = nomf_by_dirty_nomf.get(nomf)

            kantar_budget_share = kantar_budget_share.append(extract)

        kantar_budget_share.fillna(0, inplace = True)  # TODO
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

    iterables = [list(range(4)), list(range(4)), nomks]
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
    log.info('{} k-kprime elasticities are not found'.format(nomk_cross_price_elasticity.isnull().sum().sum()))
    nomk_cross_price_elasticity.fillna(0, inplace = True)

    nomk_cross_price_elasticity.to_csv(kantar_cross_price_elasticities_path)
    return nomk_cross_price_elasticity


def compute_expenditures_coefficient(reform_key = None):
    from openfisca_france_indirect_taxation.reforms.aliss import build_aliss_reform

    assert reform_key in ['sante', 'environnement', 'tva_sociale', 'mixte', 'ajustable']
    aliss_uncomplete = build_clean_aliss_data_frame()
    aliss = add_poste_coicop(aliss_uncomplete)
    aliss_extract = aliss[['nomf', 'nomk', 'poste_bdf', 'poste_coicop']].copy()
    aliss_extract.drop_duplicates(inplace = True)

    legislation_directory = os.path.join(
        assets_directory,
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
    if reform_key == 'ajustable':
        aliss_reform = build_aliss_reform(ajustable = True)
    else:
        aliss_reform = build_aliss_reform()

    columns = ['nomf', 'nomc', 'code_bdf', 'categorie_fiscale'] + [reform_key]  # TODO remove nomc
    reform_extract = aliss_reform[columns].copy()
    reform_extract.rename(columns = {reform_key: 'reform_categorie_fiscale'}, inplace = True)

    # TODO gérér les catégories fiscales
    correction = correction.merge(
        reform_extract[['nomf', 'reform_categorie_fiscale']].drop_duplicates().copy(), on = 'nomf', how = 'outer')

    taux_by_categorie_fiscale = {
        'tva_taux_super_reduit': .021,
        'tva_taux_reduit': .055,
        'tva_taux_intermediaire': .1,
        'tva_taux_plein': .2,
        }

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

    iterables = [list(range(4)), list(range(4)), sorted(correction.nomk.unique())]
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
            'Problem at age={} and revenus={}\n {}, {}'.format(
                age, revenus, len(matrix.index.tolist()), len(correction.nomk))
        assert matrix.shape == (nomk_len, nomk_len)
        expense_factor = (
            (1 + correction.taux_reforme) / (1 + correction.taux) * (1 + np.dot(matrix, correction.elasticity_factor))
            )
        assert len(expense_factor) == nomk_len
        tweeked_expense_factor = (
            (1 + np.dot(matrix, correction.elasticity_factor))
            )
        correction['expenditure_variation'] = expense_factor
        correction['tweeked_expenditure_variation'] = tweeked_expense_factor
        correction['inelastic_expenditure_variation'] = (1 + correction.taux_reforme) / (1 + correction.taux)

        final_corrections = final_corrections.combine_first(correction.set_index(['age', 'revenus', 'nomk']))

    return final_corrections[[
        'expenditure_variation', 'tweeked_expenditure_variation', 'inelastic_expenditure_variation', 'taux',
        'taux_reforme'
        ]].copy()


def compute_adjusted_expenditures(reform_key = None):
    correction = compute_expenditures_coefficient(reform_key = reform_key)
    expenditures = compute_expenditures(drop_dom = True)
    adjusted_expenditures = expenditures.combine_first(correction)
    adjusted_expenditures['adjusted_kantar_expenditures'] = (
        adjusted_expenditures.kantar_expenditures * adjusted_expenditures.tweeked_expenditure_variation
        )
    adjusted_expenditures['adjusted_kantar_budget_share'] = (
        adjusted_expenditures.kantar_budget_share * adjusted_expenditures.tweeked_expenditure_variation
        )
    #    adjusted_expenditures['adjusted_kantar_budget_share'] = adjusted_expenditures.groupby(
    #        ['age', 'revenus'])['adjusted_kantar_budget_share'].transform(
    #            lambda x: x / x.sum()
    #            )
    adjusted_expenditures = build_aggregated_shares(
        adjusted_expenditures.reset_index(), kantar_prefix = 'adjusted_kantar'
        )
    adjusted_expenditures.reset_index(inplace = True)

    adjusted_expenditures.eval(
        'adjusted_bdf_budget_share = kantar_budget_share_to_bdf * adjusted_kantar_aggregated_budget_share',
        inplace = True
        )

    return adjusted_expenditures  # , total_expenditures_variation


def get_adjusted_input_data_frame(reform_key = None, verbose = False):
    assert reform_key is not None
    year = 2011
    input_data_frame = complete_input_data_frame(get_input_data_frame(year))
    adjusted_expenditures = compute_adjusted_expenditures(reform_key = reform_key)

    bdf_adjusted_expenditures = adjusted_expenditures[
        ['age', 'revenus', 'poste_coicop', 'adjusted_bdf_budget_share', 'bdf_budget_share']
        ].drop_duplicates().copy()
    # TODO fix upstream
    bdf_adjusted_expenditures.fillna(0, inplace = True)

    postes_coicop = bdf_adjusted_expenditures.poste_coicop.unique().copy()

    iterator = itertools.product(
        bdf_adjusted_expenditures.age.unique().copy(),
        bdf_adjusted_expenditures.revenus.unique().copy(),
        postes_coicop,
        )

    bdf_adjusted_expenditures.set_index(['age', 'revenus', 'poste_coicop'], inplace = True)

    for age, revenus, poste in iterator:
        selection = (input_data_frame.age == age) & (input_data_frame.revenus == revenus)
        if verbose:
            print(poste)
            before = (
                input_data_frame.loc[selection, poste] * input_data_frame.loc[selection, 'pondmen']
                ).sum()
            print(('before: ', before))
            print(('adjusted_bdf_budget_share', bdf_adjusted_expenditures.loc[
                (age, revenus, poste), 'adjusted_bdf_budget_share']))
            print(('bdf_budget_share', bdf_adjusted_expenditures.loc[(age, revenus, poste), 'bdf_budget_share']))

        try:
            if bdf_adjusted_expenditures.loc[(age, revenus, poste), 'bdf_budget_share'] != 0:
                input_data_frame.loc[selection, poste] = (
                    bdf_adjusted_expenditures.loc[(age, revenus, poste), 'adjusted_bdf_budget_share']
                    / bdf_adjusted_expenditures.loc[(age, revenus, poste), 'bdf_budget_share']
                    * input_data_frame.loc[selection, poste]
                    )
        except Exception:
            print((bdf_adjusted_expenditures.loc[(age, revenus, poste), 'bdf_budget_share']))
            print((bdf_adjusted_expenditures.loc[(age, revenus, poste)]))
            raise

        if verbose:
            print(('after/before: ', (
                input_data_frame.loc[selection, poste] * input_data_frame.loc[selection, 'pondmen']
                ).sum() / (before + 1) - 1
                ))
    return input_data_frame


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    input_data_frame = get_adjusted_input_data_frame(reform_key = 'tva_sociale')
#    print(input_data_frame.columns[input_data_frame.isnull().any()])

    # df = build_clean_aliss_data_frame()
