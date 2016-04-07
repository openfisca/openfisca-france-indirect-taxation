# -*- coding: utf-8 -*-


# Import de modules généraux
from __future__ import division

import pandas
import seaborn

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_bis import get_inflators_by_year
# from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities


# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette("Set2", 12))


if __name__ == '__main__':

    inflators_by_year = get_inflators_by_year(rebuild = False)
    # Liste des coicop agrégées en 12 postes
    suffixes = ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12"]
    simulated_variables = ['poste_agrege_{}'.format(suffix) for suffix in suffixes]

    year = 2011
    # elasticities = get_elasticities(year)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    survey_scenario = SurveyScenario.create(
        # elasticities = elasticities,
        # inflation_kwargs = inflation_kwargs,
        year = year,
        )
    poste_agrege_01 = survey_scenario.simulation.calculate('poste_agrege_01')
    elasticite_1 = survey_scenario.simulation.calculate('elas_exp_1')

    pivot_table = pandas.DataFrame()
    for values in simulated_variables:
        pivot_table = pandas.concat([
            pivot_table,
            survey_scenario.compute_pivot_table(values = [values], columns = ['niveau_vie_decile'])
            ])
    df = pivot_table.T
    df['depenses_tot'] = df[['poste_agrege_{}'.format(suffix) for suffix in suffixes]].sum(axis = 1)

    for suffix in suffixes:
        df['part_poste_agrege_{}'.format(suffix)] = \
            df['poste_agrege_{}'.format(suffix)] / df['depenses_tot']

    graph_builder_bar(df[['part_poste_agrege_{}'.format(suffix) for suffix in suffixes]])

