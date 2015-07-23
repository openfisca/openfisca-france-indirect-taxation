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


import datetime

from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation.tests import base


def test_ticpe_diesel():
    year = 2015
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        personne_de_reference = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        menage = dict(
            diesel_quantite = 100,
            ),
        ).new_simulation(debug = True)

    assert_near(simulation.calculate('ticpe_diesel'), 100 * 46.82, .01)


def test_ticpe_supercarburants():
    year = 2015
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        personne_de_reference = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        menage = dict(
            supercarburants_quantite = 100,
            ),
        ).new_simulation(debug = True)

    assert_near(simulation.calculate('ticpe_supercarburants'), 100 * 62.41, .01)

# def test_ticpe_super95():
#    year = 2015
#    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
#        period = year,
#        personne_de_reference = dict(
#            birth = datetime.date(year - 40, 1, 1),
#            ),
#        menage = dict(
#            super95_quantite = 100,
#            ),
#        ).new_simulation(debug = True)
#
#
#    assert_near(simulation.calculate('ticpe_super95'), 100 * 62.41, .01)'''
#
# def test_ticpe_super98():
#    year = 2015
#    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
#        period = year,
#        personne_de_reference = dict(
#            birth = datetime.date(year - 40, 1, 1),
#            ),
#        menage = dict(
#            super98_quantite = 100,
#            ),
#        ).new_simulation(debug = True)
#
#
#    assert_near(simulation.calculate('ticpe_super98'), 100 * 62.41, .01)
#
#
# def test_ticpe_superE10():
#    year = 2015
#    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
#        period = year,
#        personne_de_reference = dict(
#            birth = datetime.date(year - 40, 1, 1),
#            ),
#        menage = dict(
#            superE10_quantite = 100,
#            ),
#        ).new_simulation(debug = True)
#
#    assert_near(simulation.calculate('ticpe_superE10'), 100 * 62.41, .01)

if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_ticpe()
