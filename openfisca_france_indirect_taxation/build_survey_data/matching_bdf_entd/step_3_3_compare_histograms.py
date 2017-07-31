# -*- coding: utf-8 -*-

from __future__ import division


# Dans ce script on utilise des histogrammes pour comparer la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

import matplotlib.pyplot as plt
import numpy as np
import seaborn

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_2_homogenize_variables import \
    create_niveau_vie_quantiles

seaborn.set_palette(seaborn.color_palette("Set2", 12))

data = create_niveau_vie_quantiles()
data_entd = data[0]
data_bdf = data[1]


def histogrammes(list_keys, list_values_bdf, list_values_entd):
    size_hist = np.arange(len(list_keys))
    plot_bdf = plt.bar(size_hist-0.125, list_values_bdf, color = 'b', align='center', width=0.25)
    plot_entd = plt.bar(size_hist+0.125, list_values_entd, color = 'r', align='center', width=0.25)
    plt.xticks(size_hist, list_keys)
    plt.legend((plot_bdf[0], plot_entd[0]), ('BdF', 'ENTD'))
    
    return plt


def histogram_aba():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0, 1, 2]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.aba == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
       
        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.aba == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]
    
        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_bdf, list_values_entd)
    
    return plt
    
histogram_aba()


def histogram_agepr():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        list_values_bdf.append(data_bdf['agepr'].quantile(i))
        list_values_entd.append(data_entd['agepr'].quantile(i))
        list_keys.append('{}'.format(i)) 

    histogrammes(list_keys, list_values_bdf, list_values_entd)

    return plt

histogram_agepr()


def histogram_cataeu():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [111, 112, 120, 211, 212, 221, 222, 300, 400]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.cataeu == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
        
        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.cataeu == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]
    
        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_bdf, list_values_entd)
    
    return plt
    
histogram_cataeu()


def histogram_dip14():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0, 10, 12, 20, 30, 31, 33, 41, 42, 43, 44, 50, 60, 70, 71]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['dip14pr'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd['dip14pr'] == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]
    
        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_bdf, list_values_entd)
    
    return plt
    
histogram_dip14()


def histogram_nactifs():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0, 1, 2, 3, 4, 5, 6]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['nactifs'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd['nactifs'] == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]
    
        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_bdf, list_values_entd)
    
    return plt
    
histogram_nactifs()


def histogram_nbphab():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.nbphab == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
        
        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.nbphab == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]
    
        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_bdf, list_values_entd)
    
    return plt
    
histogram_nbphab()


def histogram_nenfants():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0, 1, 2, 3, 4, 5, 6]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['nenfants'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd['nenfants'] == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]
    
        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_bdf, list_values_entd)
    
    return plt
    
histogram_nenfants()


def histogram_ocde10():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.ocde10 == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.ocde10 == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]
    
        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_bdf, list_values_entd)
    
    return plt
    
histogram_ocde10()


def histogram_niveau_vie():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        list_values_bdf.append(data_bdf['niveau_vie'].quantile(i))
        list_values_entd.append(data_entd['niveau_vie'].quantile(i))
        list_keys.append('{}'.format(i)) 

    histogrammes(list_keys, list_values_bdf, list_values_entd)
    
    return plt
    
histogram_niveau_vie()


def histogram_tau():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.tau == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.tau == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]
    
        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_bdf, list_values_entd)
    
    return plt
    
histogram_tau()


def histogram_tuu():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.tuu == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]
    
        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.tuu == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]
    
        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    histogrammes(list_keys, list_values_bdf, list_values_entd)
    
    return plt
    
histogram_tuu()
