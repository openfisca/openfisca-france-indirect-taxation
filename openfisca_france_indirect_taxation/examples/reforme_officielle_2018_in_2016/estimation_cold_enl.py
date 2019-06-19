# -*- coding: utf-8 -*-

# In this script we estimate from the data ENL the probability for an household
# to be cold according to several of his characteristics.
# The aime will then be to compute the effect of the reform on the likelihood of being cold

# Import general modules
from __future__ import division

import statsmodels.formula.api as smf

from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_2_homogenize_variables import \
    create_niveau_vie_quantiles

def estimate_froid():
    data_enl = create_niveau_vie_quantiles()[0]

    variables_use_baseline =[
        'pondmen',
        'quantites_combustibles_liquides',
        'quantites_electricite_selon_compteur',
        'quantites_gaz_final',
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
    df_use_baseline =survey_scenario.create_data_frame_by_entity(variables_reference, period = year)['menage']

    data_enl = data_enl.query('niveau_vie_decile < 4')
    data_enl['froid_4_criteres_3_deciles'] = (
        data_enl['froid_cout'] + data_enl['froid_isolation'] + data_enl['froid_impaye'] + data_enl['froid_installation']
        )
    data_enl['froid_4_criteres_3_deciles'] = 1 * (data_enl['froid_4_criteres_3_deciles'] > 0)

    data_enl = data_enl.query('revtot > 0')

    quantites_moyennes_combustibles_liquides = \
        (df_reference['quantites_combustibles_liquides'] * df_reference['pondmen']).sum() / df_reference['pondmen'].sum()
    quantites_moyennes_electricite = \
        (df_reference['quantites_electricite_selon_compteur'] * df_reference['pondmen']).sum() / df_reference['pondmen'].sum()
    quantites_moyennes_gaz_ville = \
        (df_reference['quantites_gaz_final'] * df_reference['pondmen']).sum() / df_reference['pondmen'].sum()

    depenses_moyennes_combustibles_liquides = \
        (data_enl['depenses_combustibles_liquides'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()
    depenses_moyennes_electricite = \
        (data_enl['depenses_electricite'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()
    depenses_moyennes_gaz_ville = \
        (data_enl['depenses_gaz_ville'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

    data_enl['quantites_combustibles_liquides'] = \
        data_enl['depenses_combustibles_liquides'] * quantites_moyennes_combustibles_liquides / depenses_moyennes_combustibles_liquides
    data_enl['quantites_electricite_selon_compteur'] = \
        data_enl['depenses_electricite'] * quantites_moyennes_electricite / depenses_moyennes_electricite
    data_enl['quantites_gaz_final'] = \
        data_enl['depenses_gaz_ville'] * quantites_moyennes_gaz_ville / depenses_moyennes_gaz_ville

    # Logisctic regression
    regressors = [
        'revtot',
        'quantites_combustibles_liquides',
        'quantites_electricite_selon_compteur',
        'quantites_gaz_final',
        'isolation_murs',
        'isolation_fenetres',
        'isolation_toit',
        'majorite_double_vitrage',
        #'brde_m2_rev_disponible',
        #'tee_10_3_deciles_rev_disponible',
        'ouest_sud',
        'rural',
        'paris',
        'surfhab_d',
        'aides_logement',
        'electricite',
        'agepr',
        'ocde10',
        #'npers',
        #'monoparental',
        ]

    regression_logit = smf.Logit(data_enl['froid_4_criteres_3_deciles'], data_enl[regressors]).fit()

    return regression_ols, regression_logit


if __name__ == "__main__":
    estimations = estimate_froid()
    regression_ols = estimations[0]
    regression_logit = estimations[1]

    print regression_logit.summary()
