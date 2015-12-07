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


reference_input_variable(
    column = FloatCol,
    entity_class = Menages,
    label = u"Décile de niveau de vie (revenu/unité de consommation)",
    name = 'decuc',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Revenu disponible du ménage auquel on ajoute le loyer imputé",
    name = 'rev_disp_loyerimput',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Menages,
    is_permanent = True,
    label = u"Revenu disponible du ménage",
    name = 'rev_disponible',
    )

reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Revenu total du ménage",
    name = 'revtot',
    )

reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Revenu total par unité de consommation du ménage",
    name = 'revtotuc',
    )


class niveau_de_vie(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Revenus disponibles divisés par ocde10 soit le nombre d'unités de consommation du ménage"

    def function(self, simulation, period):
        rev_disponible = simulation.calculate('rev_disponible', period)
        ocde10 = simulation.calculate('ocde10', period)
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

    def function(self, simulation, period):
        niveau_de_vie = simulation.calculate('niveau_de_vie', period)
        pondmen = simulation.calculate('pondmen', period)
        labels = numpy.arange(1, 11)
        # Alternative method
        # method = 2
        # niveau_vie_decile, values = mark_weighted_percentiles(niveau_de_vie, labels, pondmen, method, return_quantiles = True)
        niveau_vie_decile, values = weighted_quantiles(niveau_de_vie, labels, pondmen, return_quantiles = True)
        return period, niveau_vie_decile
