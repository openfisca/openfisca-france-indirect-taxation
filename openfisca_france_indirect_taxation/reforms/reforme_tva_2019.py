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
            "nouveau_taux_tva_a_2019": {
                "@type": "Parameter",
                "description": u"Augmentation de la TVA prévue par la LF 2019",
                "format": 'float',
                "values": [{'start': u'2013-01-01', 'value': 0.2}]
                },
            "nouveau_taux_tva_b_2019": {
                "@type": "Parameter",
                "description": u"Augmentation de la TVA prévue par la LF 2019",
                "format": 'float',
                "values": [{'start': u'2013-01-01', 'value': 0.2}]
                },
            },
        }

    reference_legislation_json_copy['children']['reforme_tva_2019'] = reform_legislation_subtree
    return reference_legislation_json_copy



class reforme_tva_2019(Reform):
    key = 'reforme_tva_2019',
    name = u"Réforme de la TVA prévue par la loi de finance 2019",


    class poste_11_1_1_1_1_reforme_tva_2019(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses en restaurant augmentation de la TVA"
    
        def formula(self, simulation, period):
            poste_11_1_1_1_1 = simulation.calculate('poste_11_1_1_1_1', period)
            ancien_taux_intermediaire = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
            nouveau_taux_tva = simulation.legislation_at(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0
            
            poste_11_1_1_1_1_reforme_tva_2019 = (
                poste_11_1_1_1_1
                * (1 +
                    (1+ elasticite_prix)
                    *(incidence_consommateur
                    *(nouveau_taux_tva - ancien_taux_intermediaire))/(1+incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_1_1_1_1_reforme_tva_2019
    

    class poste_11_1_1_1_2_reforme_tva_2019(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses en café/bars augmentation de la TVA"
    
        def formula(self, simulation, period):
            poste_11_1_1_1_2 = simulation.calculate('poste_11_1_1_1_2', period)
            ancien_taux_intermediaire = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
            nouveau_taux_tva = simulation.legislation_at(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0
            
            poste_11_1_1_1_2_reforme_tva_2019 = (
                poste_11_1_1_1_2
                * (1 +
                    (1+ elasticite_prix)
                    *(incidence_consommateur
                    *(nouveau_taux_tva - ancien_taux_intermediaire))/(1+incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_1_1_1_2_reforme_tva_2019
    

    class poste_11_1_2_1_1_reforme_tva_2019(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses en cantine augmentation de la TVA"
    
        def formula(self, simulation, period):
            poste_11_1_2_1_1 = simulation.calculate('poste_11_1_2_1_1', period)
            ancien_taux_intermediaire = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
            nouveau_taux_tva = simulation.legislation_at(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0
            
            poste_11_1_2_1_1_reforme_tva_2019 = (
                poste_11_1_2_1_1
                * (1 +
                    (1+ elasticite_prix)
                    *(incidence_consommateur
                    *(nouveau_taux_tva - ancien_taux_intermediaire))/(1+incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_1_2_1_1_reforme_tva_2019
    

    class poste_11_1_3_1_reforme_tva_2019(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Autres dépenses en restauration, augmentation de la TVA"
    
        def formula(self, simulation, period):
            poste_11_1_3_1 = simulation.calculate('poste_11_1_3_1', period)
            ancien_taux_intermediaire = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
            nouveau_taux_tva = simulation.legislation_at(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0
            
            poste_11_1_3_1_reforme_tva_2019 = (
                poste_11_1_3_1
                * (1 +
                    (1+ elasticite_prix)
                    *(incidence_consommateur
                    *(nouveau_taux_tva - ancien_taux_intermediaire))/(1+incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_1_3_1_reforme_tva_2019
    

    class poste_11_1_3_2_reforme_tva_2019(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Autres dépenses en restauration (cadeaux à autres ménages), augmentation de la TVA"
    
        def formula(self, simulation, period):
            poste_11_1_3_2 = simulation.calculate('poste_11_1_3_2', period)
            ancien_taux_intermediaire = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
            nouveau_taux_tva = simulation.legislation_at(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0
            
            poste_11_1_3_2_reforme_tva_2019 = (
                poste_11_1_3_2
                * (1 +
                    (1+ elasticite_prix)
                    *(incidence_consommateur
                    *(nouveau_taux_tva - ancien_taux_intermediaire))/(1+incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_1_3_2_reforme_tva_2019
    

    class poste_11_2_1_1_1_reforme_tva_2019(YearlyVariable):
        column = FloatCol
        entity = Menage
        label = u"Dépenses en hébergements augmentation de la TVA"
    
        def formula(self, simulation, period):
            poste_11_2_1_1_1 = simulation.calculate('poste_11_2_1_1_1', period)
            ancien_taux_intermediaire = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
            nouveau_taux_tva = simulation.legislation_at(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0
            
            poste_11_2_1_1_1_reforme_tva_2019 = (
                poste_11_2_1_1_1
                * (1 +
                    (1+ elasticite_prix)
                    *(incidence_consommateur
                    *(nouveau_taux_tva - ancien_taux_intermediaire))/(1+incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_2_1_1_1_reforme_tva_2019
    

    def apply(self):
        self.update_variable(self.poste_11_1_1_1_1_reforme_tva_2019)
        self.update_variable(self.poste_11_1_1_1_2_reforme_tva_2019)
        self.update_variable(self.poste_11_1_2_1_1_reforme_tva_2019)
        self.update_variable(self.poste_11_1_3_1_reforme_tva_2019)
        self.update_variable(self.poste_11_1_3_2_reforme_tva_2019)
        self.update_variable(self.poste_11_2_1_1_1_reforme_tva_2019)
        self.modify_legislation_json(modifier_function = modify_legislation_json)
