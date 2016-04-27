# -*- coding: utf-8 -*-

from __future__ import division


import numpy as np
import os
import pandas as pd
import pkg_resources


from openfisca_core import reforms

from openfisca_france_indirect_taxation.model.base import get_legislation_data_frames

from openfisca_france_indirect_taxation.model.consommation.postes_coicop import generate_postes_agreges_variables
from openfisca_france_indirect_taxation.model.consommation.categories_fiscales import generate_variables
from openfisca_france_indirect_taxation.build_survey_data.calibration_aliss import (
    add_poste_coicop,
    build_clean_aliss_data_frame,
    )


aliss_assets_reform_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'reforms',
    'aliss_assets',
    )


def build_aliss_reform(rebuild = False):
    aliss_reform_path = os.path.join(aliss_assets_reform_directory, 'aliss_reform.csv')
    if os.path.exists(aliss_reform_path) and rebuild is False:
        aliss_reform = pd.read_csv(aliss_reform_path)
        return aliss_reform

    aliss_reform_data = pd.read_csv(os.path.join(aliss_assets_reform_directory, 'aliss_reform_unprocessed_data.csv'))
    aliss_uncomplete = build_clean_aliss_data_frame()
    aliss = add_poste_coicop(aliss_uncomplete)
    aliss_extract = aliss[['nomf', 'nomc', 'poste_bdf']].copy()
    aliss_extract.drop_duplicates(inplace = True)
    legislation_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
        'openfisca_france_indirect_taxation',
        'assets',
        'legislation',
        )
    codes_coicop_data_frame = pd.read_csv(
        os.path.join(legislation_directory, 'coicop_legislation.csv'),
        )
    legislation = codes_coicop_data_frame[['code_bdf', 'categorie_fiscale']].copy()
    legislation.rename(columns = {'code_bdf': 'poste_bdf'}, inplace = True)
    aliss_legislation = aliss_extract.merge(legislation)
    aliss_legislation.rename(columns = {'poste_bdf': 'code_bdf'}, inplace = True)
    aliss_reform = aliss_legislation.merge(aliss_reform_data)

    # Dealing with mismatch in reforms
    reforms = ['sante', 'environnement', 'tva_sociale', 'mixte']
    for reform in reforms:
        labels = [removed_reform for removed_reform in reforms if removed_reform != reform]
        print labels
        mismatch = aliss_reform.drop(
            labels,
            axis = 1,
            ).groupby(['code_bdf']).filter(
                lambda x: x[reform].nunique() > 1,
                ).sort_values('code_bdf')

        mismatch.nomc = mismatch.nomc.str.decode('latin-1').str.encode('utf-8')
        mismatch.to_csv(
            os.path.join(aliss_assets_reform_directory, '{}_reform_mismatch.csv'.format(reform)),
            index = False,
            )

    if rebuild:
        aliss_reform.to_csv(aliss_reform_path, index = False)

    return aliss_reform


def build_reform_environnement(tax_benefit_system):
    key = 'aliss_environnement'
    name = u"Réforme Aliss-Environnement de l'imposition indirecte des biens alimentaires"
    return build_custom_aliss_reform(tax_benefit_system, key = key, name = name)


def build_reform_sante(tax_benefit_system):
    key = 'aliss_sante'
    name = u"Réforme Aliss-Santé de l'imposition indirecte des biens alimentaires"
    return build_custom_aliss_reform(tax_benefit_system, key = key, name = name)


def build_reform_tva_sociale(tax_benefit_system):
    key = 'aliss_tva_sociale'
    name = u"Réforme Aliss-TVA sociale de l'imposition indirecte des biens alimentaires"
    return build_custom_aliss_reform(tax_benefit_system, key = key, name = name)


def build_custom_aliss_reform(tax_benefit_system = None, key = None, name = None):
    assert key is not None
    assert tax_benefit_system is not None
    Reform = reforms.make_reform(
        key = key,
        name = name,
        reference = tax_benefit_system,
        )
    reform_key = key[6:]
    aliss_reform = build_aliss_reform()
    categories_fiscales_reform = aliss_reform[[reform_key, 'code_bdf']].drop_duplicates().copy()
    reform_mismatch = categories_fiscales_reform.groupby(['code_bdf']).filter(
        lambda x: x[reform_key].nunique() > 1).copy().sort_values('code_bdf')

    categories_fiscales_reform[reform_key].unique()
    if not reform_mismatch.empty:
        categories_fiscales_reform[reform_key] = categories_fiscales_reform[reform_key].astype(
            'category',
            categories = ['tva_taux_reduit', 'tva_taux_intermediaire', 'tva_taux_plein'],
            ordered = True,
            )
        # Keeping higher rate
        categories_fiscales_reform = categories_fiscales_reform.sort_values(['code_bdf', reform_key]).drop_duplicates(
            subset = 'code_bdf', keep = 'last')
        assert not categories_fiscales_reform.code_bdf.duplicated().any()
        categories_fiscales_reform[reform_key] = categories_fiscales_reform[reform_key].astype(str)

    categories_fiscales_reform.rename(columns=({reform_key: 'categorie_fiscale'}), inplace = True)
    year = 2014
    categories_fiscales_data_frame, _ = get_legislation_data_frames()
    categories_fiscales = categories_fiscales_data_frame.query('start <= @year & @year <= stop').copy()

    assert not categories_fiscales.empty
    assert not categories_fiscales.code_bdf.duplicated().any()

    categories_fiscales_reform = categories_fiscales_reform.loc[
        categories_fiscales_reform.code_bdf.str[:3] == 'c01'].copy()

    assert not (categories_fiscales_reform.code_bdf == 'c02131').any()

    codes_bdf_by_reform_categorie_fiscale = dict(
        (
            categorie_fiscale,
            categories_fiscales_reform.query('categorie_fiscale == @categorie_fiscale')['code_bdf'].unique().tolist()
            )
        for categorie_fiscale in categories_fiscales_reform.categorie_fiscale.unique()
        )

    for categorie_fiscale, codes_bdf in codes_bdf_by_reform_categorie_fiscale.iteritems():
        categories_fiscales.loc[
            categories_fiscales.code_bdf.isin(codes_bdf), 'categorie_fiscale'] = categorie_fiscale

    assert not categories_fiscales.code_bdf.duplicated().any(), "there are {} duplicated entries".format(
        categories_fiscales.code_bdf.duplicated().sum())

    generate_variables(
        categories_fiscales = categories_fiscales,
        Reform = Reform,
        tax_benefit_system = tax_benefit_system,
        )
    generate_postes_agreges_variables(
        categories_fiscales = categories_fiscales,
        Reform = Reform,
        tax_benefit_system = tax_benefit_system,
        )
    reform = Reform()
    return reform



def build_budget_shares():
    aliss = build_clean_aliss_data_frame()
    aliss = add_poste_coicop(aliss)
    kept_variables = ['dt_k', 'nomf', 'nomc', 'poste_coicop', 'tpoids']
    aliss = aliss[kept_variables].copy()
    aliss_expenditures = aliss.groupby(
        ['poste_coicop', 'nomc', 'nomf']).apply(
            lambda df: (df.tpoids * df.dt_k).sum()
            ).reset_index()
    aliss_expenditures.rename(columns = {0: "expenditures"}, inplace = True)

    aliss_expenditures['budget_share'] = aliss_expenditures.groupby(
        ['poste_coicop'])['expenditures'].transform(
            lambda x: x / x.sum()
            )
    return aliss_expenditures.query('budget_share < 1').copy()


def build_legislation_including_f_nomencalture():
    aliss_uncomplete = build_clean_aliss_data_frame()
    aliss = add_poste_coicop(aliss_uncomplete)
    aliss_extract = aliss[['nomf', 'nomk', 'poste_bdf', 'poste_coicop']].copy()
    aliss_extract.drop_duplicates(inplace = True)

    legislation_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
        'openfisca_france_indirect_taxation',
        'assets',
        'legislation',
        )
    codes_coicop_data_frame = pd.read_csv(
        os.path.join(legislation_directory, 'coicop_legislation.csv'),
        )
    legislation = codes_coicop_data_frame[['code_bdf', 'categorie_fiscale']].copy()
    legislation.rename(columns = {'code_bdf': 'poste_bdf'}, inplace = True)
    return aliss_extract.merge(legislation)


if __name__ == '__main__':

    reform_key = 'mixte'
    mismatch = pd.read_csv(os.path.join(
        aliss_assets_reform_directory,
        '{}_reform_mismatch.csv'.format(reform_key)
        ))
    mismatch['nomc_shrinked'] = mismatch.nomc.str[:4].copy()
    mismatch.drop('nomc', axis = 1, inplace = True)
    budget_shares = build_budget_shares()
    budget_shares['nomc_shrinked'] = budget_shares.nomc.str[:4].copy()

    taux_by_categorie_fiscale = {
        'tva_taux_super_reduit': .021,
        'tva_taux_reduit': .055,
        'tva_taux_intermediaire': .1,
        'tva_taux_plein': .2,
        }

    result = mismatch.merge(budget_shares)

    result['reform_rate'] = result[reform_key].map(taux_by_categorie_fiscale)
    weighted_mean = lambda x: np.average(x, weights = result.loc[x.index, "budget_share"])

    reform_rate = result.groupby(['code_bdf', 'poste_coicop'])['reform_rate'].agg(
        weighted_mean).reset_index()
    result2 = result.drop('reform_rate', axis = 1).merge(reform_rate)
    result2[reform_key] = "tva_taux_" + result2.poste_coicop.str[6:]

    taux_by_categorie_fiscale_update = result2[
        [reform_key, 'reform_rate']
        ].set_index(reform_key).to_dict()['reform_rate']
    taux_by_categorie_fiscale.update(taux_by_categorie_fiscale_update)

    aliss_reform = build_aliss_reform(rebuild = True)
    columns = ['nomf', 'nomc', 'code_bdf', 'categorie_fiscale'] + [reform_key]
    reform_extract = aliss_reform[columns].copy()


    reform_extract.set_index(['nomf', 'nomc'], inplace = True)
    reform_extract.update(result2.set_index(['nomf', 'nomc']))
    reform_extract.reset_index(inplace = True)
    reform_extract.rename(columns = {reform_key: 'reform_categorie_fiscale', 'code_bdf': 'poste_bdf'}, inplace = True)

    # TODO gérér les catégories fiscales

    correction =  build_legislation_including_f_nomencalture()

    correction = correction[['nomf', 'nomk', 'poste_bdf', 'categorie_fiscale']].drop_duplicates().copy()

    # Compute taux
    correction = correction.merge(
        reform_extract[['poste_bdf', 'reform_categorie_fiscale']].drop_duplicates().copy(), on = 'poste_bdf', how = 'outer')


    correction['taux'] = correction.categorie_fiscale.apply(
        lambda x: taux_by_categorie_fiscale.get(x, 0))

    correction['taux_reforme'] = correction.reform_categorie_fiscale.apply(
        lambda x: taux_by_categorie_fiscale.get(x))

