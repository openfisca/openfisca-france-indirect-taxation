# -*- coding: utf-8 -*-


# from sortedcontainers.sorteddict import SortedDict
import logging


from openfisca_france_indirect_taxation.variables.base import *


log = logging.getLogger(__name__)


categories_fiscales_data_frame = None
codes_coicop_data_frame = None


def generate_depenses_ht_categories_fiscales_variables(tax_benefit_system, legislation_dataframe=None, reform_key=None):
    '''
    Génère et ajoute au tax and benefit system les fonctions pour calculer les dépenses HT agrégées par catégories fiscales.

   Args:
        tax_benefit_system : Un tax and benefit system.
        legislation_dataframe (pd.DataFrame, optional): DataFrame contenant la législation.
        reform_key (str, optional): Clé de réforme si applicable.
    '''
    if legislation_dataframe is None:
        legislation_dataframe = get_legislation_data_frames()

    reference_categories = legislation_dataframe['categorie_fiscale'].drop_duplicates().astype(str).tolist()
    completed_categories_fiscales = insert_tva(legislation_dataframe)

    if reform_key:
        reference_categories = set(reference_categories).union(set(legislation_dataframe.categorie_fiscale.unique()))

    for categorie_fiscale in reference_categories:
        if categorie_fiscale == '':
            continue

        year_start = 1994
        year_final_stop = 2024
        functions_by_name = dict()
        previous_postes_coicop = None

        for year in range(year_start, year_final_stop + 1):
            postes_coicop = completed_categories_fiscales.query(
                'start <= @year and stop >= @year and categorie_fiscale == @categorie_fiscale'
                )['adjusted_bdf'].astype(str).tolist()
   
            if year == year_start:
                previous_postes_coicop = postes_coicop
                continue

            if previous_postes_coicop == postes_coicop and year != year_final_stop:
                continue
            else:
                year_stop = year - 1 if year != year_final_stop else year_final_stop

                dated_func = depenses_ht_categorie_function_creator(
                    previous_postes_coicop,
                    year_start=year_start,
                    year_stop=year_stop,
                    )
                dated_function_name = f'formula_{year_start}'
                log.debug('Creating fiscal category {} ({}-{}) with the following products {}'.format(
                    categorie_fiscale, year_start, year_stop, previous_postes_coicop))

                functions_by_name[dated_function_name] = dated_func
                year_start = year

            previous_postes_coicop = postes_coicop

        # Créer une fonction pour la dernière période
        dated_func = depenses_ht_categorie_function_creator(
            previous_postes_coicop,
            year_start=year_start,
            year_stop=year_final_stop,
            )
        dated_function_name = f'formula_{year_start}'
        functions_by_name[dated_function_name] = dated_func

        class_name = 'depenses_ht_{}'.format(slugify(categorie_fiscale, separator='_'))

        if reform_key is None:
            definitions_by_name = dict(
                value_type=float,
                entity=Menage,
                label='Dépenses hors taxes: {}'.format(categorie_fiscale),
                )
            definitions_by_name.update(functions_by_name)
            tax_benefit_system.add_variable(
                type(class_name, (YearlyVariable,), definitions_by_name)
                )
        else:
            if class_name in tax_benefit_system.variables:
                definitions_by_name = tax_benefit_system.variables[class_name].__dict__.copy()
                definitions_by_name.update(functions_by_name)
                for attribute in ['name', 'baseline_variable', 'dtype', 'json_type', 'is_neutralized', 'formulas']:
                    definitions_by_name.pop(attribute, None)
                tax_benefit_system.update_variable(
                    type(class_name, (YearlyVariable,), definitions_by_name)
                    )
            else:
                definitions_by_name = dict(
                    value_type=float,
                    entity=Menage,
                    label='Dépenses hors taxes: {}'.format(categorie_fiscale),
                    )
                definitions_by_name.update(functions_by_name)
                tax_benefit_system.add_variable(
                    type(class_name, (YearlyVariable,), definitions_by_name)
                    )
        del definitions_by_name


def preload_categories_fiscales_data_frame(tax_benefit_system):
    bdf_legislation = get_legislation_data_frames()

    generate_depenses_ht_categories_fiscales_variables(tax_benefit_system, legislation_dataframe= bdf_legislation)
