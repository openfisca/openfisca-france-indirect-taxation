# -*- coding: utf-8 -*-

'''
Computing the Hellinger distance between two discrete
probability distributions
'''

# To be completed : add missing variables

import pandas as pd
from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_2_homogenize_variables import \
    create_niveau_vie_quantiles
from openfisca_france_indirect_taxation.build_survey_data.utils import \
    hellinger

data_entd, data_bdf = create_niveau_vie_quantiles(year_data = 2017)


def hellinger_variable(df1, df2, var, weight_col="pondmen"):
    """
    Compute Hellinger distance between two weighted distributions of a variable.

    Parameters
    ----------
    df1 : pd.DataFrame
        First dataset.
    df2 : pd.DataFrame
        Second dataset.
    var : str
        Variable name to compare (categorical or numeric).
    weight_col : str
        Column name for weights (default: 'pondmen').

    Returns
    -------
    float
        Hellinger distance between distributions of `var` in df1 and df2.
    """
    # Vérification des colonnes
    for df in [df1, df2]:
        if var not in df.columns or weight_col not in df.columns:
            raise ValueError(f"La colonne '{var}' ou '{weight_col}' est manquante.")

    # Suppression des NaN
    df1 = df1.dropna(subset=[var, weight_col])
    df2 = df2.dropna(subset=[var, weight_col])

    # Conversion en numérique
    df1[var] = pd.to_numeric(df1[var], errors='coerce')
    df2[var] = pd.to_numeric(df2[var], errors='coerce')

    # Calcul des distributions
    categories = pd.Index(sorted(set(df1[var].unique()) | set(df2[var].unique())))
    dist1 = (df1.groupby(var)[weight_col].sum() / df1[weight_col].sum()).reindex(categories, fill_value=0)
    dist2 = (df2.groupby(var)[weight_col].sum() / df2[weight_col].sum()).reindex(categories, fill_value=0)

    # Calcul de la distance
    distance = hellinger(dist1.tolist(), dist2.tolist())

    return dist1, dist2, distance


# Age de le personne de référence
dist1, dist2, hellinger_distance = hellinger_variable(data_bdf, data_entd, var = 'agepr', weight_col = 'pondmen')

# hellinger_age_carte_grise = hellinger_age_carte_grise(data_bdf, data_entd)

# Age du véhicule
dist1, dist2, hellinger_distance = hellinger_variable(data_bdf, data_entd, var = 'age_vehicule', weight_col = 'pondmen')

# By construction, the distance should be extremely close to 0 but not really the case here)
dist1, dist2, hellinger_distance = hellinger_variable(data_bdf, data_entd, var = 'niveau_vie_decile', weight_col = 'pondmen')

# Diplôme le plus élevé de la personne de référence
dist1, dist2, hellinger_distance = hellinger_variable(data_bdf, data_entd, var = 'dip14pr', weight_col = 'pondmen')

# Nombre d'attifs dans le ménage
dist1, dist2, hellinger_distance = hellinger_variable(data_bdf, data_entd, var = 'nactifs', weight_col = 'pondmen')

# Nombre de véhicules diesel 
dist1, dist2, hellinger_distance = hellinger_variable(data_bdf, data_entd, var = 'nb_diesel', weight_col = 'pondmen')

# Nombre de véhicules essence
dist1, dist2, hellinger_distance = hellinger_variable(data_bdf, data_entd, var = 'nb_essence', weight_col = 'pondmen')

# Nombre de véhicules essence
dist_essence, _, hellinger_nb_essence = hellinger_variable(data_bdf, data_entd, var='nb_essence', weight_col='pondmen')

# Nombre de personnes par habitation
_, _, hellinger_nbphab = hellinger_variable(data_bdf, data_entd, var='nbphab', weight_col='pondmen')

# Nombre d'enfants
_, _, hellinger_nenfants = hellinger_variable(data_bdf, data_entd, var='nenfants', weight_col='pondmen')

# Nombre total de personnes
_, _, hellinger_npers = hellinger_variable(data_bdf, data_entd, var='npers', weight_col='pondmen')

# OCDE 10
_, _, hellinger_ocde10 = hellinger_variable(data_bdf, data_entd, var='ocde10', weight_col='pondmen')

# Quintiles
_, _, hellinger_quintiles = hellinger_variable(data_bdf, data_entd, var='quintiles', weight_col='pondmen')

# Situation professionnelle
_, _, hellinger_situapr = hellinger_variable(data_bdf, data_entd, var='situapr', weight_col='pondmen')

# Statut logique (stalog)
_, _, hellinger_stalog = hellinger_variable(data_bdf, data_entd, var='stalog', weight_col='pondmen')

# Taux d'activité (tau)
_, _, hellinger_tau = hellinger_variable(data_bdf, data_entd, var='tau', weight_col='pondmen')

# Test (variable de test)
_, _, hellinger_test = hellinger_variable(data_bdf, data_entd, var='test', weight_col='pondmen')

# Taux d'urbanisme (tuu)
_, _, hellinger_tuu = hellinger_variable(data_bdf, data_entd, var='tuu', weight_col='pondmen')

# Type de ménage (typmen)
_, _, hellinger_typmen = hellinger_variable(data_bdf, data_entd, var='typmen', weight_col='pondmen')

# Nombre total de véhicules
_, _, hellinger_veh_tot = hellinger_variable(data_bdf, data_entd, var='veh_tot', weight_col='pondmen')


def hellinger_mloy_d(data_bdf, data_entd):  # comprendre ce qui ne va pas ici
    data_bdf['mloy_d'] = data_bdf['mloy_d'].astype(float)
    data_bdf['mloy_d_racine'] = (data_bdf['mloy_d']) ** (0.5)
    mloy_d_racine_max_bdf = data_bdf['mloy_d_racine'].max()

    data_entd['mloy_d'] = data_entd['mloy_d'].astype(float)
    data_entd['mloy_d_racine'] = (data_entd['mloy_d']) ** (0.5)
    mloy_d_racine_max_entd = data_entd['mloy_d_racine'].max()

    mloy_d_racine_max = max(mloy_d_racine_max_bdf, mloy_d_racine_max_entd)
    data_bdf['mloy_d_groupe'] = (data_bdf['mloy_d_racine'] / mloy_d_racine_max).round(decimals = 2)
    data_entd['mloy_d_groupe'] = (data_entd['mloy_d_racine'] / mloy_d_racine_max).round(decimals = 2)

    distribution_bdf = dict()
    for i in range(0, 101):
        j = float(i) / 100
        distribution_bdf['{}'.format(j)] = (data_bdf.query('mloy_d_groupe == {}'.format(j))['pondmen'].sum()
/ data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, 101):
        j = float(i) / 100
        distribution_entd['{}'.format(j)] = (data_entd.query('mloy_d_groupe == {}'.format(j))['pondmen'].sum()
/ data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_mloy_d = hellinger_mloy_d(data_bdf, data_entd)


# Test if two opposite distributions have hellinger distance = 1
def hellinger_test(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(1, 51):
        distribution_bdf['{}'.format(i)] = 0.02
    for i in range(51, 101):
        distribution_bdf['{}'.format(i)] = 0

    distribution_entd = dict()
    for i in range(1, 51):
        distribution_entd['{}'.format(i)] = 0
    for i in range(51, 101):
        distribution_entd['{}'.format(i)] = 0.02

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance
