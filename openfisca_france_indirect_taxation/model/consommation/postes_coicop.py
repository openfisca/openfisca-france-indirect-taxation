#! /usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import division

from datetime import date
import logging

from biryani.strings import slugify

from openfisca_core.columns import FloatCol
from openfisca_core.formulas import Variable


from openfisca_france_indirect_taxation.model.base import *


log = logging.getLogger(__name__)


categories_fiscales_data_frame = None
codes_coicop_data_frame = None


def generate_postes_variables():
    codes_bdf = [element for element in codes_coicop_data_frame.code_bdf.unique()]
    for code_bdf in codes_bdf:
        label = codes_coicop_data_frame.query('code_bdf == @code_bdf')['label'].drop_duplicates().tolist()
        assert len(label) == 1, u"Too many labels for {}: {}".format(code_bdf, label)
        label = label[0]
        code_coicop = codes_coicop_data_frame.query('code_bdf == @code_bdf')['code_coicop'].drop_duplicates().tolist()
        assert len(code_coicop) == 1, u"Too many code_coicop for {}: {}".format(code_bdf, code_coicop)
        code_coicop = code_coicop[0]
        class_name = u"poste_{}".format(slugify(unicode(code_coicop), separator = u'_'))
        log.info(u'Creating variable {} with label {}'.format(class_name, label.decode('utf-8')))
        # Trick to create a class with a dynamic name.
        type(class_name.encode('utf-8'), (Variable,), dict(
            column = FloatCol,
            entity_class = Menages,
            label = label.decode('utf-8'),
            ))


def generate_depenses_ht_postes_variables(categories_fiscales = None, Reform = None, tax_benefit_system = None):
    assert categories_fiscales is not None
    reference_categories = sorted(categories_fiscales_data_frame['categorie_fiscale'].drop_duplicates())
    removed_categories = set()
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
                    if not Reform:
                        dated_func = depenses_ht_postes_function_creator(
                            poste_coicop,
                            categorie_fiscale = categorie_fiscale,
                            year_start = year_start,
                            year_stop = year_stop
                            )
                    else:
                        dated_func = depenses_ht_postes_function_creator(
                            poste_coicop,
                            categorie_fiscale = reference_categorie_fiscale,
                            year_start = year_start,
                            year_stop = year_stop
                            )

                    dated_function_name = u"function_{year_start}_{year_stop}".format(
                        year_start = year_start, year_stop = year_stop)
                    log.info(u'Creating fiscal category {} ({}-{}) with the following products {}'.format(
                        categorie_fiscale, year_start, year_stop, postes_coicop))

                    if poste_coicop not in functions_by_name_by_poste:
                            functions_by_name_by_poste[poste_coicop] = dict()
                    functions_by_name_by_poste[poste_coicop][dated_function_name] = dated_func

                year_start = year

            previous_postes_coicop = postes_coicop
            postes_coicop_all = set.union(set(postes_coicop), postes_coicop_all)

    assert set(functions_by_name_by_poste.keys()) == postes_coicop_all

    for poste, functions_by_name in functions_by_name_by_poste.iteritems():
        class_name = u'depenses_ht_poste_{}'.format(slugify(poste, separator = u'_'))
        # Trick to create a class with a dynamic name.
        definitions_by_name = dict(
            column = FloatCol,
            entity_class = Menages,
            label = u"Dépenses hors taxe du poste_{0}".format(poste),
            )
        definitions_by_name.update(functions_by_name)
        type(class_name.encode('utf-8'), (DatedVariable,), definitions_by_name)

        del definitions_by_name


def generate_postes_agreges_variables(categories_fiscales = None, Reform = None, tax_benefit_system = None):

    codes_bdf = [element for element in codes_coicop_data_frame.code_bdf.unique()]
    for num_prefix in ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12"]:
        codes_coicop = codes_coicop_data_frame.loc[
            codes_coicop_data_frame.code_coicop.str.startswith(num_prefix)
            ]['code_coicop'].drop_duplicates().tolist()
        class_name = u"poste_agrege_{}".format(num_prefix)
        log.info(u'Creating variable {} with label {} using {}'.format(class_name, num_prefix, codes_coicop))

        # Trick to create a class with a dynamic name.
        dated_func = depenses_postes_agreges_function_creator(
            codes_coicop,
            categories_fiscales = categories_fiscales,
            Reform = Reform,
            )

        functions_by_name = dict(fucntion = dated_func)
        label = u"Poste agrégé {}".format(num_prefix)
        if not Reform:
            definitions_by_name = dict(
                column = FloatCol,
                entity_class = Menages,
                label = label,
                )
        else:
            definitions_by_name = dict(
                reference = tax_benefit_system.column_by_name[class_name.encode('utf-8')]
                )
        definitions_by_name.update(functions_by_name)
        type(class_name.encode('utf-8'), (DatedVariable,), definitions_by_name)
        del definitions_by_name


def preload_postes_coicop_data_frame():
    global categories_fiscales_data_frame
    global codes_coicop_data_frame
    if categories_fiscales_data_frame is None or codes_coicop_data_frame is None:
        categories_fiscales_data_frame, codes_coicop_data_frame = get_legislation_data_frames()
        generate_postes_variables()
        generate_postes_agreges_variables()
        generate_depenses_ht_postes_variables(categories_fiscales = categories_fiscales_data_frame.copy())
