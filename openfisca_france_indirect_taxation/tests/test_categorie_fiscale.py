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

import datetime

from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation.tests import base


def test_categorie_fiscale_1():
    year = 2010
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        personne_de_reference = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        menage = dict(
            poste_coicop_611 = 100,
            poste_coicop_952 = 50
            ),
        ).new_simulation(debug = True)

    assert_near(simulation.calculate('categorie_fiscale_1'), 150, .01)


def test_categorie_fiscale_0():
    year = 2010
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        personne_de_reference = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        menage = dict(
            poste_coicop_230 = 100,
            ),
        ).new_simulation(debug = True)

    assert_near(simulation.calculate('categorie_fiscale_0'), 100, .01)


if __name__ == '__main__':
    import logging
    import sys
    test_categorie_fiscale_0()
    test_categorie_fiscale_1()
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
