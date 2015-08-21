# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 16:20:13 2015

@author: thomas.douenne
"""

import pkg_resources
import os

from openfisca_france_indirect_taxation.build_survey_data.step_04_homogeneisation_categories_fiscales import (
    get_parametres_fiscalite_data_frame)

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
    'consommation', 'categorie_fiscale_generator.py'), 'w'
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
    definition_function = '''
'categorie_fiscale: {0}'


@reference_formula
class categorie_fiscale_{0}(DatedFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale {0}"'''.format(categorie_fiscale)

    print >>script_categorie_fiscale, definition_function

    for year in range(1994, 2015):
        postes_coicop_par_annee = ensemble_postes_coicop[ensemble_postes_coicop['annee'] == year]
        z = [
            str(element[0]) for element in
            postes_coicop_par_annee.loc[postes_coicop_par_annee.categoriefiscale ==
            categorie_fiscale, ['posteCOICOP']].values
            ]
        variables = ', '.join(z)
        not_empty = len(z) != 0
        function_itself = '''
    @dated_function(start = date({3}, 1, 1), stop = date({3}, 12, 31))
    def function_{3}(self, simulation, period):
        categorie_fiscale_{0} = 0
        for each_variable in {1}:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_{0} = simulation.calculate(element, period)
            categorie_fiscale_{0} += bien_pour_categorie_fiscale_{0}
        return period, categorie_fiscale_{0}'''.format(categorie_fiscale, z, variables, year)

        if not_empty is True:
            print >>script_categorie_fiscale, function_itself

script_categorie_fiscale.close()
