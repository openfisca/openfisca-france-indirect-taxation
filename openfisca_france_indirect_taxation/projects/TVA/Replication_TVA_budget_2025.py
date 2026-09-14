import numpy as np
import pandas as pd
import os
import csv
import ast
import seaborn as sns
from matplotlib import pyplot as plt
import wquantiles 

from tqdm import tqdm
from wquantiles import quantile
from openfisca_survey_manager.utils import asof

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.utils import assets_directory, get_input_data_frame
from openfisca_france_indirect_taxation.examples.utils_example import (
    dataframe_by_group,
    df_weighted_average_grouped,
    wavg)
from openfisca_france_indirect_taxation.build_survey_data.utils import weighted_sum
from openfisca_france_indirect_taxation.Calage_consommation_bdf import get_inflators_by_year
from openfisca_france_indirect_taxation.Calage_revenus_bdf import calage_bdf_niveau_vie, compute_erfs_decile 
from openfisca_france_indirect_taxation.projects.TVA.Utils import weighted_quantiles, stacked_bar_plot, double_stacked_bar_plot, bootstrap_weighted_mean_by_decile
from openfisca_france_indirect_taxation.projects.TVA.Reform_TVA_budget_2025 import augmente_tous_les_taux


simulated_variables = ['depenses_tva_taux_plein',
'depenses_tva_taux_intermediaire',
'depenses_tva_taux_reduit',
'depenses_tva_taux_super_reduit',
'depenses_ht_tva_taux_plein',
'depenses_ht_tva_taux_intermediaire',
'depenses_ht_tva_taux_reduit',
'depenses_ht_tva_taux_super_reduit',
'depenses_tva_exonere',
'depenses_totales',
'depenses_tot',
'tva_total',
'rev_disponible',
 'niveau_de_vie',
 'niveau_vie_decile',
 'decile_indiv_niveau_vie',
 'ocde10',
 'pondmen',
 'pondindiv',
 'agepr',
 'situapr',
 'situacj',
 'situaagr',
 'nactifs',
 'npers',
 'nadultes',
 'nenfants',
 'nenfact',
 'identifiant_menage']

# Décile par individus rev disponible et niveau de vie pour 2025 dans TaxIPP
data = {"decile_indiv_niveau_vie": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'rev_disponible_taxipp' : [16096, 28268, 33790, 38630, 44127, 50111, 56587, 64575, 77033, 136448],
    'niveau_de_vie' : [9033, 15217, 18578, 21603, 24476, 27480, 30917, 35394, 42436, 74370]
}
decile_taxipp = pd.DataFrame(data)
decile_taxipp.set_index('decile_indiv_niveau_vie', inplace = True)
input_bdf = get_input_data_frame(2017)
input_bdf = input_bdf.loc[input_bdf['rev_disponible'] > 0]
input_bdf , df_calage = calage_bdf_niveau_vie(input_bdf, decile_taxipp)
year = 2025
data_year = 2017
tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
inflators_by_year = get_inflators_by_year(rebuild = False, year_range = range(2017, 2026), data_year = data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

survey_scenario = SurveyScenario.create(
    input_data_frame = input_bdf,        # on prend la base Bdf avec les revenus calées sur TaxIPP comme entrée pour la simulation
    inflation_kwargs =  inflation_kwargs,
    baseline_tax_benefit_system = tax_benefit_system,
    reform = augmente_tous_les_taux,
    period = year
    )

depenses_ht_totales = (survey_scenario.compute_aggregate(variable = 'depenses_ht_tva_taux_plein', use_baseline = True, period = year) +
 survey_scenario.compute_aggregate(variable = 'depenses_ht_tva_taux_intermediaire', use_baseline = True, period = year) + 
 survey_scenario.compute_aggregate(variable = 'depenses_ht_tva_taux_reduit', use_baseline = True, period = year) + 
 survey_scenario.compute_aggregate(variable = 'depenses_ht_tva_taux_super_reduit', use_baseline = True, period = year)
 )
depenses_ht_totales
tva_total = survey_scenario.compute_aggregate(variable = 'tva_total', use_baseline = True, period = year)
emplois_taxables_tot = 13.7E11 # old: 13E11 (2024)
part_conso_menages = 0.562  # old: 0.605 (Adrivon et al. (2016) Le modèle d'estimation de la TVA théorique)

coeff = part_conso_menages * emplois_taxables_tot / depenses_ht_totales
inflators_2025 = { k:v if k in ['loyer_impute','rev_disponible'] else  v*coeff 
                      for k,v in inflators_by_year[2025].items()}
inflation_kwargs = dict(inflator_by_variable = inflators_2025)

survey_scenario = SurveyScenario.create(
    input_data_frame = input_bdf,        # on prend la base Bdf avec les revenus calées sur TaxIPP comme entrée pour la simulation
    inflation_kwargs =  inflation_kwargs,
    baseline_tax_benefit_system = tax_benefit_system,
    reform = augmente_tous_les_taux,
    period = year,
    )

recolte_taux_plein = survey_scenario.compute_aggregate(variable='tva_taux_plein', filter_by = 'rev_disponible > 0', difference= True, period = year) * 1e-9
recolte_taux_inter = survey_scenario.compute_aggregate(variable='tva_taux_intermediaire', filter_by = 'rev_disponible > 0', difference= True, period = year) * 1e-9
recolte_taux_reduit = survey_scenario.compute_aggregate(variable='tva_taux_reduit', filter_by = 'rev_disponible > 0', difference= True, period = year) * 1e-9
recolte_taux_super_reduit = survey_scenario.compute_aggregate(variable='tva_taux_super_reduit', filter_by = 'rev_disponible > 0', difference= True, period = year) * 1e-9

total_recolte = recolte_taux_plein + recolte_taux_inter + recolte_taux_reduit + recolte_taux_super_reduit
total_recolte / part_conso_menages 

survey_scenario.compute_aggregate(variable ='tva_total', filter_by = 'rev_disponible > 0', use_baseline= True, period = year) * 1e-9
baseline_menage = survey_scenario.create_data_frame_by_entity(simulated_variables, filter_by = 'rev_disponible > 0', use_baseline = True, period = year)['menage']
reform_menage   = survey_scenario.create_data_frame_by_entity(simulated_variables, filter_by = 'rev_disponible > 0', use_baseline = False, period = year)['menage']

difference_menage = pd.DataFrame()
baseline_variables = ['depenses_tot','rev_disponible','niveau_de_vie','decile_indiv_niveau_vie','ocde10','pondmen',
                      'nactifs','npers','nadultes','nenfants','agepr','identifiant_menage'] 
difference_menage[baseline_variables] = baseline_menage[baseline_variables]

difference_menage['depenses_totales'] = baseline_menage['depenses_totales'] - reform_menage['depenses_totales']
difference_menage['depenses_tot_par_uc'] = difference_menage['depenses_tot'] / difference_menage['ocde10']
difference_menage['depenses_totales_par_uc'] = difference_menage['depenses_totales'] / difference_menage['ocde10']

liste_taux = ['plein','intermediaire', 'reduit', 'super_reduit']
for taux in liste_taux:
    difference_menage['depenses_tva_taux_{}'.format(taux)] = baseline_menage['depenses_tva_taux_{}'.format(taux)] - reform_menage['depenses_tva_taux_{}'.format(taux)] 
    difference_menage['depenses_par_uc_tva_taux_{}'.format(taux)] = difference_menage['depenses_tva_taux_{}'.format(taux)] / difference_menage['ocde10']
    
difference_menage['pondindiv'] = difference_menage['pondmen'] * difference_menage['npers']
 
output_path = 'C:/Users/veve1/OneDrive/Documents/IPP/Budget 2025 TVA/'
# Les effets d'une hausse de TVA par décile de niveau de vie

difference_by_decile = df_weighted_average_grouped(dataframe = difference_menage, 
                                                   groupe = 'decile_indiv_niveau_vie', 
                                                   varlist = ['depenses_tot','depenses_tot_par_uc','depenses_totales_par_uc',
                                                              'rev_disponible','niveau_de_vie'] +
                                                   ['depenses_par_uc_tva_taux_{}'.format(taux) for taux in liste_taux],
                                                   weights = 'pondindiv'
                                                    )
difference_by_decile['taux_epargne'] = 1 - difference_by_decile['depenses_tot'] / difference_by_decile['rev_disponible']
difference_by_decile
for taux in liste_taux:
   difference_by_decile['Taux_effort_tva_taux_{}'.format(taux)] = difference_by_decile['depenses_par_uc_tva_taux_{}'.format(taux)] / difference_by_decile['niveau_de_vie'] * 100
difference_by_decile['Taux_effort_total'] = difference_by_decile['depenses_totales_par_uc'] / difference_by_decile['niveau_de_vie'] * 100


df = difference_menage.copy()
results_bootstrap_all = bootstrap_weighted_mean_by_decile(df, 'pondindiv', 'decile_indiv_niveau_vie', B = 10000)
errors_all = pd.DataFrame(pd.DataFrame(results_bootstrap_all).std(axis = 0))
errors_all = errors_all.reset_index().drop('index',axis = 1).rename({0 : 'std'},axis = 1)
errors_all = errors_all.reset_index().rename({'index' : 'decile_indiv_niveau_vie'}, axis = 1).set_index('decile_indiv_niveau_vie')
errors_all.index = errors_all.index + 1
errors_all['errors'] = 1.96 * errors_all['std']
difference_by_decile = difference_by_decile.merge(errors_all, left_index = True, right_index = True)
bottom_50 = pd.DataFrame(difference_by_decile.loc[difference_by_decile.index < 6, ['depenses_totales_par_uc','niveau_de_vie','Taux_effort_total']].mean(axis = 0)).T
bottom_50['taux_effort_moyen'] = bottom_50['depenses_totales_par_uc'] / bottom_50['niveau_de_vie'] * 100
bottom_50
difference_by_decile.loc[difference_by_decile.index.isin([6,7,8,9]), ['depenses_totales_par_uc','niveau_de_vie','Taux_effort_total']]
middle_40 = pd.DataFrame(difference_by_decile.loc[difference_by_decile.index.isin([6,7,8,9]), ['depenses_totales_par_uc','niveau_de_vie','Taux_effort_total']].mean(axis = 0)).T
middle_40['taux_effort_moyen'] = middle_40['depenses_totales_par_uc'] / middle_40['niveau_de_vie'] * 100
middle_40
difference_by_decile
    
stacked_bar_plot(difference_by_decile, 
                 variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                 labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                 title = "Effets de l'augmentation d'un point de TVA",
                 xlabel = 'Déciles de niveau de vie' ,
                 ylabel ='Variation (en % du niveau de vie)',
                 colors = list(sns.color_palette("Paired")),
                 savefig = False,
                 outfile = 'Taux_effort.pdf',
                 ylim = (-1.2, 0)
                )

# Decomposition actifs / inactifs

difference_by_decile_actifs = df_weighted_average_grouped(dataframe = difference_menage.loc[difference_menage['nactifs'] >= 1], 
                                                   groupe = 'decile_indiv_niveau_vie', 
                                                   varlist = ['depenses_tot','depenses_tot_par_uc','depenses_totales_par_uc',
                                                              'rev_disponible','niveau_de_vie'] +
                                                   ['depenses_par_uc_tva_taux_{}'.format(taux) for taux in liste_taux],
                                                   weights = 'pondindiv'
                                                    )
difference_by_decile_actifs['taux_epargne_actifs'] = 1 - difference_by_decile_actifs['depenses_tot'] / difference_by_decile_actifs['rev_disponible']
# difference_by_decile_actifs[['taux_epargne_actifs']]
for taux in liste_taux:
   difference_by_decile_actifs['Taux_effort_tva_taux_{}'.format(taux)] = difference_by_decile_actifs['depenses_par_uc_tva_taux_{}'.format(taux)] / difference_by_decile_actifs['niveau_de_vie'] * 100
difference_by_decile_actifs['Taux_effort_total'] = difference_by_decile_actifs['depenses_totales_par_uc'] / difference_by_decile_actifs['niveau_de_vie'] * 100
# Bootstrap 

results_bootstrap_actifs = bootstrap_weighted_mean_by_decile(df.loc[df['nactifs'] >= 1], 'pondindiv', 'decile_indiv_niveau_vie', B = 1000)
errors_actifs = pd.DataFrame(pd.DataFrame(results_bootstrap_actifs).std(axis = 0))
errors_actifs = errors_actifs.reset_index().drop('index',axis = 1).rename({0 : 'std'},axis = 1)
errors_actifs = errors_actifs.reset_index().rename({'index' : 'decile_indiv_niveau_vie'}, axis = 1).set_index('decile_indiv_niveau_vie')
errors_actifs.index = errors_actifs.index + 1
errors_actifs['errors'] = 1.96 * errors_actifs['std']
difference_by_decile_actifs = difference_by_decile_actifs.merge(errors_actifs, left_index = True, right_index = True)

stacked_bar_plot(difference_by_decile_actifs, 
                 variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                 labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                 title = "Effets de l'augmentation d'un point de TVA - Actifs",
                 xlabel = 'Déciles de niveau de vie' ,
                 ylabel ='Variation (en % du niveau de vie)',
                 colors = list(sns.color_palette("Paired")),
                 savefig = False,
                 outfile = 'Taux_effort_actifs_only.pdf',
                #  errors = 'errors'
                )
difference_by_decile_not_actifs = df_weighted_average_grouped(dataframe = difference_menage.loc[difference_menage['nactifs'] < 1], 
                                                   groupe = 'decile_indiv_niveau_vie', 
                                                   varlist = ['depenses_tot','depenses_tot_par_uc','depenses_totales_par_uc',
                                                              'rev_disponible','niveau_de_vie'] +
                                                   ['depenses_par_uc_tva_taux_{}'.format(taux) for taux in liste_taux],
                                                   weights= 'pondindiv'
                                                    )
difference_by_decile_not_actifs['taux_epargne_inactifs'] = 1 - difference_by_decile_not_actifs['depenses_tot'] / difference_by_decile_not_actifs['rev_disponible']
difference_by_decile_not_actifs[['taux_epargne_inactifs']]
for taux in liste_taux:
   difference_by_decile_not_actifs['Taux_effort_tva_taux_{}'.format(taux)] = difference_by_decile_not_actifs['depenses_par_uc_tva_taux_{}'.format(taux)] / difference_by_decile_not_actifs['niveau_de_vie'] * 100
difference_by_decile_not_actifs['Taux_effort_total'] = difference_by_decile_not_actifs['depenses_totales_par_uc'] / difference_by_decile_not_actifs['niveau_de_vie'] * 100
# Bootstrap 

results_bootstrap_inactifs = bootstrap_weighted_mean_by_decile(df.loc[df['actifs'] < 1], 'pondindiv', 'decile_indiv_niveau_vie', B = 1000)
errors_inactifs = pd.DataFrame(pd.DataFrame(results_bootstrap_inactifs).std(axis = 0))
errors_inactifs = errors_inactifs.reset_index().drop('index',axis = 1).rename({0 : 'std'},axis = 1)
errors_inactifs = errors_inactifs.reset_index().rename({'index' : 'decile_indiv_niveau_vie'}, axis = 1).set_index('decile_indiv_niveau_vie')
errors_inactifs.index = errors_inactifs.index + 1
errors_inactifs['errors'] = 1.96 * errors_inactifs['std']
difference_by_decile_not_actifs = difference_by_decile_not_actifs.merge(errors_inactifs, left_index = True, right_index = True)
stacked_bar_plot(difference_by_decile_not_actifs, 
                 variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                 labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                 title = "Effets de l'augmentation d'un point de TVA - Inactifs",
                 xlabel = 'Déciles de niveau de vie' ,
                 ylabel ='Variation (en % du niveau de vie)',
                 colors = list(sns.color_palette("Paired")),
                 savefig = False,
                 outfile = 'Taux_effort_not_actifs.pdf',
                #  errors = 'errors'
                 )
double_stacked_bar_plot(difference_by_decile_not_actifs,
                        difference_by_decile_actifs, 
                        variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                        labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                        title1 = "Effets d'un point de TVA - Inactifs",
                        title2 = "Effets d'un point de TVA - Actifs",
                        xlabel = 'Déciles de niveau de vie' ,
                        ylabel = 'Variation (en % du niveau de vie)',
                        colors = list(sns.color_palette("Paired")),
                        savefig = False,
                        outfile = 'Taux_effort_actifs_not_actifs.pdf')

# Par type de ménage
difference_menage['cat_famille_menage'] = pd.NA

difference_menage.loc[
    (difference_menage['nadultes'] == 1) & (difference_menage['nenfants'] == 0),
    'cat_famille_menage',] = 1
difference_menage.loc[
    (difference_menage['nadultes'] == 1) & (difference_menage['nenfants'] > 0),
    'cat_famille_menage',] = 2
difference_menage.loc[
    (difference_menage['nadultes'] >= 2) & (difference_menage['nenfants'] == 0),
    'cat_famille_menage',] = 3
difference_menage.loc[
    (difference_menage['nadultes'] >= 2) & (difference_menage['nenfants'] > 0),
    'cat_famille_menage',] = 4

# difference_menage['cat_famille_menage'].value_counts(dropna=False)

def effect_by_decile(df):
    difference_by_decile = df_weighted_average_grouped(dataframe = df, 
                                                      groupe = 'decile_indiv_niveau_vie', 
                                                      varlist = ['depenses_tot','depenses_tot_par_uc','depenses_totales_par_uc',
                                                               'rev_disponible','niveau_de_vie'] +
                                                      ['depenses_par_uc_tva_taux_{}'.format(taux) for taux in liste_taux],
                                                      weights = 'pondindiv'
                                                      )
    for taux in liste_taux:
        difference_by_decile['Taux_effort_tva_taux_{}'.format(taux)] = difference_by_decile['depenses_par_uc_tva_taux_{}'.format(taux)] / difference_by_decile['niveau_de_vie'] * 100
    difference_by_decile['Taux_effort_total'] = difference_by_decile['depenses_totales_par_uc'] / difference_by_decile['niveau_de_vie'] * 100
    return(difference_by_decile)


df_famille_1 = difference_menage.loc[difference_menage['cat_famille_menage'] == 1]
df_by_decile_famille_1 = effect_by_decile(df_famille_1)
df_famille_2 = difference_menage.loc[difference_menage['cat_famille_menage'] == 2]
df_by_decile_famille_2 = effect_by_decile(df_famille_2)
df_famille_3 = difference_menage.loc[difference_menage['cat_famille_menage'] == 3]
df_by_decile_famille_3 = effect_by_decile(df_famille_3)
df_famille_4 = difference_menage.loc[difference_menage['cat_famille_menage'] == 4]
df_by_decile_famille_4 = effect_by_decile(df_famille_4)

# df_famille_2.groupby('decile_indiv_niveau_vie')['depenses_tva_taux_intermediaire'].sum()
# df_famille_2.loc[:,['decile_indiv_niveau_vie','depenses_tva_taux_intermediaire']].sort_values(by = 'depenses_tva_taux_intermediaire', ascending = False)

stacked_bar_plot(df_by_decile_famille_1, 
                 variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                 labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                 title = "Effets de l'augmentation d'un point de TVA - Celibataires sans enfant",
                 xlabel = 'Déciles de niveau de vie' ,
                 ylabel ='Variation (en % du niveau de vie)',
                 colors = list(sns.color_palette("Paired")),
                 savefig = True,
                 outfile = 'Taux_effort_celib_no_kids.pdf',
                 output_path = output_path,
                 ylim = (-1.4, 0)
                #  errors = 'errors'
                )

stacked_bar_plot(df_by_decile_famille_2, 
                 variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                 labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                 title = "Effets de l'augmentation d'un point de TVA - Celibataires avec enfant",
                 xlabel = 'Déciles de niveau de vie' ,
                 ylabel ='Variation (en % du niveau de vie)',
                 colors = list(sns.color_palette("Paired")),
                 savefig = False,
                 ylim = (-1.4, 0),
                 outfile = 'Taux_effort_celib_with_kids.pdf',
                #  errors = 'errors'
                )
stacked_bar_plot(df_by_decile_famille_3, 
                 variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                 labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                 title = "Effets de l'augmentation d'un point de TVA - Couples sans enfant",
                 xlabel = 'Déciles de niveau de vie' ,
                 ylabel ='Variation (en % du niveau de vie)',
                 colors = list(sns.color_palette("Paired")),
                 savefig = False,
                 ylim = (-1.4, 0),
                 outfile = 'Taux_effort_couples_no_kids.pdf',
                #  errors = 'errors'
                )
stacked_bar_plot(df_by_decile_famille_4, 
                 variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                 labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                 title = "Effets de l'augmentation d'un point de TVA - Couples avec enfant",
                 xlabel = 'Déciles de niveau de vie' ,
                 ylabel ='Variation (en % du niveau de vie)',
                 colors = list(sns.color_palette("Paired")),
                 savefig = False,
                 ylim = (-1.2, 0),
                 outfile = 'Taux_effort_couples_with_kids.pdf',
                #  errors = 'errors'
                )

# Par catégorie d'age de la personne de réf 

difference_menage["categorie_age"] = pd.cut(
    difference_menage["agepr"],
    bins=[18, 35, 50, 65, float("inf")],
    labels=["18-34", "35-49", "50-64", "65+"],
    right=False,
)

difference_menage["categorie_age"].value_counts(sort=False, dropna=False)
difference_menage.groupby(['decile_indiv_niveau_vie','categorie_age'])['identifiant_menage'].count()
df_age_1 = difference_menage.loc[difference_menage['categorie_age'] == "18-34"]
df_by_decile_age_1 = effect_by_decile(df_age_1)
df_age_2 = difference_menage.loc[difference_menage['categorie_age'] == "35-49"]
df_by_decile_age_2 = effect_by_decile(df_age_2)
df_age_3 = difference_menage.loc[difference_menage['categorie_age'] == "50-64"]
df_by_decile_age_3 = effect_by_decile(df_age_3)
df_age_4 = difference_menage.loc[difference_menage['categorie_age'] == "65+"]
df_by_decile_age_4 = effect_by_decile(df_age_4)   

stacked_bar_plot(df_by_decile_age_1, 
                variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                title = "Effets de l'augmentation d'un point de TVA - 18-34 ans",
                xlabel = 'Déciles de niveau de vie' ,
                ylabel ='Variation (en % du niveau de vie)',
                colors = list(sns.color_palette("Paired")),
                savefig = True,
                outfile = 'Taux_effort_18_34_ans.pdf',
                ylim = (-1.4, 0),
                #  errors = 'errors'
                )
stacked_bar_plot(df_by_decile_age_2, 
                 variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                 labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                 title = "Effets de l'augmentation d'un point de TVA - 35-49 ans",
                 xlabel = 'Déciles de niveau de vie' ,
                 ylabel ='Variation (en % du niveau de vie)',
                 colors = list(sns.color_palette("Paired")),
                 savefig = False,
                 outfile = 'Taux_effort_35_49_ans.pdf',
                 ylim = (-1.4, 0)
                #  errors = 'errors'
                )
stacked_bar_plot(df_by_decile_age_3, 
                 variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                 labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                 title = "Effets de l'augmentation d'un point de TVA - 50-64 ans",
                 xlabel = 'Déciles de niveau de vie' ,
                 ylabel ='Variation (en % du niveau de vie)',
                 colors = list(sns.color_palette("Paired")),
                 savefig = False,
                 outfile = 'Taux_effort_50_64ans.pdf',
                 ylim = (-1.4, 0)
                #  errors = 'errors'
                )
stacked_bar_plot(df_by_decile_age_4, 
                 variables = ['Taux_effort_tva_taux_{}'.format(taux) for taux in liste_taux],
                 labels = ['Taux plein','Taux intermédiaire','Taux réduit','Taux super réduit'],
                 title = "Effets de l'augmentation d'un point de TVA - 65+ ans",
                 xlabel = 'Déciles de niveau de vie' ,
                 ylabel ='Variation (en % du niveau de vie)',
                 colors = list(sns.color_palette("Paired")),
                 savefig = False,
                 outfile = 'Taux_effort_65_ans_plus.pdf',
                #  errors = 'errors'
                )