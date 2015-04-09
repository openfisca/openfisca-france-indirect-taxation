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
    make_reference_formula_decorator, dated_function, DatedFormulaColumn, reference_input_variable, SimpleFormulaColumn
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
    'montant_droit_d_accise',
    'reference_formula',
    'reference_input_variable',
    'SimpleFormulaColumn',
    'tax_from_expense_including_tax',
    'weighted_quantiles',
    ]


# Functions and decorators

reference_formula = make_reference_formula_decorator(entity_class_by_symbol = entity_class_by_symbol)


def montant_droit_d_accise(depense, droit_cn, consommation_cn, taux_plein_tva):
    """
    Calcule le montant de droit d'accise sur un volume de dépense payé pour le poste adéquat.
    """
    return depense * ((1 + taux_plein_tva) * droit_cn) / (consommation_cn - (1 + taux_plein_tva) * droit_cn)


def taux_implicite_tipp_essence(tipp_super9598, taux_plein_tva, prix_ttc_super95, prix_ttc_super98):
    """Calcule le taux implicite sur l'essence"""
    return tipp_super9598 * (1 + taux_plein_tva) / (
        (prix_ttc_super95 + prix_ttc_super98) / 2 - (tipp_super9598) * (1 + taux_plein_tva))


def taux_implicite_tipp_gazole(tipp_gazole, taux_plein_tva, prix_ttc_gazole):
    """Calcule le taux implicite sur le gazole"""
    return (tipp_gazole * (1 + taux_plein_tva)) / (prix_ttc_gazole - (tipp_gazole) * (1 + taux_plein_tva))


def taux_implicite_vin(droit_cn_vin, taux_plein_tva, masse_conso_cn_vin):
    """Calcule le taux implicite pour le vin"""
    return droit_cn_vin * (1 + taux_plein_tva) / (masse_conso_cn_vin - droit_cn_vin * (1 + taux_plein_tva))


def taux_implicite_biere(droit_cn_biere, taux_plein_tva, masse_conso_cn_biere):
    """Calcule le taux implicite pour la biere"""
    return droit_cn_biere * (1 + taux_plein_tva) / (masse_conso_cn_biere - droit_cn_biere * (1 + taux_plein_tva))

def taux_implicite_alcool(droit_cn_alcools_total, taux_plein_tva, masse_conso_cn_alcools):
    """Calcule le taux implicite pour l'alcool"""
    return droit_cn_alcools_total * (1 + taux_plein_tva) / (masse_conso_cn_alcools - droit_cn_alcools_total * (1 + taux_plein_tva))


def tax_from_expense_including_tax(expense = None, tax_rate = None):
    """Compute the tax amount form the expense including tax"""
    return expense * tax_rate / (1 + tax_rate)


