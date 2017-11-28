# -*- coding: utf-8 -*-

# In this script we estimate from the data ENL the probability for an household
# to be cold according to several of his characteristics.
# The aime will then be to compute the effect of the reform on the likelihood of being cold

# Import general modules
from __future__ import division

import statsmodels.formula.api as smf
import pandas as pd

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_2_homogenize_variables import \
    create_niveau_vie_quantiles
from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem


def estimate_froid():
    data_enl = create_niveau_vie_quantiles()[0]
            
    data_enl = data_enl.query('niveau_vie_decile < 4')
    data_enl['froid_4_criteres_3_deciles'] = (
        data_enl['froid_cout'] + data_enl['froid_isolation'] + data_enl['froid_impaye'] + data_enl['froid_installation']
        )
    data_enl['froid_4_criteres_3_deciles'] = 1 * (data_enl['froid_4_criteres_3_deciles'] > 0)
    
    data_enl = data_enl.query('revtot > 0')
    data_enl['revtot_2'] = data_enl['revtot'] ** 2
    
    data_enl['part_energies_revtot'] = data_enl['depenses_energies'] / data_enl['revtot']

    for i in range(0, 5):
        data_enl['strate_{}'.format(i)] = 0
        data_enl.loc[data_enl['strate'] == i, 'strate_{}'.format(i)] = 1

    data_enl['combustibles_liquides'] = 1 * (data_enl['depenses_combustibles_liquides'] > 0)
    data_enl['gaz_ville'] = 1 * (data_enl['depenses_gaz_ville'] > 0)

    data_enl['majorite_double_vitrage'] = 1 * (data_enl['majorite_double_vitrage'] == 1)
    data_enl['mauvaise_isolation_fenetres'] = 1 * (data_enl['isolation_fenetres'] == 1)
    data_enl['bonne_isolation_murs'] = 1 * (data_enl['isolation_murs'] == 1)
    data_enl['mauvaise_isolation_murs'] = 1 * (data_enl['isolation_murs'] == 3)


    # Compute quantities from expenditures
    tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
    legislation_json = tax_benefit_system.get_legislation()

    dict_prix_combustibles_liquides = \
        legislation_json['children']['tarification_energie_logement']['children']['prix_fioul_domestique']['children']['prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre']

    df_prix = pd.DataFrame.from_dict(dict_prix_combustibles_liquides['values'])
    df_prix['start'] = df_prix['start'].str[:4]
    df_prix = df_prix.set_index('start')

    prix_combustibles_liquides = df_prix['value']['2013']

    data_enl['quantites_combustibles_liquides'] = (
        data_enl['depenses_combustibles_liquides'] / prix_combustibles_liquides
        )

    # Quantités gaz
    dict_prix_fixe_gaz_base = \
        legislation_json['children']['tarification_energie_logement']['children']['tarif_fixe_gdf_ttc']['children']['base_0_1000']
    df_prix = pd.DataFrame.from_dict(dict_prix_fixe_gaz_base['values'])
    df_prix['start'] = df_prix['start'].str[:4]
    df_prix = df_prix.set_index('start')
    prix_fixe_base = df_prix['value']['2013']

    dict_prix_unitaire_gaz_base = \
        legislation_json['children']['tarification_energie_logement']['children']['prix_unitaire_gdf_ttc']['children']['prix_kwh_base_ttc']
    df_prix = pd.DataFrame.from_dict(dict_prix_unitaire_gaz_base['values'])
    df_prix['start'] = df_prix['start'].str[:4]
    df_prix = df_prix.set_index('start')
    prix_unitaire_base = df_prix['value']['2013']

    data_enl['quantites_base'] = (
        (data_enl['depenses_gaz_ville'] - prix_fixe_base)
        / prix_unitaire_base
        )


    dict_prix_fixe_gaz_b0 = \
        legislation_json['children']['tarification_energie_logement']['children']['tarif_fixe_gdf_ttc']['children']['b0_1000_6000']
    df_prix = pd.DataFrame.from_dict(dict_prix_fixe_gaz_b0['values'])
    df_prix['start'] = df_prix['start'].str[:4]
    df_prix = df_prix.set_index('start')
    prix_fixe_base = df_prix['value']['2013']

    dict_prix_unitaire_gaz_b0 = \
        legislation_json['children']['tarification_energie_logement']['children']['prix_unitaire_gdf_ttc']['children']['prix_kwh_b0_ttc']
    df_prix = pd.DataFrame.from_dict(dict_prix_unitaire_gaz_b0['values'])
    df_prix['start'] = df_prix['start'].str[:4]
    df_prix = df_prix.set_index('start')
    prix_unitaire_base = df_prix['value']['2013']

    data_enl['quantites_b0'] = (
        (data_enl['depenses_gaz_ville'] - prix_fixe_base)
        / prix_unitaire_base
        )


    dict_prix_fixe_gaz_1 = \
        legislation_json['children']['tarification_energie_logement']['children']['tarif_fixe_gdf_ttc']['children']['b1_6_30000']
    df_prix = pd.DataFrame.from_dict(dict_prix_fixe_gaz_1['values'])
    df_prix['start'] = df_prix['start'].str[:4]
    df_prix = df_prix.set_index('start')
    prix_fixe_base = df_prix['value']['2013']

    dict_prix_unitaire_gaz_1 = \
        legislation_json['children']['tarification_energie_logement']['children']['prix_unitaire_gdf_ttc']['children']['prix_kwh_b1_ttc']
    df_prix = pd.DataFrame.from_dict(dict_prix_unitaire_gaz_1['values'])
    df_prix['start'] = df_prix['start'].str[:4]
    df_prix = df_prix.set_index('start')
    prix_unitaire_base = df_prix['value']['2013']

    data_enl['quantites_b1'] = (
        (data_enl['depenses_gaz_ville'] - prix_fixe_base)
        / prix_unitaire_base
        )

    data_enl['quantites_gaz_ville'] = (
        data_enl['quantites_base'] * (data_enl['quantites_base'] > data_enl['quantites_b0']) * (data_enl['quantites_base'] > data_enl['quantites_b1'])
        + data_enl['quantites_b0'] * (data_enl['quantites_b0'] > data_enl['quantites_base']) * (data_enl['quantites_b0'] > data_enl['quantites_b1'])
        + data_enl['quantites_b1'] * (data_enl['quantites_b1'] > data_enl['quantites_base']) * (data_enl['quantites_b1'] > data_enl['quantites_b0'])
        )
    
    data_enl['quantites_gaz_ville'] = 1 * (data_enl['quantites_gaz_ville'] > 0)

    data_enl['quantites_kwh'] = 9.96 * data_enl['quantites_combustibles_liquides'] + data_enl['quantites_gaz_ville']






    regressors = [
        #'quantites_kwh',
        #'revdecm',
        'revtot',
        #'quantites_kwh',
        #'part_energies_revtot',
        #'quantites_combustibles_liquides',
        'quantites_gaz_ville',
        #'depenses_gaz_ville',
        #'depenses_electricite',
        #'depenses_energies',
        'quantites_combustibles_liquides',
        #'quantites_electricite_selon_compteur',
        #'quantites_gaz_final',
        #'isolation_murs',
        'mauvaise_isolation_fenetres',
        'mauvaise_isolation_murs',
        'bonne_isolation_murs',        
        #'isolation_toit',
        'majorite_double_vitrage',
        #'niveau_de_vie',
        #'brde_m2_rev_disponible',
        #'tee_10_3_deciles_rev_disponible',
        'ouest_sud',
        #'rural',
        #'paris',
        'surfhab_d',
        'aides_logement',
        #'electricite',
        'agepr',
        'ocde10',
        'bat_av_49',
        'bat_49_74',
        'log_indiv',
        #'npers',
        #'monoparental',
        'combustibles_liquides',
        'gaz_ville',
        'strate_0',
        'strate_1',
        'strate_2',
        'strate_3',
        #'strate',
        #'depenses_tot',
        ]


    regression_logit = smf.Logit(data_enl['froid_4_criteres_3_deciles'], data_enl[regressors]).fit()
    
    return regression_logit


if __name__ == "__main__":
    regression_logit = estimate_froid()
    print regression_logit.summary()
    print regression_logit.get_margeff().summary()

