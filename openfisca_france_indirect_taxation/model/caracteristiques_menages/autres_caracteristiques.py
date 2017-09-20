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


class ident_men(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Identifiant du ménage"


class identifiant_menage(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Code identifiant le ménage"


class ocde10(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"unités de consommation"


class pondmen(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Pondération du ménage"


class situacj(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Situation du conjoint vis-à-vis du travail"


class situapr(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Situation de la personne de référence vis-à-vis du travail"


class strate(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"catégorie de la commune de résidence"


class cataeu(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"catégorie de la commune de résidence 2011"


class tuu(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"unité urbaine"


class typmen(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"type du ménage"


class vag(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"numéro de la vague d'interrogation du ménage"


class zeat(YearlyVariable):
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
    entity = Menage
    label = u"Zone d'étude et d'aménagement du territoire"
