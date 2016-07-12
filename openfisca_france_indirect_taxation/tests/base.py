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


from openfisca_core.reforms import Reform, compose_reforms
from openfisca_core.tools import assert_near

from openfisca_core.tools import assert_near

from .. import FranceIndirectTaxationTaxBenefitSystem
from ..reforms import (
    alimentation,
    aliss,
    contribution_climat_energie,
    taxes_carburants,
    taxe_carbone,
    )


__all__ = [
    'assert_near',
    'get_cached_composed_reform',
    'get_cached_reform',
    'tax_benefit_system',
    'TaxBenefitSystem',
    ]

# Initialize a tax_benefit_system

tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()

# The reforms commented haven't been adapted to the new core API yet.
reform_list = {
    'aliss_environnement': aliss.aliss_environnement,
    'aliss_mixte': aliss.aliss_mixte,
    'aliss_sante': aliss.aliss_sante,
    'aliss_tva_sociale': aliss.aliss_tva_sociale,
    # 'contribution_climat_energie': contribution_climat_energie.build_reform,
    # 'test_reforme_alimentation': alimentation.build_reform,
    # 'taxes_carburants': taxes_carburants.build_reform,
    # 'taxe_carbone': taxe_carbone.build_reform,
    }

build_reform_function_by_key = {

    }
reform_by_full_key = {}


# Reforms cache, used by long scripts like test_yaml.py

def get_cached_composed_reform(reform_keys, tax_benefit_system):
    full_key = '.'.join(
        [tax_benefit_system.full_key] + reform_keys
        if isinstance(tax_benefit_system, Reform)
        else reform_keys
        )
    composed_reform = reform_by_full_key.get(full_key)

    if composed_reform is None:
        reforms = []
        for reform_key in reform_keys:
            assert reform_key in reform_list, \
                'Error loading cached reform "{}" in build_reform_functions'.format(reform_key)
            reform = reform_list[reform_key]
            reforms.append(reform)
        composed_reform = compose_reforms(
            reforms = reforms,
            tax_benefit_system = tax_benefit_system,
            )
        assert full_key == composed_reform.full_key, (full_key, composed_reform.full_key)
        reform_by_full_key[full_key] = composed_reform
    return composed_reform


def get_cached_reform(reform_key, tax_benefit_system):
    return get_cached_composed_reform([reform_key], tax_benefit_system)
