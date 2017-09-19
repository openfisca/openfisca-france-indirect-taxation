# -*- coding: utf-8 -*-

from __future__ import division


# Dans ce script on compare la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

import matplotlib.pyplot as plt
import seaborn

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_2_homogenize_variables import \
    create_niveau_vie_quantiles

seaborn.set_palette(seaborn.color_palette("Set2", 12))

data = create_niveau_vie_quantiles()
data_enl = data[0]
data_bdf = data[1]


# aba - aides au logement
# 1 = Oui, 2 = Non, 0 = ?
def check_aba():
    results = dict()
    for i in [0, 1, 2]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.aba == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
       
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl.aba == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]

        results['{} - BdF'.format(i)] = part_bdf
        results['{} - ENL'.format(i)] = part_enl
        
    return results

results_aba = check_aba()


# agepr - age de la personne de référence
def check_agepr():
    results = dict()
    results['Average - BdF'] = \
        (data_bdf['agepr'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
    results['Average - ENL'] = \
        (data_enl['agepr'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()
 
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        results['{} th quantile - BdF'.format(i)] = \
            data_bdf['agepr'].quantile(i)
        results['{} th quantile - ENL'.format(i)] = \
            data_enl['agepr'].quantile(i)

    return results

results_agepr = check_agepr()
# Bons résultats


# amr - montant des aides au logement
def check_amr():
    results = dict()
    amr_bdf = data_bdf.query('aba == 1')
    amr_enl = data_enl.query('aba == 1')
    results['Average - BdF'] = \
        (amr_bdf['amr'] * amr_bdf['pondmen']).sum() / amr_bdf['pondmen'].sum()
    results['Average - ENL'] = \
        (amr_enl['amr'] * amr_enl['pondmen']).sum() / amr_enl['pondmen'].sum()
    for i in [0.8, 0.85, .9, 0.95, 0.99, 0.995, 0.999]:
        results['{} th quantile - BdF'.format(i)] = \
            data_bdf['amr'].quantile(i)
        results['{} th quantile - ENL'.format(i)] = \
            data_enl['amr'].quantile(i)
    
    return results

results_amr = check_amr()
# fonctionne moyennement : plus d'aide au logement dans l'ENL


# ancons - année de construction
def check_ancons():
    results = dict()
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.ancons == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl.ancons == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]
    
        results['{} - BdF'.format(i)] = part_bdf * 100
        results['{} - ENL'.format(i)] = part_enl * 100

    return results

results_ancons = check_ancons()
# Petit problème sur 8, 9 et 10 + problème des 99 de BdF -> revoir la définition


# cataeu - catégorie de la commune
# 111 : grand pôle, 112 : couronne d'un GP, 120: multipolarisé grande aire urbaine,
# 211 : moyen pôle, 212 : couronne MP, 221 : petit pôle, 222 : couronne PP,
# 300 : autre multipolarisé, 400 : isolée
def check_cataeu():
    results = dict()
    for i in [111, 112, 120, 211, 212, 221, 222, 300, 400]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.cataeu == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
        
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl.cataeu == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]
    
        results['{} - BdF'.format(i)] = part_bdf
        results['{} - ENL'.format(i)] = part_enl
        
    return results

results_cataeu = check_cataeu()


# cs42 - catégorie socioprofessionnelle
def check_cs42():
    results_pr = dict()
    results_cj = dict()
    for j in ['pr', 'cj']:
        for i in range(11,87):
            data_bdf['pondmen_{}'.format(i)] = 0
            data_bdf['pondmen_{}'.format(i)].loc[data_bdf['cs42{}'.format(j)] == i] = data_bdf['pondmen']
            part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
            del data_bdf['pondmen_{}'.format(i)]
        
            data_enl['pondmen_{}'.format(i)] = 0
            data_enl['pondmen_{}'.format(i)].loc[data_enl['cs42{}'.format(j)] == i] = data_enl['pondmen']
            part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
            del data_enl['pondmen_{}'.format(i)]

            if j == 'pr':      
                results_pr['{} - BdF'.format(i)] = part_bdf * 100
                results_pr['{} - ENL'.format(i)] = part_enl * 100
            else:
                results_cj['{} - BdF'.format(i)] = part_bdf * 100
                results_cj['{} - ENL'.format(i)] = part_enl * 100


    return results_pr, results_cj

results_cs42pr = check_cs42()[0]
# 13 et 44 produisent des mauvais résultats, pour le reste ça va
results_cs42cj = check_cs42()[1]
# 12, 13, 23 en particulier sont mauvais, pas mal dans l'ensemble


def check_depenses_energies():
    results = dict()
    results['Average - BdF'] = \
        (data_bdf['depenses_energies'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
    results['Average - ENL'] = \
        (data_enl['depenses_energies'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        results['{} th quantile - BdF'.format(i)] = \
            data_bdf['depenses_energies'].quantile(i)
        results['{} th quantile - ENL'.format(i)] = \
            data_enl['depenses_energies'].quantile(i)
    
    return results

results_depenses_energies = check_depenses_energies()


# dip14pr - diplôme de la personne de référence
def check_dip14():
    results = dict()
    for i in [0, 10, 12, 20, 30, 31, 33, 41, 42, 43, 44, 50, 60, 70, 71]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['dip14pr'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl['dip14pr'] == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]

        results['{} - BdF'.format(i)] = part_bdf * 100
        results['{} - ENL'.format(i)] = part_enl * 100

    return results

results_dip14pr = check_dip14()
# Bien


# htl - type de logement
def check_htl():
    results = dict()
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.htl == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl.htl == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]

        results['{} - BdF'.format(i)] = part_bdf * 100
        results['{} - ENL'.format(i)] = part_enl * 100

    return results

results_htl = check_htl()
# Assez bonnes performances -> revoir la définition


def check_log_indiv():
    results = dict()
    results['BdF'] = \
        (data_bdf['log_indiv'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
    results['ENL'] = \
        (data_enl['log_indiv'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

    return results

results_log_indiv = check_log_indiv()


# mchof_d - montant annuel des dépenses en chauffage collectif
def check_mchof_d():
    results = dict()
    results['BdF'] = \
        (data_bdf['mchof_d'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
    results['ENL'] = \
        (data_enl['mchof_d'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

    return results

results_mchof_d = check_mchof_d()
# Catastrophique...


# mfac_eau1_d - montant annuel des dépenses d'eau, redressé
def check_mfac_eau1_d():
    results = dict()
    results['BdF'] = \
        (data_bdf['mfac_eau1_d'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
    results['ENL'] = \
        (data_enl['mfac_eau1_d'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

    return results

results_mfac_eau1_d = check_mfac_eau1_d()
# fonctionne mal, dépenses beaucoup plus importantes dans ENL


# mloy_d - montant mensuel du loyer hors charges
def check_mloy_d():
    results = dict()
    results['BdF'] = \
        (data_bdf['mloy_d'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
    results['ENL'] = \
        (data_enl['mloy_d'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()

    return results

results_mloy_d = check_mloy_d()
# résultats catastrophiques


# nactifs - nombre d'actifs
def check_nactifs():
    results = dict()
    for i in [0, 1, 2, 3, 4, 5, 6]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['nactifs'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl['nactifs'] == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]

        results['{} - BdF'.format(i)] = part_bdf * 100
        results['{} - ENL'.format(i)] = part_enl * 100

    return results

results_nactifs = check_nactifs()
# Super


# nbphab - nombre de pièces habitables
def check_nbphab():
    results = dict()
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.nbphab == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
        
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl.nbphab == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]
    
        results['{} - BdF'.format(i)] = part_bdf * 100
        results['{} - ENL'.format(i)] = part_enl * 100

    return results

results_nbphab = check_nbphab()
# Très Bonnes performances


# nenfants - nombre d'enfants à charge
def check_nenfants():
    results = dict()
    for i in [0, 1, 2, 3, 4, 5, 6]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['nenfants'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl['nenfants'] == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]

        results['{} - BdF'.format(i)] = part_bdf * 100
        results['{} - ENL'.format(i)] = part_enl * 100

    return results

results_nenfants = check_nenfants()
# Bon dans l'ensemble


# revtot - revenu total du ménage
def check_revtot():
    results = dict()
    results['Average - BdF'] = \
        (data_bdf['revtot'] * data_bdf['pondmen']).sum() / data_bdf['pondmen'].sum()
    results['Average - ENL'] = \
        (data_enl['revtot'] * data_enl['pondmen']).sum() / data_enl['pondmen'].sum()
 
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        results['{} th quantile - BdF'.format(i)] = \
            data_bdf['revtot'].quantile(i)
        results['{} th quantile - ENL'.format(i)] = \
            data_enl['revtot'].quantile(i)

    return results

results_revtot = check_revtot()
# Plutôt bon, mais la distribution de l'ENL est un peu plus dispersée


# ocde10 - unités de consommations
def check_ocde10():
    results = dict()
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.ocde10 == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl.ocde10 == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]
 
        results['{} - BdF'.format(i)] = part_bdf * 100
        results['{} - ENL'.format(i)] = part_enl * 100

    return results

results_ocde10 = check_ocde10()
# Bien


# Part dépenses énergies logement
def check_part_energies_revtot(data_bdf, data_enl):
    results = dict()
    results['Average - BdF'] = (
        100 * (data_bdf['part_energies_revtot'] * data_bdf['pondmen']).sum() /
        data_bdf['pondmen'].sum()
        )
    results['Average - ENL'] = (
        100 * (data_enl['part_energies_revtot'] * data_enl['pondmen']).sum() /
        data_enl['pondmen'].sum()
        )
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        results['{} th quantile - BdF'.format(i)] = \
            100 * data_bdf['part_energies_revtot'].quantile(i)
        results['{} th quantile - ENL'.format(i)] = \
            100 * data_enl['part_energies_revtot'].quantile(i)

    data_bdf = data_bdf.sort_values(by = ['part_energies_revtot'])
    data_bdf = data_bdf.query('part_energies_revtot < 1').copy()
    data_bdf['rank'] = data_bdf['pondmen'].cumsum() / sum(data_bdf['pondmen'])
    plot_bdf = plt.plot(data_bdf['rank'], data_bdf['part_energies_revtot'])

    data_enl = data_enl.sort_values(by = ['part_energies_revtot'])
    data_enl = data_enl.query('part_energies_revtot < 1').copy()
    data_enl['rank'] = data_enl['pondmen'].cumsum() / sum(data_enl['pondmen'])
    plot_enl = plt.plot(data_enl['rank'], data_enl['part_energies_revtot'])
    
    return results, plot_bdf, plot_enl

results_part_energies_revtot = check_part_energies_revtot(data_bdf, data_enl)[0]
plot_bdf = check_part_energies_revtot(data_bdf, data_enl)[1]
plot_enl = check_part_energies_revtot(data_bdf, data_enl)[2]
# Correct


# poste_45(1,2,3) - dépenses d'électricité, de gaz et de fioul domestique
def check_postes_energies():
    results = dict()
    for i in ['electricite', 'gaz_ville', 'combustibles_liquides', 'combustibles_solides']:
        results['depenses_{} - BdF'.format(i)] = (
            (data_bdf['depenses_{}'.format(i)] * data_bdf['pondmen']).sum() /
            data_bdf['pondmen'].sum()
            )
        results['depenses_{} - ENL'.format(i)] = (
            (data_enl['depenses_{}'.format(i)] * data_enl['pondmen']).sum() /
            data_enl['pondmen'].sum()
            )

        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['depenses_{}'.format(i)] > 0] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl['depenses_{}'.format(i)] > 0] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]
        
        results['part_consommateurs_depenses_{} - BdF'.format(i)] = part_bdf
        results['part_consommateurs_depenses_{} - ENL'.format(i)] = part_enl

    return results

results_check_postes_energies = check_postes_energies()
# Fonctionne plutôt bien


# situa - occupation principale
def check_situa():
    results_pr = dict()
    results_cj = dict()
    for j in ['pr', 'cj']:
        for i in [1, 2, 3, 4, 5, 6, 7]:
            data_bdf['pondmen_{}'.format(i)] = 0
            data_bdf['pondmen_{}'.format(i)].loc[data_bdf['situa{}'.format(j)] == i] = data_bdf['pondmen']
            part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
            del data_bdf['pondmen_{}'.format(i)]
        
            data_enl['pondmen_{}'.format(i)] = 0
            data_enl['pondmen_{}'.format(i)].loc[data_enl['situa{}'.format(j)] == i] = data_enl['pondmen']
            part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
            del data_enl['pondmen_{}'.format(i)]

            if j == 'pr':      
                results_pr['{} - BdF'.format(i)] = part_bdf * 100
                results_pr['{} - ENL'.format(i)] = part_enl * 100
            else:
                results_cj['{} - BdF'.format(i)] = part_bdf * 100
                results_cj['{} - ENL'.format(i)] = part_enl * 100


    return results_pr, results_cj

results_situapr = check_situa()[0]
# Plutôt bien
results_situacj = check_situa()[1]
# Bien


def check_surfhab_d():
    results = dict()
    results['Average - BdF'] = (
        (data_bdf['surfhab_d'] * data_bdf['pondmen']).sum() /
        data_bdf['pondmen'].sum()
        )
    results['Average - ENL'] = (
        (data_enl['surfhab_d'] * data_enl['pondmen']).sum() /
        data_enl['pondmen'].sum()
        )
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        results['{} th quantile - BdF'.format(i)] = \
            data_bdf['surfhab_d'].quantile(i)
        results['{} th quantile - ENL'.format(i)] = \
            data_enl['surfhab_d'].quantile(i)

    return results

results_surfhab_d = check_surfhab_d()
# Très bon


# tau - taille de l'aire urbaine par tranche
def check_tau():
    results = dict()
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.tau == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl.tau == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]
  
        results['{} - BdF'.format(i)] = part_bdf * 100
        results['{} - ENL'.format(i)] = part_enl * 100

    return results

results_tau = check_tau()
# Quelques petits soucis (2,5,6) mais ça va


# tuu - taille de l'unité urbaine par tranche
def check_tuu():
    results = dict()
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.tuu == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl.tuu == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]
  
        results['{} - BdF'.format(i)] = part_bdf * 100
        results['{} - ENL'.format(i)] = part_enl * 100

    return results

results_tuu = check_tuu()
# Pas mal


# zeat - zone d'étude et d'aménagement du territoire
def check_zeat():
    results = dict()
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.zeat == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_enl['pondmen_{}'.format(i)] = 0
        data_enl['pondmen_{}'.format(i)].loc[data_enl.zeat == i] = data_enl['pondmen']
        part_enl = data_enl['pondmen_{}'.format(i)].sum() / data_enl['pondmen'].sum()
        del data_enl['pondmen_{}'.format(i)]
  
        results['{} - BdF'.format(i)] = part_bdf * 100
        results['{} - ENL'.format(i)] = part_enl * 100

    return results

results_zeat = check_zeat()
# Très bien !
