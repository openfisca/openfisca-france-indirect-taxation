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
import numpy

from openfisca_survey_manager.scenarios import AbstractSurveyScenario
from openfisca_france_indirect_taxation.utils import get_input_data_frame
from openfisca_france_indirect_taxation.tests import base


log = logging.getLogger(__name__)


class SurveyScenario(AbstractSurveyScenario):
    @classmethod
    def create(cls, calibration_kwargs = None, data_year = None, elasticities = None, inflation_kwargs = None,
            input_data_frame = None, reference_tax_benefit_system = None, reform = None, reform_key = None, tax_benefit_system = None,
            year = None):  # Add debug parameters debug, debug_all trace for simulation)

        assert year is not None

        # it is either reform or reform_key which is not None
        assert not(
            (reform is not None) and (reform_key is not None)
            )

        if reform_key is not None:
            reform = base.get_cached_reform(
                reform_key = reform_key,
                tax_benefit_system = reference_tax_benefit_system or base.tax_benefit_system,
                )

        if reform is None:
            assert reference_tax_benefit_system is None, "No need of reference_tax_benefit_system if no reform"
            reference_tax_benefit_system = base.tax_benefit_system
        else:
            tax_benefit_system = reform
            reference_tax_benefit_system = base.tax_benefit_system

        if calibration_kwargs is not None:
            print calibration_kwargs
            assert set(calibration_kwargs.keys()).issubset(set(
                ['target_margins_by_variable', 'parameters', 'total_population']))

        if inflation_kwargs is not None:
            assert set(inflation_kwargs.keys()).issubset(set(['inflator_by_variable', 'target_by_variable']))

        assert data_year is None or input_data_frame is None

        if input_data_frame is None:
            data_year = data_year or year
            input_data_frame = get_input_data_frame(data_year)

        if elasticities is not None:
            assert 'ident_men' in elasticities.columns
            input_data_frame['ident_men'] = input_data_frame.ident_men.astype(numpy.int64)
            input_data_frame = input_data_frame.merge(elasticities, how = "left", on = 'ident_men')
            for col in elasticities.columns:
                assert col in input_data_frame.columns

        survey_scenario = cls().init_from_data_frame(
            input_data_frame = input_data_frame,
            tax_benefit_system = tax_benefit_system or reference_tax_benefit_system,
            reference_tax_benefit_system = reference_tax_benefit_system,
            year = year,
            )

        survey_scenario.new_simulation()
        if reform or reform_key:
            survey_scenario.new_simulation(reference = True)

        if calibration_kwargs:
            survey_scenario.calibrate(**calibration_kwargs)

        if inflation_kwargs:
            print 'inflating using {}'.format(inflation_kwargs)
            survey_scenario.inflate(**inflation_kwargs)

        return survey_scenario

    def initialize_weights(self):
        self.weight_column_name_by_entity_key_plural['menages'] = 'pondmen'
        # self.weight_column_name_by_entity__key_plural['individus'] = 'weight_ind'
