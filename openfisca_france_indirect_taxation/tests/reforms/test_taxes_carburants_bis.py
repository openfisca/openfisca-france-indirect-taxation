# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.Calage_consommation_bdf import new_get_inflators_by_year
from openfisca_france_indirect_taxation.reforms.rattrapage_diesel import reforme_rattrapage_diesel


def test_rattrapage_diesel_bis():
    year = 2011
    inflators_by_year = get_inflators_by_year(rebuild = False)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])  # noqa analysis:ignore
    elasticities = get_elasticities(year)
    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        # inflation_kwargs = inflation_kwargs,
        reform = reforme_rattrapage_diesel,
        period = year,
        )

    simulated_variables = ['depenses_essence_ajustees_rattrapage_diesel', 'depenses_essence', 'elas_price_1_1']
    df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
    df['menage']['depenses_essence_ajustees_rattrapage_diesel'] = df['menage']['depenses_essence_ajustees_rattrapage_diesel'].astype(float)
    df['menage']['check'] = (
        df['menage']['depenses_essence'] * (1 + (1 + df['menage']['elas_price_1_1']) * 10 / 149.9535)
        - df['menage']['depenses_essence_ajustees_rattrapage_diesel']
        )
    absolute_error_margin = 0.01
    assert (df['menage']['check'] < absolute_error_margin).any()
    assert (-absolute_error_margin < df['menage']['check']).any()


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
