import logging
import numpy as np
import os
import pandas as pd

from openfisca_core.reforms import Reform

from openfisca_france_indirect_taxation.location import openfisca_france_indirect_taxation_location
from openfisca_france_indirect_taxation.yearly_variable import YearlyVariable
from openfisca_france_indirect_taxation.variables.base import get_legislation_data_frames, Menage
from openfisca_france_indirect_taxation.utils import assets_directory
from openfisca_france_indirect_taxation.variables.consommation.postes_coicop import generate_postes_agreges_variables
from openfisca_france_indirect_taxation.variables.consommation.categories_fiscales import generate_depenses_ht_categories_fiscales_variables
from openfisca_france_indirect_taxation.build_survey_data.calibration_aliss import (
    add_poste_coicop,
    build_clean_aliss_data_frame,
    )


log = logging.getLogger(__name__)


aliss_assets_reform_directory = os.path.join(
    openfisca_france_indirect_taxation_location,
    'openfisca_france_indirect_taxation',
    'reforms',
    'aliss_assets',
    )

legislation_directory = os.path.join(
    assets_directory,
    'legislation',
    )


def build_aliss_reform(rebuild = False, ajustable = False):
    aliss_reform_path = os.path.join(aliss_assets_reform_directory, 'aliss_reform.csv')

    if os.path.exists(aliss_reform_path) and rebuild is False and ajustable is False:
        aliss_reform = pd.read_csv(aliss_reform_path)
        return aliss_reform

    if ajustable is True:
        aliss_reform_data = pd.read_csv(os.path.join(
            aliss_assets_reform_directory, 'ajustable_aliss_reform_unprocessed_data.csv'))
        reforms = ['ajustable']
    else:
        reforms = ['sante', 'environnement', 'tva_sociale', 'mixte']

    aliss_uncomplete = build_clean_aliss_data_frame()
    aliss = add_poste_coicop(aliss_uncomplete)
    aliss_extract = aliss[['nomf', 'nomc', 'poste_bdf']].copy()
    aliss_extract.drop_duplicates(inplace = True)

    codes_coicop_data_frame = pd.read_csv(
        os.path.join(legislation_directory, 'coicop_legislation.csv'),
        )
    legislation = codes_coicop_data_frame[['code_bdf', 'categorie_fiscale']].copy()
    legislation.rename(columns = {'code_bdf': 'poste_bdf'}, inplace = True)
    aliss_legislation = aliss_extract.merge(legislation)
    aliss_legislation.rename(columns = {'poste_bdf': 'code_bdf'}, inplace = True)
    aliss_reform = aliss_legislation.merge(aliss_reform_data)

    # Dealing with mismatch in reforms

    for reform in reforms:
        labels = [removed_reform for removed_reform in reforms if removed_reform != reform]
        mismatch = aliss_reform.drop(
            labels,
            axis = 1,
            ).groupby(['code_bdf']).filter(
                lambda x: x[reform].nunique() > 1,  # noqa B023
                ).sort_values('code_bdf')

        mismatch.nomc = mismatch.nomc.str.decode('latin-1').str.encode('utf-8')
        mismatch.to_csv(
            os.path.join(aliss_assets_reform_directory, '{}_reform_mismatch.csv'.format(reform)),
            index = False,
            )

    if rebuild is True and ajustable is False:
        aliss_reform.to_csv(aliss_reform_path, index = False)

    return aliss_reform


class aliss_ajustable(Reform):
    name = 'Réforme Aliss- Ajustable'
    key = 'aliss_ajustable'

    def apply(self):
        build_custom_aliss_reform(self, key = self.key, name = self.name)


class aliss_environnement(Reform):
    name = "Réforme Aliss-Environnement de l'imposition indirecte des biens alimentaires"
    key = 'aliss_environnement'

    def apply(self):
        build_custom_aliss_reform(self, key = self.key, name = self.name)


class aliss_mixte(Reform):
    key = 'aliss_mixte'
    name = "Réforme Aliss-Mixte-Environnement-Sante de l'imposition indirecte des biens alimentaires"

    def apply(self):
        build_custom_aliss_reform(self, key = self.key, name = self.name)


class aliss_sante(Reform):
    key = 'aliss_sante'
    name = "Réforme Aliss-Santé de l'imposition indirecte des biens alimentaires"

    def apply(self):
        build_custom_aliss_reform(self, key = self.key, name = self.name)


class aliss_tva_sociale(Reform):
    name = "Réforme Aliss-TVA sociale de l'imposition indirecte des biens alimentaires"

    def apply(self):
        key = 'aliss_tva_sociale'
        build_custom_aliss_reform(self, key = key, name = self.name)


def build_custom_aliss_reform(tax_benefit_system = None, key = None, name = None, missmatch_rates = 'weighted'):
    assert missmatch_rates in ['higher', 'weighted']  # "lower"]
    assert key is not None
    assert tax_benefit_system is not None
    taux_by_categorie_fiscale = None

    reform_key = key[6:]
    if reform_key == 'ajustable':
        aliss_reform = build_aliss_reform(rebuild = True, ajustable = True)
    else:
        aliss_reform = build_aliss_reform()

    categories_fiscales_reform = aliss_reform[[reform_key, 'code_bdf']].drop_duplicates().copy()
    reform_mismatch = categories_fiscales_reform.groupby(['code_bdf']).filter(
        lambda x: x[reform_key].nunique() > 1).copy().sort_values('code_bdf')

    if not reform_mismatch.empty:
        if missmatch_rates == 'weighted':
            categories_fiscales_reform, taux_by_categorie_fiscale = build_updated_categorie_fiscale(
                reform_key, categories_fiscales_reform)

        elif missmatch_rates == 'higher':
            categories_fiscales_reform[reform_key] = categories_fiscales_reform[reform_key].astype(
                'category',
                categories = ['tva_taux_reduit', 'tva_taux_intermediaire', 'tva_taux_plein'],
                ordered = True,
                )
            # Keeping higher rate
            categories_fiscales_reform = categories_fiscales_reform.sort_values(
                ['code_bdf', reform_key]
                ).drop_duplicates(
                    subset = 'code_bdf', keep = 'last'
                    )
            assert not categories_fiscales_reform.code_bdf.duplicated().any()
            categories_fiscales_reform[reform_key] = categories_fiscales_reform[reform_key].astype(str)

    categories_fiscales_reform.rename(columns = ({reform_key: 'categorie_fiscale'}), inplace = True)
    year = 2014  # noqa :analysis:ignore
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

    for categorie_fiscale, codes_bdf in list(codes_bdf_by_reform_categorie_fiscale.items()):
        categories_fiscales.loc[
            categories_fiscales.code_bdf.isin(codes_bdf), 'categorie_fiscale'] = categorie_fiscale

    assert not categories_fiscales.code_bdf.duplicated().any(), 'there are {} duplicated entries'.format(
        categories_fiscales.code_bdf.duplicated().sum())

    generate_depenses_ht_categories_fiscales_variables(
        tax_benefit_system,
        legislation_dataframe = categories_fiscales,
        reform_key = key,
        )  # Dépenses hors taxes
    generate_postes_agreges_variables(
        tax_benefit_system,
        categories_fiscales = categories_fiscales,
        reform_key = key,
        taux_by_categorie_fiscale = taux_by_categorie_fiscale,
        )  # Dépenses taxes comprises des postes agrégés
    taux_by_categorie_fiscale = taux_by_categorie_fiscale if taux_by_categorie_fiscale is not None else dict()
    generate_additional_tva_variables(
        tax_benefit_system,
        reform_key = key,
        taux_by_categorie_fiscale = taux_by_categorie_fiscale,
        )


def build_budget_shares(rebuild = False):
    budget_shares_csv_path = os.path.join(aliss_assets_reform_directory, 'budget-shares.csv')
    if not rebuild and os.path.exists(budget_shares_csv_path):
        return pd.read_csv(budget_shares_csv_path)

    aliss = build_clean_aliss_data_frame()
    aliss = add_poste_coicop(aliss)
    kept_variables = ['dt_k', 'nomf', 'nomc', 'poste_coicop']
    aliss = aliss[kept_variables].copy()
    aliss_expenditures = aliss.groupby(
        ['poste_coicop', 'nomc', 'nomf']).apply(
            lambda df: (df.dt_k).sum()
            ).reset_index()
    aliss_expenditures.rename(columns = {0: 'expenditures'}, inplace = True)

    aliss_expenditures['budget_share'] = aliss_expenditures.groupby(
        ['poste_coicop'])['expenditures'].transform(
            lambda x: x / x.sum()
            )
    budget_shares = aliss_expenditures.query('budget_share < 1').copy()
    budget_shares.to_csv(budget_shares_csv_path)

    return budget_shares


def build_legislation_including_f_nomencalture():
    aliss_uncomplete = build_clean_aliss_data_frame()
    aliss = add_poste_coicop(aliss_uncomplete)
    aliss_extract = aliss[['nomf', 'nomk', 'poste_bdf', 'poste_coicop']].copy()
    aliss_extract.drop_duplicates(inplace = True)

    codes_coicop_data_frame = pd.read_csv(
        os.path.join(legislation_directory, 'coicop_legislation.csv'),
        )
    legislation = codes_coicop_data_frame[['code_bdf', 'categorie_fiscale']].copy()
    legislation.rename(columns = {'code_bdf': 'poste_bdf'}, inplace = True)
    return aliss_extract.merge(legislation)


def build_updated_categorie_fiscale(reform_key, categories_fiscales_reform):
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

    weighted_categories_fiscales = mismatch.merge(budget_shares)
    weighted_categories_fiscales['reform_rate'] = weighted_categories_fiscales[reform_key].map(
        taux_by_categorie_fiscale)

    def weighted_mean(x):
        return np.average(x, weights = weighted_categories_fiscales.loc[x.index, 'budget_share'])

    reform_rate = weighted_categories_fiscales.groupby(['code_bdf', 'poste_coicop'])['reform_rate'].agg(
        weighted_mean).reset_index()

    weighted_categories_fiscales = weighted_categories_fiscales.drop('reform_rate', axis = 1).merge(reform_rate)
    weighted_categories_fiscales[reform_key] = 'tva_taux_' + weighted_categories_fiscales.poste_coicop.str[6:]

    # Updating taux_by_categorie_fiscale
    taux_by_categorie_fiscale_update = weighted_categories_fiscales[
        [reform_key, 'reform_rate']
        ].set_index(reform_key).to_dict()['reform_rate']
    taux_by_categorie_fiscale.update(taux_by_categorie_fiscale_update)

    # Updating categories_fiscales_reform
    weighted_categories_fiscales = weighted_categories_fiscales[
        ['code_bdf', reform_key, 'reform_rate']
        ].drop_duplicates()

    duplicated_code_bdf = categories_fiscales_reform.code_bdf.loc[
        categories_fiscales_reform.code_bdf.duplicated(keep = False)
        ].unique()

    # We check that the duplicated code_bdf corresponds to the mismatched ones ...
    assert set(duplicated_code_bdf) == set(weighted_categories_fiscales.code_bdf.unique())
    # ... so we can remove them ...
    categories_fiscales_reform.drop_duplicates(subset = 'code_bdf', keep = False, inplace = True)
    assert not categories_fiscales_reform.code_bdf.duplicated().any()
    # ... to replace them by the ad hoc categories fiscales
    categories_fiscales_reform.set_index('code_bdf', inplace = True)
    categories_fiscales_reform = categories_fiscales_reform.combine_first(
        weighted_categories_fiscales[[reform_key, 'code_bdf']].set_index('code_bdf')
        )
    categories_fiscales_reform.reset_index(inplace = True)
    log.info('The tva categries for reform_key {} are:\n{}'.format(reform_key, sorted(taux_by_categorie_fiscale)))
    return categories_fiscales_reform, taux_by_categorie_fiscale


def depenses_new_tva_function_creator(categorie_fiscale = None, taux = None):
    assert categorie_fiscale is not None
    assert taux is not None

    def func(self, simulation, period, categorie_fiscale = categorie_fiscale, taux = taux):
        return (
            simulation.calculate('depenses_ht_poste_{}'.format(categorie_fiscale[9:]), period) * (1 + taux)
            )

    func.__name__ = 'formula'
    return func


def new_tva_function_creator(categorie_fiscale = None, taux = None):
    assert categorie_fiscale is not None
    assert taux is not None

    def func(self, simulation, period, categorie_fiscale = categorie_fiscale, taux = taux):
        return (
            simulation.calculate('depenses_ht_poste_{}'.format(categorie_fiscale[9:]), period) * taux
            )

    func.__name__ = 'formula'
    return func


def new_tva_total_function_creator(categories_fiscales):
    def func(self, simulation, period):
        return sum(
            simulation.calculate(categorie_fiscale, period) for categorie_fiscale in categories_fiscales
            )

    func.__name__ = 'formula'
    return func


def generate_additional_tva_variables(tax_benefit_system, reform_key = None, taux_by_categorie_fiscale = None):
    for categorie_fiscale, taux in list(taux_by_categorie_fiscale.items()):
        if not categorie_fiscale.startswith('tva'):
            continue
        # Create a depenses (TTC) class with a dynamic name.
        depenses_class_name = 'depenses_{}'.format(categorie_fiscale)

        if depenses_class_name not in tax_benefit_system.variables:
            depenses_new_tva_func = depenses_new_tva_function_creator(
                categorie_fiscale = categorie_fiscale, taux = taux)
            definitions_by_name = dict(
                value_type = float,
                entity = Menage,
                label = 'Dépenses taxes comprises: {0}'.format(categorie_fiscale),
                formula = depenses_new_tva_func,
                )
            depenses_variable_class = type(depenses_class_name, (YearlyVariable,), definitions_by_name)
            tax_benefit_system.add_variable(depenses_variable_class)
            del definitions_by_name

        # Create a tva (TTC) class with a dynamic name.
        tva_class_name = '{}'.format(categorie_fiscale)

        if tva_class_name not in tax_benefit_system.variables:
            new_tva_func = new_tva_function_creator(categorie_fiscale = categorie_fiscale, taux = taux)
            definitions_by_name = dict(
                value_type = float,
                entity = Menage,
                label = 'Montant de la TVA acquitée à {0}'.format(categorie_fiscale),
                formula = new_tva_func,
                )
            tva_variable_class = type(tva_class_name, (YearlyVariable,), definitions_by_name)
            tax_benefit_system.add_variable(tva_variable_class)
            del definitions_by_name

        log.debug('{} Created new fiscal category {}'.format(reform_key, categorie_fiscale))

    # tva_total variable creation
    categories_fiscales = [
        categorie_fiscale
        for categorie_fiscale in list(taux_by_categorie_fiscale.keys())
        if categorie_fiscale.startswith('tva_taux_')
        ]
    new_tva_total_func = new_tva_total_function_creator(categories_fiscales)
    definitions_by_name = dict(
        function = new_tva_total_func,
        )
    type('tva_total', (YearlyVariable,), definitions_by_name)
    del definitions_by_name
