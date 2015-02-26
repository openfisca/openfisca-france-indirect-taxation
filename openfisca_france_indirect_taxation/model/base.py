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


from openfisca_core.columns import AgeCol, DateCol, FloatCol, IntCol, EnumCol
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import make_reference_formula_decorator, reference_input_variable, SimpleFormulaColumn

from openfisca_france_data.statshelpers import mark_weighted_percentiles


from ..entities import entity_class_by_symbol, Individus, Menages


__all__ = [
    'AgeCol',
    'DateCol',
    'Enum',
    'EnumCol',
    'FloatCol',
    'Individus',
    'IntCol',
    'mark_weighted_percentiles',
    'Menages',
    'reference_formula',
    'reference_input_variable',
    'SimpleFormulaColumn',
    ]


# Functions and decorators

reference_formula = make_reference_formula_decorator(entity_class_by_symbol = entity_class_by_symbol)
