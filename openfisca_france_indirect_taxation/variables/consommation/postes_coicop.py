#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging

from slugify import slugify

from openfisca_france_indirect_taxation.variables.base import *

log = logging.getLogger(__name__)


bdf_legislation_data_frame = None


def generate_postes_variables(tax_benefit_system, legislation_dataframe = None):
    if legislation_dataframe is None:
        legislation_dataframe = get_legislation_data_frames()
    adjusted_codes_bdf = [element for element in legislation_dataframe.adjusted_bdf.unique()]
    for adjusted_code_bdf in adjusted_codes_bdf:
        label = legislation_dataframe.query('adjusted_bdf == @adjusted_code_bdf')['Label_sous_classe'].drop_duplicates().tolist()
        assert len(label) == 1, 'Too many labels for {}: {}'.format(adjusted_code_bdf, label)
        label = label[0]
        class_name = 'poste_{}'.format(slugify(adjusted_code_bdf, separator = '_'))
        log.debug('Creating variable {} with label {}'.format(class_name, label))
        # Use type to create a class with a dynamic name
        tax_benefit_system.add_variable(
            type(class_name, (YearlyVariable,), dict(
                value_type = float,
                entity = Menage,
                label = label,
                set_input = set_input_divide_by_period,
                ))
            )


def generate_depenses_ht_postes_variables(tax_benefit_system, legislation_dataframe=None, reform_key=None):
    """
    Génère des variables de dépenses HT pour chaque poste COICOP en fonction des catégories fiscales et des années de validité.
    """
    if legislation_dataframe is None:
        legislation_dataframe = get_legislation_data_frames()
    postes_coicop_all = set()
    functions_by_name_by_poste = {}

    # Obtenir tous les postes COICOP uniques
    postes_coicop = legislation_dataframe['adjusted_bdf'].drop_duplicates().astype(str).tolist()

    for poste_coicop in postes_coicop:
        postes_coicop_all.add(poste_coicop)

        # Filtrer les lignes pour ce poste COICOP
        poste_data = legislation_dataframe[legislation_dataframe['adjusted_bdf'] == poste_coicop]

        # Trier les données par année de début
        poste_data = poste_data.sort_values(by='start')

        previous_category = None
        start_year = None

        for _, row in poste_data.iterrows():
            current_category = row['categorie_fiscale']
            current_start = row['start']
            current_stop = row['stop']

            if current_category != previous_category or current_start != start_year:
                # Si la catégorie ou la période a changé, créer une nouvelle fonction
                if start_year is not None:
                    # Créer la fonction pour la période précédente
                    dated_func = depenses_ht_postes_function_creator(
                        poste_coicop,
                        categorie_fiscale=previous_category,
                        year_start=start_year,
                        year_stop=current_start - 1
                        )

                    function_name = f'formula_{start_year}'

                    if poste_coicop not in functions_by_name_by_poste:
                        functions_by_name_by_poste[poste_coicop] = {}

                    functions_by_name_by_poste[poste_coicop][function_name] = dated_func

                # Mettre à jour la catégorie et l'année de début actuelles
                previous_category = current_category
                start_year = current_start

        # Créer la fonction pour la dernière période
        dated_func = depenses_ht_postes_function_creator(
            poste_coicop,
            categorie_fiscale=previous_category,
            year_start=start_year,
            year_stop=current_stop
            )

        function_name = f'formula_{start_year}'

        if poste_coicop not in functions_by_name_by_poste:
            functions_by_name_by_poste[poste_coicop] = {}

        functions_by_name_by_poste[poste_coicop][function_name] = dated_func

    # Ajouter les variables au système
    for poste, functions_by_name in functions_by_name_by_poste.items():
        class_name = f'depenses_ht_poste_{slugify(poste, separator="_")}'
        definitions_by_name = {
            'value_type': float,
            'entity': Menage,
            'label': f'Dépenses hors taxe du poste {poste}',
            }
        definitions_by_name.update(functions_by_name)
        tax_benefit_system.add_variable(
            type(class_name, (YearlyVariable,), definitions_by_name)
            )
        del definitions_by_name


def generate_postes_agreges_variables(tax_benefit_system, legislation_dataframe=None, reform_key=None,
                                      taux_by_categorie_fiscale=None):
    """
    Génère des variables de postes agrégés pour chaque préfixe de code COICOP,
    en créant des fonctions datées pour chaque période de validité.
    """
    year_start = 1994
    year_final_stop = 2024

    if legislation_dataframe is None:
        legislation_dataframe = get_legislation_data_frames()
        
    for num_prefix in ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12", "13"]:
        codes_bdf = legislation_dataframe.loc[legislation_dataframe['adjusted_bdf'].str.startswith(num_prefix)]['adjusted_bdf'].drop_duplicates().tolist()

        class_name = 'poste_agrege_{}'.format(num_prefix)
        label = 'Poste agrégé {}'.format(num_prefix)
        log.debug('Creating variable {} with label {} using {}'.format(class_name, label, codes_bdf))

        # Dictionnaire pour stocker les fonctions datées
        functions_by_name = {}

        # Déterminer les périodes de validité pour les postes COICOP
        previous_categories = None
        current_year_start = year_start

        for year in range(year_start, year_final_stop + 1):
            # Vérifier les catégories fiscales pour chaque poste COICOP
            current_categories = {}
            for poste in codes_bdf:
                categorie_fiscale = get_poste_categorie_fiscale(poste, legislation_dataframe, year)
                current_categories[poste] = categorie_fiscale[0] if categorie_fiscale else None

            # Si les catégories ont changé ou si c'est la dernière année, créer une fonction datée
            if current_categories != previous_categories or year == year_final_stop:
                if previous_categories is not None:
                    year_stop = year - 1
                    dated_func = depenses_postes_agreges_function_creator(
                        codes_bdf,
                        legislation_dataframe=legislation_dataframe,
                        reform_key=reform_key,
                        taux_by_categorie_fiscale=taux_by_categorie_fiscale,
                        year_start=current_year_start,
                        year_stop=year_stop
                        )
                    function_name = f'formula_{current_year_start}'
                    functions_by_name[function_name] = dated_func

                current_year_start = year

            previous_categories = current_categories

        # Créer une fonction pour la dernière période
        dated_func = depenses_postes_agreges_function_creator(
            codes_bdf,
            legislation_dataframe=legislation_dataframe,
            reform_key=reform_key,
            taux_by_categorie_fiscale=taux_by_categorie_fiscale,
            year_start=current_year_start,
            year_stop=year_final_stop
            )
        function_name = f'formula_{current_year_start}'
        functions_by_name[function_name] = dated_func

        if reform_key is None:
            definitions_by_name = dict(
                value_type=float,
                entity=Menage,
                label=label,
                )
            definitions_by_name.update(functions_by_name)
            tax_benefit_system.add_variable(
                type(class_name, (YearlyVariable,), definitions_by_name)
                )
        else:
            definitions_by_name = functions_by_name
            tax_benefit_system.update_variable(
                type(class_name, (YearlyVariable,), definitions_by_name)
                )

        del definitions_by_name


def preload_postes_bdf_data_frame(tax_benefit_system):
    bdf_legislation = get_legislation_data_frames()

    generate_postes_variables(tax_benefit_system, legislation_dataframe = bdf_legislation)
    generate_postes_agreges_variables(tax_benefit_system, legislation_dataframe = bdf_legislation)
    generate_depenses_ht_postes_variables(tax_benefit_system, legislation_dataframe = bdf_legislation)
