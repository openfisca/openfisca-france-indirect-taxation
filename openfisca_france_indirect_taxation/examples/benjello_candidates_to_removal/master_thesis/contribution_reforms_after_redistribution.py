# -*- coding: utf-8 -*-


import pandas


from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_line_percent, graph_builder_bar, \
    save_dataframe_to_graph
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy

# Simulate contribution to fuel tax reform by categories
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2014_2015', 'cce_2014_2016']:
    simulated_variables = [
        'difference_contribution_totale_{}_tva_plein_reduit_super_reduit'.format(reforme),
        'difference_contribution_totale_{}_tva_plein'.format(reforme),
        'pondmen'
        ]

    if reforme[:3] != 'cce':
        survey_scenario = SurveyScenario.create(
            elasticities = elasticities,
            inflation_kwargs = inflation_kwargs,
            reform = '{}'.format(reforme),
            year = year,
            data_year = data_year
            )
    else:
        survey_scenario = SurveyScenario.create(
            elasticities = elasticities,
            inflation_kwargs = inflation_kwargs,
            reform = 'contribution_climat_energie_reforme',
            year = year,
            data_year = data_year
            )

    for category in ['niveau_vie_decile']:
        pivot_table = pandas.DataFrame()
        for values in simulated_variables:
            pivot_table = pandas.concat([
                pivot_table,
                survey_scenario.compute_pivot_table(values = [values], columns = ['{}'.format(category)])
                ])
        df = pivot_table.T
        save_dataframe_to_graph(
            df, 'Contributions_reforme/TVA/contribution_{}_apres_redistribution_reforme_tva.csv'.format(reforme)
            )

        # Réalisation de graphiques
        graph_builder_bar(df)

        df_by_entity = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
        menages = df_by_entity['menage']

        sum_reduit = (
            menages['difference_contribution_totale_{}_tva_plein_reduit_super_reduit'.format(reforme)]
            * menages['pondmen']
            ).sum()

        sum_plein = (
            menages['difference_contribution_totale_{}_tva_plein'.format(reforme)]
            * menages['pondmen']
            ).sum()

        print(reforme, sum_reduit / menages['pondmen'].sum())
        print(reforme, sum_plein / menages['pondmen'].sum())
