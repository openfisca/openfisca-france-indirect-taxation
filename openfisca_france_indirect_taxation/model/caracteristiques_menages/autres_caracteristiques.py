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


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class ident_men(Variable):
    column = StrCol
    entity_class = Menages
    is_permanent = True
    label = u"Identifiant du ménage"


class ocde10(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"unités de consommation"


class pondmen(Variable):
    column = IntCol
    entity_class = Menages
    is_permanent = True
    label = u"Pondération du ménage"


class situacj(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Situation du conjoint vis-à-vis du travail"


class situapr(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Situation de la personne de référence vis-à-vis du travail"


class strate(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"catégorie de la commune de résidence"


class strate_agrege(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"catégorie de la commune de résidence, construction d'une nomenclature plus agrégée pour 2011"

    def function(self, simulation, period):
        strate = simulation.calculate('strate', period)
        strate_agrege = (
            1 * (strate == 111) +
            2 * ((strate == 120) + (strate == 211) + (strate == 221)) +
            3 * ((strate == 400) + (strate == 222) + (strate == 300) + (strate == 212) + (strate == 112))
            ) + (
            1 * ((strate == 4) + (strate == 3) + (strate == 2)) +
            2 * (strate == 1) +
            3 * (strate == 0)
            )

        return period, strate_agrege


class typmen(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"type du ménage"


class vag(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"numéro de la vague d'interrogation du ménage"


class zeat(Variable):
    column = EnumCol(
        enum = Enum([
            u"DOM",
            u"Région parisienne",
            u"Bassin parisien",
            u"Nord",
            u"Est",
            u"Ouest",
            u"Sud-Ouest",
            u"Centre-Est",
            u"Méditerrannée"], start = 0)
    )
    entity_class = Menages
    label = u"Zone d'étude et d'aménagement du territoire"

