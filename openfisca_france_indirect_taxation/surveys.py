# -*- coding: utf-8 -*-


import logging
import numpy

from openfisca_survey_manager.scenarios.reform_scenario import ReformScenario
from openfisca_france_indirect_taxation.utils import get_input_data_frame
from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem

log = logging.getLogger(__name__)


class SurveyScenario(ReformScenario):
    id_variable_by_entity_key = dict(
        menage = 'ident_men',
        )
    filtering_variable_by_entity = None
    role_variable_by_entity_key = dict(
        menage = 'role_menage',
        )

    @classmethod
    def create(cls, calibration_kwargs = None, data_year = None, elasticities = None, inflation_kwargs = None,
            input_data_frame = None, baseline_tax_benefit_system = None, reform = None,
            tax_benefit_system = None, period = None):

        assert period is not None

        if reform is None:
            assert baseline_tax_benefit_system is None, 'No need of reference_tax_benefit_system if no reform'
            if tax_benefit_system is None:
                tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
        else:
            if baseline_tax_benefit_system is None:
                baseline_tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()

            tax_benefit_system = reform(baseline_tax_benefit_system)

        if calibration_kwargs is not None:
            assert set(calibration_kwargs.keys()).issubset(set(
                ['target_margins_by_variable', 'parameters', 'total_population']))

        if inflation_kwargs is not None:
            assert set(inflation_kwargs.keys()).issubset(set(['inflator_by_variable', 'target_by_variable']))

        assert data_year is None or input_data_frame is None

        if input_data_frame is None:
            data_year = data_year or period
            input_data_frame = get_input_data_frame(data_year)

        if elasticities is not None:
            assert 'ident_men' in elasticities.columns
            input_data_frame['ident_men'] = input_data_frame.ident_men.astype(numpy.int64)
            input_data_frame = input_data_frame.merge(elasticities, how = 'left', on = 'ident_men')
            for col in elasticities.columns:
                assert col in input_data_frame.columns

        survey_scenario = cls()
        if baseline_tax_benefit_system is not None:
            survey_scenario.set_tax_benefit_systems({'reform': tax_benefit_system,
                                                 'baseline': baseline_tax_benefit_system})
        else:
            survey_scenario.set_tax_benefit_systems({'baseline': tax_benefit_system})
        survey_scenario.used_as_input_variables = list(set(input_data_frame.columns).intersection(
            set(tax_benefit_system.variables.keys())))
        survey_scenario.period = period
        data = dict(input_data_frame = input_data_frame)

        survey_scenario.init_from_data(data = data)
        survey_scenario.initialize_weights()

        if calibration_kwargs:
            survey_scenario.calibrate(**calibration_kwargs)

        if inflation_kwargs:
            log.debug('inflating for year = {} using {}'.format(period, inflation_kwargs))
            survey_scenario.inflate(period = period, **inflation_kwargs)

        assert survey_scenario.simulations is not None
        assert survey_scenario.tax_benefit_systems is not None
        return survey_scenario

    def initialize_weights(self):
        for simulation in self.simulations.values():
            simulation.weight_variable_by_entity = dict()
            simulation.weight_variable_by_entity['menage'] = 'pondmen'
            simulation.weight_variable_by_entity['individu'] = 'weight_ind'
