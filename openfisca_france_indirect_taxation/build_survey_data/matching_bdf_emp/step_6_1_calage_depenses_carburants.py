# Dans ce script on transforme les distances imputées en dépenses, sur la base des dépenses
# moyennes de chaque groupe de ménages. On prend ainsi en compte les différences de consommation
# des véhicules par type de ménage.

import os
import pandas as pd

from openfisca_france_indirect_taxation.utils import assets_directory


def calage_depenses_from_distance(data_matched):
    """
    Adjust fuel expenditures based on distance traveled,
    corrected by decile of living standard and rural/urban status.
    """

    # group by decile and rural flag
    grouped = data_matched.groupby(['niveau_vie_decile', 'rural'])

    for (decile, rur), group in grouped:
        # weighted averages
        avg_distance = (group['distance'] * group['pondmen']).sum() / group['pondmen'].sum()
        avg_depenses = (group['poste_07_2_2_1'] * group['pondmen']).sum() / group['pondmen'].sum()

        # correction factor
        factor = avg_depenses / avg_distance if avg_distance != 0 else 0

        # assign corrected expenditures
        idx = (data_matched['niveau_vie_decile'] == decile) & (data_matched['rural'] == rur)
        data_matched.loc[idx, 'depenses_carburants_corrigees_emp'] = data_matched.loc[idx, 'distance'] * factor
        data_matched.loc[idx, 'depenses_diesel_corrigees_emp'] = data_matched.loc[idx, 'distance_diesel'] * factor
        data_matched.loc[idx, 'depenses_essence_corrigees_emp'] = data_matched.loc[idx, 'distance_essence'] * factor

    return data_matched


def cale_bdf_emp_matching_data():
    data_matched_distance = pd.read_csv(
        os.path.join(
            assets_directory,
            'matching',
            'matching_emp',
            'data_matched_distance.csv'
            ), sep =',', decimal = '.'
        )
    data = calage_depenses_from_distance(data_matched_distance)
    data.to_csv(
        os.path.join(assets_directory, 'matching', 'matching_emp', 'data_matched_final.csv'),
        sep = ',', index= False)
