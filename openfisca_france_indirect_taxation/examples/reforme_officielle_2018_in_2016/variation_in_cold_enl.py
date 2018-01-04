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
    
    data_enl['agepr_2'] = data_enl['agepr'] ** 2
    
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
    
    data_enl['quantites_gaz_ville'] = (data_enl['quantites_gaz_ville'] > 0) * data_enl['quantites_gaz_ville']

    data_enl['quantites_kwh'] = 9.96 * data_enl['quantites_combustibles_liquides'] + data_enl['quantites_gaz_ville']

    data_enl['proprietaire'] = 0
    data_enl.loc[data_enl.stalog.isin([1,2]), 'proprietaire'] = 1
    
    data_enl['etudiant'] = 0
    data_enl.loc[data_enl.situapr == 3, 'etudiant'] = 1
    
    data_enl['monoparental'] = 0
    data_enl.loc[data_enl.mtypmena.isin([31,32]), 'monoparental'] = 1

    data_enl.rename(
        columns = {
            'froid_4_criteres_3_deciles' : 'FC_indicator',
            'revtot' : 'Disposable_income',
            'quantites_gaz_ville' : 'Quantity_natural_gaz',
            'quantites_combustibles_liquides' : 'Quantity_domestic_fuel',
            'combustibles_liquides' : 'Domestic_fuel',
            'gaz_ville' : 'Natural_gas',
            'strate_0' : 'Rural',
            'strate_1' : 'Small_cities',
            'strate_3' : 'Large_cities',
            'strate_4' : 'Paris',
            'majorite_double_vitrage' : 'Majority_double_glazing',
            'mauvaise_isolation_murs' : 'Bad_walls_isolation',
            'bonne_isolation_murs' : 'Good_walls_isolation',
            'ouest_sud' : 'Ouest_south',
            'surfhab_d' : 'Living_area_m2',
            'aides_logement' : 'Housing_benefits',
            'etudiant': 'Student',
            'agepr' : 'Age_representative',
            'agepr_2' : 'Age_representative_squared',
            'nactifs' : 'Number_in_labor_force',
            'ocde10' : 'Consumption_units',
            'monoparental' : 'Monoparental',
            'bat_av_49' : 'Building_before_1949',
            'bat_49_74' : 'Building_1949_74',
            'log_indiv' : 'Individual_housing',
            'proprietaire' : 'Owner'
            },
        inplace = True
        )

    regressors = [
        'Disposable_income',
        'Quantity_natural_gaz',
        'Quantity_domestic_fuel',
        'Bad_walls_isolation',
        'Good_walls_isolation',        
        'Majority_double_glazing',
        'Building_before_1949',
        'Building_1949_74',
        'Owner',
        'Individual_housing',
        'Living_area_m2',
        'Consumption_units',
        'Number_in_labor_force',
        'Housing_benefits',
        'Rural',
        'Small_cities',
        'Large_cities',
        'Paris',
        'Ouest_south',
        'Domestic_fuel',
        'Natural_gas',
        'Student',
        'Age_representative',
        'Age_representative_squared',
        'Monoparental',
        #'isolation_toit',
        #'quantites_electricite_selon_compteur',
        #'quantites_gaz_final',
        #'isolation_murs',
        #'mauvaise_isolation_fenetres',
        #'depenses_gaz_ville',
        #'depenses_electricite',
        #'depenses_energies',
        #'quantites_kwh',
        #'part_energies_revtot',
        #'quantites_combustibles_liquides',
        #'niveau_de_vie',
        #'brde_m2_rev_disponible',
        #'tee_10_3_deciles_rev_disponible',
        #'rural',
        #'paris',
        #'electricite',
        #'npers',
        #'strate',
        #'depenses_tot',
        #'quantites_kwh',
        #'revdecm',
        ]


    regression_logit = smf.Logit(data_enl['FC_indicator'], data_enl[regressors]).fit()
    
    return regression_logit


if __name__ == "__main__":
    regression_logit = estimate_froid()
    #print regression_logit.summary()
    print regression_logit.get_margeff().summary()

