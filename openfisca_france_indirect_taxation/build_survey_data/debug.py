# -*- coding: utf-8 -*-

from __future__ import division

#from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


simulated_variables = [
    'pondmen',
    #'ident_men',
    'identifiant_menage'
    ]

year = 2011
data_year = 2011

#inflators_by_year = get_inflators_by_year_energy(rebuild = True)
#inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

survey_scenario = SurveyScenario.create(
    #inflation_kwargs = inflation_kwargs,
    year = year,
    data_year = data_year
    )

indiv_df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

#for category in ['niveau_vie_decile']:
    #df = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)
    

liste = survey_scenario.tax_benefit_system.column_by_name.keys()


print aggregates_data_frame['identifiant_menage']


