# -*- coding: utf-8 -*-


# Import de modules généraux
from __future__ import division

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import simulate, df_weighted_average_grouped, \
    graph_builder_bar


if __name__ == '__main__':

    # Liste des coicop agrégées en 12 postes
    list_coicop12 = []
    for coicop12_index in range(1, 13):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))
    # Liste des variables que l'on veut simuler
    simulated_variables = [
        'pondmen',
        'decuc',
        'niveau_vie_decile',
        ]
    # Merge des deux listes
    simulated_variables += list_coicop12

    p = dict()
    df_to_graph = None
    for year in [2000, 2005, 2011]:
        # Constition d'une base de données des parts de chaque poste de consommation dans les dépenses des
        # ménages, par décile de revenu
        simulation_data_frame = simulate(simulated_variables = simulated_variables, year = year)
        if year == 2011:
            simulation_data_frame.niveau_vie_decile[simulation_data_frame.decuc == 10] = 10
        simulation_data_frame['depenses_tot'] = 0
        for i in range(1, 13):
            simulation_data_frame['depenses_tot'] += simulation_data_frame['coicop12_{}'.format(i)]
        var_to_concat = list_coicop12 + ['depenses_tot']
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame,
            groupe = 'niveau_vie_decile', varlist = var_to_concat)

        # Calcul des parts de chaque poste et réalisation des graphiques
        for i in range(1, 13):
            aggregates_data_frame['part_coicop12_{}'.format(i)] = \
                aggregates_data_frame['coicop12_{}'.format(i)] / aggregates_data_frame['depenses_tot']

        appendable = aggregates_data_frame[['part_coicop12_{}'.format(i) for i in range(1, 13)]]

        graph_builder_bar(appendable)
