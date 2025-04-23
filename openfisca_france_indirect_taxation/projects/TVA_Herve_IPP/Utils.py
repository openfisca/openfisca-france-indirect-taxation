import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns 

output_path = "C:/Users/veve1/OneDrive/Documents/IPP/Budget 2026 TVA/Figures/"

def stacked_bar_plot(df, variables, labels, title="Graphique à barres empilées", xlabel="Catégories", ylabel="Valeurs", colors = None, savefig = False, outfile = None):
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
    fig, ax =  plt.subplots(figsize=(10, 7.5))

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
    ax.set_xlabel(xlabel, fontdict= {'fontsize' : 15})
    ax.set_ylabel(ylabel,  fontdict= {'fontsize' : 15})
    ax.set_title(title, fontdict= {'fontsize' : 17})
    ax.tick_params(axis='y', labelsize=12)
    #ax.set_yticks(np.arange(0.1,1.1,0.1))
    ax.set_xticks(x)
    ax.set_xticklabels(df.index, fontsize = 12)
    ax.legend(loc = 'upper center', bbox_to_anchor = (0.5, -0.1), ncol = 3, fontsize = 12)
    
    plt.xticks()
    if savefig and outfile:
            plt.savefig(os.path.join(output_path,outfile), bbox_inches = 'tight')
    plt.show()
