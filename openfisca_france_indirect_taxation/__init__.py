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


from openfisca_core.formulas import make_reference_formula_decorator
from openfisca_core.taxbenefitsystems import AbstractTaxBenefitSystem

from .entities import entity_class_by_symbol
from .param.param import legislation_json
from .scenarios import Scenario

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENCY = u"€"


# TaxBenefitSystems

def init_country():
    class TaxBenefitSystem(AbstractTaxBenefitSystem):
        entity_class_by_key_plural = {
            entity_class.key_plural: entity_class
            for entity_class in entity_class_by_symbol.itervalues()
            }
        legislation_json = legislation_json

    # Define class attributes after class declaration to avoid "name is not defined" exceptions.
    TaxBenefitSystem.Scenario = Scenario

    from model import input_variables  # noqa analysis:ignore
    from model import output_variables  # noqa analysis:ignore
    return TaxBenefitSystem


reference_formula = make_reference_formula_decorator(entity_class_by_symbol = entity_class_by_symbol)
