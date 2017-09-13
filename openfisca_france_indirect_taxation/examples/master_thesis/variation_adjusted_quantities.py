# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

# Simulate contribution to fuel tax reform by categories
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
del inflation_kwargs['inflator_by_variable']['somme_coicop12']

variations_quantites = dict()
for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']:
    simulated_variables_reference = [
        'quantites_diesel',
        'quantites_essence',
        'quantites_electricite_selon_compteur',
        'quantites_fioul_domestique',
        'quantites_gaz_contrat_optimal',
        'pondmen',
        ]

    simulated_variables_reform = [
        'quantites_diesel',
        'quantites_essence',
        'quantites_electricite_selon_compteur_ajustees_taxe_carbone',
        'quantites_fioul_domestique',
        'quantites_gaz_contrat_optimal_ajustees_{}'.format(reforme),
        'pondmen',
        ]

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = '{}'.format(reforme),
        year = year,
        data_year = data_year
        )

    indiv_df_reform = survey_scenario.create_data_frame_by_entity(simulated_variables_reform, period = year)
    indiv_df_reference = survey_scenario.create_data_frame_by_entity(simulated_variables_reference,
        reference = True, period = year)

    menages_reform = indiv_df_reform['menages']
    menages_reference = indiv_df_reference['menages']

    variations_quantites['diesel_{}'.format(reforme)] = (
        (menages_reform['quantites_diesel'] - menages_reference['quantites_diesel']) *
        menages_reform['pondmen']
        ).sum() / 1e06
    variations_quantites['essence_{}'.format(reforme)] = (
        (menages_reform['quantites_essence'] - menages_reference['quantites_essence']) *
        menages_reform['pondmen']
        ).sum() / 1e06

    if reforme != 'rattrapage_diesel':
        variations_quantites['gaz_{}'.format(reforme)] = (
            (menages_reform['quantites_gaz_contrat_optimal_ajustees_{}'.format(reforme)] -
            menages_reference['quantites_gaz_contrat_optimal']) *
            menages_reform['pondmen']
            ).sum() / 1e06
        variations_quantites['fioul_domestique_{}'.format(reforme)] = (
            (menages_reform['quantites_fioul_domestique'] -
            menages_reference['quantites_fioul_domestique']) *
            menages_reform['pondmen']
            ).sum() / 1e06

    if reforme == 'taxe_carbone':
        variations_quantites['electricite_{}'.format(reforme)] = (
            (menages_reform['quantites_electricite_selon_compteur_ajustees_{}'.format(reforme)] -
            menages_reference['quantites_electricite_selon_compteur']) *
            menages_reform['pondmen']
            ).sum() / 1e06
