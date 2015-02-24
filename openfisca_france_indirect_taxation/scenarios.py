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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import collections
import itertools

from openfisca_core import conv
from openfisca_core.scenarios import AbstractScenario


class Scenario(AbstractScenario):
    def init_single_entity(self, autres = None, axes = None, conjoint = None, enfants = None,
                           menage = None, period = None, personne_de_reference = None):
        if enfants is None:
            enfants = []
        if autres is None:
            autres = []
        assert personne_de_reference is not None
        menage = menage.copy() if menage is not None else {}
        individus = []
        for index, individu in enumerate([personne_de_reference, conjoint] + (enfants or []) + (autres or [])):
            if individu is None:
                continue
            id = individu.get('id')
            if id is None:
                individu = individu.copy()
                individu['id'] = id = 'ind{}'.format(index)
            individus.append(individu)
            if index == 0:
                menage['personne_de_reference'] = id
            elif index == 1:
                menage['conjoint'] = id
            else:
                menage.setdefault('enfants', []).append(id)

        conv.check(self.make_json_or_python_to_attributes())(dict(
            axes = axes,
            period = period,
            test_case = dict(
                menages = [menage],
                individus = individus,
                ),
            ))
        return self

    def make_json_or_python_to_test_case(self, period = None, repair = False):
        assert period is not None

        def json_or_python_to_test_case(value, state = None):
            if value is None:
                return value, None
            if state is None:
                state = conv.default_state

            column_by_name = self.tax_benefit_system.column_by_name

            # First validation and conversion step
            test_case, error = conv.pipe(
                conv.test_isinstance(dict),
                conv.struct(
                    dict(
                        menages = conv.pipe(
                            conv.condition(
                                conv.test_isinstance(list),
                                conv.pipe(
                                    conv.uniform_sequence(
                                        conv.test_isinstance(dict),
                                        drop_none_items = True,
                                        ),
                                    conv.function(lambda values: collections.OrderedDict(
                                        (value.pop('id', index), value)
                                        for index, value in enumerate(values)
                                        )),
                                    ),
                                ),
                            conv.test_isinstance(dict),
                            conv.uniform_mapping(
                                conv.pipe(
                                    conv.test_isinstance((basestring, int)),
                                    conv.not_none,
                                    ),
                                conv.pipe(
                                    conv.test_isinstance(dict),
                                    conv.struct(
                                        dict(itertools.chain(
                                            dict(
                                                autres = conv.pipe(
                                                    conv.test_isinstance(list),
                                                    conv.uniform_sequence(
                                                        conv.test_isinstance((basestring, int)),
                                                        drop_none_items = True,
                                                        ),
                                                    conv.default([]),
                                                    ),
                                                conjoint = conv.pipe(
                                                    conv.test_isinstance(basestring, int),
                                                    conv.default(None),
                                                    ),
                                                enfants = conv.pipe(
                                                    conv.test_isinstance(list),
                                                    conv.uniform_sequence(
                                                        conv.test_isinstance((basestring, int)),
                                                        drop_none_items = True,
                                                        ),
                                                    conv.default([]),
                                                    ),
                                                personne_de_reference = conv.pipe(
                                                    conv.test_isinstance(basestring, int),
                                                    conv.default(None),
                                                    ),
                                                ).iteritems(),
                                            (
                                                (column.name, column.json_to_python)
                                                for column in column_by_name.itervalues()
                                                if column.entity == 'men'
                                                ),
                                            )),
                                        drop_none_values = True,
                                        ),
                                    ),
                                drop_none_values = True,
                                ),
                            conv.default({}),
                            ),
                        individus = conv.pipe(
                            conv.condition(
                                conv.test_isinstance(list),
                                conv.pipe(
                                    conv.uniform_sequence(
                                        conv.test_isinstance(dict),
                                        drop_none_items = True,
                                        ),
                                    conv.function(lambda values: collections.OrderedDict(
                                        (value.pop('id', index), value)
                                        for index, value in enumerate(values)
                                        )),
                                    ),
                                ),
                            conv.test_isinstance(dict),
                            conv.uniform_mapping(
                                conv.pipe(
                                    conv.test_isinstance((basestring, int)),
                                    conv.not_none,
                                    ),
                                conv.pipe(
                                    conv.test_isinstance(dict),
                                    conv.struct(
                                        dict(
                                            (column.name, column.json_to_python)
                                            for column in column_by_name.itervalues()
                                            if column.entity == 'ind' and column.name not in (
                                                'idmen', 'quimen')
                                            ),
                                        drop_none_values = True,
                                        ),
                                    ),
                                drop_none_values = True,
                                ),
                            conv.empty_to_none,
                            conv.not_none,
                            ),
                        ),
                    ),
                )(value, state = state)
            if error is not None:
                return test_case, error

            # Second validation step
            menages_individus_id = list(test_case['individus'].iterkeys())
            test_case, error = conv.struct(
                dict(
                    menages = conv.uniform_mapping(
                        conv.noop,
                        conv.struct(
                            dict(
                                autres = conv.uniform_sequence(conv.test_in_pop(menages_individus_id)),
                                conjoint = conv.test_in_pop(menages_individus_id),
                                enfants = conv.uniform_sequence(conv.test_in_pop(menages_individus_id)),
                                personne_de_reference = conv.test_in_pop(menages_individus_id),
                                ),
                            default = conv.noop,
                            ),
                        ),
                    ),
                default = conv.noop,
                )(test_case, state = state)

            remaining_individus_id = set(menages_individus_id)
            if remaining_individus_id:
                if error is None:
                    error = {}
                for individu_id in remaining_individus_id:
                    error.setdefault('individus', {})[individu_id] = state._(u"Individual is missing from {}").format(
                        state._(u' & ').join(
                            word
                            for word in [
                                u'menages' if individu_id in menages_individus_id else None,
                                ]
                            if word is not None
                            ))
            if error is not None:
                return test_case, error

            return test_case, error

        return json_or_python_to_test_case
