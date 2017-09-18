# -*- coding: utf-8 -*-

from __future__ import division

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


simulated_variables = [
    'pondmen',
    'emissions_CO2_energies_totales',
    'emissions_CO2_gaz_ville',
    'emissions_CO2_gaz_liquefie'
    ]

year = 2005
data_year = 2005

#inflators_by_year = get_inflators_by_year_energy(rebuild = True)
#inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

survey_scenario = SurveyScenario.create(
    #inflation_kwargs = inflation_kwargs,
    year = year,
    data_year = data_year
    )

for category in ['niveau_vie_decile']:
    #df = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)
    indiv_df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']


quantites_gpl = sum((indiv_df['quantites_gaz_liquefie'] * indiv_df['pondmen'])) / sum(indiv_df['pondmen'])
quantites_gaz_ville = sum((indiv_df['quantites_gaz_contrat_optimal'] * indiv_df['pondmen'])) / sum(indiv_df['pondmen'])

depenses_gpl = sum((indiv_df['depenses_gaz_liquefie'] * indiv_df['pondmen'])) / sum(indiv_df['pondmen'])
depenses_gaz_ville = sum((indiv_df['depenses_gaz_ville'] * indiv_df['pondmen'])) / sum(indiv_df['pondmen'])

emissions_gpl = sum((indiv_df['emissions_CO2_gaz_liquefie'] * indiv_df['pondmen'])) / sum(indiv_df['pondmen'])
emissions_gaz_ville = sum((indiv_df['emissions_CO2_gaz_ville'] * indiv_df['pondmen'])) / sum(indiv_df['pondmen'])



from openfisca_france_indirect_taxation.utils import get_input_data_frame
df = get_input_data_frame(year)
print df['strate']

df_postes = []
df_columns = df.columns.tolist()
for element in df_columns:
    if element[:5] == 'poste':
        df_postes.append(element)


bibi = coicop_poste_bdf.dropna()

liste = survey_scenario.tax_benefit_system.column_by_name.keys()


import pandas as pd

year = 2005
data_year = 2005
year_calage = 2005 
year_data = 2005

data_frame_bis = data_frame.copy()
df_ident_men = pd.DataFrame({'ident_men' : range(0,len(data_frame_bis))})
bibi = pd.concat([data_frame_bis, df_ident_men])


data_frame_bis['ident_men'] = 0
data_frame_bis['ident_men'] = range(0,len(data_frame_bis))
print data_frame_bis['ident_men']
data_frame_bis = data_frame_bis.set_index('ident_men')
list_bibi = bibi['ident_men'].values.tolist()

