import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns 
import wquantiles
from collections import OrderedDict

from openfisca_france_indirect_taxation.variables.base import * 
from openfisca_survey_manager.variables import create_quantile
from openfisca_survey_manager.statshelpers import mark_weighted_percentiles

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
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
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


def weighted_quantiles(data, labels, weights, return_quantiles = False):
    num_categories = len(labels)
    breaks = np.linspace(0, 1, num_categories + 1)
    quantiles = quantiles = [wquantiles.quantile_1D(data, weights, b) for b in breaks]
    ret = np.zeros(len(data))
    for i in range(len(labels)):
        lower = quantiles[i]
        upper = quantiles[i + 1]

        if i == len(labels) - 1:
            # Include upper bound in the last bin
            mask = (data >= lower) & (data <= upper)
        else:
            mask = (data >= lower) & (data < upper)

        ret[mask] = labels[i]

    if return_quantiles:
        return ret, quantiles
    else:
        return ret
    

# Sera utile le jour où l'entity 'Individu' sera initialisée.
def create_quantile_indiv(x, nquantiles, entity_name):
    class quantile_indiv(Variable):
        value_type = int
        entity = Individu
        label = "Quantile"
        definition_period = YEAR

        def formula(individu, period):

            uc = individu.menage('ocde10', period)
            liste_par_uc = [
                'niveau_de_vie',
                ]
            try:
                if entity_name == 'menage':
                    if x in liste_par_uc:
                        variable = individu.menage(x, period) * uc
                    else:
                        variable = individu.menage(x, period)
                        
                elif entity_name == 'individu':
                    variable = individu.menage.sum(individu.menage.members(x, period))

            except ValueError:
                if entity_name == 'menage':
                    if x in liste_par_uc:
                        variable = individu.menage(x, period, options = [ADD]) * uc
                    else:
                        variable = individu.menage(x, period, options = [ADD])
                elif entity_name == 'individu':
                    variable = individu.menage.sum(individu.menage.members(x, period, options = [ADD]))

            variable_indiv = variable / uc

            if 'weight_ind' in individu.variables(period):
                weight = individu('weight_ind', period)
            else:
                weight = individu.menage('pondmen', period)

            labels = np.arange(1, nquantiles + 1)
            method = 2
            if len(weight) == 1:
                return weight * 0
            quantile, values = mark_weighted_percentiles(variable_indiv, labels, weight, method, return_quantiles = True)
            del values
            return quantile

    return quantile_indiv

def create_data_frame_by_quantile_indiv(
    survey_scenario,
    use_baseline = True,
    difference = False,
    filter_by = None, # Restriction pour les statistiques produites, pas pour la définition des quantiles
    year = None,
    y_variables = [], x_variable = 'niveau_de_vie', filter_variables = [],
    nquantiles = 10,
    aggfunc = 'mean',
    export_casd = False,
    ):
    """

    Produit une table avec les montants moyens (ou autres opérations) d'une variable par quantile d'une autre.

    :param y_variable: Variable d'intérêt représentée
    :param x_variable: Variable servant à classer la population par quantile
    :param xtile: Nombre de quantiles à définir

    """
    assert year is not None
    assert len(y_variables) > 0
    entity = survey_scenario.tax_benefit_systems["baseline"].variables[x_variable].entity.key
    quantile_indiv = create_quantile_indiv(
            x = x_variable,
            nquantiles = nquantiles,
            entity_name = entity,
            )
    survey_scenario.tax_benefit_systems["baseline"].replace_variable(quantile_indiv)
    survey_scenario.simulations["baseline"].delete_arrays('quantile_indiv')
    if "reform" in survey_scenario.tax_benefit_systems.keys():
        survey_scenario.tax_benefit_systems["reform"].replace_variable(quantile_indiv)
    if "reform" in survey_scenario.simulations.keys():
        survey_scenario.simulations["reform"].delete_arrays('quantile_indv')

    df = survey_scenario.create_data_frame_by_entity(
    variables = [x_variable,'quantile', 'unites_consommation', 'wprm'] + y_variables + filter_variables,
    period = year,
    merge = True,
    )

    if difference:
        reform_df = survey_scenario.create_data_frame_by_entity(
            variables = [x_variable] + y_variables,
            use_baseline = False,
            period = year,
            merge = True,
            )
        df = survey_scenario.create_data_frame_by_entity(
            variables = [x_variable,'quantile','unites_consommation', 'weight_ind', 'wprm'] + y_variables + filter_variables,
            use_baseline = True,
            period = year,
            merge = True,
            )
        df[[x_variable] + y_variables] = reform_df[[x_variable] + y_variables] - df[[x_variable] + y_variables]

    else :
        df = survey_scenario.create_data_frame_by_entity(
            variables = [x_variable,'quantile','unites_consommation', 'weight_ind', 'wprm'] + y_variables + filter_variables,
            use_baseline = True,
            period = year,
            merge = True,
            )

    for y in y_variables:
        if y not in ['age', 'nb_pac', 'unites_consommation', 'menage_etudiant']: # liste non exhaustive d'exceptions
            if  survey_scenario.tax_benefit_systems["baseline"].variables[y].entity.key == "individu":
                df[y] = df[y].groupby(df['menage_id']).transform('sum') / df['unites_consommation']
            if  ((survey_scenario.tax_benefit_systems["baseline"].variables[y].entity.key == "menage") & (y not in ["niveau_de_vie","revenus_bruts_menage_par_uc"])):
                df[y] = df[y] / df['unites_consommation']

    if filter_by is not None:
        df = df.query(filter_by)

    df_quantile = pd.DataFrame()
    df= df[['quantile', 'weight_ind', 'ocde10', 'wprm', 'menage_id', 'menage_role'] + y_variables]
    df['n'] = 1
    if aggfunc == 'mean':
        for y in y_variables:
            df[y] = df[y] * df['weight_ind']
            df_quantile[y] = df.groupby('quantile')[y].sum() / df.groupby('quantile')['weight_ind'].sum()
# montant perçu par les ménages, la somme totale du ménage est attribuée au représentant du ménage, qu'importe l'entité initiale de la variable   
#    elif aggfunc == 'sum':
#        for y in y_variables:
#            df_temp = df.query('menage_role == 0')
#            df_temp[y] = df_temp[y] * df_temp['unites_consommation'] * df_temp['wprm']
#            df_quantile[y] = df_temp.groupby('quantile')[y].sum()
# Nombre de personnes qui sont dans un ménage qui perçoit un montant non nul
#    elif aggfunc == 'count':
#        for y in y_variables:
#            df[y] = np.where(df[y] != 0, 1, 0)
#            df[y] = df[y] * df['weight_ind']
#            df_quantile[y] = df.groupby('quantile')[y].sum()

    df_quantile['n'] = df.groupby('quantile')['n'].sum()
    df_quantile['effectif_pondere'] = df.groupby('quantile')['weight_ind'].sum()

    df_quantile['quantile'] = df_quantile.index

    if export_casd == True:
        df_quantile = df_quantile.query('n > 11')

    return df_quantile




