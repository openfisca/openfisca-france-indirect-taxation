import pytest
try:
    import seaborn
    # Import d'une nouvelle palette de couleurs
    seaborn.set_palette(seaborn.color_palette("Set2", 12))
except ImportError:
    seaborn = None


from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.build_survey_data.calibration_aliss import get_adjusted_input_data_frame
from openfisca_france_indirect_taxation.reforms.aliss import aliss_tva_sociale


def build_aliss_scenarios(reform = None):
    year = 2014
    data_year = 2011
    scenario_kwargs = dict(year = year, data_year = data_year, reform = reform)
    survey_scenario = SurveyScenario.create(**scenario_kwargs)
    #
    reform_key = reform.__name__
    adjusted_scenario_kwargs = dict(scenario_kwargs)
    adjusted_scenario_kwargs.update(dict(
        data_year = None,
        input_data_frame = get_adjusted_input_data_frame(reform_key = reform_key[6:])
        ))
    adjusted_survey_scenario = SurveyScenario.create(**adjusted_scenario_kwargs)
    return survey_scenario, adjusted_survey_scenario

# Do not run on laptop msika
@pytest.mark.skip(reason = "Need to fix aliss .dta file problem with utf8")
def test():
    reform = aliss_tva_sociale
    survey_scenario, adjusted_survey_scenario = build_aliss_scenarios(reform = reform)


if __name__ == '__main__':
    test()
