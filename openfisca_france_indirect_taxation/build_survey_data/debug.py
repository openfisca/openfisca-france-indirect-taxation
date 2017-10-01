# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


simulated_variables = [
    'depenses_essence_ajustees_cce_2014_2016', 
    'depenses_essence',
    'depenses_diesel_ajustees_cce_2014_2016',
    'depenses_diesel',
    #'depenses_essence',
    #'combustibles_liquides_ticpe',
    'diesel_ticpe',
    'emissions_CO2_carburants',
    #'depenses_tot',
    #'depenses_electricite',
    #'depenses_carburants',
    ]

year = 2014
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
elasticities = get_elasticities(data_year)

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    #inflation_kwargs = inflation_kwargs,
    reform_key = 'cce_2016_in_2014',
    year = year,
    data_year = data_year
    )


indiv_df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

for category in ['niveau_vie_decile']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)

print indiv_df['diesel_ticpe'].mean()
print indiv_df['emissions_CO2_carburants'].mean()

"""
print indiv_df['brde_m2_depenses_tot'].mean()
print indiv_df['brde_transports_depenses_tot'].mean()


#for category in ['niveau_vie_decile']:
#    df = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)


print indiv_df['rev_apres_loyer'].mean()
print indiv_df['rev_disponible'].mean()
print indiv_df['poste_04_1_1_1_1'].mean()

print indiv_df['revtot'].mean()
print indiv_df['rev_disponible'].mean()
print indiv_df['rev_disp_loyerimput'].mean()
print indiv_df['depenses_tot'].mean()




print indiv_df['precarite_energetique_3_indicateurs'].mean()


print indiv_df['brde'].mean()
print indiv_df['brde_bis'].mean()


liste = survey_scenario.tax_benefit_system.column_by_name.keys()


print data_frame['ident_men'].dtype
print data_matched['ident_men'].dtype

year_data = 2011
year_calage = 2011
"""