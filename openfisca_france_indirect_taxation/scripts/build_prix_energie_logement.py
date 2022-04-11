# -*- coding: utf-8 -*-


import os
import numpy

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.utils import assets_directory


simulated_variables = [
    'depenses_electricite_prix_unitaire',
    'depenses_gaz_prix_unitaire',
    'identifiant_menage',
    ]

for year in [2017]:
    inflators_by_year = get_inflators_by_year_energy(rebuild = True, year_range = range(2011, 2020), data_year = year)
    elasticities = get_elasticities(year)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        tax_benefit_system = tax_benefit_system,
        inflation_kwargs = inflation_kwargs,
        year = year,
        data_year = year
        )

    df_by_entity = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
    menages = df_by_entity['menage']

    assert not menages.identifiant_menage.duplicated().any(), 'Some households are duplicated'

    menages['identifiant_menage'] = menages['identifiant_menage'].astype(numpy.int64)
    menages.to_csv(os.path.join(assets_directory, 'prix', 'prix_unitaire_gaz_electricite_par_menage_{}.csv'.format(year)), sep = ',')
