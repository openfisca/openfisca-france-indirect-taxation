# -*- coding: utf-8 -*-

# In this script we take the estimates obtained in the estimation with the matched sample,
# and we compute the probabilities of being cold for BdF households.
# We then replicate this with adjusted quantities after the reform and do the difference.

# Import general modules
from __future__ import division

import numpy as np

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.reforme_officielle_2018_in_2016.variation_in_cold import estimate_froid

logit = estimate_froid()[1]
params = logit.params
params = params.to_frame().T
explanatory_vars = params.columns.tolist()

def effect_reform_cold():
    cold = dict()
    variables_reference = [
        'agepr',
        'aides_logement',
        'brde_m2_rev_disponible',
        'tee_10_3_deciles_rev_disponible',
        'quantites_combustibles_liquides',
        'quantites_electricite_selon_compteur',
        'quantites_gaz_final',
        'dip14pr',
        'electricite',
        'froid_4_criteres_3_deciles',
        'gaz_ville',
        'isolation_fenetres',
        'isolation_murs',
        'isolation_toit',
        'majorite_double_vitrage',
        'nactifs',
        'nenfants',
        'niveau_vie_decile',
        'npers',
        'ocde10',
        'ouest_sud',
        'paris',
        'petite_ville',
        'pondmen',
        'revtot',
        'rural',
        'surfhab_d',
        'typmen',
        ]

    variables_reforme = [
        'agepr',
        'aides_logement',
        'cheques_energie_officielle_2018_in_2016',
        'brde_m2_rev_disponible',
        'tee_10_3_deciles_rev_disponible',
        'dip14pr',
        'electricite',
        'froid_4_criteres_3_deciles',
        'gaz_ville',
        'isolation_fenetres',
        'isolation_murs',
        'isolation_toit',
        'majorite_double_vitrage',
        'nactifs',
        'nenfants',
        'niveau_vie_decile',
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
        'revtot',
        'rural',
        'surfhab_d',
        'typmen',
        ]

    inflators_by_year = get_inflators_by_year_energy(rebuild = False)
    year = 2016
    data_year = 2011
    elasticities = get_elasticities(data_year)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = 'officielle_2018_in_2016',
        year = year,
        data_year = data_year
        )
    
    df_reference = survey_scenario.create_data_frame_by_entity(variables_reference, period = year)['menage']
    df_reforme = survey_scenario.create_data_frame_by_entity(variables_reforme, period = year)['menage']
    
    # Reference case :
    df_reference = df_reference.query('revtot > 0')

    df_reference['monoparental'] = 0
    df_reference.loc[df_reference['typmen'] == 2, 'monoparental'] = 1

    df_reference['predict_log_odds'] = 0
    for var in explanatory_vars:
        df_reference['predict_log_odds'] += df_reference[var] * params[var][0]

    df_reference['predict_odds'] = np.exp(df_reference['predict_log_odds'])
    df_reference['predict_proba'] = df_reference['predict_odds'] / (1 + df_reference['predict_odds'])
    df_reference.loc[df_reference['niveau_vie_decile'] > 3, 'predict_proba'] = 0

    # Official reform :
    df_reforme.rename(
        columns = {
            'quantites_combustibles_liquides_officielle_2018_in_2016': 'quantites_combustibles_liquides',
            'quantites_gaz_final_officielle_2018_in_2016': 'quantites_gaz_final',
                   },
        inplace = True,
        )

    df_reforme = df_reforme.query('revtot > 0')
    df_reforme['revtot'] = (
        df_reforme['revtot'] +
        df_reforme['reste_transferts_neutre_officielle_2018_in_2016'] +
        df_reforme['cheques_energie_officielle_2018_in_2016'] -
        df_reforme['pertes_financieres_avant_redistribution_officielle_2018_in_2016']
        )
    df_reforme['monoparental'] = 0
    df_reforme.loc[df_reforme['typmen'] == 2, 'monoparental'] = 1

    df_reforme['predict_log_odds'] = 0
    for var in explanatory_vars:
        df_reforme['predict_log_odds'] += df_reforme[var] * params[var][0]

    df_reforme['predict_odds'] = np.exp(df_reforme['predict_log_odds'])
    df_reforme['predict_proba'] = df_reforme['predict_odds'] / (1 + df_reforme['predict_odds'])
    df_reforme.loc[df_reforme['niveau_vie_decile'] > 3, 'predict_proba'] = 0
    
    # Results
    cold['number_cold_reference'] = (df_reference['predict_proba'] * df_reference['pondmen']).sum()
    cold['number_cold_reforme'] = (df_reforme['predict_proba'] * df_reforme['pondmen']).sum()
    cold['increase_number_cold'] = cold['number_cold_reforme'] - cold['number_cold_reference']
    
    cold['share_cold_reference'] = cold['number_cold_reference'] / df_reference['pondmen'].sum() * 100
    cold['share_cold_reforme'] = cold['number_cold_reforme'] / df_reforme['pondmen'].sum() * 100
    cold['increase_share_cold'] = (cold['share_cold_reforme'] - cold['share_cold_reference']) / cold['share_cold_reference'] * 100

    return cold


if __name__ == "__main__":
    cold = effect_reform_cold()
    print logit.summary()
