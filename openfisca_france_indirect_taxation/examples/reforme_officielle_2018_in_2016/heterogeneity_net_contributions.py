# -*- coding: utf-8 -*-

# This script depicts households' net fiscal transfers from the reform.
# It is equal to the transfers received from the reform, minus the additional
# taxes paid. A positive value means the household received higher transfers than
# the increase in taxes he faced. These amounts do not take into account VAT.
# ....

# Import general modules
from __future__ import division

import pandas as pd

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group, age_group, energy_modes
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
#elasticities = get_elasticities(data_year)
elasticities = get_elasticities_aidsills(data_year, True)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'revenu_reforme_officielle_2018_in_2016',
    'cheques_energie_officielle_2018_in_2016',
    'reste_transferts_neutre_officielle_2018_in_2016',
    'strate',
    'niveau_vie_decile',
    'pondmen',
    'combustibles_liquides',
    'gaz_ville',
    'agepr',
    'isolation_murs',
    'isolation_fenetres',
    'nenfants',
    'ocde10',
    ]

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'officielle_2018_in_2016',
    year = year,
    data_year = data_year
    )

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df_reforme = age_group(df_reforme)
df_reforme = energy_modes(df_reforme)


def net_transfers_by_sub_group(df_reforme, group):

    df_reforme['transferts_nets_apres_redistribution_uc'] = (
        df_reforme['cheques_energie_officielle_2018_in_2016'] +
        df_reforme['reste_transferts_neutre_officielle_2018_in_2016'] -
        df_reforme['revenu_reforme_officielle_2018_in_2016']
        ) / df_reforme['ocde10']

    df_reforme[group] = df_reforme[group].astype(int)

    min_group = df_reforme[group].min()
    max_group = df_reforme[group].max()
    elements_group = range(min_group, max_group+1)
    deciles = range(1, 11)
    df_to_plot = pd.DataFrame(index = deciles, columns = elements_group)

    for element in range(min_group, max_group+1):
        for decile in deciles:
            df = df_reforme.query('{0} == {1}'.format(group, element)).query('niveau_vie_decile == {}'.format(decile))
            df_to_plot[element][decile] = \
                (df['transferts_nets_apres_redistribution_uc'] * df['pondmen']).sum() / df['pondmen'].sum()

    graph_builder_bar(df_to_plot, False)
    save_dataframe_to_graph(df_to_plot, 'Monetary/heterogeneity_transfers_by_uc_by_{}.csv'.format(group))

    return df_to_plot


if __name__ == "__main__":
    
    df_to_plot_strate = net_transfers_by_sub_group(df_reforme, 'strate')
    df_to_plot_combustibles_liquides = net_transfers_by_sub_group(df_reforme, 'combustibles_liquides')
    df_to_plot_gaz_ville = net_transfers_by_sub_group(df_reforme, 'gaz_ville')
    df_to_plot_energy_mode = net_transfers_by_sub_group(df_reforme, 'energy_mode')
    df_to_plot_age = net_transfers_by_sub_group(df_reforme, 'age_group')

    df_reforme['qualite_isolation'] = df_reforme['isolation_fenetres'] * df_reforme['isolation_murs']
    df_selected = df_reforme.query('qualite_isolation != 0')
    df_selected.loc[df_selected['qualite_isolation'] == 6, 'qualite_isolation'] = 5
    df_to_plot = net_transfers_by_sub_group(df_selected, 'qualite_isolation')

    df_reforme['household_size'] = (
        1 * (df_reforme['ocde10'] == 1)
        + 2 * (df_reforme['ocde10'] < 2) * (df_reforme['ocde10'] > 1)
        + 3 * ((df_reforme['ocde10'] == 2) + (df_reforme['ocde10'] > 2))
        )

    df_to_plot = net_transfers_by_sub_group(df_reforme, 'household_size')


