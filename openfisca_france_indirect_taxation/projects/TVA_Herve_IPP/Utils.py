import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 

def stacked_bar_plot(df, variables, labels, title="Graphique à barres empilées", xlabel="Catégories", ylabel="Valeurs", colors = None):
    """
    Crée un bar plot empilé à partir des variables sélectionnées dans un DataFrame.

    :param df: DataFrame contenant les données
    :param variables: Liste des colonnes à empiler
    :param labels: Liste des labels pour chaque colonne
    :param title: Titre du graphique
    :param xlabel: Nom de l'axe des abscisses
    :param ylabel: Nom de l'axe des ordonnées
    """

    # Vérification que les listes sont cohérentes
    if len(variables) != len(labels):
        raise ValueError("Le nombre de variables et de labels doit être identique.")

    if colors and len(colors) < len(variables):
        raise ValueError("Le nombre de couleurs doit être supérieur au nombre de variables.")
    # Création de la figure et des axes
    fig, ax = plt.subplots(figsize=(12, 10))

    # Indices des catégories (suppose que l'index est utilisé pour l'axe des x)
    x = np.arange(len(df))

    # Initialisation de la base pour l'empilement
    bottom = np.zeros(len(df))

    # Création des barres empilées
    for i, (var, label) in enumerate(zip(variables, labels)):
        color = colors[i] if colors else None
        ax.bar(x, df[var], label=label, bottom=bottom, color = color)
        bottom +=df[var].values

    # Ajout des légendes et titres
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    #ax.set_yticks(np.arange(0.1,1.1,0.1))
    ax.set_xticks(x)
    ax.set_xticklabels(df.index)
    ax.legend(loc = 'upper center', bbox_to_anchor = (0.5, -0.1), ncol= 3)
    
    plt.xticks()
    plt.show()
