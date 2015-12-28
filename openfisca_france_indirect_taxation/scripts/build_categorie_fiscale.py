#! /usr/bin/env python
# -*- coding: utf-8 -*-


import pkg_resources
import os

from openfisca_france_indirect_taxation.utils import get_parametres_fiscalite_data_frame

selected_parametres_fiscalite_data_frame = get_parametres_fiscalite_data_frame()

selected_parametres_fiscalite_data_frame = \
    selected_parametres_fiscalite_data_frame[['posteCOICOP', 'annee', 'categoriefiscale']]
# print selected_parametres_fiscalite_data_frame
selected_parametres_fiscalite_data_frame.set_index('posteCOICOP', inplace = True)
ensemble_postes_coicop = selected_parametres_fiscalite_data_frame.reset_index()

consommation_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )

script_categorie_fiscale = open(
    os.path.join(consommation_directory, 'openfisca_france_indirect_taxation', 'model',
    'consommation', 'categorie_fiscale_generator2.py'), 'w'
    )

presentation_and_imports = '''
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from datetime import date

from openfisca_france_indirect_taxation.model.base import *
'''
print >>script_categorie_fiscale, presentation_and_imports

existing_categ = selected_parametres_fiscalite_data_frame['categoriefiscale'].drop_duplicates()
existing_categ = sorted(existing_categ)


for categorie_fiscale in existing_categ:
    year_start = 1994
    year_final_stop = 2014
    variable_header = '''
class categorie_fiscale_{0}(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale {0}"'''.format(categorie_fiscale)

    print >>script_categorie_fiscale, variable_header

    for year in range(year_start, year_final_stop + 1):
        postes_coicop = sorted(
            ensemble_postes_coicop.query(
                'annee == @year and categoriefiscale == @categorie_fiscale'
                )['posteCOICOP'].astype(str))
        variables = ', '.join(postes_coicop)

        if year == year_start:
            previous_variables = variables
            previous_postes_coicop = postes_coicop
            continue

        if previous_postes_coicop == postes_coicop and year != year_final_stop:
            print previous_postes_coicop
            print postes_coicop
            print previous_postes_coicop == postes_coicop
            continue
        else:
            year_stop = year - 1 if year != year_final_stop else year_final_stop

            dated_function = '''
    @dated_function(start = date({year_start}, 1, 1), stop = date({year_stop}, 12, 31))
    def function_{year_start}_{year_stop}(self, simulation, period):
        categorie_fiscale_{categorie_fiscale} = 0
        for poste in {postes_coicop}:
            categorie_fiscale_{categorie_fiscale} += simulation.calculate('poste_coicop_' + poste, period)
        return period, categorie_fiscale_{categorie_fiscale}
'''.format(
                categorie_fiscale = categorie_fiscale,
                postes_coicop = previous_postes_coicop,
                year_start = year_start,
                year_stop = year_stop
                )
            year_start = year
            if len(previous_postes_coicop) != 0:
                print >>script_categorie_fiscale, dated_function

        previous_postes_coicop = postes_coicop

script_categorie_fiscale.close()
