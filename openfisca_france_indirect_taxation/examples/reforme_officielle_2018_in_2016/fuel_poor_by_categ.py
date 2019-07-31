# -*- coding: utf-8 -*-

# Import general modules


import numpy as np
import pandas as pd

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import brde, \
    cheque_energie_logement_transport, tee_10_3, precarite
from openfisca_france_indirect_taxation.examples.utils_example import \
    graph_builder_bar_percent, save_dataframe_to_graph, age_group, energy_modes


def number_fuel_poors_by_categ(df_reforme, group, variables_precarite):

    min_group = df_reforme[group].min()
    max_group = df_reforme[group].max()
    elements_group = list(range(min_group, max_group + 1))
    df_to_plot = pd.DataFrame(index = elements_group, columns = variables_precarite)

    for variable in variables_precarite:
        for i in elements_group:
            df = df_reforme.query('{0} == {1}'.format(group, i))
            df_to_plot[variable][i] = \
                (df[variable] * df['pondmen']).sum() / df['pondmen'].sum()

    #save_dataframe_to_graph(df_to_plot, 'Precarite/fuel_poor_by_{}.csv'.format(group))
    df_to_plot = df_to_plot.transpose()
    graph_builder_bar_percent(df_to_plot)

    return df_to_plot


if __name__ == '__main__':

    year = 2016
    data_year = 2011
    inflators_by_year = get_inflators_by_year_energy(rebuild = False)
    #elasticities = get_elasticities(data_year)
    elasticities = get_elasticities_aidsills(data_year, False)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = 'officielle_2018_in_2016',
        year = year,
        data_year = data_year
        )

    simulated_variables = [
        'cheques_energie_officielle_2018_in_2016',
        'cheques_energie_integral_inconditionnel_officielle_2018_in_2016',
        'depenses_carburants_corrigees',
        'depenses_carburants_corrigees_officielle_2018_in_2016',
        'depenses_energies_logement',
        'depenses_energies_logement_officielle_2018_in_2016',
        'depenses_tot',
        'froid_4_criteres_3_deciles',
        'niveau_vie_decile',
        'pondmen',
        'ocde10',
        'rev_disponible',
        'surfhab_d',
        'strate',
        'agepr',
        'gaz_ville',
        'combustibles_liquides'
        ]

    df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

    df_reforme = age_group(df_reforme)
    df_reforme = energy_modes(df_reforme)

    df_reforme = brde(df_reforme, 'depenses_energies_logement', 'rev_disponible', 'logement')
    df_reforme = tee_10_3(df_reforme, 'depenses_energies_logement', 'rev_disponible', 'logement')
    df_reforme = brde(df_reforme, 'depenses_carburants_corrigees', 'rev_disponible', 'transport')
    df_reforme = tee_10_3(df_reforme, 'depenses_carburants_corrigees', 'rev_disponible', 'transport')

    df_reforme = precarite(df_reforme, 'brde_m2_logement_rev_disponible', 'tee_10_3_rev_disponible_logement', 'logement')
    df_reforme = precarite(df_reforme, 'brde_m2_transport_rev_disponible', 'tee_10_3_rev_disponible_transport', 'transport')

    df_reforme['double_precarite'] = (
        (df_reforme['precarite_logement'] * df_reforme['precarite_transport'])
        )
    df_reforme['precarite_joint'] = (
        df_reforme['precarite_logement'] + df_reforme['precarite_transport']
        - (df_reforme['precarite_logement'] * df_reforme['precarite_transport'])
        )

    variables_precarite = ['brde_m2_logement_rev_disponible', 'tee_10_3_rev_disponible_logement',
        'brde_m2_transport_rev_disponible', 'tee_10_3_rev_disponible_transport', 'froid_4_criteres_3_deciles']

    #variables_precarite = ['precarite_joint']

    df_to_plot = number_fuel_poors_by_categ(df_reforme, 'strate', variables_precarite)
    df_to_plot = number_fuel_poors_by_categ(df_reforme, 'age_group', variables_precarite)
    df_to_plot = number_fuel_poors_by_categ(df_reforme, 'energy_mode', variables_precarite)
    #df_to_plot = number_fuel_poors_by_categ(df_reforme, 'age_group')
