# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


year = 2016
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
elasticities = get_elasticities_aidsills(data_year, True)

reforme = 'officielle_2018_in_2016'

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = reforme,
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'niveau_vie_decile',
    'pondmen',
    'depenses_energies_logement',
    'combustibles_liquides',
    'gaz_ville',
    'emissions_CO2_energies_totales',
    'depenses_energies_totales',
    'depenses_energies_logement',
    'ticpe_totale',
    'diesel_ticpe',
    'essence_ticpe',
    'rev_disp_loyerimput',
    'depenses_tot'

    ]

df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

for i in range(1,11):
    df_decile = df.query('niveau_vie_decile == {}'.format(i))
    print i, \
    (df_decile.pondmen * df_decile.depenses_energies_logement / df_decile.depenses_tot).sum() / df_decile.pondmen.sum()


