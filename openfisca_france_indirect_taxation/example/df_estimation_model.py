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


from __future__ import division


import logging


from pandas import DataFrame

import openfisca_france_indirect_taxation
from openfisca_survey_manager.survey_collections import SurveyCollection

from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_indirect_taxation.surveys import SurveyScenario


def get_input_data_frame(year):
    openfisca_survey_collection = SurveyCollection.load(
        collection = "openfisca_indirect_taxation", config_files_directory = config_files_directory)
    openfisca_survey = openfisca_survey_collection.get_survey("openfisca_indirect_taxation_data_{}".format(year))
    input_data_frame = openfisca_survey.get_values(table = "input")
    input_data_frame.reset_index(inplace = True)
    return input_data_frame


def simulate_df(var_to_be_simulated, year = 2000):
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
        'typmen'
        ]
    # Merge des deux listes
    var_to_be_simulated += list_coicop12

    # Constition d'une base de données agrégée par décile (= collapse en stata)
    df = simulate_df(var_to_be_simulated = var_to_be_simulated)

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
    df['ident_men'] = df['ident_men'].astype('int')
    df.set_index('ident_men', inplace = True)

    # on crée une data frame pour calculer les parts budgétaires
    #depenses = temporary_store["depenses_{}".format(year)]
    # incorporation de la variable depenses_tot
    df_part_budg = depenses
    df_dep_tot = df
    var_list_alpha = ['depenses_tot']
    df_dep_tot = df_dep_tot[var_list_alpha]
    df_part_budg = df_part_budg.merge(df_dep_tot, left_index = True, right_index = True)


    # calcul les parts budgétaires:
    var_list = [column for column in df_part_budg.columns if column.startswith('0') or column.startswith('1') or column.startswith('dep')]
    df_part_budg = df_part_budg[var_list]
    var_list_1 = [column for column in df_part_budg.columns if column.startswith('0') or column.startswith('1')]
    df_part_budg['depenses_tot'] = df_part_budg['depenses_tot'].astype('float')

    for var in var_list_1:
        df_part_budg[var] = df_part_budg[var].astype('float')

    for var in var_list_1:
        try:
            df_part_budg[var] = df_part_budg[var]/df_part_budg['depenses_tot']
        except:
            df_part_budg[var]

    #on enlève les variables commençant par 9 car elles correspondent à des impôts etc.
    var_to_keep = [column for column in df_part_budg.columns if column.startswith('0') or column.startswith('1')]
    df_part_budg = df_part_budg[var_to_keep]

    #on renomme les variables car ce sont maintenant des parts budgétaires
    var_list_bis = [column for column in df_part_budg.columns if column.startswith('0') or column.startswith('1')]
    for var in var_list_bis:
        df_part_budg['pb_{}'.format(var)] = df_part_budg[var]

    for var in var_list_bis:
        del df_part_budg[var]

    df = df.merge(df_part_budg, left_index = True, right_index = True)


    df_1995 = df
    df_1995.to_stata('C:\Users\hadrien\Desktop\Travail\ENSAE\Statapp\data_frame_estimation_model\df_1995.dta')



