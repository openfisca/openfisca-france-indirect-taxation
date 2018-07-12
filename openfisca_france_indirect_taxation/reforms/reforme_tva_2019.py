# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core.reforms import Reform, update_legislation

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore
#from ..model.taxes_indirectes import tva, ticpe
#from ..model.consommation import emissions_co2, quantites_energie


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "reforme_tva_2019",
        "children": {
            "variation_1_tva_2019": {
                "@type": "Parameter",
                "description": u"Augmentation de la TVA prévue par la LF 2019",
                "format": 'float',
                "values": [{'start': u'2013-01-01', 'value': 0.01}]
                },
            "variation_2_tva_2019": {
                "@type": "Parameter",
                "description": u"Augmentation de la TVA prévue par la LF 2019",
                "format": 'float',
                "values": [{'start': u'2013-01-01', 'value': 0.02}]
                },
            },
        }

    reference_legislation_json_copy['children']['reforme_tva_2019'] = reform_legislation_subtree
    return reference_legislation_json_copy



class reforme_tva_2019(Reform):
    key = 'reforme_tva_2019',
    name = u"Réforme de la TVA prévue par la loi de finance 2019",


    class poste_agrege_11_reforme_tva_2019(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses dans le poste 11 après augmentation de la TVA"
    
        def formula(self, simulation, period):
            poste_agrege_11 = simulation.calculate('poste_agrege_11', period)
            reforme_tva = simulation.legislation_at(period.start).reforme_tva_2019.variation_1_tva_2019
            incidence_consommateur = 0.5
            #elasticite_prix_bien = -0.2
            
            poste_agrege_11_reforme_tva_2019 = (
                poste_agrege_11 * (1 + (reforme_tva * incidence_consommateur))
                )

            return poste_agrege_11_reforme_tva_2019

    

    def apply(self):
        self.update_variable(self.poste_agrege_11_reforme_tva_2019)
        self.modify_legislation_json(modifier_function = modify_legislation_json)
