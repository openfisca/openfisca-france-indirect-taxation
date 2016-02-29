# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 17:53:44 2016

@author: thomas.douenne
"""

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_bis import get_inflators_by_year


def test_taxes_carburants_bis():
    year = 2011
    inflators_by_year = get_inflators_by_year()
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
    elasticities = get_elasticities(year)
    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = 'taxes_carburants',
        year = year,
        )

    simulated_variables = ['depenses_essence_ajustees', 'depenses_essence', 'elas_price_1_1']
    df = survey_scenario.create_data_frame_by_entity_key_plural(simulated_variables)
    df['menages']['depenses_essence_ajustees'] = df['menages']['depenses_essence_ajustees'].astype(float)
    df['menages']['check'] = (
        df['menages']['depenses_essence'] * (1 + (1 + df['menages']['elas_price_1_1']) * 10 / 149.9535) -
        df['menages']['depenses_essence_ajustees']
        )
    absolute_error_margin = 0.01
    assert (df['menages']['check'] < absolute_error_margin).any()
    assert (-absolute_error_margin < df['menages']['check']).any()


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_taxes_carburants_bis()
