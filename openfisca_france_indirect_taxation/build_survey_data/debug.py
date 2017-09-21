# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


simulated_variables = [
    'depenses_diesel_ajustees_rattrapage_diesel',
    'identifiant_menage',
    ]

year = 2011
data_year = 2011

#inflators_by_year = get_inflators_by_year_energy(rebuild = True)
#inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

survey_scenario = SurveyScenario.create(
    #elasticities = elasticities,
    #inflation_kwargs = inflation_kwargs,
    reform_key = 'rattrapage_diesel',
    year = year,
    )


indiv_df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

indiv_df['depenses_assurance_sante'].mean()
indiv_df['depenses_assurance_transport'].mean()
indiv_df['depenses_autres_assurances'].mean()


#for category in ['niveau_vie_decile']:
#    df = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)


liste = survey_scenario.tax_benefit_system.column_by_name.keys()


print data_frame['ident_men'].dtype
print data_matched['ident_men'].dtype

year_data = 2011
year_calage = 2011
