import matplotlib.pyplot as plt
import os
import numpy as np
import wquantiles

from tqdm import tqdm
from openfisca_france_indirect_taxation.variables.base import *
from openfisca_survey_manager.statshelpers import mark_weighted_percentiles
from openfisca_france_indirect_taxation.examples.utils_example import wavg

output_path = "C:/Users/veve1/OneDrive/Documents/IPP/Budget 2026 TVA/Figures/"


def bootstrap_weighted_mean_by_decile(df, weight_col ='pondmen', decile_col='quantile_indiv_niveau_vie', B=1000):
    bootstrap_means = {'Decile {}'.format(decile): [] for decile in sorted(df[decile_col].unique())}
    seed = 100
    for _ in tqdm(range(B)):

        for decile in sorted(df[decile_col].unique()):

            group = df.loc[df[decile_col] == decile]

            data = group[['depenses_totales_par_uc', 'niveau_de_vie', weight_col, 'npers']]
            sample_menage = data.sample(n = len(data), replace = True, random_state = seed)
            sample_indiv = sample_menage.loc[sample_menage.index.repeat(sample_menage['npers'])]
            mean_depenses = wavg(groupe = sample_indiv, var = 'depenses_totales_par_uc', weights = weight_col)  # pondération à changer
            mean_niveau_vie = wavg(groupe = sample_indiv, var = 'niveau_de_vie', weights = weight_col)         # pondération à changer
            bootstrap_means['Decile {}'.format(decile)].append(mean_depenses / mean_niveau_vie * 100)
        seed += 1
    return (bootstrap_means)


def stacked_bar_plot(df, variables, labels, title="Graphique à barres empilées", xlabel="Catégories", ylabel="Valeurs", colors = None, note = "Note", savefig = False, outfile = None, errors = None):
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
    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Indices des catégories (suppose que l'index est utilisé pour l'axe des x)
    x = np.arange(len(df))

    # Initialisation de la base pour l'empilement
    bottom = np.zeros(len(df))

    # Création des barres empilées
    for i, (var, label) in enumerate(zip(variables, labels)):
        color = colors[i] if colors else None
        yerr = df[errors] if errors is not None and i == len(label) else None
        ax.bar(x, df[var], label=label, bottom=bottom, color = color, yerr=yerr, capsize=4)
        bottom += df[var].values

    # Add error bars on the total only
    if errors is not None:
        ax.errorbar(x, bottom, yerr = df[errors], fmt='none', ecolor='black', capsize=5, linewidth=1.5)

    # Ajout des légendes et titres
    ax.set_xlabel(xlabel, fontdict= {'fontsize': 15}, fontweight ='bold')
    ax.set_ylabel(ylabel, fontdict= {'fontsize': 15}, fontweight ='bold')
    ax.set_title(title, fontdict= {'fontsize': 17}, loc = 'left', fontweight ='bold')
    ax.tick_params(axis='y', labelsize=13)
    # ax.set_yticks(np.arange(0.1,1.1,0.1))
    ax.set_xticks(x)
    ax.set_xticklabels(df.index, fontsize = 13)
    ax.legend(loc = 'upper center', bbox_to_anchor = (0.5, -0.1), ncol = 3, fontsize = 13)

    plt.xticks()
    if savefig and outfile:
        plt.savefig(os.path.join(output_path, outfile), bbox_inches = 'tight')
    plt.show()


def double_stacked_bar_plot(df1, df2, variables, labels,
                            title1="Graphique 1", title2="Graphique 2",
                            xlabel="Catégories", ylabel="Valeurs",
                            colors=None, savefig=False, outfile=None):
    """
    Trace deux graphiques à barres empilées côte à côte, axes indépendants.
    """

    if len(variables) != len(labels):
        raise ValueError("Le nombre de variables et de labels doit être identique.")
    if colors and len(colors) < len(variables):
        raise ValueError("Le nombre de couleurs doit être supérieur au nombre de variables.")

    fig, axes = plt.subplots(1, 2, figsize=(18, 7.5), sharey=True)  # <-- DIFFERENCE: sharey=False

    for ax, df, title in zip(axes, [df1, df2], [title1, title2]):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        x = np.arange(len(df))
        bottom = np.zeros(len(df))

        for i, (var, label) in enumerate(zip(variables, labels)):
            color = colors[i] if colors else None
            ax.bar(x, df[var], label=label, bottom=bottom, color=color)
            bottom += df[var].values

        ax.set_xlabel(xlabel, fontdict={'fontsize': 18}, fontweight='bold')
        ax.set_title(title, fontdict={'fontsize': 20}, loc='left', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(df.index, fontsize=16)
        ax.yaxis.set_tick_params(labelleft=True)
        ax.tick_params(axis='y', labelsize=16)

    # Add y-label to both subplots
    for ax in axes:
        ax.set_ylabel(ylabel, fontdict={'fontsize': 18}, fontweight='bold')

    # Only one legend for the two plots
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=len(variables), fontsize=17)

    plt.tight_layout()
    if savefig and outfile:
        plt.savefig(os.path.join(output_path, outfile), bbox_inches='tight')

    plt.show()


def weighted_quantiles(data, labels, weights, return_quantiles = False):
    num_categories = len(labels)
    breaks = np.linspace(0, 1, num_categories + 1)
    quantiles = [wquantiles.quantile_1D(data, weights, b) for b in breaks]
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
        filter_by = None,  # Restriction pour les statistiques produites, pas pour la définition des quantiles
        year = None,
        y_variables = None,
        x_variable = 'niveau_de_vie',
        filter_variables = None,
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
    if y_variables is None:
        y_variables = []
    if filter_variables is None:
        filter_variables = []
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
        variables = [x_variable, 'quantile', 'unites_consommation', 'wprm'] + y_variables + filter_variables,
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
            variables = [x_variable, 'quantile', 'unites_consommation', 'weight_ind', 'wprm'] + y_variables + filter_variables,
            use_baseline = True,
            period = year,
            merge = True,
            )
        df[[x_variable] + y_variables] = reform_df[[x_variable] + y_variables] - df[[x_variable] + y_variables]

    else:
        df = survey_scenario.create_data_frame_by_entity(
            variables = [x_variable, 'quantile', 'unites_consommation', 'weight_ind', 'wprm'] + y_variables + filter_variables,
            use_baseline = True,
            period = year,
            merge = True,
            )

    for y in y_variables:
        if y not in ['age', 'nb_pac', 'unites_consommation', 'menage_etudiant']:  # liste non exhaustive d'exceptions
            if survey_scenario.tax_benefit_systems["baseline"].variables[y].entity.key == "individu":
                df[y] = df[y].groupby(df['menage_id']).transform('sum') / df['unites_consommation']
            if ((survey_scenario.tax_benefit_systems["baseline"].variables[y].entity.key == "menage") & (y not in ["niveau_de_vie", "revenus_bruts_menage_par_uc"])):
                df[y] = df[y] / df['unites_consommation']

    if filter_by is not None:
        df = df.query(filter_by)

    df_quantile = pd.DataFrame()
    df = df[['quantile', 'weight_ind', 'ocde10', 'wprm', 'menage_id', 'menage_role'] + y_variables]
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

    if export_casd:
        df_quantile = df_quantile.query('n > 11')

    return df_quantile
