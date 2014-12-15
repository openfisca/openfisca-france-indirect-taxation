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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import logging


from openfisca_france_data.surveys import AbstractSurveyScenario

log = logging.getLogger(__name__)


class SurveyScenario(AbstractSurveyScenario):

    def init_from_data_frame(self, input_data_frame = None, tax_benefit_system = None, year = None):
        assert input_data_frame is not None
        self.input_data_frame = input_data_frame
        assert tax_benefit_system is not None
        self.tax_benefit_system = tax_benefit_system
#        survey_tax_benefit_system = adapt_to_survey(tax_benefit_system)
        self.tax_benefit_system = tax_benefit_system
        assert year is not None
        self.year = year

        return self

    def initialize_weights(self):
        self.weight_column_name_by_entity_symbol['men'] = 'wprm'
        self.weight_column_name_by_entity_symbol['ind'] = 'weight_ind'
