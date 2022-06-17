

# Dans ce script on utilise des histogrammes pour comparer la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

import os
import pandas as pd
import seaborn


from openfisca_france_indirect_taxation.examples.utils_example import (
    graph_builder_bar, save_dataframe_to_graph)


from openfisca_france_indirect_taxation.utils import assets_directory


seaborn.set_palette(seaborn.color_palette('Set2', 12))


# Importation des bases de données appariées et de la base de référence entd
data_enl = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'data_matching_enl.csv'
        ), sep =',', decimal = '.'
    )

data_matched_enl = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'data_matched_rank.csv'
        ), sep =',', decimal = '.'
    )


data_entd = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matching_entd.csv'
        ), sep =',', decimal = '.'
    )


data_matched_entd = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matched_distance.csv'
        ), sep =',', decimal = '.'
    )

data_matched_final_entd = pd.read_csv(
    os.path.join(
        assets_directory,
        'matching',
        'matching_entd',
        'data_matched_final.csv'
        ), sep =',', decimal = '.'
    )


def strate_from_tuu(data):
    data['strate'] = 0
    data.loc[data['tuu'].isin([1, 2, 3]), 'strate'] = 1
    data.loc[data['tuu'].isin([4, 5, 6]), 'strate'] = 2
    data.loc[data['tuu'] == 7, 'strate'] = 3
    data.loc[data['tuu'] == 8, 'strate'] = 4

    return data


def froid_4_criteres(data):
    data['froid_4_criteres'] = 1 * ((
        data['froid_cout']
        + data['froid_impaye']
        + data['froid_installation']
        + data['froid_isolation']
        ) > 0)

    return data


data_enl = strate_from_tuu(data_enl)
data_entd = strate_from_tuu(data_entd)
data_matched_enl = strate_from_tuu(data_matched_enl)
data_matched_entd = strate_from_tuu(data_matched_entd)

data_enl = froid_4_criteres(data_enl)
data_matched_enl = froid_4_criteres(data_matched_enl)


def histogram_froid_group(data_matched, data_enl, froid, group):
    min_group = data_enl[group].min()
    max_group = data_enl[group].max()
    database = ['Matched', 'ENL', ]
    elements = list(range(min_group, max_group + 1))
    df_to_plot = pd.DataFrame(index = elements, columns = database)
    for i in range(min_group, max_group + 1):
        data_enl_decile = data_enl.query('{0} == {1}'.format(group, i))
        data_matched_decile = data_matched.query('{0} == {1}'.format(group, i))

        part_enl = (
            sum(data_enl_decile['pondmen'] * (data_enl_decile[froid] == 1))
            / sum(data_enl_decile['pondmen'])
            )
        part_matched = (
            sum(data_matched_decile['pondmen'] * (data_matched_decile[froid] == 1))
            / sum(data_matched_decile['pondmen'])
            )

        df_to_plot['Matched'][i] = part_matched
        df_to_plot['ENL'][i] = part_enl

    return df_to_plot


def histogram_distance_group(data_matched, data_entd, distance, group):
    min_group = data_entd[group].min()
    max_group = data_entd[group].max()
    database = ['Matched', 'ENTD', ]
    elements = list(range(min_group, max_group + 1))
    df_to_plot = pd.DataFrame(index = elements, columns = database)
    for i in range(min_group, max_group + 1):
        data_matched_group = data_matched.query('{} == {}'.format(group, i))
        distance_matched = (
            sum(data_matched_group[distance] * data_matched_group['pondmen'])
            / data_matched_group['pondmen'].sum()
            )
        data_entd_group = data_entd.query('{} == {}'.format(group, i))
        distance_entd = (
            sum(data_entd_group[distance] * data_entd_group['pondmen'])
            / data_entd_group['pondmen'].sum()
            )

        df_to_plot['Matched'][i] = distance_matched
        df_to_plot['ENTD'][i] = distance_entd

    return df_to_plot


def histogram_distribution_depenses_annuelle(data_matched):
    variables = ['Ex ante', 'Ex post', ]
    quantiles = [.05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95]
    df_to_plot = pd.DataFrame(index = quantiles, columns = variables)
    for i in quantiles:
        df_to_plot['Ex ante'][i] = data_matched['poste_07_2_2_1_1'].quantile(i)
        df_to_plot['Ex post'][i] = data_matched['depenses_carburants_corrigees_entd'].quantile(i)

    return df_to_plot


# for categ in ['niveau_vie_decile', 'strate']:
#    for froid in ['froid', 'froid_4_criteres']:
#        df_to_plot = histogram_froid_group(data_matched_enl, data_enl, froid, categ)
#        graph_builder_bar_percent(df_to_plot)
#        save_dataframe_to_graph(df_to_plot, 'Matching/enl_{0}_{1}.csv'.format(froid, categ))

# for categ in ['niveau_vie_decile', 'strate']:
#    for distance in ['distance']:
#        df_to_plot = histogram_distance_group(data_matched_entd, data_entd, distance, categ)
#        graph_builder_bar(df_to_plot, False)
#        save_dataframe_to_graph(df_to_plot, 'Matching/entd_{0}_{1}.csv'.format(distance, categ))

df_to_plot = histogram_distribution_depenses_annuelle(data_matched_final_entd)
graph_builder_bar(df_to_plot, False)
save_dataframe_to_graph(df_to_plot, 'Matching/entd_distance_before_after_matching.csv')
