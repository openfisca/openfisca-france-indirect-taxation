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


import collections
import itertools

from openfisca_core import entities


class Individus(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    is_persons_entity = True
    key_plural = 'individus'
    key_singular = 'individu'
    label = u'Personne'
    name_key = 'nom_individu'
    symbol = 'ind'


class Menages(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    index_for_person_variable_name = 'ident_men'
    key_plural = 'menages'
    key_singular = 'menage'
    label = u'Ménage'
    max_cardinality_by_role_key = {'conjoint': 1, 'personne_de_reference': 1}
    name_key = 'nom_menage'
    role_for_person_variable_name = 'role_menage'
    roles_key = ['personne_de_reference', 'conjoint', 'enfants', 'autres']
    label_by_role_key = {
        'autres': u'Autres',
        'conjoint': u'Conjoint',
        'enfants': u'Enfants',
        'personne_de_reference': u'Personne de référence',
        }
    symbol = 'men'

    def iter_member_persons_role_and_id(self, member):
        role = 0

        personne_de_reference_id = member['personne_de_reference']
        assert personne_de_reference_id is not None
        yield role, personne_de_reference_id
        role += 1

        conjoint_id = member.get('conjoint')
        if conjoint_id is not None:
            yield role, conjoint_id
        role += 1

        autres_id = member.get('autres') or []
        enfants_id = member.get('enfants') or []
        for enfant_role, enfant_id in enumerate(itertools.chain(enfants_id, autres_id), role):
            yield enfant_role, enfant_id


entity_class_by_symbol = dict(
    ind = Individus,
    men = Menages,
    )
