# -*- coding: utf-8 -*-

# This script computes the percentage decrease in quantity of energy consumed by income deciles.
# The objective is to capture the effort made in terms of privation due to the policy.
# It gives another point of view than the financial effort.


import pandas as pd

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar_percent, save_dataframe_to_graph
# from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


simulated_variables = [
    'quantites_combustibles_liquides_officielle_2018_in_2016',
    'quantites_combustibles_liquides',
    'quantites_diesel_officielle_2018_in_2016',
    'quantites_diesel',
    'quantites_essence_officielle_2018_in_2016',
    'quantites_essence',
    'quantites_gaz_final_officielle_2018_in_2016',
    'quantites_gaz_final',
    'niveau_vie_decile',
    'strate',
    'pondmen',
    ]


def change_quantities_by_categ(df_reforme, group):

    i_min = df_reforme[group].min()
    i_max = df_reforme[group].max()
    df_by_categ = pd.DataFrame(index = list(range(i_min, i_max + 1)), columns =
        ['change_in_combustibles_liquides', 'change_in_diesel', 'change_in_essence', 'change_in_gaz_ville']
        )

    for i in range(i_min, i_max + 1):
        df_category = df_reforme.query('{0} == {1}'.format(group, i))
        df_category['change_in_combustibles_liquides'] = ((
            df_category['quantites_combustibles_liquides_officielle_2018_in_2016']
            - df_category['quantites_combustibles_liquides']
            ) / df_category['quantites_combustibles_liquides']
            )
        change_in_combustibles_liquides = (
            (df_category['change_in_combustibles_liquides'] * df_category['pondmen']).sum()
            / df_category['pondmen'].sum()
            )
        df_by_categ['change_in_combustibles_liquides'][i] = change_in_combustibles_liquides

        df_category['change_in_diesel'] = ((
            df_category['quantites_diesel_officielle_2018_in_2016']
            - df_category['quantites_diesel']
            ) / df_category['quantites_diesel']
            )
        change_in_diesel = (
            (df_category['change_in_diesel'] * df_category['pondmen']).sum()
            / df_category['pondmen'].sum()
            )
        df_by_categ['change_in_diesel'][i] = change_in_diesel

        df_category['change_in_essence'] = ((
            df_category['quantites_essence_officielle_2018_in_2016']
            - df_category['quantites_essence']
            ) / df_category['quantites_essence']
            )
        change_in_essence = (
            (df_category['change_in_essence'] * df_category['pondmen']).sum()
            / df_category['pondmen'].sum()
            )
        df_by_categ['change_in_essence'][i] = change_in_essence

        df_category['change_in_gaz_ville'] = ((
            df_category['quantites_gaz_final_officielle_2018_in_2016']
            - df_category['quantites_gaz_final']
            ) / df_category['quantites_gaz_final']
            )
        change_in_gaz_ville = (
            (df_category['change_in_gaz_ville'] * df_category['pondmen']).sum()
            / df_category['pondmen'].sum()
            )
        df_by_categ['change_in_gaz_ville'][i] = change_in_gaz_ville

    df_to_plot = df_by_categ[
        ['change_in_diesel']
        + ['change_in_essence']
        + ['change_in_combustibles_liquides']
        + ['change_in_gaz_ville']
        ]
    graph_builder_bar_percent(df_to_plot)

    return df_to_plot


def change_quantities_among_consumers_by_categ(df_reforme, group):

    i_min = df_reforme[group].min()
    i_max = df_reforme[group].max()
    df_by_categ = pd.DataFrame(index = list(range(i_min, i_max + 1)), columns =
        ['change_in_combustibles_liquides', 'change_in_diesel', 'change_in_essence', 'change_in_gaz_ville']
        )

    for i in range(i_min, i_max + 1):
        df_category = df_reforme.query('{} == {}'.format(group, i))
        df_restricted = df_category.query('quantites_combustibles_liquides > 0')
        df_restricted['change_in_combustibles_liquides'] = ((
            df_restricted['quantites_combustibles_liquides_officielle_2018_in_2016']
            - df_restricted['quantites_combustibles_liquides']
            ) / df_restricted['quantites_combustibles_liquides']
            )
        change_in_combustibles_liquides = (
            (df_restricted['change_in_combustibles_liquides'] * df_restricted['pondmen']).sum()
            / df_restricted['pondmen'].sum()
            )
        df_by_categ['change_in_combustibles_liquides'][i] = change_in_combustibles_liquides

        df_restricted = df_category.query('quantites_diesel > 0')
        df_restricted['change_in_diesel'] = ((
            df_restricted['quantites_diesel_officielle_2018_in_2016']
            - df_restricted['quantites_diesel']
            ) / df_restricted['quantites_diesel']
            )
        change_in_diesel = (
            (df_restricted['change_in_diesel'] * df_restricted['pondmen']).sum()
            / df_restricted['pondmen'].sum()
            )
        df_by_categ['change_in_diesel'][i] = change_in_diesel

        df_restricted = df_category.query('quantites_essence > 0')
        df_restricted['change_in_essence'] = ((
            df_restricted['quantites_essence_officielle_2018_in_2016']
            - df_restricted['quantites_essence']
            ) / df_restricted['quantites_essence']
            )
        change_in_essence = (
            (df_restricted['change_in_essence'] * df_restricted['pondmen']).sum()
            / df_restricted['pondmen'].sum()
            )
        df_by_categ['change_in_essence'][i] = change_in_essence

        df_restricted = df_category.query('quantites_gaz_final > 0')
        df_restricted['change_in_gaz_ville'] = ((
            df_restricted['quantites_gaz_final_officielle_2018_in_2016']
            - df_restricted['quantites_gaz_final']
            ) / df_restricted['quantites_gaz_final']
            )
        change_in_gaz_ville = (
            (df_restricted['change_in_gaz_ville'] * df_restricted['pondmen']).sum()
            / df_restricted['pondmen'].sum()
            )
        df_by_categ['change_in_gaz_ville'][i] = change_in_gaz_ville

    df_to_plot = df_by_categ[
        ['change_in_diesel']
        + ['change_in_essence']
        + ['change_in_combustibles_liquides']
        + ['change_in_gaz_ville']
        ]
    graph_builder_bar_percent(df_to_plot)
    save_dataframe_to_graph(df_to_plot, 'Quantities/change_in_quantities_by_{}.csv'.format(group))

    return df_to_plot


if __name__ == '__main__':
    year = 2016
    data_year = 2011
    inflators_by_year = get_inflators_by_year_energy(rebuild = False)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
    # elasticities = get_elasticities(data_year)
    elasticities = get_elasticities_aidsills(data_year, True)

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform = reforme_officielle_2018_in_2016,
        year = year,
        data_year = data_year
        )

    df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
    df_to_plot = change_quantities_among_consumers_by_categ(df_reforme, 'niveau_vie_decile')
