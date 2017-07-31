# -*- coding: utf-8 -*-
"""
Created on Mon Jul 03 13:23:15 2017

@author: t.douenne
"""


from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_2_homogenize_variables import \
    homogenize_variables_definition_bdf_enl


data = homogenize_variables_definition_bdf_enl()    
data_enl = data[0]
data_bdf = data[1]


for i in range(0,9):
    data_tuu = data_bdf.query('tuu == {}'.format(i))
    print i, len(data_tuu)
    

for i in range(0,9):
    print i, len(data_bdf.query('htl == {}'.format(i)))
    
    
    
    
    
    
energie_logement = ['poste_coicop_451', 'poste_coicop_4511', 'poste_coicop_452', 'poste_coicop_4522',
'poste_coicop_453', 'poste_coicop_454', 'poste_coicop_455', 'poste_coicop_4552']

for energie in energie_logement:
    data['depenses_energies'] = data['depenses_energies'].copy() + data[energie].copy()

