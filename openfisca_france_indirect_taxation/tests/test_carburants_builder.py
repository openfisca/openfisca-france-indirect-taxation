import pytest


from openfisca_core.tools import assert_near
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.utils import get_input_data_frame


# TODO 2005 is failing see https://github.com/openfisca/openfisca-france-indirect-taxation/issues/177
# TODO 200 is failing at IPP
@pytest.mark.parametrize('year', [2011])
def test_carburants_builder(year):
    aggregates_data_frame = get_input_data_frame(year)
    postes_07 = [column for column in aggregates_data_frame.columns if column.startswith('poste_07')]
    pondmen = aggregates_data_frame.pondmen.copy()
    carburants = aggregates_data_frame[postes_07].copy()
    data_year = year
    survey_scenario = SurveyScenario().create(year = year, data_year = data_year)

    openfisca_postes = set([
        variable
        for variable in survey_scenario.tax_benefit_system.variables
        if variable.startswith('poste_07')
        ])

    assert set(postes_07) == openfisca_postes, \
        '''year {}:
 - {} is not present in tax_benefit_system
 - {} is not present in input data'''.format(
        year,
        set(postes_07).difference(openfisca_postes),
        set(openfisca_postes).difference(set(postes_07)),
        )

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
    assert_near(weighted_input_data, weighted_computed_aggregate, relative_error_margin = .001), \
        'the total of transport differs from the sum of its components'
