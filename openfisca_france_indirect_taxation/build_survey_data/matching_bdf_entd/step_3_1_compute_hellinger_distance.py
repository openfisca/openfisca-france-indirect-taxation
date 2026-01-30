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

data_bdf, data_entd = create_niveau_vie_quantiles(year_data = 2017)


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
    df1.loc[:, var] = pd.to_numeric(df1[var], errors='coerce')
    df2.loc[:, var] = pd.to_numeric(df2[var], errors='coerce')

    # Calcul des distributions
    categories = pd.Index(sorted(set(df1[var].unique()) | set(df2[var].unique())))
    dist1 = (df1.groupby(var)[weight_col].sum() / df1[weight_col].sum()).reindex(categories, fill_value=0)
    dist2 = (df2.groupby(var)[weight_col].sum() / df2[weight_col].sum()).reindex(categories, fill_value=0)

    # Calcul de la distance
    distance = hellinger(dist1.tolist(), dist2.tolist())

    return dist1, dist2, distance


# Âge de la personne de référence
dist_bdf_agepr, dist_entd_agepr, hellinger_agepr = hellinger_variable(data_bdf, data_entd, var='agepr', weight_col='pondmen')

# Âge du véhicule
dist_bdf_age_vehicule, dist_entd_age_vehicule, hellinger_age_vehicule = hellinger_variable(data_bdf, data_entd, var='age_vehicule', weight_col='pondmen')

# Niveau de vie (déciles)
dist_bdf_niveau_vie_decile, dist_entd_niveau_vie_decile, hellinger_niveau_vie_decile = hellinger_variable(data_bdf, data_entd, var='niveau_vie_decile', weight_col='pondmen')

# Diplôme le plus élevé de la personne de référence
dist_bdf_dip14pr, dist_entd_dip14pr, hellinger_dip14pr = hellinger_variable(data_bdf, data_entd, var='dip14pr', weight_col='pondmen')

# Nombre d'actifs dans le ménage
dist_bdf_nactifs, dist_entd_nactifs, hellinger_nactifs = hellinger_variable(data_bdf, data_entd, var='nactifs', weight_col='pondmen')

# Nombre de véhicules diesel
dist_bdf_nb_diesel, dist_entd_nb_diesel, hellinger_nb_diesel = hellinger_variable(data_bdf, data_entd, var='nb_diesel', weight_col='pondmen')

# Nombre de véhicules essence
dist_bdf_nb_essence, dist_entd_nb_essence, hellinger_nb_essence = hellinger_variable(data_bdf, data_entd, var='nb_essence', weight_col='pondmen')

# Nombre d'enfants
dist_bdf_nenfants, dist_entd_nenfants, hellinger_nenfants = hellinger_variable(data_bdf, data_entd, var='nenfants', weight_col='pondmen')

# Nombre total de personnes
dist_bdf_npers, dist_entd_npers, hellinger_npers = hellinger_variable(data_bdf, data_entd, var='npers', weight_col='pondmen')

# OCDE 10
dist_bdf_ocde10, dist_entd_ocde10, hellinger_ocde10 = hellinger_variable(data_bdf, data_entd, var='ocde10', weight_col='pondmen')

# Quintiles
dist_bdf_quintiles, dist_entd_quintiles, hellinger_quintiles = hellinger_variable(data_bdf, data_entd, var='niveau_vie_quintile', weight_col='pondmen')

# Situation professionnelle
dist_bdf_situapr, dist_entd_situapr, hellinger_situapr = hellinger_variable(data_bdf, data_entd, var='situapr', weight_col='pondmen')

# Taux d'urbanisme (tuu)
dist_bdf_tuu, dist_entd_tuu, hellinger_tuu = hellinger_variable(data_bdf, data_entd, var='tuu', weight_col='pondmen')

# Type de ménage (typmen)
dist_bdf_typmen, dist_entd_typmen, hellinger_typmen = hellinger_variable(data_bdf, data_entd, var='typmen', weight_col='pondmen')

# Nombre total de véhicules
dist_bdf_veh_tot, dist_entd_veh_tot, hellinger_veh_tot = hellinger_variable(data_bdf, data_entd, var='veh_tot', weight_col='pondmen')
