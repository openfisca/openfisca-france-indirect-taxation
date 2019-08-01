# -*- coding: utf-8 -*-


from openfisca_core.reforms import Reform

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


def modify_parameters(parameters):

    node = ParameterNode(
        'reforme_tva_2019',
        data = {
            "description": "reforme_tva_2019",
            "nouveau_taux_tva_a_2019": {
                "description": "Augmentation de la TVA prévue par la LF 2019",
                "unit": '/1',
                "values": {'2013-01-01': 0.2}
                },
            "nouveau_taux_tva_b_2019": {
                "description": "Augmentation de la TVA prévue par la LF 2019",
                "unit": '/1',
                "values": {'2013-01-01': 0.2}
                },
            }
        )
    parameters.add_child('reforme_tva_2019', node)
    return parameters


class reforme_tva_2019(Reform):
    key = 'reforme_tva_2019',
    name = "Réforme de la TVA prévue par la loi de finance 2019",

    class poste_11_1_1_1_1_reforme_tva_2019(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en restaurant augmentation de la TVA"

        def formula(menage, period, parameters):
            poste_11_1_1_1_1 = menage('poste_11_1_1_1_1', period)
            ancien_taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            nouveau_taux_tva = parameters(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0

            poste_11_1_1_1_1_reforme_tva_2019 = (
                poste_11_1_1_1_1
                * (1
+ (1 + elasticite_prix)
                    * (incidence_consommateur
                    * (nouveau_taux_tva - ancien_taux_intermediaire)) / (1 + incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_1_1_1_1_reforme_tva_2019

    class poste_11_1_1_1_2_reforme_tva_2019(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en café/bars augmentation de la TVA"

        def formula(menage, period, parameters):
            poste_11_1_1_1_2 = menage('poste_11_1_1_1_2', period)
            ancien_taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            nouveau_taux_tva = parameters(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0

            poste_11_1_1_1_2_reforme_tva_2019 = (
                poste_11_1_1_1_2
                * (1
+ (1 + elasticite_prix)
                    * (incidence_consommateur
                    * (nouveau_taux_tva - ancien_taux_intermediaire)) / (1 + incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_1_1_1_2_reforme_tva_2019

    class poste_11_1_2_1_1_reforme_tva_2019(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en cantine augmentation de la TVA"

        def formula(menage, period, parameters):
            poste_11_1_2_1_1 = menage('poste_11_1_2_1_1', period)
            ancien_taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            nouveau_taux_tva = parameters(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0

            poste_11_1_2_1_1_reforme_tva_2019 = (
                poste_11_1_2_1_1
                * (1
+ (1 + elasticite_prix)
                    * (incidence_consommateur
                    * (nouveau_taux_tva - ancien_taux_intermediaire)) / (1 + incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_1_2_1_1_reforme_tva_2019

    class poste_11_1_3_1_reforme_tva_2019(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Autres dépenses en restauration, augmentation de la TVA"

        def formula(menage, period, parameters):
            poste_11_1_3_1 = menage('poste_11_1_3_1', period)
            ancien_taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            nouveau_taux_tva = parameters(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0

            poste_11_1_3_1_reforme_tva_2019 = (
                poste_11_1_3_1
                * (1
+ (1 + elasticite_prix)
                    * (incidence_consommateur
                    * (nouveau_taux_tva - ancien_taux_intermediaire)) / (1 + incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_1_3_1_reforme_tva_2019

    class poste_11_1_3_2_reforme_tva_2019(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Autres dépenses en restauration (cadeaux à autres ménages), augmentation de la TVA"

        def formula(menage, period, parameters):
            poste_11_1_3_2 = menage('poste_11_1_3_2', period)
            ancien_taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            nouveau_taux_tva = parameters(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0

            poste_11_1_3_2_reforme_tva_2019 = (
                poste_11_1_3_2
                * (1
+ (1 + elasticite_prix)
                    * (incidence_consommateur
                    * (nouveau_taux_tva - ancien_taux_intermediaire)) / (1 + incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_1_3_2_reforme_tva_2019

    class poste_11_2_1_1_1_reforme_tva_2019(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en hébergements augmentation de la TVA"

        def formula(menage, period, parameters):
            poste_11_2_1_1_1 = menage('poste_11_2_1_1_1', period)
            ancien_taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            nouveau_taux_tva = parameters(period.start).reforme_tva_2019.nouveau_taux_tva_a_2019
            incidence_consommateur = 0.5
            elasticite_prix = -0.0

            poste_11_2_1_1_1_reforme_tva_2019 = (
                poste_11_2_1_1_1
                * (1
+ (1 + elasticite_prix)
                    * (incidence_consommateur
                    * (nouveau_taux_tva - ancien_taux_intermediaire)) / (1 + incidence_consommateur * ancien_taux_intermediaire))
                )

            return poste_11_2_1_1_1_reforme_tva_2019

    def apply(self):
        self.update_variable(self.poste_11_1_1_1_1_reforme_tva_2019)
        self.update_variable(self.poste_11_1_1_1_2_reforme_tva_2019)
        self.update_variable(self.poste_11_1_2_1_1_reforme_tva_2019)
        self.update_variable(self.poste_11_1_3_1_reforme_tva_2019)
        self.update_variable(self.poste_11_1_3_2_reforme_tva_2019)
        self.update_variable(self.poste_11_2_1_1_1_reforme_tva_2019)
        self.modify_parameters(modifier_function = modify_parameters)
