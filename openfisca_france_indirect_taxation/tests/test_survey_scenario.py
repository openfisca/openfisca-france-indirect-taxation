# -*- coding: utf-8 -*-


# Import de modules généraux
from __future__ import division

import pandas
import seaborn

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar
from openfisca_france_indirect_taxation.surveys import SurveyScenario
# from openfisca_france_indirect_taxation.examples.calage_bdf_cn_bis import get_inflators_by_year
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities


# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette("Set2", 12))


def test():
    # inflators_by_year = get_inflators_by_year()
    # Liste des coicop agrégées en 12 postes
    simulated_variables = ['coicop12_{}'.format(coicop12_index) for coicop12_index in range(1, 13)]

    year = 2011
    elasticities = get_elasticities(year)
    inflation_kwargs = None  # dict(inflator_by_variable = inflators_by_year[year])

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        year = year,
        )

    pivot_table = pandas.DataFrame()
    for values in simulated_variables:
        pivot_table = pandas.concat([
            pivot_table,
            survey_scenario.compute_pivot_table(values = [values], columns = ['niveau_vie_decile'])
            ])
    df = pivot_table.T
    df['depenses_tot'] = df[['coicop12_{}'.format(i) for i in range(1, 13)]].sum(axis = 1)

    for i in range(1, 13):
        df['part_coicop12_{}'.format(i)] = \
            df['coicop12_{}'.format(i)] / df['depenses_tot']

    graph_builder_bar(df[['part_coicop12_{}'.format(i) for i in range(1, 13)]])
    return toto


if __name__ == '__main__':
    toto = test()