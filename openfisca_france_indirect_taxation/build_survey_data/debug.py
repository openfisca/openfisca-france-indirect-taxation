# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


year = 2016
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
elasticities = get_elasticities(data_year)

reforme = 'officielle_2018_in_2016'

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = reforme,
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'depenses_energies_logement',
    'depenses_carburants_corrigees',
    'pondmen',
    'rev_disponible',
    'depenses_tot',
    ]

df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

df = df.query('rev_disponible > 0')
df['part_logement_rev'] = df['depenses_energies_logement'] / df['rev_disponible']
df['part_logement_dep'] = df['depenses_energies_logement'] / df['depenses_tot']

share_log_rev = (df['part_logement_rev'] * df['pondmen']).sum() / df['pondmen'].sum()
share_log_dep = (df['part_logement_dep'] * df['pondmen']).sum() / df['pondmen'].sum()

df['part_transport_rev'] = df['depenses_carburants_corrigees'] / df['rev_disponible']
df['part_transport_dep'] = df['depenses_carburants_corrigees'] / df['depenses_tot']

share_tr_rev = (df['part_transport_rev'] * df['pondmen']).sum() / df['pondmen'].sum()
share_tr_dep = (df['part_transport_dep'] * df['pondmen']).sum() / df['pondmen'].sum()

share_log_dep_median = df['part_logement_dep'].median() * 100
share_tr_dep_median = df['part_transport_dep'].median() * 100
