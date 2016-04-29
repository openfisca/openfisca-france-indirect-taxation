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


from datetime import date
import os
import pandas as pd
import pkg_resources


from biryani.strings import slugify


from openfisca_core.columns import AgeCol, DateCol, FloatCol, IntCol, EnumCol, StrCol
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import dated_function, DatedVariable, Variable
try:
    from openfisca_survey_manager.statshelpers import mark_weighted_percentiles, weighted_quantiles
except ImportError:
    mark_weighted_percentiles, weighted_quantiles = None, None

from ..entities import Individus, Menages


__all__ = [
    'AgeCol',
    'DateCol',
    'DatedVariable',
    'dated_function',
    'depenses_postes_agreges_function_creator',
    'depenses_ht_categorie_function_creator',
    'depenses_ht_postes_function_creator',
    'droit_d_accise',
    'Enum',
    'EnumCol',
    'FloatCol',
    'get_legislation_data_frames',
    'get_poste_categorie_fiscale',
    'Individus',
    'IntCol',
    'insert_tva',
    'mark_weighted_percentiles',
    'Menages',
    'StrCol',
    'tax_from_expense_including_tax',
    'Variable',
    'weighted_quantiles',
    ]

tva_by_categorie_primaire = dict(
    biere = 'tva_taux_plein',
    vin = 'tva_taux_plein',
    alcools_forts = 'tva_taux_plein',
    cigares = 'cigares',
    cigarettes = 'cigarettes',
    tabac_a_rouler = 'tabac_a_rouler',
    ticpe = 'tva_taux_plein',
    assurance_transport = '',
    assurance_sante = '',
    autres_assurances = '',
    )


def get_tva(categorie_fiscale):
    tva = tva_by_categorie_primaire.get(categorie_fiscale, categorie_fiscale)
    if tva in ['tva_taux_plein', 'tva_taux_intermediaire', 'tva_taux_reduit', 'tva_taux_super_reduit']:
        return tva
    else:
        return None


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


def insert_tva(categories_fiscales):
    categories_fiscales = categories_fiscales.copy()
    extracts = pd.DataFrame()
    for categorie_primaire, tva in tva_by_categorie_primaire.iteritems():
        extract = categories_fiscales.query('categorie_fiscale == @categorie_primaire').copy()
        extract['categorie_fiscale'] = tva
        extracts = pd.concat([extracts, extract], ignore_index=True)

    return pd.concat([extracts, categories_fiscales], ignore_index=True)


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


def depenses_postes_agreges_function_creator(postes_coicop, categories_fiscales = None, Reform = None,
        year_start = None, year_stop = None):
        start = date(year_start, 1, 1) if year_start is not None else None
        stop = date(year_stop, 12, 31) if year_stop is not None else None
        if len(postes_coicop) != 0:
            if not Reform:
                @dated_function(start = start, stop = stop)
                def func(self, simulation, period):
                    return period, sum(simulation.calculate(
                        'poste_' + slugify(poste, separator = u'_'), period) for poste in postes_coicop
                        )
                func.__name__ = "function_{year_start}_{year_stop}".format(
                    year_start = year_start, year_stop = year_stop)
                return func

            elif Reform is not None and categories_fiscales is not None:
                categorie_fiscale_by_poste = dict(
                    (poste, get_poste_categorie_fiscale(poste, categories_fiscales)[0])
                    for poste in postes_coicop)

                @dated_function(start = start, stop = stop)
                def func(self, simulation, period, categorie_fiscale_by_poste = categorie_fiscale_by_poste):

                    def taux(poste):
                        tva = get_tva(categorie_fiscale_by_poste[poste])
                        if tva is not None:
                            return simulation.legislation_at(period.start).imposition_indirecte.tva[tva[4:]]
                        else:
                            return 0

                    poste_agrege = sum(simulation.calculate(
                        'depenses_ht_poste_' + slugify(poste, separator = u'_'), period
                        ) * (1 + taux(poste))
                        for poste in postes_coicop
                        )
                    return period, poste_agrege

                func.__name__ = "function_{year_start}_{year_stop}".format(
                    year_start = year_start, year_stop = year_stop)
                return func
            else:
                raise


def depenses_ht_categorie_function_creator(postes_coicop, year_start = None, year_stop = None):
    start = date(year_start, 1, 1) if year_start is not None else None
    stop = date(year_stop, 12, 31) if year_stop is not None else None

    if len(postes_coicop) != 0:
        @dated_function(start = start, stop = stop)
        def func(self, simulation, period):
            return period, sum(simulation.calculate(
                'depenses_ht_poste_' + slugify(poste, separator = u'_'), period) for poste in postes_coicop
                )

        func.__name__ = "function_{year_start}_{year_stop}".format(year_start = year_start, year_stop = year_stop)
        return func

    else:  # To deal with Reform emptying some fiscal categories

        @dated_function(start = start, stop = stop)
        def func(self, simulation, period):
            return period, self.zeros()

    func.__name__ = "function_{year_start}_{year_stop}".format(year_start = year_start, year_stop = year_stop)
    return func


def depenses_ht_postes_function_creator(poste_coicop, categorie_fiscale = None, year_start = None, year_stop = None):
    start = date(year_start, 1, 1) if year_start is not None else None
    stop = date(year_stop, 12, 31) if year_stop is not None else None
    assert categorie_fiscale is not None

    @dated_function(start = start, stop = stop)
    def func(self, simulation, period, categorie_fiscale = categorie_fiscale):
        tva = get_tva(categorie_fiscale)
        if tva is not None:
            taux = simulation.legislation_at(period.start).imposition_indirecte.tva[tva[4:]]
        else:
            taux = 0

        return period, simulation.calculate('poste_' + slugify(poste_coicop, separator = u'_'), period) / (1 + taux)

    func.__name__ = "function_{year_start}_{year_stop}".format(year_start = year_start, year_stop = year_stop)
    return func
