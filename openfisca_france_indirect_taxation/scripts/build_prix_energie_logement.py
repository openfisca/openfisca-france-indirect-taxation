# -*- coding: utf-8 -*-


import os
import pkg_resources
import numpy

from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_bis import get_inflators_by_year


inflators_by_year = get_inflators_by_year(rebuild = False)

simulated_variables = [
    'depenses_electricite_prix_unitaire',
    'depenses_gaz_prix_unitaire',
    'identifiant_menage',
    ]

for year in [2000, 2005, 2011]:
    elasticities = get_elasticities(year)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    survey_scenario = SurveyScenario.create(
        #elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        #reform_key = 'rattrapage_diesel_bis',
        year = year,
        )

    df_by_entity = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
    menages = df_by_entity['menage']

    assert not menages.identifiant_menage.duplicated().any(), 'Some households are duplicated'

    assets_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
        )
    menages['identifiant_menage'] = menages['identifiant_menage'].astype(numpy.int64)
    menages.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets',
        'prix', 'prix_unitaire_gaz_electricite_par_menage_{}.csv'.format(year)), sep = ',')
