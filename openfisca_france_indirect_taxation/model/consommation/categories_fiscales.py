
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

from openfisca_core.columns import FloatCol
from openfisca_core.formulas import dated_function, DatedVariable


from openfisca_france_indirect_taxation.model.base import *
from openfisca_france_indirect_taxation.utils import get_parametres_fiscalite_data_frame


categories_fiscales_data_frame = None


def function_creator(postes_coicop, year_start = None, year_stop = None):
    start = date(year_start, 1, 1) if year_start is not None else None
    stop = date(year_stop, 12, 31) if year_stop is not None else None

    @dated_function(start = start, stop = stop)
    def func(menage, period, parameters):
        return period, sum(menage('poste_coicop_' + poste, period) for poste in postes_coicop)

    func.__name__ = "function_{year_start}_{year_stop}".format(year_start = year_start, year_stop = year_stop)
    return func


def generate_variables():
    existing_categ = sorted(categories_fiscales_data_frame['categoriefiscale'].drop_duplicates())

    for categorie_fiscale in existing_categ:
        year_start = 1994
        year_final_stop = 2014
        functions_by_name = dict()
        for year in range(year_start, year_final_stop + 1):
            postes_coicop = sorted(
                categories_fiscales_data_frame.query(
                    'annee == @year and categoriefiscale == @categorie_fiscale'
                    )['posteCOICOP'].astype(str))
            variables = ', '.join(postes_coicop)

            if year == year_start:
                previous_variables = variables
                previous_postes_coicop = postes_coicop
                continue

            if previous_postes_coicop == postes_coicop and year != year_final_stop:
                continue
            else:
                year_stop = year - 1 if year != year_final_stop else year_final_stop

                dated_func = function_creator(previous_postes_coicop, year_start = year_start, year_stop = year_stop)
                dated_function_name = u"function_{year_start}_{year_stop}".format(
                    year_start = year_start, year_stop = year_stop)

                if len(previous_postes_coicop) != 0:
                    functions_by_name[dated_function_name] = dated_func

                year_start = year

            previous_postes_coicop = postes_coicop

        class_name = u'categorie_fiscale_{}'.format(categorie_fiscale)
        # Trick to create a class with a dynamic name.
        definitions_by_name = dict(
            column = FloatCol,
            entity_class = Menages,
            label = u"Categorie fiscale {0}".format(categorie_fiscale),
            )
        definitions_by_name.update(functions_by_name)
        type(class_name.encode('utf-8'), (DatedVariable,), definitions_by_name)
        del definitions_by_name


def preload_categories_fiscales_data_frame():
    global categories_fiscales_data_frame
    if categories_fiscales_data_frame is None:
        categories_fiscales_data_frame = get_parametres_fiscalite_data_frame()
        categories_fiscales_data_frame = categories_fiscales_data_frame[
            ['posteCOICOP', 'annee', 'categoriefiscale']
            ].copy()
        generate_variables()
