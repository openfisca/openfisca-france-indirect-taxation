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

from openfisca_france_data.temporary import TemporaryStore
from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame, simulate_df



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
        'niveau_vie_decile',
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
    df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
    if year == 2011:
        df.niveau_vie_decile[df.decuc == 10 ] = 10



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

    #♥df['niveau_vie_decile_bis']= weighted_quantiles('niveau_de_vie', 'labels', 'pondmen', return_quantiles = True)

    df_2011 = df
    df_2011.to_stata('C:\Users\hadrien\Desktop\Travail\ENSAE\Statapp\data_frame_estimation_model_\df_2011.dta')
