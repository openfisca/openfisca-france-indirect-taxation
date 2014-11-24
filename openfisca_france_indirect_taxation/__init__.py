# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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

import numpy as np


from openfisca_core.columns import AgeCol, DateCol, FloatCol, IntCol, reference_input_variable
from openfisca_core.formulas import (make_reference_formula_decorator, SimpleFormulaColumn)
from openfisca_core.taxbenefitsystems import AbstractTaxBenefitSystem

from .scenarios import Scenario
from .entities import entity_class_by_symbol, Menages, Individus

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENCY = u"€"


# TaxBenefitSystems

def init_country():
    class TaxBenefitSystem(AbstractTaxBenefitSystem):
        entity_class_by_key_plural = {
            entity_class.key_plural: entity_class
            for entity_class in entity_class_by_symbol.itervalues()
            }

    # Define class attributes after class declaration to avoid "name is not defined" exceptions.
    TaxBenefitSystem.Scenario = Scenario

    from .model import input_variables
    from .model import model

    return TaxBenefitSystem


# Input variables


reference_input_variable(
    column = DateCol,
    entity_class = Individus,
    is_permanent = True,
    label = "Date de naissance",
    name = 'birth',
    )

reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Identifiant du ménage",
    name = 'idmen',
    )


reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Rôle dans le ménage",
    name = 'quimen',
    )


reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = "Salaire brut",
    name = 'salaire_brut',
    )


# Calculated variables


reference_formula = make_reference_formula_decorator(entity_class_by_symbol = entity_class_by_symbol)


@reference_formula
class age(SimpleFormulaColumn):
    column = AgeCol
    entity_class = Individus
    label = u"Age de l'individu"

    def function(self, birth, period):
        return (np.datetime64(period.date) - birth).astype('timedelta64[Y]')

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')
