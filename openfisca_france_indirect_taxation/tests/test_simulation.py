# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.surveys import SurveyScenario


def run_survey_simulation(year = None):
    assert year is not None
    data_year = year
    survey_scenario = SurveyScenario().create(year = year, data_year = data_year)
    basic_variables = [
        'ident_men',
        'pondmen',
        'decuc',
        'poste_01_1_1_1_1',
        'poste_11_1_1_1_1',
        'poste_07_2_2_1_1',
        'depenses_ht_ticpe',
        'depenses_ticpe',
        'depenses_carburants',
        'tva_taux_plein',
        'tva_taux_reduit',
        'tva_taux_super_reduit',
        ]
    categorie_fiscale_yaml_variables = [
        'poste_06_1_1_1_1',
        'poste_09_5_2_1_1',
        'depenses_tva_taux_super_reduit',
        'depenses_ht_poste_06_1_1_1_1',
        'depenses_ht_poste_09_5_2_1_1',
        'poste_agrege_06',
        'poste_agrege_09',
        ]

    tva_yaml_lait_variables = [
        'poste_01_1_4_1_1_a',  # Lait entier tva_taux__reduit devient taux_reduit
        'depenses_ht_poste_01_1_4_1_1_a'
        ]

    return survey_scenario, survey_scenario.create_data_frame_by_entity(
        variables = (
            tva_yaml_lait_variables +
            categorie_fiscale_yaml_variables +
            basic_variables +
            []),
        period = year,
        )


def test_survey_simulation():
    for year in [2000, 2005, 2011]:
        yield run_survey_simulation, year


def get_ht_variables(year):
    assert year is not None
    data_year = year
    survey_scenario = SurveyScenario().create(year = year, data_year = data_year)
    return [
        variable for variable in list(survey_scenario.tax_benefit_system.variables.keys())
        if '_ht_' in variable
        ]


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.DEBUG, stream = sys.stdout)

    for year in [2011]:  # [2000, 2005, 2011]:

        survey_scenario, df_by_entity = run_survey_simulation(year)
        df = df_by_entity['menage']
        for column in df.columns:
            assert not (df[column] == 0).all(), 'variable {} contains only 0s'.format(column)
