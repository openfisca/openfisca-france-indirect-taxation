# -*- coding: utf-8 -*-

import datetime
import pandas as pd

from openfisca_france_indirect_taxation.tests import base
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_line, save_dataframe_to_graph

"""Nous simulons les montants de ticpe payés par un ménage selon le type de véhicule dont il dispose
Nous prenons un ménage dont les dépenses annuelles en carburants s'élèveraient à 1000 euros
C'est en dessous de la moyenne de nos samples (plutôt autour de 1500)"""

index = range(2000, 2014)
columns = ['si une essence et une diesel', 'si seulement vehicules diesel', 'si seulement vehicules essence']
depenses_ticpe_pour_1000_euros_carbu = pd.DataFrame(index = index, columns = columns)

for element in columns:
    if element == 'si seulement vehicules essence':
        dies = 0
    else:
        dies = 1
    if element == 'si seulement vehicules diesel':
        ess = 0
    else:
        ess = 1
    for year in range(2000, 2014):
        year = year
        simulation = base.tax_benefit_system.new_scenario().init_single_entity(
            period = year,
            personne_de_reference =dict(
                birth = datetime.date(year - 40, 1, 1),
                ),
            menage = dict(
                depenses_carburants = 1000,
                veh_essence = ess,
                veh_diesel = dies,
                ),
            ).new_simulation(debug = True)

        depenses_ticpe_pour_1000_euros_carbu.loc[depenses_ticpe_pour_1000_euros_carbu.index == year, element] = \
            simulation.calculate('ticpe_totale')

graph_builder_line(depenses_ticpe_pour_1000_euros_carbu)
save_dataframe_to_graph(depenses_ticpe_pour_1000_euros_carbu, 'cas_type_1000€_carbu.csv')
