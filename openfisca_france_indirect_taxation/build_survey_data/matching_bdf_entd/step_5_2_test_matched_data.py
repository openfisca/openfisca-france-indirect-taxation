# -*- coding: utf-8 -*-

# Dans ce script, on test la qualité de l'appariement.
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from openfisca_france_indirect_taxation.utils import assets_directory
sns.set_palette(sns.color_palette("Set2"))

output_path = "C:/Users/veve1/OneDrive/Documents/ENSAE PhD/Carbon tax/Output/Figures"

data_entd = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matching_entd.csv'
        ), sep =',', decimal = '.'
    )

data_matched_distance = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matched_distance.csv'
        ), sep =',', decimal = '.'
    )

data_matched_random = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matched_random.csv'
        ), sep =',', decimal = '.'
    )

data_matched_rank = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matched_rank.csv'
        ), sep =',', decimal = '.'
    )


def test_var_niveau_vie_decile(data_entd, data_matched, var):
    results_dict = dict()
    average_entd = sum(data_entd['pondmen'] * (data_entd[var])) / sum(data_entd['pondmen'])
    average_matched = sum(data_matched['pondmen'] * (data_matched[var])) / sum(data_matched['pondmen'])
    results_dict['Average'] = [average_entd, average_matched]
    for i in range(1, 11):
        data_entd_decile = data_entd.loc[data_entd['niveau_vie_decile'] == i]
        data_matched_decile = data_matched.loc[data_matched['niveau_vie_decile'] == i]
        part_entd = sum(data_entd_decile['pondmen'] * (data_entd_decile[var])) / sum(data_entd_decile['pondmen'])
        part_matched = sum(data_matched_decile['pondmen'] * (data_matched_decile[var])) / sum(data_matched_decile['pondmen'])
        results_dict['{}'.format(i)] = [part_entd, part_matched]

    return results_dict


test_distance_niveau_vie_decile_distance = test_var_niveau_vie_decile(data_entd, data_matched_distance, var = 'distance')
test_distance_niveau_vie_decile_random = test_var_niveau_vie_decile(data_entd, data_matched_random, var = 'distance')
test_distance_niveau_vie_decile_rank = test_var_niveau_vie_decile(data_entd, data_matched_rank, var = 'distance')

test_distance_diesel_niveau_vie_decile_distance = test_var_niveau_vie_decile(data_entd, data_matched_distance, var = 'distance_diesel')
test_distance_diesel_niveau_vie_decile_random = test_var_niveau_vie_decile(data_entd, data_matched_random, var = 'distance_diesel')
test_distance_diesel_niveau_vie_decile_rank = test_var_niveau_vie_decile(data_entd, data_matched_rank, var = 'distance_diesel')

test_distance_essence_niveau_vie_decile_distance_essence = test_var_niveau_vie_decile(data_entd, data_matched_distance, var = 'distance_diesel')
test_distance_essence_niveau_vie_decile_random = test_var_niveau_vie_decile(data_entd, data_matched_random, var = 'distance_diesel')
test_distance_essence_niveau_vie_decile_rank = test_var_niveau_vie_decile(data_entd, data_matched_rank, var = 'distance_diesel')

# Barplot comparaison distance annuelle par décile niveau de vie
data_matched_distance['source'] = 'Matched'
data_entd['source'] = 'EMP'
data_plot = pd.concat([data_matched_distance, data_entd])

plt.figure(figsize=(10, 6))
sns.barplot(data_plot, x = 'niveau_vie_decile', y = 'distance', hue = 'source', hue_order=['EMP', 'Matched'], estimator = 'mean', weights = 'pondmen')
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.xlabel('Income decile', size = 14)
plt.ylabel('Average annual distance (in km)', size = 14)
plt.title('Comparison between EMP and matched dataset', size = 16)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig(os.path.join(output_path, 'Matching_bdf_emp/bar_plot_distance_matched_decile.pdf'))
plt.close()

# Density plot distance annuelle 
plt.figure(figsize=(10, 6))
sns.kdeplot(data = data_entd, x = 'distance', weights = 'pondmen', bw_adjust=0.7)
sns.kdeplot(data = data_matched_distance, x = 'distance', weights = 'pondmen', bw_adjust=0.7)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.xlabel('Annual distance traveled (in km)', size = 14)
plt.ylabel('Density', size = 14)  
plt.title('Distribution of annual distance traveled', size = 16)
plt.legend(['Matched', 'EMP'], fontsize = 14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig(os.path.join(output_path, 'Matching_bdf_emp/Compare_distance_density_distribution.pdf'))
plt.close()

# Cumulative distribution distance annuelle

plt.figure(figsize=(10, 6))
sns.kdeplot(data = data_entd, x = 'distance', weights = 'pondmen', cumulative= True, bw_adjust=0.7)
sns.kdeplot(data = data_matched_distance, x = 'distance', weights = 'pondmen', cumulative = True, bw_adjust=0.7)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.xlabel('Annual distance traveled (in km)', size = 14)
plt.ylabel('Cumulative proportion', size = 14)  
plt.title('Cumulative distribution of annual distance traveled', size = 16)
plt.legend(['Matched', 'EMP'], fontsize = 14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig(os.path.join(output_path, 'Matching_bdf_emp/Compare_distance_cumulative_distribution.pdf'))
plt.close()

# By income decile
# Density 
fig, axes = plt.subplots(2, 5, figsize=(20, 10))
fig.suptitle('Distribution of annual distance traveled', fontsize=18)

for i, ax in enumerate(axes.flat):
    decile = i + 1
    sns.kdeplot(data=data_entd.loc[data_entd['niveau_vie_decile'] == decile], x='distance', weights='pondmen', 
                bw_adjust=0.7, ax = ax)
    sns.kdeplot(data=data_matched_distance.loc[data_matched_distance['niveau_vie_decile'] == decile], x='distance', weights='pondmen', 
                bw_adjust=0.7, ax = ax)

    ax.set_title(f'Decile {decile}', size = 16)
    ax.set_yticks([])
    xticks_positions = ax.get_xticks()
    ax.set_xticks(xticks_positions)
    xticks_labels = ax.get_xticklabels()
    ax.set_xticklabels(labels = xticks_labels, rotation = 45)
    ax.set_xlabel('Annual distance traveled (in km)', size = 14)
    ax.set_ylabel('Density', size = 14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(['EMP', 'Matched'], fontsize = 14)
fig.align_labels()
fig.align_titles()
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(output_path, 'Matching_bdf_emp/Distance_density_distribution_by_decile.pdf'))
plt.close()

# Cumulative distribution
fig, axes = plt.subplots(2, 5, figsize=(20, 10))
fig.suptitle('Cumulative distribution of annual distance traveled', fontsize=18)

for i, ax in enumerate(axes.flat):
    decile = i + 1
    sns.kdeplot(data=data_entd.loc[data_entd['niveau_vie_decile'] == decile], x='distance', weights='pondmen', 
                bw_adjust=0.7, ax = ax, cumulative = True)
    sns.kdeplot(data=data_matched_distance.loc[data_matched_distance['niveau_vie_decile'] == decile], x='distance', weights='pondmen', 
                bw_adjust=0.7, ax = ax, cumulative = True)

    ax.set_title(f'Decile {decile}', size = 16)
    xticks_positions = ax.get_xticks()
    ax.set_xticks(xticks_positions)
    xticks_labels = ax.get_xticklabels()
    ax.set_xticklabels(labels = xticks_labels, rotation = 45)
    ax.set_xlabel('Annual distance traveled (in km)', size = 14)
    ax.set_ylabel('Cumulative proportion', size = 14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(['EMP', 'Matched'], fontsize = 14)
fig.align_labels()
fig.align_titles()
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(output_path, 'Matching_bdf_emp/Distance_cumulative_distribution_by_decile.pdf'))
plt.close()

# By urban categories 
# Density
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Distribution of annual distance traveled', fontsize=18)

urban_cat = ['rural', 'petite_ville', 'moyenne_ville', 'grande_ville', 'paris']
cat_labels = ['Rural', 'Small cities', 'Medium-large cities', 'Large cities', 'Paris']

for i, ax in enumerate(axes.flat):
    if i < len(urban_cat):
        cat = urban_cat[i]
        sns.kdeplot(data=data_entd.loc[data_entd[cat] == 1], x='distance', weights='pondmen', 
                    bw_adjust=0.7, ax = ax)
        sns.kdeplot(data=data_matched_distance.loc[data_matched_distance[cat] == 1], x='distance', weights='pondmen', 
                    bw_adjust=0.7, ax = ax)

        ax.set_title(cat_labels[i], size = 16)
        ax.set_yticks([])
        xticks_positions = ax.get_xticks()
        ax.set_xticks(xticks_positions)
        xticks_labels = ax.get_xticklabels()
        ax.set_xticklabels(labels = xticks_labels, rotation = 45)
        ax.set_xlabel('Annual distance traveled (in km)', size = 14)
        ax.set_ylabel('Density', size = 14)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend(['EMP', 'Matched'], fontsize = 14)
    else:
        ax.axis('off')
fig.align_labels()
fig.align_titles()
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(output_path, 'Matching_bdf_emp/Distance_density_distribution_by_urban_cat.pdf'))
plt.close()
