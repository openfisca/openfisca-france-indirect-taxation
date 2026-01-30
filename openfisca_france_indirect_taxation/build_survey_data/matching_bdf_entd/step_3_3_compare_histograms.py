# -*- coding: utf-8 -*-


# Dans ce script on utilise des histogrammes pour comparer la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_2_homogenize_variables import \
    create_niveau_vie_quantiles
from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes


data_bdf, data_entd = create_niveau_vie_quantiles(2017)


def histogram_cat_variable(data_bdf, data_entd, var, data_name_1='BdF', data_name_2='ENTD'):
    """
    Crée un histogramme comparatif pour une variable catégorielle donnée entre deux DataFrames.

    Parameters
    ----------
    data_bdf : pd.DataFrame
        Premier DataFrame.
    data_entd : pd.DataFrame
        Deuxième DataFrame.
    var : str
        Nom de la variable à analyser.
    data_name_1 : str
        Légende pour le premier DataFrame (par défaut : 'BdF').
    data_name_2 : str
        Légende pour le deuxième DataFrame (par défaut : 'ENTD').

    Returns
    -------
    matplotlib.pyplot
        Figure contenant l'histogramme.
    """
    categories = set(data_bdf[var].dropna().unique()).union(set(data_entd[var].dropna().unique()))
    list_values_bdf = []
    list_values_entd = []
    list_keys = []

    # Cas d'une variable catégorielle : utiliser les catégories fournies
    list_keys = [str(cat) for cat in categories]
    for cat in categories:
        # Calcul des proportions pondérées pour chaque catégorie
        part_bdf = data_bdf.loc[data_bdf[var] == cat, 'pondmen'].sum() / data_bdf['pondmen'].sum()
        part_entd = data_entd.loc[data_entd[var] == cat, 'pondmen'].sum() / data_entd['pondmen'].sum()
        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)

    # Appel de ta fonction histogrammes
    histogrammes(list_keys, list_values_bdf, list_values_entd, data_name_1, data_name_2)

    # Ajout des labels et titres
    plt.xlabel(f'Catégories de {var}')
    plt.ylabel('Proportion pondérée')
    plt.title(f'Comparaison des catégories de {var} entre {data_name_1} et {data_name_2}')

    plt.grid(True, linestyle='--', alpha=0.7)
    return plt


def boxplot_variable(data_bdf, data_entd, var, data_name_1='BdF', data_name_2='ENTD'):
    """
    Crée un boxplot comparatif pour une variable donnée entre deux DataFrames.

    Parameters
    ----------
    data_bdf : pd.DataFrame
        Premier DataFrame.
    data_entd : pd.DataFrame
        Deuxième DataFrame.
    var : str
        Nom de la variable à analyser.
    title_bdf : str
        Légende pour le premier DataFrame (par défaut : 'BdF').
    title_entd : str
        Légende pour le deuxième DataFrame (par défaut : 'ENTD').

    Returns
    -------
    matplotlib.axes.Axes
        Axe contenant le boxplot.
    """
    # Préparation des données
    df_plot = pd.concat([
        data_bdf[[var]].copy().assign(dataset=data_name_1),
        data_entd[[var]].copy().assign(dataset=data_name_2)
        ])

    # Création du boxplot
    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(x='dataset', y=var, data=df_plot)
    plt.title(f'Comparaison des distributions de {var} entre {data_name_1} et {data_name_2}')
    plt.grid(True, linestyle='--', alpha=0.7)

    return ax


histogram_cat_variable(data_bdf, data_entd, var = 'age_vehicule', data_name_1='BdF', data_name_2='ENTD')

boxplot_variable(data_bdf, data_entd, var = 'age_carte_grise', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'aides_logement', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'cataeu', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'cs42pr', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'dip14pr', data_name_1='BdF', data_name_2='ENTD')

boxplot_variable(data_bdf, data_entd, var = 'mloy_d', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'nactifs', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'veh_tot', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'nb_diesel', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'nb_essence', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'nenfants', data_name_1='BdF', data_name_2='ENTD')

boxplot_variable(data_bdf, data_entd, var = 'niveau_vie', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'npers', data_name_1='BdF', data_name_2='ENTD')

boxplot_variable(data_bdf, data_entd, var = 'ocde10', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'situapr', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'stalog', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'typmen', data_name_1='BdF', data_name_2='ENTD')

histogram_cat_variable(data_bdf, data_entd, var = 'tuu', data_name_1='BdF', data_name_2='ENTD')
