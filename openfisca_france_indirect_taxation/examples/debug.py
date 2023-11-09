# -*- coding: utf-8 -*-

# Import de modules généraux


import seaborn

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import (
    dataframe_by_group,
    )
from openfisca_france_indirect_taxation.surveys import SurveyScenario

# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette('Set2', 12))


if __name__ == '__main__':

    simulated_variables = [
        'rev_disp_loyerimput',
        'poste_07_2_2_1_1',
        'poste_agrege_07',
        'depenses_ht_vin'
        ]
    year = 2014
    data_year = 2011
    survey_scenario = SurveyScenario.create(
        year = year,
        data_year = data_year
        )
    for category in ['niveau_vie_decile']:  # , 'age_group_pr', 'strate_agrege'
        taxes_indirectes = dataframe_by_group(survey_scenario, category, simulated_variables)

    # gazole = get_accises_carburants(['ticpe_gazole'])
    print(taxes_indirectes)
