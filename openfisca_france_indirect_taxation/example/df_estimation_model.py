# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 17:00:01 2015

@author: hadrien
"""


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import logging
import numpy
import pandas

from __future__ import division

from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import openfisca_france_indirect_taxation
from openfisca_survey_manager.survey_collections import SurveyCollection

from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_data.temporary import TemporaryStore


def get_input_data_frame(year):
    openfisca_survey_collection = SurveyCollection.load(
        collection = "openfisca_indirect_taxation", config_files_directory = config_files_directory)
    openfisca_survey = openfisca_survey_collection.get_survey("openfisca_indirect_taxation_data_{}".format(year))
    input_data_frame = openfisca_survey.get_values(table = "input")
    input_data_frame.reset_index(inplace = True)
    return input_data_frame


def simulate_df(var_to_be_simulated, year = 2011):
    '''
    Construction de la DataFrame à partir de laquelle sera faite l'analyse des données
    '''
    input_data_frame = get_input_data_frame(year)
    TaxBenefitSystem = openfisca_france_indirect_taxation.init_country()

    tax_benefit_system = TaxBenefitSystem()
    survey_scenario = SurveyScenario().init_from_data_frame(
        input_data_frame = input_data_frame,
        tax_benefit_system = tax_benefit_system,
        year = year,
        )
    simulation = survey_scenario.new_simulation()
    return DataFrame(
        dict([
            (name, simulation.calculate(name)) for name in var_to_be_simulated

            ])
        )


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)


    list_coicop12 = []
    for coicop12_index in range(1, 13):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))
    # Liste des variables que l'on veut simuler
    var_to_be_simulated = [
        'ident_men',
        'pondmen',
        'decile',
        'revtot',
        'somme_coicop12',
        'ocde10',
        'vag',
        'typmen',
        'decuc',
        'rev_disponible',
        'niveau_de_vie'
        ]
    # Merge des deux listes
    var_to_be_simulated += list_coicop12

    # Constition d'une base de données agrégée par décile (= collapse en stata)
    df = simulate_df(var_to_be_simulated = var_to_be_simulated)
    if year == 2011:
        df.decile[df.decuc == 10 ] = 10


    # Construction des parts
    list_part_coicop12 = []
    for i in range(1, 13):
        df['part_coicop12_{}'.format(i)] = df['coicop12_{}'.format(i)] / df['somme_coicop12']

    for i in range(1, 13):
        del df['coicop12_{}'.format(i)]
        df['w{}'.format(i)] = df['part_coicop12_{}'.format(i)]
        del df['part_coicop12_{}'.format(i)]


    df['depenses_tot'] = df['somme_coicop12']
    del df['somme_coicop12']
    var_list = [column for column in input_data_frame.columns if column.startswith('0') or column.startswith('1')]
    data_merge = input_data_frame[var_list]
    df = df.merge(data_merge, left_index = True, right_index = True)
    for var in var_list:
        df[var] = df[var]/df['depenses_tot']
    for var in var_list:
        df['pb_{}'.format(var)] = df[var]
    for var in var_list:
        del df[var]
    df = df[(df.typmen > 0)]
    df['vag'] = df['vag'].astype(int)

    df['ident_men'] = df['ident_men'].astype(int)
    df['typmen'] = df['typmen'].astype(int)
    var_list_ = [column for column in df.columns if column.startswith('w') or column.startswith('pb')]
    for var in var_list_:
         df[var] = df[var].astype(float)

    #♥df['decile_bis']= weighted_quantiles('niveau_de_vie', 'labels', 'pondmen', return_quantiles = True)

    df_2011 = df
    df_2011.to_stata('C:\Users\hadrien\Desktop\Travail\ENSAE\Statapp\data_frame_estimation_model_\df_2011.dta')


