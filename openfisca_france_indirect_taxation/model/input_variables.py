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


from openfisca_core.columns import DateCol, EnumCol, FloatCol, IntCol, reference_input_variable
from ..entities import Individus, Menages


reference_input_variable(
    column = DateCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Date de naissance",
    name = 'birth',
    )


reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Identifiant du ménage",
    name = 'idmen',
    )


reference_input_variable(
    column = IntCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Rôle dans le ménage",
    name = 'quimen',
    )


reference_input_variable(
    column = IntCol,
    entity_class = Menages,
    is_permanent = True,
    label = u"Pondération du ménage",
    name = 'pondmen',
    )


reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = u"Salaire brut",
    name = 'salaire_brut',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = u"Consommation soumis à une TVA à taux intermédiaire",
    name = 'consommation_tva_taux_intermediaire',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = u"Consommation soumis à une TVA à taux plein",
    name = 'consommation_tva_taux_plein',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = u"Consommation soumis à une TVA à taux réduit",
    name = 'consommation_tva_taux_reduit',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = u"Consommation soumis à une TVA à taux super réduit",
    name = 'consommation_tva_taux_super_reduit',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = u"Consommation droit d'accise alcool 0211",
    name = 'consommation_alcool_0211',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = u"Consommation droit d'accise alcool 0212",
    name = 'consommation_alcool_0212',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = u"Consommation droit d'accise alcool 0213",
    name = 'consommation_alcool_0213',
    )