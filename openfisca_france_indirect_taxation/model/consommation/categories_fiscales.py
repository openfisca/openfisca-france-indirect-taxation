# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from datetime import date
import logging

from biryani.strings import slugify

from openfisca_core.formulas import dated_function, DatedVariable


from openfisca_france_indirect_taxation.model.base import *


log = logging.getLogger(__name__)


categories_fiscales_data_frame = None
codes_coicop_data_frame = None


def depenses_function_creator(postes_coicop, categorie_fiscale, year_start = None, year_stop = None,
        depenses_type = None):
    assert depenses_type is not None
    start = date(year_start, 1, 1) if year_start is not None else None
    stop = date(year_stop, 12, 31) if year_stop is not None else None
    if len(postes_coicop) != 0:

        if depenses_type == 'ht':
            @dated_function(start = start, stop = stop)
            def func(self, simulation, period):
                return period, sum(simulation.calculate(
                    'depenses_ht_poste_' + slugify(poste, separator = u'_'), period) for poste in postes_coicop
                    )
            func.__name__ = "function_{year_start}_{year_stop}".format(year_start = year_start, year_stop = year_stop)
            return func
        elif depenses_type == 'ttc':  # Does not work with reform ! Should update poste_
            @dated_function(start = start, stop = stop)
            def func(self, simulation, period):
                return period, sum(simulation.calculate(
                    'poste_' + slugify(poste, separator = u'_'), period) for poste in postes_coicop
                    )
            func.__name__ = "function_{year_start}_{year_stop}".format(year_start = year_start, year_stop = year_stop)
            return func

    else:  # To deal with Reform emptying some fiscal categories
        @dated_function(start = start, stop = stop)
        def func(self, simulation, period):
            return period, self.zeros()

        func.__name__ = "function_{year_start}_{year_stop}".format(year_start = year_start, year_stop = year_stop)
        return func


def generate_variables(categories_fiscales = None, Reform = None, tax_benefit_system = None):
    assert categories_fiscales is not None
    reference_categories = sorted(categories_fiscales_data_frame['categorie_fiscale'].drop_duplicates())
    removed_categories = set()
    if Reform:
        removed_categories = set(reference_categories).difference(
            set(categories_fiscales['categorie_fiscale'].drop_duplicates()))
        Reform.categories_fiscales = categories_fiscales

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

                dated_func = depenses_function_creator(
                    previous_postes_coicop,
                    categorie_fiscale,
                    year_start = year_start,
                    year_stop = year_stop,
                    depenses_type = 'ht',
                    )
                dated_function_name = u"function_{year_start}_{year_stop}".format(
                    year_start = year_start, year_stop = year_stop)
                log.info(u'Creating fiscal category {} ({}-{}) with the following products {}'.format(
                    categorie_fiscale, year_start, year_stop, postes_coicop))

                if len(previous_postes_coicop) != 0:
                    functions_by_name[dated_function_name] = dated_func

                if len(previous_postes_coicop) == 0 and categorie_fiscale in removed_categories:
                    functions_by_name[dated_function_name] = dated_func

                year_start = year

            previous_postes_coicop = postes_coicop

        class_name = u'depenses_ht_{}'.format(categorie_fiscale)
        # Trick to create a class with a dynamic name.
        if not Reform:
            definitions_by_name = dict(
                column = FloatCol,
                entity_class = Menages,
                label = u"Categorie fiscale {0}".format(categorie_fiscale),
                )
            definitions_by_name.update(functions_by_name)
            type(class_name.encode('utf-8'), (DatedVariable,), definitions_by_name)
        else:
            definitions_by_name = dict(
                reference = tax_benefit_system.column_by_name[class_name.encode('utf-8')]
                )
            definitions_by_name.update(functions_by_name)
            type(class_name.encode('utf-8'), (Reform.DatedVariable,), definitions_by_name)

        del definitions_by_name


def preload_categories_fiscales_data_frame():
    from openfisca_france_indirect_taxation.model.consommation.postes_coicop import get_legislation_data_frames
    global codes_coicop_data_frame
    global categories_fiscales_data_frame
    if codes_coicop_data_frame is None or categories_fiscales_data_frame is None:
        categories_fiscales_data_frame, codes_coicop_data_frame = get_legislation_data_frames()
        generate_variables(categories_fiscales = categories_fiscales_data_frame)
