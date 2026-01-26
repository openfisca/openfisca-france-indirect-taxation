# -*- coding: utf-8 -*-


# Import de modules généraux


import pandas
import seaborn

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.Calage_consommation_bdf import new_get_inflators_by_year  # noqa analysis:ignore
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities


# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette('Set2', 12))


def test(display_plot = False):
    # inflators_by_year = get_inflators_by_year()
    # Liste des coicop agrégées en 12 postes
    postes_agreges = ['poste_agrege_{}'.format(index) for index in
        ['0{}'.format(i) for i in range(1, 10)] + ['10', '11', '12']
        ]
    year = 2011
    elasticities = get_elasticities(year)
    inflation_kwargs = None  # dict(inflator_by_variable = inflators_by_year[year])

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        year = year,
        )

    pivot_table = pandas.DataFrame()
    for values in postes_agreges:
        pivot_table = pandas.concat([
            pivot_table,
            survey_scenario.compute_pivot_table(
                values = [values],
                columns = ['niveau_vie_decile'],
                period = year,
                )
            ])
    df = pivot_table.T
    df['depenses_tot'] = df[postes_agreges].sum(axis = 1)

    parts_postes_agreges = []
    for poste_agrege in postes_agreges:
        df['part_{}'.format(poste_agrege)] = df[poste_agrege] / df['depenses_tot']
        parts_postes_agreges.append('part_{}'.format(poste_agrege))

    if display_plot:
        graph_builder_bar(df[parts_postes_agreges])

    return survey_scenario, df


if __name__ == '__main__':
    survey_scenario, df = test(display_plot = True)
