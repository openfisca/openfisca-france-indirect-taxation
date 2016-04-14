# -*- coding: utf-8 -*-

from __future__ import division


import os
import pandas
import pkg_resources


from openfisca_core import reforms

from openfisca_france_indirect_taxation.model.base import get_legislation_data_frames

from openfisca_france_indirect_taxation.model.consommation.postes_coicop import generate_postes_agreges_variables
from openfisca_france_indirect_taxation.model.consommation.categories_fiscales import generate_variables
from openfisca_france_indirect_taxation.build_survey_data.calibration_aliss import (
    add_poste_coicop,
    build_clean_aliss_data_frame,
    )


def build_aliss_reform(rebuild = False):
    aliss_refom_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
        'openfisca_france_indirect_taxation',
        'reforms',
        )
    aliss_reform_path = os.path.join(aliss_refom_directory, 'aliss_reform.csv')
    if os.path.exists(aliss_reform_path) and rebuild is False:
        aliss_reform = pandas.read_csv(aliss_reform_path)
        return aliss_reform

    aliss_reform_data = pandas.read_csv(os.path.join(aliss_refom_directory, 'aliss_reform_unprocessed_data.csv'))
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
    codes_coicop_data_frame = pandas.read_csv(
        os.path.join(legislation_directory, 'coicop_legislation.csv'),
        )
    legislation = codes_coicop_data_frame[['code_bdf', 'categorie_fiscale']].copy()
    legislation.rename(columns = {'code_bdf': 'poste_bdf'}, inplace = True)
    aliss_legislation = aliss_extract.merge(legislation)
    aliss_legislation.rename(columns = {'poste_bdf': 'code_bdf'}, inplace = True)
    aliss_reform = aliss_legislation.merge(aliss_reform_data)

    mismatch = aliss_reform.groupby(['code_bdf']).filter(
        lambda x: (
            x.sante.nunique() > 1 or
            x.environnement.nunique() > 1 or
            x.tva_sociale.nunique() > 1
            )).copy().sort_values('code_bdf')

    mismatch.nomc = mismatch.nomc.str.decode('latin-1').str.encode('utf-8')
    mismatch.to_csv('reform_mismatch.csv', index = False)
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

    assert not categories_fiscales.code_bdf.duplicated().any(), "there are {} duplicated".format(
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
