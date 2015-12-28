# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division


import os


import logging
import pandas
import pkg_resources


log = logging.getLogger(__name__)


def get_transfert_data_frames(year = None):
    assert year is not None
    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    matrice_passage_file_path = os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'Matrice passage {}-COICOP.xls'.format(year),
        )
    matrice_passage_data_frame = pandas.read_excel(matrice_passage_file_path)
    selected_parametres_fiscalite_data_frame = get_parametres_fiscalite_data_frame(year = year)
    return matrice_passage_data_frame, selected_parametres_fiscalite_data_frame


def get_parametres_fiscalite_data_frame(year = None):
    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    parametres_fiscalite_file_path = os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'Parametres fiscalite indirecte.xls',
        )
    parametres_fiscalite_data_frame = pandas.read_excel(parametres_fiscalite_file_path, sheetname = "categoriefiscale")
    # print parametres_fiscalite_data_frame
    if year:
        selected_parametres_fiscalite_data_frame = \
            parametres_fiscalite_data_frame[parametres_fiscalite_data_frame.annee == year].copy()
        return selected_parametres_fiscalite_data_frame
    else:
        return parametres_fiscalite_data_frame