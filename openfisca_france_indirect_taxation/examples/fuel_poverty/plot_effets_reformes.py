# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

import numpy as np
import pandas as pd
import seaborn

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.fuel_poverty.nombre_precaires import nombre_precaires_reformes
from openfisca_france_indirect_taxation.examples.fuel_poverty.effets_reformes import effets_reformes_precarite
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar_percent, save_dataframe_to_graph

seaborn.set_palette(seaborn.color_palette("Set2", 12))


def plot_precarite(indicateur):
    reformes = ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']
    statuts = ['reference', 'before', 'after']
    dataframe_logement = pd.DataFrame(index = reformes, columns=statuts)
    dataframe_logement = dataframe_logement.drop(['rattrapage_diesel'])
    dataframe_transport = pd.DataFrame(index = reformes, columns=statuts)
    dict_reformes = dict()
    for reforme in reformes:
        (dict_reformes['logement - {}'.format(reforme)], dict_reformes['transport - {}'.format(reforme)]) = \
            nombre_precaires_reformes(reforme, year, data_year)
        for statut in statuts:
            if reforme != 'rattrapage_diesel':
                dataframe_logement[statut][reforme] = \
                    dict_reformes['logement - {}'.format(reforme)]['{0} - {1} - {2}'.format(indicateur, reforme, statut)]
            dataframe_transport[statut][reforme] = \
                dict_reformes['transport - {}'.format(reforme)]['{0} - {1} - {2}'.format(indicateur, reforme, statut)]

    graph_builder_bar_percent(dataframe_logement)
    graph_builder_bar_percent(dataframe_transport)


def plot_effet_reformes_indicateurs(indicateur):
    reformes = ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']
    statuts = ['before', 'after']
    dataframe_logement = pd.DataFrame(index = reformes, columns=statuts)
    dataframe_logement = dataframe_logement.drop(['rattrapage_diesel'])
    dataframe_transport = pd.DataFrame(index = reformes, columns=statuts)
    dict_reformes = dict()
    for reforme in reformes:
        (dict_reformes['logement - {}'.format(reforme)], dict_reformes['transport - {}'.format(reforme)]) = \
            effets_reformes_precarite(reforme, year, data_year)
        for statut in statuts:
            if reforme != 'rattrapage_diesel':
                dataframe_logement[statut][reforme] = \
                    dict_reformes['logement - {}'.format(reforme)]['{0} - {1} - {2}'.format(indicateur, reforme, statut)]
            dataframe_transport[statut][reforme] = \
                dict_reformes['transport - {}'.format(reforme)]['{0} - {1} - {2}'.format(indicateur, reforme, statut)]

    save_dataframe_to_graph(
        dataframe_logement, 'Precarite/effet_reformes_{}_logement.csv'.format(indicateur)
        )
    save_dataframe_to_graph(
        dataframe_transport, 'Precarite/effet_reformes_{}_transport.csv'.format(indicateur)
        )


    graph_builder_bar_percent(dataframe_logement)
    graph_builder_bar_percent(dataframe_transport)



if __name__ == '__main__':    
    year = 2014
    data_year = 2011
    inflators_by_year = get_inflators_by_year_energy(rebuild = False)
    elasticities = get_elasticities(data_year)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
    
    #plot_precarite('precarite')
    plot_effet_reformes_indicateurs('precarite')
