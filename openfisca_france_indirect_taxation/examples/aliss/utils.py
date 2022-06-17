# -*- coding: utf-8 -*-


import numpy as np
import os
import pkg_resources
import pandas as pd


from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.build_survey_data.calibration_aliss import get_adjusted_input_data_frame


aliss_assets_reform_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'reforms',
    'aliss_assets',
    )


def build_aggreggates(variables, by = 'niveau_vie_decile', survey_scenario = None, adjusted_survey_scenario = None):
    aggregates = dict()
    reference_aggregates = dict()
    adjusted_aggregates = dict()
    for variable in variables:
        aggregates[variable] = survey_scenario.compute_aggregate(variable) / 1e9
        adjusted_aggregates[variable] = adjusted_survey_scenario.compute_aggregate(variable) / 1e9
        if not np.isfinite(survey_scenario.compute_aggregate(variable, use_baseline =True)):
            print(('variable {} aggregates is infinite').format(variable))
            reference_aggregates[variable] = (
                survey_scenario.compute_aggregate(
                    variable,
                    use_baseline =True,
                    missing_variable_default_value = 0,
                    ) / 1e9
                )
            continue
        reference_aggregates[variable] = (
            survey_scenario.compute_aggregate(variable, use_baseline =True) / 1e9
            )

    aggregates = pd.DataFrame({
        'reform': aggregates,
        'reference': reference_aggregates,
        'adjusted': adjusted_aggregates,
        })
    aggregates['reform - reference'] = aggregates.reform - aggregates.reference
    aggregates['adjusted - reform'] = aggregates.adjusted - aggregates.reform
    aggregates['adjusted - reference'] = aggregates.adjusted - aggregates.reference
    return aggregates


def build_pivot_table(variables, by = 'niveau_vie_decile', survey_scenario = None, adjusted_survey_scenario = None,
        aggfunc = 'mean'):
    pivot_table = pd.DataFrame()
    reference_pivot_table = pd.DataFrame()
    adjusted_pivot_table = pd.DataFrame()
    for variable in variables:
        pivot_table = pd.concat([
            pivot_table,
            survey_scenario.compute_pivot_table(
                values = [variable],
                columns = [by],
                aggfunc = aggfunc,
                missing_variable_default_value = 0,
                )
            ])
        reference_pivot_table = pd.concat([
            reference_pivot_table,
            survey_scenario.compute_pivot_table(
                values = [variable],
                columns = [by],
                use_baseline =True,
                aggfunc = aggfunc,
                missing_variable_default_value = 0,
                )
            ])
        adjusted_pivot_table = pd.concat([
            adjusted_pivot_table,
            adjusted_survey_scenario.compute_pivot_table(
                values = [variable],
                columns = [by],
                aggfunc = aggfunc,
                missing_variable_default_value = 0,
                )
            ])
    pivot_table = pd.concat({
        'reform': pivot_table,
        'reference': reference_pivot_table,
        'adjusted': adjusted_pivot_table,
        'reform-reference': pivot_table - reference_pivot_table,
        'adjusted-reform': adjusted_pivot_table - pivot_table,
        'adjusted-reference': adjusted_pivot_table - reference_pivot_table,
        })
    return pivot_table.reset_index().rename(columns = {'level_0': 'simulation', 'level_1': 'variable'})


def build_scenarios(data_year = 2011, reform_key = None, year = 2014):
    scenario_kwargs = dict(year = year, data_year = data_year, reform_key = reform_key)
    survey_scenario = SurveyScenario.create(**scenario_kwargs)
    #
    adjusted_scenario_kwargs = dict(scenario_kwargs)
    adjusted_scenario_kwargs.update(dict(
        data_year = None,
        input_data_frame = get_adjusted_input_data_frame(reform_key = reform_key[6:])
        ))
    adjusted_survey_scenario = SurveyScenario.create(**adjusted_scenario_kwargs)
    return survey_scenario, adjusted_survey_scenario


def get_reform(reform_key = 'ajustable'):
    if reform_key == 'ajustable':
        csv_file_path = os.path.join(aliss_assets_reform_directory, 'ajustable_aliss_reform_unprocessed_data.csv')
        dataframe = pd.read_csv(
            csv_file_path,
            index_col = 'nomf'
            )
    else:
        assert reform_key in ['sante', 'environnement', 'tva_sociale', 'mixte']
        csv_file_path = os.path.join(aliss_assets_reform_directory, 'aliss_reform_unprocessed_data.csv')
        dataframe = pd.read_csv(
            csv_file_path,
            usecols = ['nomf', reform_key],
            ).set_index('nomf')
    return dataframe.rename(columns = {reform_key: 'ajustable'})


def set_adjustable_reform(dataframe):
    csv_file_path = os.path.join(aliss_assets_reform_directory, 'ajustable_aliss_reform_unprocessed_data.csv')
    old_dataframe = get_reform()
    from pandas.util.testing import assert_index_equal
    assert_index_equal(old_dataframe.index, dataframe.index)
    assert dataframe.ajustable.isin(
        ['tva_taux_super_reduit', 'tva_taux_reduit', 'tva_taux_intermediaire', 'tva_taux_plein']
        ).all(), 'Type de taux de TVA invalide'
    dataframe.to_csv(csv_file_path)


def run_reform(reform_key = None, aggfunc = 'mean'):
    survey_scenario, adjusted_survey_scenario = build_scenarios(reform_key = reform_key)
    alimentation_domicile_hors_alcool = [
        'depenses_ht_{}'.format(key) for key in list(survey_scenario.tax_benefit_system.variables.keys())
        if key.startswith('poste_01')
        ]
    alimentation_domicile = alimentation_domicile_hors_alcool + [
        'depenses_biere',
        'depenses_vin',
        'depenses_alcools_forts'
        ]
    depenses_ht_tvas = [
        'depenses_ht_{}'.format(key) for key in list(survey_scenario.tax_benefit_system.variables.keys())
        if key.startswith('tva_taux_')
        ]
    tvas = [
        key for key in list(survey_scenario.tax_benefit_system.variables.keys())
        if key.startswith('tva_taux_')
        ] + ['tva_total']
    variables = alimentation_domicile + ['poste_agrege_01', 'poste_agrege_02', ] + depenses_ht_tvas + tvas
    aggregates = build_aggreggates(
        variables, survey_scenario = survey_scenario, adjusted_survey_scenario = adjusted_survey_scenario)
    pivot_table = build_pivot_table(
        variables, survey_scenario = survey_scenario, adjusted_survey_scenario = adjusted_survey_scenario,
        aggfunc = aggfunc)

    # Some tests
    assert (pd.DataFrame(
        aggregates.loc[aliment, 'reform'] - aggregates.loc[aliment, 'reform'] for aliment in alimentation_domicile
        ) == 0).all().all()

    assert aggregates.loc['poste_agrege_02', 'reform'] - aggregates.loc['poste_agrege_02', 'reference'] < 1e-7

    return aggregates, pivot_table
