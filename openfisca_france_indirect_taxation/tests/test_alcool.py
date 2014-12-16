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

from nose.tools import assert_equal

from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation.tests import base


def test_droit_d_accise_alcool():
    year = 2013
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        personne_de_reference = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        menage = dict(
            consommation_alcool_0211 = 100,
            consommation_alcool_0212 = 100,
            consommation_alcool_0213 = 100,

            ),
        ).new_simulation(debug = True)

    alcool_list = ["0211", "0212", "0123"]
    consommations = [
        "consommation_alcool_{}".format(taux) for taux in alcool_list]

    for consommation in consommations:
        assert_equal(simulation.calculate(consommation), 100)

    assert_near(simulation.calculate('montant_droit_d_accise_alcool_0211'), 100 * 1.734 / (1 + 1.734), .01)
    assert_near(simulation.calculate('montant_droit_d_accise_alcool_0212'), 100 * 0.015 / (1 + 0.015), .01)
    assert_near(simulation.calculate('montant_droit_d_accise_alcool_0213'), 100 * 0.411 / (1 + 0.411), .01)


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_droit_d_accise_alcool()
