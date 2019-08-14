#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging

from slugify import slugify

from openfisca_france_indirect_taxation.variables.base import *

log = logging.getLogger(__name__)


categories_fiscales_data_frame = None
codes_coicop_data_frame = None


def generate_postes_variables(tax_benefit_system):
    codes_bdf = [element for element in codes_coicop_data_frame.code_bdf.unique()]
    for code_bdf in codes_bdf:
        label = codes_coicop_data_frame.query('code_bdf == @code_bdf')['label'].drop_duplicates().tolist()
        assert len(label) == 1, "Too many labels for {}: {}".format(code_bdf, label)
        label = label[0]
        code_coicop = codes_coicop_data_frame.query('code_bdf == @code_bdf')['code_coicop'].drop_duplicates().tolist()
        assert len(code_coicop) == 1, "Too many code_coicop for {}: {}".format(code_bdf, code_coicop)
        code_coicop = code_coicop[0]
        class_name = "poste_{}".format(slugify(code_coicop, separator = '_'))
        log.info('Creating variable {} with label {}'.format(class_name, label))
        # Use type to create a class with a dynamic name
        tax_benefit_system.add_variable(
            type(class_name, (YearlyVariable,), dict(
                value_type = float,
                entity = Menage,
                label = label,
                ))
            )


def generate_depenses_ht_postes_variables(tax_benefit_system, categories_fiscales = None, reform_key = None):
    assert categories_fiscales is not None
    reference_categories = sorted(categories_fiscales_data_frame['categorie_fiscale'].drop_duplicates())
    functions_by_name_by_poste = dict()
    postes_coicop_all = set()

    for categorie_fiscale in reference_categories:
        year_start = 1994
        year_final_stop = 2014
        functions_by_name = dict()
        for year in range(year_start, year_final_stop + 1):
            postes_coicop = sorted(
                categories_fiscales.query(
                    'start <= @year and stop >= @year and categorie_fiscale == @categorie_fiscale'
                    )['code_coicop'].astype(str))
            if year == year_start:
                previous_postes_coicop = postes_coicop
                continue
            if previous_postes_coicop == postes_coicop and year != year_final_stop:
                continue
            else:
                year_stop = year - 1 if year != year_final_stop else year_final_stop

                for poste_coicop in previous_postes_coicop:
                    # if not Reform:
                    dated_func = depenses_ht_postes_function_creator(
                        poste_coicop,
                        categorie_fiscale = categorie_fiscale,
                        year_start = year_start,
                        year_stop = year_stop
                        )

                    dated_function_name = "formula_{year_start}".format(
                        year_start = year_start, year_stop = year_stop)
                    log.debug('Creating fiscal category {} ({}-{}) with the following products {}'.format(
                        categorie_fiscale, year_start, year_stop, postes_coicop))

                    if poste_coicop not in functions_by_name_by_poste:
                        functions_by_name_by_poste[poste_coicop] = dict()
                    functions_by_name_by_poste[poste_coicop][dated_function_name] = dated_func

                year_start = year

            previous_postes_coicop = postes_coicop
            postes_coicop_all = set.union(set(postes_coicop), postes_coicop_all)

    assert set(functions_by_name_by_poste.keys()) == postes_coicop_all

    for poste, functions_by_name in list(functions_by_name_by_poste.items()):
        class_name = 'depenses_ht_poste_{}'.format(slugify(poste, separator = '_'))
        # if Reform is None:
        definitions_by_name = dict(
            value_type = float,
            entity = Menage,
            label = "Dépenses hors taxe du poste_{0}".format(poste),
            )
        definitions_by_name.update(functions_by_name)
        tax_benefit_system.add_variable(
            type(class_name, (YearlyVariable,), definitions_by_name)
            )
        del definitions_by_name


def generate_postes_agreges_variables(tax_benefit_system, categories_fiscales = None, reform_key = None,
        taux_by_categorie_fiscale = None):
    # codes_bdf = [element for element in codes_coicop_data_frame.code_bdf.unique()]
    for num_prefix in ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12"]:
        codes_coicop = codes_coicop_data_frame.loc[
            codes_coicop_data_frame.code_coicop.str.startswith(num_prefix)
            ]['code_coicop'].drop_duplicates().tolist()
        class_name = "poste_agrege_{}".format(num_prefix)
        label = "Poste agrégé {}".format(num_prefix)
        log.info('Creating variable {} with label {} using {}'.format(class_name, label, codes_coicop))

        # Trick to create a class with a dynamic name.
        dated_func = depenses_postes_agreges_function_creator(
            codes_coicop,
            categories_fiscales = categories_fiscales,
            reform_key = reform_key,
            taux_by_categorie_fiscale = taux_by_categorie_fiscale,
            )

        functions_by_name = dict(formula = dated_func)
        if reform_key is None:
            definitions_by_name = dict(
                value_type = float,
                entity = Menage,
                label = label,
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


def preload_postes_coicop_data_frame(tax_benefit_system):
    global categories_fiscales_data_frame
    global codes_coicop_data_frame
    if categories_fiscales_data_frame is None or codes_coicop_data_frame is None:
        categories_fiscales_data_frame, codes_coicop_data_frame = get_legislation_data_frames()

    generate_postes_variables(tax_benefit_system)
    generate_postes_agreges_variables(tax_benefit_system)
    generate_depenses_ht_postes_variables(
        tax_benefit_system, categories_fiscales = categories_fiscales_data_frame.copy())
