# -*- coding: utf-8 -*-

from __future__ import division

import os

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore
from ..model.taxes_indirectes import tva, ticpe
from ..model.consommation import emissions_co2, quantites_energie


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')


def modify_parameters(parameters):
    file_path = os.path.join(dir_path, 'rattrapage-diesel-parameters.yaml')
    reform_parameters_subtree = load_parameter_file(name='rattrapage-diesel-parameters', file_path=file_path)
    parameters.add_child('rattrapage-diesel-parameters', reform_parameters_subtree)
    return parameters


class rattrapage_diesel(Reform):
    #key = 'rattrapage_diesel',
    name = u"Réforme de l'imposition indirecte des carburants",


    class depenses_diesel_ajustees_rattrapage_diesel(Variable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses en diesel après réaction à la réforme - taxes carburants"
    
        def function(self, simulation, period):
            depenses_diesel = simulation.calculate('depenses_diesel', period)
            diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
            reforme_diesel = simulation.legislation_at(period.start).rattrapage_diesel.diesel
            carburants_elasticite_prix = simulation.calculate('elas_price_1_1')
            depenses_diesel_ajustees_rattrapage_diesel = \
                depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

            return period, depenses_diesel_ajustees_rattrapage_diesel
    
    def apply(self):
        self.update_variable(self.depenses_diesel_ajustees_rattrapage_diesel)
        self.modify_parameters(modifier_function = modify_parameters)
