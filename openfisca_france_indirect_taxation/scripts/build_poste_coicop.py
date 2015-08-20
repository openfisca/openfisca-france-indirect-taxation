# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 16:22:47 2015

@author: thomas.douenne
"""

from openfisca_france_indirect_taxation.build_survey_data.step_04_homogeneisation_categories_fiscales import (
    get_parametres_fiscalite_data_frame)

selected_parametres_fiscalite_data_frame = get_parametres_fiscalite_data_frame()

selected_parametres_fiscalite_data_frame = \
    selected_parametres_fiscalite_data_frame[['posteCOICOP', 'annee', 'description', 'categoriefiscale']]
# print selected_parametres_fiscalite_data_frame
selected_parametres_fiscalite_data_frame.set_index('posteCOICOP', inplace = True)
ensemble_postes_coicop = selected_parametres_fiscalite_data_frame.reset_index()

script_poste_coicop = open('poste_coicop_generator.py', 'w')

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

from openfisca_france_indirect_taxation.model.base import *
'''

print >>script_poste_coicop, presentation_and_imports

postes_coicop_par_annee = ensemble_postes_coicop[ensemble_postes_coicop['annee'] == 2000]
z = [str(element) for element in postes_coicop_par_annee['posteCOICOP'].values]
for each_poste in z:
    label = postes_coicop_par_annee['description'][postes_coicop_par_annee['posteCOICOP'] == int(each_poste)].values
    def_poste_coicop = '''
@reference_formula
class poste_coicop_{0}(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"{1}"

    def function(self, simulation, period):
        poste_coicop_{0} = simulation.calculate({0}, period)
        return period, poste_coicop_{0}
'''.format(each_poste, label)
    print >>script_poste_coicop, def_poste_coicop

script_poste_coicop.close()
