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


from openfisca_core.columns import AgeCol, DateCol, FloatCol, IntCol, EnumCol, StrCol
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import dated_function, DatedVariable, Variable
from openfisca_survey_manager.statshelpers import mark_weighted_percentiles, weighted_quantiles


from ..entities import Individus, Menages


__all__ = [
    'AgeCol',
    'DateCol',
    'DatedVariable',
    'dated_function',
    'droit_d_accise',
    'Enum',
    'EnumCol',
    'FloatCol',
    'Individus',
    'IntCol',
    'mark_weighted_percentiles',
    'Menages',
    'StrCol',
    'tax_from_expense_including_tax',
    'Variable',
    'weighted_quantiles',
    ]


def droit_d_accise(depense, droit_cn, consommation_cn, taux_plein_tva):
    """
    Calcule le montant de droit d'accise sur un volume de dépense payé pour le poste adéquat.
    """
    return depense * ((1 + taux_plein_tva) * droit_cn) / (consommation_cn - (1 + taux_plein_tva) * droit_cn)


def taux_implicite(accise, tva, prix_ttc):
    """Calcule le taux implicite sur les carburants : pttc = pht * (1+ti) * (1+tva), ici on obtient ti"""
    return (accise * (1 + tva)) / (prix_ttc - accise * (1 + tva))


def tax_from_expense_including_tax(expense = None, tax_rate = None):
    """Compute the tax amount form the expense including tax : si Dttc = (1+t) * Dht, ici on obtient t * Dht"""
    return expense * tax_rate / (1 + tax_rate)
