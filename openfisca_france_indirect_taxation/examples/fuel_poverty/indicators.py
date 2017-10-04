# -*- coding: utf-8 -*-

from __future__ import division

import pandas
import seaborn

from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar_percent, \
    dataframe_by_group, save_dataframe_to_graph
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette("Set2", 12))

simulated_variables_depenses_tot = [
    'precarite_energetique_depenses_tot',
    'brde_m2_depenses_tot',
    'froid_4_criteres_3_deciles',
    'tee_10_3_deciles_depenses_tot',
    ]

simulated_variables_rev_disponible = [
    'precarite_energetique_rev_disponible',
    'brde_m2_rev_disponible',
    'froid_4_criteres_3_deciles',
    'tee_10_3_deciles_rev_disponible',
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


for category in ['niveau_vie_decile', 'age_group_pr', 'strate']:
    dataframe_depenses_tot = \
        dataframe_by_group(survey_scenario, category, simulated_variables_depenses_tot, reference = True)
    if category == 'niveau_vie_decile':
        dataframe_depenses_tot = dataframe_depenses_tot.drop(range(4,11))
    graph_builder_bar_percent(dataframe_depenses_tot)

    dataframe_rev_disponible = \
        dataframe_by_group(survey_scenario, category, simulated_variables_rev_disponible, reference = True)
    if category == 'niveau_vie_decile':
        dataframe_rev_disponible = dataframe_rev_disponible.drop(range(4,11))
    graph_builder_bar_percent(dataframe_rev_disponible)
    save_dataframe_to_graph(dataframe_depenses_tot, 'Precarite/indicators_depenses_tot_{}.csv'.format(category))
    save_dataframe_to_graph(dataframe_rev_disponible, 'Precarite/indicators_rev_disponible_{}.csv'.format(category))
