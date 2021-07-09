# Import de modules généraux


import csv
import os

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import simulate_df_calee_on_ticpe
from openfisca_france_indirect_taxation.utils import assets_directory

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Liste des variables que l'on veut simuler
    simulated_variables = [
        'pondmen',
        'depenses_diesel',
        'depenses_essence',
        'coicop12_7'
        ]

    # Calcul des dépenses agrégées des ménages dans les transports, dont les carburants, dont l'essence et le diesel
    depenses_transports_totales = dict()
    depenses_carburants_totales = dict()
    depenses_diesel_totales = dict()
    depenses_essence_totales = dict()
    for year in [2000, 2005, 2011]:
        data_simulation = simulate_df_calee_on_ticpe(simulated_variables = simulated_variables, year = year)
        depenses_diesel = (data_simulation['depenses_diesel'] * data_simulation['pondmen']).sum()
        depenses_essence = (data_simulation['depenses_essence'] * data_simulation['pondmen']).sum()
        depenses_carburants = depenses_diesel + depenses_essence
        depenses_transports = (data_simulation['coicop12_7'] * data_simulation['pondmen']).sum()

        depenses_transports_totales['en {}'.format(year)] = depenses_transports / 1e6
        depenses_carburants_totales['en {}'.format(year)] = depenses_carburants / 1e6
        depenses_diesel_totales['en {}'.format(year)] = depenses_diesel / 1e6
        depenses_essence_totales['en {}'.format(year)] = depenses_essence / 1e6

    # Enregistrement des dépenses agrégées dans des fichiers csv

    writer_transports = csv.writer(open(os.path.join(assets_directory, 'depenses', 'depenses_transports_totales_bdf.csv'), 'wb'))
    for key, value in list(depenses_transports_totales.items()):
        writer_transports.writerow([key, value])

    writer_carburants = csv.writer(open(os.path.join(assets_directory, 'depenses', 'depenses_carburants_totales_bdf.csv'), 'wb'))
    for key, value in list(depenses_carburants_totales.items()):
        writer_carburants.writerow([key, value])

    writer_diesel = csv.writer(open(os.path.join(assets_directory, 'depenses', 'depenses_diesel_totales_bdf.csv'), 'wb'))
    for key, value in list(depenses_diesel_totales.items()):
        writer_diesel.writerow([key, value])

    writer_essence = csv.writer(open(os.path.join(assets_directory, 'depenses', 'depenses_essence_totales_bdf.csv'), 'wb'))
    for key, value in list(depenses_essence_totales.items()):
        writer_essence.writerow([key, value])
