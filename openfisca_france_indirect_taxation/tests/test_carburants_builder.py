import pytest


from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.utils import get_input_data_frame

@pytest.mark.parametrize("year", [2000, 2005, 2011])
def test_carburants_builder(year):
    aggregates_data_frame = get_input_data_frame(year)
    postes_07 = [column for column in aggregates_data_frame.columns if column.startswith('poste_07')]
    pondmen = aggregates_data_frame.pondmen.copy()
    carburants = aggregates_data_frame[postes_07].copy()
    data_year = year
    survey_scenario = SurveyScenario().create(year = year, data_year = data_year)

    for poste in postes_07:
        assert_near(
            carburants[poste].sum(),
            survey_scenario.calculate_variable(poste, period = year).sum(),
            absolute_error_margin = 1
            )

    unweighted_input_data = carburants.sum().sum()
    unweighted_computed_aggregate = survey_scenario.calculate_variable('poste_agrege_07', period = year).sum()
    assert_near(unweighted_input_data, unweighted_computed_aggregate, absolute_error_margin = 1)

    weighted_input_data = ((carburants).sum(axis = 1) * pondmen).sum()
    weighted_computed_aggregate = survey_scenario.compute_aggregate('poste_agrege_07', period = year)
    assert_near(weighted_input_data, weighted_computed_aggregate, 1), "the total of transport differs from the sum of its components"
