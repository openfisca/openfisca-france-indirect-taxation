import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes
from openfisca_france_indirect_taxation.utils import assets_directory
sns.set_palette(sns.color_palette("Set2"))
color_list = sns.color_palette("Set2")
sns_set2_orange = color_list[1]

output_path = "C:/Users/veve1/OneDrive/Documents/ENSAE PhD/Carbon tax/Output/Figures"

data_matched = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_emp',
        'data_matched_final.csv'
        ), sep =',', decimal = '.'
    )


def histogram_depenses_annuelle_group(data_matched, group):
    list_values_poste = []
    list_values_depenses_carburants = []
    list_keys = []
    if group == 'niveau_vie_decile':
        min_element = 1
        max_element = 11
    if group == 'tuu':
        min_element = 0
        max_element = 9
    for element in range(min_element, max_element):
        data_matched_group = data_matched.query('{} == {}'.format(group, element))
        poste = (
            sum(data_matched_group['poste_07_2_2_1'] * data_matched_group['pondmen'])
            / data_matched_group['pondmen'].sum()
            )
        list_values_poste.append(poste)

        data_matched_group = data_matched.query('{} == {}'.format(group, element))
        depenses_carburants = (
            sum(data_matched_group['depenses_carburants_corrigees_emp'] * data_matched_group['pondmen'])
            / data_matched_group['pondmen'].sum()
            )

        list_values_depenses_carburants.append(depenses_carburants)
        list_keys.append('{}'.format(element))

    figure = histogrammes(list_keys, list_values_poste, list_values_depenses_carburants, 'Ex ante', 'Ex post')

    return figure


def histogram_distribution_depenses_annuelle(data_matched):
    list_values_poste = []
    list_values_depenses_carburants = []
    list_keys = []
    for i in [.05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95]:
        list_values_poste.append(data_matched['poste_07_2_2_1'].quantile(i))
        list_values_depenses_carburants.append(data_matched['depenses_carburants_corrigees_emp'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_poste, list_values_depenses_carburants, 'Ex ante', 'Ex post')

    return figure


histogram_depenses_annuelle_group(data_matched, 'niveau_vie_decile')
histogram_distribution_depenses_annuelle(data_matched)

# Depenses carburants density 
plt.figure(figsize=(10, 6))
sns.kdeplot(data = data_matched, x = 'poste_07_2_2_1', weights = 'pondmen', bw_adjust=0.7, color = 'b')
sns.kdeplot(data = data_matched, x = 'depenses_carburants_corrigees_emp', weights = 'pondmen', bw_adjust=0.7, color = sns_set2_orange)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.xlabel('Annual fuel expenditures (in €)', size = 14)
plt.ylabel('Density', size = 14)  
plt.title('Distribution of annual fuel expenditures', size = 16)
plt.legend(['BDF', 'Matched'], fontsize = 14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig(os.path.join(output_path, 'Matching_bdf_emp/Compare_depenses_density_distribution.pdf'))
plt.close()

# Depenses carburants cumulative distribution
plt.figure(figsize=(10, 6))
sns.kdeplot(data = data_matched, x = 'poste_07_2_2_1', weights = 'pondmen', cumulative = True, bw_adjust=0.7, color = 'b')
sns.kdeplot(data = data_matched, x = 'depenses_carburants_corrigees_emp', weights = 'pondmen', cumulative = True, bw_adjust=0.7, color = sns_set2_orange)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.xlabel('Annual fuel expenditures (in €)', size = 14)
plt.ylabel('Cumulative proportion', size = 14)  
plt.title('Cumulative distribution of annual fuel expenditures', size = 16)
plt.legend(['BDF', 'Matched'], fontsize = 14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig(os.path.join(output_path, 'Matching_bdf_emp/Compare_depenses_cumulative_distribution.pdf'))
plt.close()

# Depenses carburants density by income decile 
fig, axes = plt.subplots(2, 5, figsize=(20, 10))
fig.suptitle('Distribution of annual fuel expenditures', size = 18)

for i, ax in enumerate(axes.flat):
    decile = i + 1
    sns.kdeplot(data=data_matched.loc[data_matched['niveau_vie_decile'] == decile], x='poste_07_2_2_1', weights='pondmen', color = 'b', 
                bw_adjust=0.7, ax = ax)
    sns.kdeplot(data=data_matched.loc[data_matched['niveau_vie_decile'] == decile], x='depenses_carburants_corrigees_emp', weights='pondmen', color = sns_set2_orange,  
                bw_adjust=0.7, ax = ax)

    ax.set_title(f'Decile {decile}', size = 16)
    ax.set_yticks([])
    ax.set_xlabel('Annual fuel expenditures (in €)', size = 14)
    ax.set_ylabel('Density', size = 14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(['EMP', 'Matched'], fontsize = 14)
fig.align_labels()
fig.align_titles()
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(output_path, 'Matching_bdf_emp/Depenses_density_distribution_by_decile.pdf'))
plt.close()

# Cumulative distribution
fig, axes = plt.subplots(2, 5, figsize=(20, 10))
fig.suptitle('Cumulative distribution of annual fuel expenditures', fontsize=18)

for i, ax in enumerate(axes.flat):
    decile = i + 1
    sns.kdeplot(data=data_matched.loc[data_matched['niveau_vie_decile'] == decile], x='poste_07_2_2_1', weights='pondmen', color = 'b', 
                bw_adjust=0.7, ax = ax, cumulative = True)
    sns.kdeplot(data=data_matched.loc[data_matched['niveau_vie_decile'] == decile], x='depenses_carburants_corrigees_emp', weights='pondmen', color = sns_set2_orange, 
                bw_adjust=0.7, ax = ax, cumulative = True)
    ax.set_title(f'Decile {decile}', size = 16)
    ax.set_yticks([])
    xticks_positions = ax.get_xticks()
    ax.set_xticks(xticks_positions)
    xticks_labels = ax.get_xticklabels()
    ax.set_xticklabels(labels = xticks_labels, rotation = 45)
    ax.set_xlabel('Annual fuel expenditures (in €)', size = 14)
    ax.set_ylabel('Cumulative proportion', size = 14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(['BDF', 'Matched'], fontsize = 14)
fig.align_labels()
fig.align_titles()
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(output_path, 'Matching_bdf_emp/Depenses_cumulative_distribution_by_decile.pdf'))
plt.close()

# By urban categories 
# Density
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Distribution of annual fuel expenditures', size = 18)

urban_cat = ['rural', 'petite_ville', 'moyenne_ville', 'grande_ville', 'paris']
cat_labels = ['Rural', 'Small cities', 'Medium-large cities', 'Large cities', 'Paris']

for i, ax in enumerate(axes.flat):
    if i < len(urban_cat):
        cat = urban_cat[i]
        sns.kdeplot(data=data_matched.loc[data_matched[cat] == 1], x='poste_07_2_2_1', weights='pondmen', color = 'b', 
                    bw_adjust=0.7, ax = ax)
        sns.kdeplot(data=data_matched.loc[data_matched[cat] == 1], x='depenses_carburants_corrigees_emp', weights='pondmen', color = sns_set2_orange,
                    bw_adjust=0.7, ax = ax)

        ax.set_title(cat_labels[i], size = 16)
        ax.set_yticks([])
        xticks_positions = ax.get_xticks()
        ax.set_xticks(xticks_positions)
        xticks_labels = ax.get_xticklabels()
        ax.set_xticklabels(labels = xticks_labels, rotation = 45)
        ax.set_xlabel('Annual fuel expenditures (in €)', size = 14)
        ax.set_ylabel('Density', size = 14)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(['EMP', 'Matched'], fontsize = 14)
    else:
        ax.axis('off')
fig.align_labels()
fig.align_titles()
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(output_path, 'Matching_bdf_emp/Depenses_density_distribution_by_urban_cat.pdf'))
plt.close()