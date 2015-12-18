#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Thu Aug 20 16:22:47 2015

@author: thomas.douenne
"""

import pkg_resources
import os

from openfisca_france_indirect_taxation.build_survey_data.step_04_homogeneisation_categories_fiscales import (
    get_parametres_fiscalite_data_frame)

selected_parametres_fiscalite_data_frame = get_parametres_fiscalite_data_frame()

selected_parametres_fiscalite_data_frame = \
    selected_parametres_fiscalite_data_frame[['posteCOICOP', 'annee', 'description', 'categoriefiscale']]
# print selected_parametres_fiscalite_data_frame
selected_parametres_fiscalite_data_frame.set_index('posteCOICOP', inplace = True)
ensemble_postes_coicop = selected_parametres_fiscalite_data_frame.reset_index()

consommation_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )

script_poste_coicop = open(
    os.path.join(consommation_directory, 'openfisca_france_indirect_taxation', 'model',
    'consommation', 'poste_coicop_generator.py'), 'w'
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

from openfisca_france_indirect_taxation.model.base import *
'''

print >>script_poste_coicop, presentation_and_imports

postes_coicop = ensemble_postes_coicop.drop_duplicates('posteCOICOP', take_last = True)
z = [str(element) for element in postes_coicop['posteCOICOP'].values]
for each_poste in z:
    liste_annees = ensemble_postes_coicop['annee'][ensemble_postes_coicop['posteCOICOP'] == int(each_poste)]
    assert liste_annees.shape == (21L,), "Some goods do not exist during certain years"
    label = postes_coicop['description'][postes_coicop['posteCOICOP'] == int(each_poste)].values
    label = label.squeeze().tolist()
    label = label.encode('utf8')
    label = 'u' + '"' + label + '"'

    def_poste_coicop = '''
class poste_coicop_{0}(Variable):
    column = FloatCol()
    entity_class = Menages
    label = {1}'''.format(each_poste, label)
    print >>script_poste_coicop, def_poste_coicop

script_poste_coicop.close()

# To do : change the name of the label, use squeeze and tot list and try to avoid unicode error.
