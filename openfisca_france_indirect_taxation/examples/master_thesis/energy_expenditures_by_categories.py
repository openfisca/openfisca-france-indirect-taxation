# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

import pandas

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_line, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

#
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
#del inflation_kwargs['inflator_by_variable']['somme_coicop12']

simulated_variables = ['depenses_carburants', 'depenses_energies_totales', 'depenses_energies_logement'] #['depenses_energies', 'depenses_energies_logement', 'poste_coicop_722']

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    #inflation_kwargs = inflation_kwargs,
    #reform_key = 'taxe_carbone',
    year = year,
    data_year = data_year
    )
for category in ['niveau_vie_decile']: #['niveau_vie_decile', 'age_group_pr', 'strate_agrege']
    df = dataframe_by_group(survey_scenario, category, simulated_variables, reference = True)
    df.rename(columns = {'depenses_energies_totales': 'Total energy expenditures',
        'depenses_energies_logement': 'Housing energy expenditures',
        'depenses_carburants': 'Fuel expenditures'},
        inplace = True)

    # Réalisation de graphiques
    graph_builder_line(df)
    #save_dataframe_to_graph(df, 'Expenditures/energy_expenditures_by_{}.csv'.format(category))
