# -*- coding: utf-8 -*-


import numpy as np
import os
import pandas as pd

from slugify import slugify

from openfisca_core.model_api import *  # noqa analysis:ignore

from openfisca_france_indirect_taxation.utils import assets_directory
# from openfisca_france_indirect_taxation.location import openfisca_france_indirect_taxation_location
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
    cigares = 'tva_taux_plein',
    cigarettes = 'tva_taux_plein',
    tabac_a_rouler = 'tva_taux_plein',
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
        assets_directory,
        'legislation',
        )

    bdf_legislation_data_frame = pd.read_csv(os.path.join(legislation_directory, 'bdf_2017_legislation.csv'))

    return bdf_legislation_data_frame


def get_poste_categorie_fiscale(poste_coicop, legislation_dataframe=None, year=None):
    """
    Récupère la catégorie fiscale associée à un poste COICOP spécifique pour une année donnée.

    Args:
        poste_coicop (str): Code COICOP pour lequel récupérer la catégorie fiscale.
        legislation_dataframe (pd.DataFrame, optional): DataFrame contenant les catégories fiscales.
        year (int, optional): Année pour laquelle récupérer la catégorie fiscale.

    Returns:
        list: Liste des catégories fiscales correspondantes.
    """
    if legislation_dataframe is None:
        legislation_dataframe = get_legislation_data_frames()

    # Vérifier que les colonnes nécessaires existent
    required_columns = ['adjusted_bdf', 'categorie_fiscale', 'start', 'stop']
    for column in required_columns:
        if column not in legislation_dataframe.columns:
            raise ValueError(f"La colonne {column} est manquante dans le DataFrame des catégories fiscales.")

    if year is None:
        raise ValueError("L'année doit être spécifiée.")

    # Filtrer les lignes pour ce poste COICOP et cette année
    result = legislation_dataframe.query(
        '(adjusted_bdf == @poste_coicop) and (start <= @year) and (stop >= @year)'
        )['categorie_fiscale'].tolist()
    return result


def depenses_postes_agreges_function_creator(postes_coicop, legislation_dataframe= None, reform_key=None,
        taux_by_categorie_fiscale=None, year_start=None):
    """
    Crée les fonctions pour calculer les dépenses agrégées pour une liste de postes COICOP,
    en tenant compte des changements de catégories fiscales d'une année à l'autre.

    Args:
        postes_coicop (list): Liste des codes COICOP.
        legislation_dataframe (pd.DataFrame, optional): DataFrame contenant la législation.
        reform_key (str, optional): Clé de réforme si applicable.
        taux_by_categorie_fiscale (dict, optional): Dictionnaire des taux de TVA par catégorie fiscale.
        year_start (int, optional): Année de début de la période.

    Returns:
        function: Une fonction pour calculer les dépenses agrégées.
    """
    if len(postes_coicop) == 0:
        def empty_func(*args, **kwargs):
            return 0
        empty_func.__name__ = 'empty_formula'
        return empty_func

    if reform_key is None:
        def func(entity, period_arg):
            return sum(entity('poste_' + slugify(str(poste), separator='_'), period_arg) for poste in postes_coicop)
        func.__name__ = f'formula_{year_start}'
        return func

    else:
        if legislation_dataframe is None:
            legislation_dataframe = get_legislation_data_frames()

        def func(entity, period_arg, parameters):
            year = period_arg.start.year
            taux_by_categorie_fiscale = {}

            # Mettre à jour les taux de TVA
            taux_de_tva = parameters(year).imposition_indirecte.tva.taux_de_tva._children
            taux_by_categorie_fiscale.update({
                'tva_taux_super_reduit': taux_de_tva.get('taux_particulier_super_reduit', 0.0),
                'tva_taux_reduit': taux_de_tva.get('taux_reduit', 0.0),
                'tva_taux_intermediaire': taux_de_tva.get('taux_intermediaire', 0.0),
                'tva_taux_plein': taux_de_tva.get('taux_normal', 0.0),
                })

            # Calculer les dépenses agrégées
            poste_agrege = 0
            for poste in postes_coicop:
                # Obtenir la catégorie fiscale pour ce poste et cette année
                categorie_fiscale = get_poste_categorie_fiscale(poste, legislation_dataframe, year)
                if categorie_fiscale:
                    categorie_fiscale = categorie_fiscale[0]
                else:
                    log.warning(f"Aucune catégorie fiscale trouvée pour le poste {poste} en {year}")
                    categorie_fiscale = None

                if categorie_fiscale is not None:
                    # Récupérer le taux de TVA en utilisant la logique imbriquée
                    taux = taux_by_categorie_fiscale.get(
                        categorie_fiscale,
                        taux_by_categorie_fiscale.get(
                            tva_by_categorie_primaire.get(
                                categorie_fiscale,
                                ''
                                ),
                            0.0
                            )
                        )
                else:
                    taux = 0.0  # ou une valeur par défaut

                poste_agrege += entity('depenses_ht_poste_' + slugify(str(poste), separator='_'), period_arg) * (1 + taux)

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


def depenses_ht_postes_function_creator(poste_coicop, categorie_fiscale = None, year_start = None):
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
