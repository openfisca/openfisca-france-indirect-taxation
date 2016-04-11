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


import os
import pandas as pd
import pkg_resources


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
    'get_legislation_data_frames',
    'get_poste_categorie_fiscale',
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


def get_legislation_data_frames():
    legislation_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
        'openfisca_france_indirect_taxation',
        'assets',
        'legislation',
        )
    codes_coicop_data_frame = pd.read_csv(
        os.path.join(legislation_directory, 'coicop_legislation.csv'),
        )
    codes_coicop_data_frame = codes_coicop_data_frame.query('not (code_bdf != code_bdf)')[  # NaN removal
        ['code_coicop', 'code_bdf', 'label', 'categorie_fiscale', 'start', 'stop']].copy()
    codes_coicop_data_frame = codes_coicop_data_frame.loc[
        codes_coicop_data_frame.code_coicop.str[:2].astype(int) <= 12
        ].copy()
    categories_fiscales_data_frame = codes_coicop_data_frame[
        ['code_coicop', 'code_bdf', 'categorie_fiscale', 'start', 'stop', 'label']
        ].copy().fillna('')
    return categories_fiscales_data_frame, codes_coicop_data_frame


def get_poste_categorie_fiscale(poste_coicop, categories_fiscales = None, start = 9999, stop = 0):
    categories_fiscales_data_frame, _ = get_legislation_data_frames()
    if categories_fiscales is None:
        categories_fiscales = categories_fiscales_data_frame.copy()
    return categories_fiscales.query(
        '(code_coicop == @poste_coicop) and (start <= @start) and (@stop <= stop)')[
        'categorie_fiscale'
        ].tolist()
