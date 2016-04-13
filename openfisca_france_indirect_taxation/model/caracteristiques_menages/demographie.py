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


from __future__ import division


import numpy

from ..base import *  # noqa analysis:ignore


class age(Variable):
    column = AgeCol
    entity_class = Individus
    label = u"Age de l'individu"

    def function(self, simulation, period):
        birth = simulation.calculate('birth', period)
        return period, (numpy.datetime64(period.date) - birth).astype('timedelta64[Y]')


class agepr(Variable):
    column = AgeCol
    entity_class = Individus
    is_permanent = True
    label = u"Age personne de référence"


class age_group_pr(Variable):
    column = AgeCol
    entity_class = Menages
    label = u"Groupe d'âge personne de référence"

    def function(self, simulation, period):
        age_group_pr = 0
        agepr = simulation.calculate('agepr', period)
        age_group_pr = (
            1 * (agepr < 30) +
            2 * (agepr < 40) * (agepr > 29) +
            3 * (agepr < 50) * (agepr > 39) +
            4 * (agepr < 60) * (agepr > 49) +
            5 * (agepr < 70) * (agepr > 59) +
            6 * (agepr > 69)
            )

        return period, age_group_pr


class birth(Variable):
    column = DateCol
    entity_class = Individus
    is_permanent = True
    label = u"Date de naissance"


class nadultes(Variable):
    column = IntCol
    entity_class = Individus
    is_permanent = True
    label = u"Nombre d'adultes dans le ménage"


class nenfants(Variable):
    column = IntCol
    entity_class = Individus
    is_permanent = True
    label = u"Nombre d'enfants dans le ménage"


class role_menage(Variable):
    column = IntCol
    entity_class = Individus
    is_permanent = True
    label = u"Rôle dans le ménage"
