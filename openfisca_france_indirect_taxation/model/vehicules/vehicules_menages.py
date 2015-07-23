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


from ..base import *  # noqa analysis:ignore

reference_input_variable(
    column = IntCol,
    entity_class = Menages,
    is_permanent = True,
    label = u"Nombre de véhicules total dans le ménage",
    name = 'veh_tot',
    )

reference_input_variable(
    column = IntCol,
    entity_class = Menages,
    is_permanent = True,
    label = u"Nombre de véhicules essence dans le ménage",
    name = 'veh_essence',
    )

reference_input_variable(
    column = IntCol,
    entity_class = Menages,
    is_permanent = True,
    label = u"Nombre de véhicules diesel dans le ménage",
    name = 'veh_diesel',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Menages,
    is_permanent = True,
    label = u"Pourcentage de véhicules essence dans le ménage",
    name = 'pourcentage_vehicule_essence',
    )
