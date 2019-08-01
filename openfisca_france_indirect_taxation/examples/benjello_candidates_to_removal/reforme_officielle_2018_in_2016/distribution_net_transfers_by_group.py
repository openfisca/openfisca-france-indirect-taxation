# -*- coding: utf-8 -*-

# This script computes the share of households that financial lose from the reform,
# after transfers. This share is given by category (in particular by income deciles).
# Losses are computed on the basis of total financial gains and losses : a person
# loses from the reform if the transfer is lower than the additional spending induced
# by the reform.


import pandas as pd

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

from openfisca_france_indirect_taxation.reforms.officielle_2018_in_2016 import reforme_officielle_2018_in_2016

simulated_variables = [
    'revenu_reforme_officielle_2018_in_2016',
    'cheques_energie_ruraux_officielle_2018_in_2016',
    'cheques_energie_officielle_2018_in_2016',
    'cheques_energie_by_energy_officielle_2018_in_2016',
    'cheques_energie_ruraux_by_energy_officielle_2018_in_2016',
    'ocde10',
    'reste_transferts_neutre_officielle_2018_in_2016',
    'niveau_vie_decile',
    'pondmen',
    'strate',
    ]


def distribution_net_transfers_by_group(df_reform, group):

    i_min = int(df_reforme[group].min())
    i_max = int(df_reforme[group].max())

    df_by_categ = pd.DataFrame(index = list(range(i_min, i_max + 1)),
        columns = ['quantile_10', 'quantile_25', 'quantile_50', 'quantile_75', 'quantile_90']
        )

    for i in range(i_min, i_max + 1):
        df_by_categ['quantile_10'][i] = df_reforme.query('{} == {}'.format(group, i))['transfert_net_cheque_officiel_uc'].quantile(0.1)
        df_by_categ['quantile_25'][i] = df_reforme.query('{} == {}'.format(group, i))['transfert_net_cheque_officiel_uc'].quantile(0.25)
        df_by_categ['quantile_50'][i] = df_reforme.query('{} == {}'.format(group, i))['transfert_net_cheque_officiel_uc'].quantile(0.5)
        df_by_categ['quantile_75'][i] = df_reforme.query('{} == {}'.format(group, i))['transfert_net_cheque_officiel_uc'].quantile(0.75)
        df_by_categ['quantile_90'][i] = df_reforme.query('{} == {}'.format(group, i))['transfert_net_cheque_officiel_uc'].quantile(0.9)

    graph_builder_bar(df_by_categ[['quantile_10'] + ['quantile_25'] + ['quantile_50'] + ['quantile_75'] + ['quantile_90']], False)
    save_dataframe_to_graph(df_by_categ, 'Monetary/distribution_loosers_within_{}.csv'.format(group))

    return df_by_categ


if __name__ == '__main__':
    year = 2016
    data_year = 2011
    from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
    inflators_by_year = get_inflators_by_year_energy(rebuild = False)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
    # elasticities = get_elasticities(data_year)
    elasticities = get_elasticities_aidsills(data_year, True)

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem(),
        inflation_kwargs = inflation_kwargs,
        reform = reforme_officielle_2018_in_2016,
        year = year,
        data_year = data_year
        )

    df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
    df_reforme['transfert_net_cheque_officiel_uc'] = (
        df_reforme['cheques_energie_officielle_2018_in_2016']
        + df_reforme['reste_transferts_neutre_officielle_2018_in_2016']
        - df_reforme['revenu_reforme_officielle_2018_in_2016']
        ) / df_reforme['ocde10']

    df_to_plot = distribution_net_transfers_by_group(df_reforme, 'niveau_vie_decile')
    print(df_to_plot)
