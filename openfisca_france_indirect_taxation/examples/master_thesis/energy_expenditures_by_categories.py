# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division


# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

year = 2016
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
elasticities = get_elasticities(data_year)

simulated_variables = ['depenses_energies_totales', 'depenses_energies_logement', 'depenses_carburants_corrigees'] #['depenses_energies', 'depenses_energies_logement', 'poste_coicop_722']

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = 'officielle_2018_in_2016',
    year = year,
    data_year = data_year
    )
for category in ['niveau_vie_decile', 'age_group_pr', 'strate']:
    df = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)
    df.rename(columns = {'depenses_energies_totales': 'Total energy expenditures',
        'depenses_energies_logement': 'Housing energy expenditures',
        'depenses_carburants_corrigees': 'Fuel expenditures'},
        inplace = True)

    # Réalisation de graphiques
    graph_builder_bar(df, False)
    save_dataframe_to_graph(df, 'Expenditures/energy_expenditures_by_{}.csv'.format(category))
