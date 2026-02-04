import matplotlib.pyplot as plt
import seaborn as sns

from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes


def histogram_cat_variable(data_bdf, data_entd, var, data_name_1='BdF', data_name_2='EMP', savefig=False, filename=None):
    """
    Crée un histogramme comparatif pour une variable catégorielle donnée entre deux DataFrames.

    Args:
    data_bdf(DataFrame): Premier DataFrame
    data_entd(DataFrame): Deuxième DataFrame.
    var(str): Nom de la variable à analyser.
    data_name_1(str): Légende pour le premier DataFrame (par défaut : 'BdF').
    data_name_2(str): Légende pour le deuxième DataFrame (par défaut : 'EMP').

    Returns:
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
    if savefig and filename is not None:
        plt.savefig(filename, bbox_inches='tight')
    return plt


def boxplot_variable(data_bdf, data_entd, var, data_name_1='BdF', data_name_2='EMP', savefig=False, filename=None):
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
    data_name_1 : str
        Légende pour le premier DataFrame (par défaut : 'BdF').
    data_name_2 : str
        Légende pour le deuxième DataFrame (par défaut : 'EMP').

    Returns
    -------
    matplotlib.axes.Axes
        Axe contenant le boxplot.
    """
    # Préparation des données
    df_bdf = data_bdf[[var]].copy().reset_index(drop=True)
    df_bdf['dataset'] = data_name_1

    df_entd = data_entd[[var]].copy().reset_index(drop=True)
    df_entd['dataset'] = data_name_2

    # Création du boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x = 'dataset', y=var, data=df_bdf, legend = False, color = 'b')
    sns.boxplot(x = 'dataset', y=var, data=df_entd, legend = False)
    plt.title(f'Comparaison des distributions de {var} entre {data_name_1} et {data_name_2}', fontsize=16)
    plt.xlabel('Dataset', fontsize=14)
    plt.ylabel(var, fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    if savefig and filename is not None:
        plt.savefig(filename, bbox_inches='tight')
    return plt