# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


simulated_variables = [
    'rev_apres_loyer' ,   
    #'loyer_impute',
    #'loyer_impute',
    #'poste_04_1_1_1_1'
    'precarite_energetique_3_indicateurs',
    #'brde',
    #'brde_bis',
    'revtot',
    'rev_disponible',
    'rev_disp_loyerimput',
    'depenses_tot',
    'poste_04_1_1_1_1'
    ]

year = 2014
data_year = 2011

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

survey_scenario = SurveyScenario.create(
    #elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    #reform_key = 'rattrapage_diesel',
    year = year,
    data_year = data_year
    )


indiv_df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
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
