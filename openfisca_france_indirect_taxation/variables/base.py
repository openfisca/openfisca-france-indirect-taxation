# -*- coding: utf-8 -*-


import numpy as np
import os
import pandas as pd

from slugify import slugify

from openfisca_core.model_api import *  # noqa analysis:ignore

from openfisca_france_indirect_taxation.location import openfisca_france_indirect_taxation_location
from openfisca_france_indirect_taxation.yearly_variable import YearlyVariable  # noqa analysis:ignore
from openfisca_france_indirect_taxation.entities import Individu, Menage  # noqa analysis:ignore

try:
    from openfisca_survey_manager.statshelpers import mark_weighted_percentiles, weighted_quantiles
except ImportError:
    mark_weighted_percentiles, weighted_quantiles = None, None


tva_by_categorie_primaire = dict(
    biere = 'tva_taux_plein',
    vin = 'tva_taux_plein',
    alcools_forts = 'tva_taux_plein',
    cigares = 'cigares',
    cigarettes = 'cigarettes',
    tabac_a_rouler = 'tabac_a_rouler',
    ticpe = 'tva_taux_plein',
    assurance_transport = '',
    assurance_sante = '',
    autres_assurances = '',
    )


def get_tva(categorie_fiscale):
    tva = tva_by_categorie_primaire.get(categorie_fiscale, categorie_fiscale)
    if tva in ['tva_taux_plein', 'tva_taux_intermediaire', 'tva_taux_reduit', 'tva_taux_super_reduit']:
        return tva
    else:
        return None


def droit_d_accise(depense, droit_cn, consommation_cn, taux_plein_tva):
    '''
    Calcule le montant de droit d'accise sur un volume de dépense payé pour le poste adéquat.
    '''
    return depense * ((1 + taux_plein_tva) * droit_cn) / (consommation_cn - (1 + taux_plein_tva) * droit_cn)


def taux_implicite(accise, tva, prix_ttc):
    '''Calcule le taux implicite sur les carburants : pttc = pht * (1+ti) * (1+tva), ici on obtient ti'''
    return (accise * (1 + tva)) / (prix_ttc - accise * (1 + tva))


def tax_from_expense_including_tax(expense = None, tax_rate = None):
    '''Compute the tax amount form the expense including tax

    if depense_ttc = (1 + t) * depense_ht, it returns t * depense_ht
    '''
    assert not np.isnan(tax_rate), 'The tax rate should not be nan'
    return expense * tax_rate / (1 + tax_rate)


def insert_tva(categories_fiscales):
    categories_fiscales = categories_fiscales.copy()
    extracts = pd.DataFrame()
    for categorie_primaire, tva in list(tva_by_categorie_primaire.items()):  # noqa analysis:ignore
        extract = categories_fiscales.query('categorie_fiscale == @categorie_primaire').copy()
        extract['categorie_fiscale'] = tva
        extracts = pd.concat([extracts, extract], ignore_index=True)

    return pd.concat([extracts, categories_fiscales], ignore_index=True)


def get_legislation_data_frames():
    legislation_directory = os.path.join(
        openfisca_france_indirect_taxation_location,
        'openfisca_france_indirect_taxation',
        'assets',
        'legislation',
        )
    codes_coicop_data_frame = pd.read_csv(
        os.path.join(legislation_directory, 'coicop_legislation.csv'),
        )
    codes_coicop_data_frame = codes_coicop_data_frame.query('not (code_bdf != code_bdf)')[  # NaN removal
        ['code_coicop', 'code_bdf', 'label', 'categorie_fiscale', 'start', 'stop']].copy()
    codes_coicop_data_frame = codes_coicop_data_frame.loc[
        codes_coicop_data_frame.code_coicop.str[:2].astype(int) <= 12
        ].copy()
    categories_fiscales_data_frame = codes_coicop_data_frame[
        ['code_coicop', 'code_bdf', 'categorie_fiscale', 'start', 'stop', 'label']
        ].copy().fillna('')
    return categories_fiscales_data_frame, codes_coicop_data_frame


def get_poste_categorie_fiscale(poste_coicop, categories_fiscales = None, start = 9999, stop = 0):
    categories_fiscales_data_frame, _ = get_legislation_data_frames()
    if categories_fiscales is None:
        categories_fiscales = categories_fiscales_data_frame.copy()
    return categories_fiscales.query(
        '(code_coicop == @poste_coicop) and (start <= @start) and (@stop <= stop)')[
        'categorie_fiscale'
        ].tolist()


def depenses_postes_agreges_function_creator(postes_coicop, categories_fiscales = None, reform_key = None,
        taux_by_categorie_fiscale = None, year_start = None, year_stop = None):
    if len(postes_coicop) != 0:
        if reform_key is None:
            def func(entity, period_arg):
                return sum(entity(
                    'poste_' + slugify(poste, separator = '_'), period_arg) for poste in postes_coicop
                    )
            func.__name__ = f'formula_{year_start}'
            return func

        else:
            assert categories_fiscales is not None
            taux_by_categorie_fiscale = taux_by_categorie_fiscale if taux_by_categorie_fiscale is not None else dict()
            categorie_fiscale_by_poste = dict(
                (poste, get_poste_categorie_fiscale(poste, categories_fiscales)[0])
                for poste in postes_coicop)

            def func(entity, period_arg, parameters, categorie_fiscale_by_poste = categorie_fiscale_by_poste,
                    taux_by_categorie_fiscale = taux_by_categorie_fiscale):

                taux_de_tva = parameters(period_arg.start).imposition_indirecte.tva.taux_de_tva._children
                taux_by_categorie_fiscale.update({
                    'tva_taux_super_reduit': taux_de_tva.get('taux_particulier_super_reduit', 0.0),
                    'tva_taux_reduit': taux_de_tva.get('taux_reduit', 0.0),
                    'tva_taux_intermediaire': taux_de_tva.get('taux_intermediaire', 0.0),
                    'tva_taux_plein': taux_de_tva.get('taux_normal', 0.0),
                    })

                poste_agrege = sum(entity(
                    'depenses_ht_poste_' + slugify(poste, separator = '_'), period_arg
                    ) * (
                    1 + taux_by_categorie_fiscale.get(
                        categorie_fiscale_by_poste[poste],
                        taux_by_categorie_fiscale.get(
                            tva_by_categorie_primaire.get(
                                categorie_fiscale_by_poste[poste],
                                ''
                                ),
                            0,
                            )
                        )
                    )
                    for poste in postes_coicop
                    )
                return poste_agrege

            func.__name__ = 'formula'
            return func


def depenses_ht_categorie_function_creator(postes_coicop, year_start = None, year_stop = None):
    if len(postes_coicop) != 0:
        def func(entity, period_arg):
            return sum(entity(
                'depenses_ht_poste_' + slugify(poste, separator = '_'), period_arg) for poste in postes_coicop
                )

        func.__name__ = f'formula_{year_start}'
        return func

    else:  # To deal with Reform emptying some fiscal categories
        def func(entity, period_arg):
            return 0

    func.__name__ = f'formula_{year_start}'.format(year_start = year_start)
    return func


def depenses_ht_postes_function_creator(poste_coicop, categorie_fiscale = None, year_start = None, year_stop = None):
    assert categorie_fiscale is not None

    def func(entity, period_arg, parameters, categorie_fiscale = categorie_fiscale):
        tva = get_tva(categorie_fiscale)
        if tva is not None:
            tva_str = tva[4:]
            if tva_str == 'taux_super_reduit':
                tva_str = 'taux_particulier_super_reduit'
            elif tva_str == 'taux_plein':
                tva_str = 'taux_normal'
            taux = parameters(period_arg.start).imposition_indirecte.tva.taux_de_tva[tva_str]
        else:
            taux = 0

        return entity('poste_' + slugify(poste_coicop, separator = '_'), period_arg) / (1 + taux)

    func.__name__ = f'formula_{year_start}'
    return func
