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
from openfisca_core.formulas import (
    make_formula_decorator, dated_function, DatedFormulaColumn, reference_input_variable, SimpleFormulaColumn
    )
from openfisca_survey_manager.statshelpers import mark_weighted_percentiles, weighted_quantiles


from ..entities import entity_class_by_symbol, Individus, Menages


__all__ = [
    'AgeCol',
    'DateCol',
    'DatedFormulaColumn',
    'dated_function',
    'Enum',
    'EnumCol',
    'FloatCol',
    'Individus',
    'IntCol',
    'mark_weighted_percentiles',
    'Menages',
    'droit_d_accise',
    'reference_formula',
    'reference_input_variable',
    'SimpleFormulaColumn',
    'tax_from_expense_including_tax',
    'weighted_quantiles',
    ]


# Functions and decorators

reference_formula = make_formula_decorator(entity_class_by_symbol = entity_class_by_symbol)


def taux_implicite(accise, tva, prix_ttc):
    """Calcule le taux implicite sur les carburants"""
    return (accise * (1 + tva)) / (prix_ttc - accise * (1 + tva))


def droit_d_accise(depense, droit_cn, consommation_cn, taux_plein_tva):
    """
    Calcule le montant de droit d'accise sur un volume de dépense payé pour le poste adéquat.
    """
    return depense * ((1 + taux_plein_tva) * droit_cn) / (consommation_cn - (1 + taux_plein_tva) * droit_cn)


def tax_from_expense_including_tax(expense = None, tax_rate = None):
    """Compute the tax amount form the expense including tax"""
    return expense * tax_rate / (1 + tax_rate)
