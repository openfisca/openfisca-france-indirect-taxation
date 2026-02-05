# -*- coding: utf-8 -*-

'''
Computing the Hellinger distance between two discrete probability distributions.
Apply it to compare distributions of variables in BDF and EMP/ENTD datasets.
'''
import pandas as pd
from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_emp.step_2_homogenize_variables import \
    create_niveau_vie_quantiles
from openfisca_france_indirect_taxation.build_survey_data.utils import \
    hellinger

output_path = "C:/Users/veve1/OneDrive/Documents/ENSAE PhD/Carbon tax/Output"
data_bdf, data_emp = create_niveau_vie_quantiles(year_data = 2017)


def hellinger_distance(df1, df2, var, weight_col="pondmen"):
    """
    Compute Hellinger distance between two weighted distributions of a variable.

    Parameters
    ----------
    df1(DataFrame): First dataset.
    df2(DataFrame): Second dataset.
    var(str): Variable name to compare (categorical or numeric).
    weight_col(str): Column name for weights (default: 'pondmen').

    Returns
    -------
    dist1(pd.Series): Weighted distribution of `var` in df1.
    dist2(pd.Series): Weighted distribution of `var` in df2.
    distance(float): Hellinger distance between distributions of `var` in df1 and df2.
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