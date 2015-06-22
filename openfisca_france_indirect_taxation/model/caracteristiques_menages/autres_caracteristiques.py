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


from ..base import *  # noqa analysis:ignore

from openfisca_france_indirect_taxation.param.param import ( # noq analysis:ignore
    # P_tva_taux_plein, P_tva_taux_intermediaire, P_tva_taux_reduit,
    # P_tva_taux_super_reduit,
    P_alcool_0211, P_alcool_0212, P_alcool_0213
    )
# TODO: supprimer les P_alcool ?

for categorie_fiscale_index in range(18):
    reference_input_variable(
        column = FloatCol,
        entity_class = Menages,
        label = u"catégorie fiscale {}".format(categorie_fiscale_index),
        name = 'categorie_fiscale_{}'.format(categorie_fiscale_index),
        )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    is_permanent = True,
    label = u"Identifiant du ménage",
    name = 'ident_men',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Menages,
    label = u"unités de consommation",
    name = 'ocde10',
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
    entity_class = Menages,
    label = u"type du ménage",
    name = 'typmen',
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Menages,
    label = u"numéro de la vague d'interrogation du ménage",
    name = 'vag',
    )
