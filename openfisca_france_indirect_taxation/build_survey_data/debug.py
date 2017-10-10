# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


year = 2014
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
elasticities = get_elasticities(data_year)

reforme = 'rattrapage_diesel'

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = reforme,
    year = year,
    data_year = data_year
    )

simulated_variables = [
    #'ticpe_totale',
    #'diesel_ticpe',
    #'essence_ticpe',
    #'rev_disp_loyerimput',
    #'depenses_diesel',
    #'depenses_diesel_corrigees',
    'total_taxes_energies',
    'total_taxes_energies_{}'.format(reforme),
    'contributions_reforme',
    'cheques_energie',
    'ocde10',
    ]

df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

print df_reforme['contributions_reforme'].mean()
print df_reforme['cheques_energie'].mean()
