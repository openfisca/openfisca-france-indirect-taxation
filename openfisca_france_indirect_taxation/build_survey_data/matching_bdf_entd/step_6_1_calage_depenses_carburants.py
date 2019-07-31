

# Dans ce script on transforme les distances imputées en dépenses, sur la base des dépenses
# moyennes de chaque groupe de ménages. On rend ainsi compte des différences de consommation
# des véhicules par type de ménage.

import os
import pkg_resources
import pandas as pd

# Importation des bases de données appariées et de la base de référence entd
default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)


data_matched_distance = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'matching_entd',
        'data_matched_distance.csv'
        ), sep =',', decimal = '.'
    )


data_matched_random = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'matching_entd',
        'data_matched_random.csv'
        ), sep =',', decimal = '.'
    )


def calage_depenses_from_distance(data_matched):
    for i in range(1, 11):
        for rur in [0, 1]:
            data_matched_group = data_matched.query('niveau_vie_decile == {}'.format(i)).query('rural == {}'.format(rur))
            avg_distance = (
                sum(data_matched_group['distance'] * data_matched_group['pondmen'])
                / data_matched_group['pondmen'].sum()
                )
            avg_depenses = (
                sum(data_matched_group['poste_07_2_2_1_1'] * data_matched_group['pondmen'])
                / data_matched_group['pondmen'].sum()
                )

            data_matched.loc[(data_matched['niveau_vie_decile'] == i) & (data_matched['rural'] == rur), 'depenses_carburants_corrigees_entd'] = \
                data_matched['distance'] * avg_depenses / avg_distance

            data_matched.loc[(data_matched['niveau_vie_decile'] == i) & (data_matched['rural'] == rur), 'depenses_diesel_corrigees_entd'] = \
                data_matched['distance_diesel'] * avg_depenses / avg_distance

            data_matched.loc[(data_matched['niveau_vie_decile'] == i) & (data_matched['rural'] == rur), 'depenses_essence_corrigees_entd'] = \
                data_matched['distance_essence'] * avg_depenses / avg_distance

    return data_matched


if __name__ == "__main__":
    data = calage_depenses_from_distance(data_matched_distance)

    # Sauvegarde des données dans des fichiers .csv
    data.to_csv(os.path.join(default_config_files_directory, 'openfisca_france_indirect_taxation', 'assets',
        'matching', 'matching_entd', 'data_matched_final.csv'), sep = ',')
