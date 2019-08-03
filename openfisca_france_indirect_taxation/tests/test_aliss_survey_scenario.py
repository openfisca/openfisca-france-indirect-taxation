import pytest


try:
    import seaborn
except ImportError:
    seaborn = None


from openfisca_france_indirect_taxation.surveys import SurveyScenario
# from openfisca_france_indirect_taxation.build_survey_data.calibration_aliss import get_adjusted_input_data_frame
from openfisca_france_indirect_taxation.reforms.aliss import aliss_tva_sociale

# Import d'une nouvelle palette de couleurs
if seaborn is not None:
    seaborn.set_palette(seaborn.color_palette("Set2", 12))


def build_aliss_scenarios(reform = None):
    year = 2014
    data_year = 2011
    scenario_kwargs = dict(year = year, data_year = data_year, reform = reform)
    survey_scenario = SurveyScenario.create(**scenario_kwargs)
    #
    adjusted_scenario_kwargs = dict(scenario_kwargs)
    adjusted_scenario_kwargs.update(dict(
        data_year = None,
        # TODO input_data_frame = get_adjusted_input_data_frame(reform_key = reform_key[6:])
        ))
    adjusted_survey_scenario = SurveyScenario.create(**adjusted_scenario_kwargs)
    return survey_scenario, adjusted_survey_scenario


@pytest.mark.skip(
    reason = "AssertionError: Survey openfisca_indirect_taxation_data_2014 cannot be found for survey collection openfisca_indirect_taxation."
    )
def test():
    reform = aliss_tva_sociale
    survey_scenario, adjusted_survey_scenario = build_aliss_scenarios(reform = reform)


if __name__ == '__main__':
    test()
