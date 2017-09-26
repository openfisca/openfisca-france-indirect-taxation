# -*- coding: utf-8 -*-

from __future__ import division

import pandas
import seaborn

from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar_percent, dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette("Set2", 12))

simulated_variables = [
    'precarite_energetique_3_indicateurs',
    'brde_m2',
    'froid_4_criteres_3_deciles',
    'tee_10_3_deciles',
    ]

year = 2011
data_year = 2011

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

survey_scenario = SurveyScenario.create(
    #elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    #reform_key = 'rattrapage_diesel',
    year = year,
    data_year = data_year
    )

for category in ['age_group_pr', 'strate']:
    dataframe = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)
    graph_builder_bar_percent(dataframe)

