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


from openfisca_core.columns import DateCol, FloatCol, IntCol
from openfisca_core.formulas import reference_input_variable
from ..entities import Individus, Menages


reference_input_variable(
    column = DateCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Date de naissance",
    name = 'birth',
    )


for categorie_fiscale_index in range(18):
    reference_input_variable(
        column = FloatCol,
        entity_class = Menages,
        label = u"catégorie fiscale {}".format(categorie_fiscale_index),
        name = 'categorie_fiscale_{}'.format(categorie_fiscale_index),
        )

reference_input_variable(
    column = FloatCol,
    entity_class = Menages,
    label = u"Consommation droit d'accise alcool 0211",
    name = 'consommation_alcool_0211',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Menages,
    label = u"Consommation droit d'accise alcool 0212",
    name = 'consommation_alcool_0212',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Menages,
    label = u"Consommation droit d'accise alcool 0213",
    name = 'consommation_alcool_0213',
    )


reference_input_variable(
    column = FloatCol,
    entity_class = Menages,
    label = u"Décile de niveau de vie (revenu/unité de consommation",
    name = 'decuc',
    )


reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Identifiant du ménage",
    name = 'ident_men',
    )


reference_input_variable(
    column = IntCol,
    entity_class = Menages,
    is_permanent = True,
    label = u"Pondération du ménage",
    name = 'pondmen',
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


reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Rôle dans le ménage",
    name = 'role_menage',
    )

