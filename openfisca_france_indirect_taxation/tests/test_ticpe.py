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


# If one spends 100 euros in fuel, and has only one diesel vehicle, how much ticpe will he pay in total?
def test_diesel_ticpe():
    year = 2010
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        personne_de_reference = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        menage = dict(
            consommation_ticpe = 100,
            veh_diesel = 1,
            veh_essence = 0,
            ),
        ).new_simulation(debug = True)
    depenses_htva = 100 / (1.196)
    taux_implicite_diesel = (0.4284 * 1.196) / (1.14675 - (0.4284 * 1.196))
    coefficient = taux_implicite_diesel / (1 + taux_implicite_diesel)

    assert_near(simulation.calculate('ticpe_totale'), depenses_htva * coefficient, .01)


# If one has only one gasoline car in 2013 and spends 100 euros in fuel, how much ticpe will he pay in total?
def test_essence_ticpe():
    year = 2013
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        personne_de_reference = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        menage = dict(
            consommation_ticpe = 100,
            veh_essence = 1,
            veh_diesel = 0,
            ),
        ).new_simulation(debug = True)
    depenses_htva = 100 / (1.196)
    sp95_depenses_htva = depenses_htva * 0.627 / 0.996
    sp98_depenses_htva = depenses_htva * 0.188 / 0.996
    sp_e10_depenses_hta = depenses_htva * 0.181 / 0.996
    taux_implicite_95 = (0.6069 * 1.196) / (1.5367 - (0.6069 * 1.196))
    taux_implicite_98 = (0.6069 * 1.196) / (1.5943 - (0.6069 * 1.196))
    taux_implicite_e10 = (0.6069 * 1.196) / (1.51 - (0.6069 * 1.196))
    coefficient_95 = taux_implicite_95 / (1 + taux_implicite_95)
    coefficient_98 = taux_implicite_98 / (1 + taux_implicite_98)
    coefficient_e10 = taux_implicite_e10 / (1 + taux_implicite_e10)

    assert_near(simulation.calculate('ticpe_totale'), coefficient_95 * sp95_depenses_htva +
        coefficient_98 * sp98_depenses_htva + coefficient_e10 * sp_e10_depenses_hta, .01)


# If one has 2 diesel and 1 gasoline car, and spends 100 euros in fuel, how much of it will go to diesel?
def test_depenses_carburants():
    year = 2006
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        personne_de_reference = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        menage = dict(
            consommation_ticpe = 100,
            veh_diesel = 2,
            veh_essence = 1,
            ),
        ).new_simulation(debug = True)

    assert_near(simulation.calculate('diesel_depenses'), 75.075, .01)


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
