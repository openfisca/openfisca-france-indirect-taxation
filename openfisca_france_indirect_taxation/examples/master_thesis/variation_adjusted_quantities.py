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
for reforme in ['taxes_carburants', 'taxe_carbone', 'cce_2014_2015', 'cce_2014_2016']:
    simulated_variables = [
        'quantites_diesel',
        'quantites_essence',
        'quantites_electricite_selon_compteur',
        'quantites_fioul_domestique',
        'quantites_gaz_contrat_optimal',
        'quantites_diesel_ajustees_{}'.format(reforme),
        'quantites_essence_ajustees_{}'.format(reforme),
        'quantites_electricite_ajustees_{}'.format(reforme),
        'quantites_gaz_ajustees_{}'.format(reforme),
        'quantites_fioul_domestique_ajustees_{}'.format(reforme),
        'pondmen',
        ]

    if reforme[:3] != 'cce':
        survey_scenario = SurveyScenario.create(
            elasticities = elasticities,
            inflation_kwargs = inflation_kwargs,
            reform_key = '{}'.format(reforme),
            year = year,
            data_year = data_year
            )
    else:
        survey_scenario = SurveyScenario.create(
            elasticities = elasticities,
            inflation_kwargs = inflation_kwargs,
            reform_key = 'contribution_climat_energie_reforme',
            year = year,
            data_year = data_year
            )

    df_by_entity = survey_scenario.create_data_frame_by_entity_key_plural(simulated_variables)
    menages = df_by_entity['menages']

    variations_quantites['diesel_{}'.format(reforme)] = (
        (menages['quantites_diesel_ajustees_{}'.format(reforme)] - menages['quantites_diesel']) *
        menages['pondmen']
        ).sum() / 1e06
    variations_quantites['essence_{}'.format(reforme)] = (
        (menages['quantites_essence_ajustees_{}'.format(reforme)] - menages['quantites_essence']) *
        menages['pondmen']
        ).sum() / 1e06

    if reforme != 'taxes_carburants':
        variations_quantites['gaz_{}'.format(reforme)] = (
            (menages['quantites_gaz_ajustees_{}'.format(reforme)] - menages['quantites_gaz_contrat_optimal']) *
            menages['pondmen']
            ).sum() / 1e06
        variations_quantites['fioul_domestique_{}'.format(reforme)] = (
            (menages['quantites_fioul_domestique_ajustees_{}'.format(reforme)] -
            menages['quantites_fioul_domestique']) *
            menages['pondmen']
            ).sum() / 1e06

    if reforme == 'taxe_carbone':
        variations_quantites['electricite_{}'.format(reforme)] = (
            (menages['quantites_electricite_ajustees_{}'.format(reforme)] -
            menages['quantites_electricite_selon_compteur']) *
            menages['pondmen']
            ).sum() / 1e06
