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


class decuc(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Décile de niveau de vie (revenu/unité de consommation)"


class niveau_de_vie(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Revenus disponibles divisés par ocde10 soit le nombre d'unités de consommation du ménage"

    def function(menage, period, parameters):
        rev_disponible = menage('rev_disponible', period)
        ocde10 = menage('ocde10', period)
        return period, rev_disponible / ocde10


class niveau_vie_decile(Variable):
    column = EnumCol(
        enum = Enum([
            u"Hors champ",
            u"1er décile",
            u"2nd décile",
            u"3e décile",
            u"4e décile",
            u"5e décile",
            u"6e décile",
            u"7e décile",
            u"8e décile",
            u"9e décile",
            u"10e décile"
            ])
        )
    entity_class = Menages
    label = u"Décile de niveau de vie"

    def function(menage, period, parameters):
        niveau_de_vie = menage('niveau_de_vie', period)
        pondmen = menage('pondmen', period)
        labels = numpy.arange(1, 11)
        # Alternative method
        # method = 2
        # niveau_vie_decile, values = mark_weighted_percentiles(
        # niveau_de_vie, labels, pondmen, method, return_quantiles = True)
        niveau_vie_decile, values = weighted_quantiles(niveau_de_vie, labels, pondmen, return_quantiles = True)
        return period, niveau_vie_decile


class rev_disp_loyerimput(Variable):
    column = FloatCol
    entity_class = Menages
    is_permanent = True
    label = u"Revenu disponible du ménage auquel on ajoute le loyer imputé"


class rev_disponible(Variable):
    column = FloatCol
    entity_class = Menages
    is_permanent = True
    label = u"Revenu disponible du ménage"


class revtot(Variable):
    column = IntCol
    entity_class = Menages
    is_permanent = True
    label = u"Revenu total du ménage"


class revtotuc(Variable):
    column = IntCol
    entity_class = Menages
    is_permanent = True
    label = u"Revenu total par unité de consommation du ménage"
