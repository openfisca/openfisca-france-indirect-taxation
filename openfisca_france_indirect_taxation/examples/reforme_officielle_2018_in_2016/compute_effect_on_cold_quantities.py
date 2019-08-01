# -*- coding: utf-8 -*-

# In this script we take the estimates obtained in the estimation with the matched sample,
# and we compute the probabilities of being cold for BdF households.
# We then replicate this with adjusted quantities after the reform and do the difference.


import numpy as np


from openfisca_france_indirect_taxation.surveys import SurveyScenario
# from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.reforme_officielle_2018_in_2016.variation_in_cold import estimate_froid

logit = estimate_froid()[1]
params = logit.params
params = params.to_frame().T
explanatory_vars = params.columns.tolist()


def effect_reform_cold():
    cold = dict()
    variables_use_baseline = [
        'agepr',
        'aides_logement',
        'brde_m2_rev_disponible',
        'tee_10_3_deciles_rev_disponible',
        'quantites_combustibles_liquides',
        'quantites_electricite_selon_compteur',
        'quantites_gaz_final',
        'dip14pr',
        'electricite',
        'combustibles_liquides',
        'froid_4_criteres',
        'gaz_ville',
        'isolation_fenetres',
        'isolation_murs',
        'isolation_toit',
        'majorite_double_vitrage',
        'nactifs',
        'nenfants',
        'niveau_vie_decile',
        'niveau_de_vie',
        'npers',
        'ocde10',
        'ouest_sud',
        'paris',
        'petite_ville',
        'pondmen',
        'rev_disponible',
        'rural',
        'surfhab_d',
        'typmen',
        'strate',
        ]

    variables_reforme = [
        'agepr',
        'aides_logement',
        'cheques_energie_officielle_2018_in_2016',
        'brde_m2_rev_disponible',
        'tee_10_3_deciles_rev_disponible',
        'dip14pr',
        'electricite',
        'combustibles_liquides',
        'froid_4_criteres',
        'gaz_ville',
        'isolation_fenetres',
        'isolation_murs',
        'isolation_toit',
        'majorite_double_vitrage',
        'nactifs',
        'nenfants',
        'niveau_vie_decile',
        'niveau_de_vie',
        'npers',
        'ocde10',
        'ouest_sud',
        'paris',
        'pertes_financieres_avant_redistribution_officielle_2018_in_2016',
        'petite_ville',
        'pondmen',
        'quantites_combustibles_liquides_officielle_2018_in_2016',
        'quantites_electricite_selon_compteur',
        'quantites_gaz_final_officielle_2018_in_2016',
        'reste_transferts_neutre_officielle_2018_in_2016',
        'rev_disponible',
        'rural',
        'surfhab_d',
        'typmen',
        'strate',
        ]

    inflators_by_year = get_inflators_by_year_energy(rebuild = False)
    year = 2016
    data_year = 2011
    # elasticities = get_elasticities(data_year)
    elasticities = get_elasticities_aidsills(data_year, True)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = 'officielle_2018_in_2016',
        year = year,
        data_year = data_year
        )

    df_use_baseline = survey_scenario.create_data_frame_by_entity(variables_reference, period = year)['menage']
    df_reforme = survey_scenario.create_data_frame_by_entity(variables_reforme, period = year)['menage']

    # On passe en kWh
    df_reference['quantites_combustibles_liquides'] = 9.96 * df_reference['quantites_combustibles_liquides']
    df_reference['quantites_kwh'] = (
        df_reference['quantites_combustibles_liquides']
        + df_reference['quantites_gaz_final']
        + df_reference['quantites_electricite_selon_compteur']
        )

    # Reference case :
    df_use_baseline = df_reference.query('rev_disponible > 0')

    df_reference['monoparental'] = 0
    df_reference.loc[df_reference['typmen'] == 2, 'monoparental'] = 1
    for i in range(0, 5):
        df_reference['strate_{}'.format(i)] = 0
        df_reference.loc[df_reference['strate'] == i, 'strate_{}'.format(i)] = 1

    df_reference['predict_log_odds'] = 0
    for var in explanatory_vars:
        df_reference['predict_log_odds'] += df_reference[var] * params[var][0]

    df_reference['predict_odds'] = np.exp(df_reference['predict_log_odds'])
    df_reference['predict_proba'] = df_reference['predict_odds'] / (1 + df_reference['predict_odds'])
    df_reference.loc[df_reference['niveau_vie_decile'] > 3, 'predict_proba'] = 0

    # Before revenue recycling :
    df_reforme.rename(
        columns = {
            'quantites_combustibles_liquides_officielle_2018_in_2016': 'quantites_combustibles_liquides',
            'quantites_gaz_final_officielle_2018_in_2016': 'quantites_gaz_final',
            },
        inplace = True,
        )

    df_reforme['quantites_combustibles_liquides'] = 9.96 * df_reforme['quantites_combustibles_liquides']
    df_reforme['quantites_kwh'] = (
        df_reforme['quantites_combustibles_liquides']
        + df_reforme['quantites_gaz_final']
        + df_reforme['quantites_electricite_selon_compteur']
        )

    df_reforme = df_reforme.query('rev_disponible > 0')
    df_reforme['monoparental'] = 0
    df_reforme.loc[df_reforme['typmen'] == 2, 'monoparental'] = 1
    for i in range(0, 5):
        df_reforme['strate_{}'.format(i)] = 0
        df_reforme.loc[df_reforme['strate'] == i, 'strate_{}'.format(i)] = 1

    df_reforme['predict_log_odds'] = 0
    for var in explanatory_vars:
        df_reforme['predict_log_odds'] += df_reforme[var] * params[var][0]

    df_reforme['predict_odds'] = np.exp(df_reforme['predict_log_odds'])
    df_reforme['predict_proba'] = df_reforme['predict_odds'] / (1 + df_reforme['predict_odds'])
    df_reforme.loc[df_reforme['niveau_vie_decile'] > 3, 'predict_proba'] = 0

    # After revenue recycling :
    df_reforme_after = df_reforme.copy()
    df_reforme_after['rev_disponible'] = (
        df_reforme_after['rev_disponible']
        + df_reforme_after['reste_transferts_neutre_officielle_2018_in_2016']
        + df_reforme_after['cheques_energie_officielle_2018_in_2016']
        - df_reforme_after['pertes_financieres_avant_redistribution_officielle_2018_in_2016']
        )

    df_reforme_after['predict_log_odds'] = 0
    for var in explanatory_vars:
        df_reforme_after['predict_log_odds'] += df_reforme_after[var] * params[var][0]

    df_reforme_after['predict_odds'] = np.exp(df_reforme['predict_log_odds'])
    df_reforme_after['predict_proba'] = df_reforme_after['predict_odds'] / (1 + df_reforme_after['predict_odds'])
    df_reforme_after.loc[df_reforme_after['niveau_vie_decile'] > 3, 'predict_proba'] = 0

    # Results
    cold['number_cold_reference'] = (df_reference['predict_proba'] * df_reference['pondmen']).sum()
    cold['number_cold_reforme_before'] = (df_reforme['predict_proba'] * df_reforme['pondmen']).sum()
    cold['number_cold_reforme_after'] = (df_reforme_after['predict_proba'] * df_reforme_after['pondmen']).sum()

    cold['increase_number_cold_before'] = cold['number_cold_reforme_before'] - cold['number_cold_reference']
    cold['increase_number_cold_after'] = cold['number_cold_reforme_after'] - cold['number_cold_reference']

    cold['share_cold_reference'] = cold['number_cold_reference'] / df_reference['pondmen'].sum() * 100
    cold['share_cold_reforme_before'] = cold['number_cold_reforme_before'] / df_reforme['pondmen'].sum() * 100
    cold['share_cold_reforme_after'] = cold['number_cold_reforme_after'] / df_reforme['pondmen'].sum() * 100

    cold['increase_share_cold_before'] = (cold['share_cold_reforme_before'] - cold['share_cold_reference']) / cold['share_cold_reference'] * 100
    cold['increase_share_cold_after'] = (cold['share_cold_reforme_after'] - cold['share_cold_reference']) / cold['share_cold_reference'] * 100

    return cold


if __name__ == "__main__":
    cold = effect_reform_cold()
    print(logit.summary())
