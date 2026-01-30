from openfisca_core.reforms import Reform
from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


def reform_modify_parameters(baseline_parameters_copy):
    reform_parameters = baseline_parameters_copy

    node = ParameterNode(
        'augmentation_tva_2025',
        data = {
            "description": 'augmentation_tva_2025',
            "delta_taux": {
                "description": "Augmentation d'un point de TVA",
                "unit": '/1',
                "values": {'2024-01-01': 0.01}
                },
            }
        )
    reform_parameters.imposition_indirecte.tva.taux_de_tva.add_child('augmentation_tva_2025', node)
    return reform_parameters


class augmente_taux_plein(Reform):
    name = u'Augmentation du taux plein de TVA'

    class depenses_tva_taux_plein(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux plein"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_plein = menage('depenses_ht_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_plein * (1 + taux_plein + augmentation)

    class tva_taux_plein(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux plein"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_plein = menage('depenses_ht_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_plein * (taux_plein + augmentation)

    def apply(self):
        self.update_variable(self.depenses_tva_taux_plein)
        self.update_variable(self.tva_taux_plein)
        self.modify_parameters(modifier_function = reform_modify_parameters)


class augmente_taux_intermediaire(Reform):
    name = u'Augmentation du taux intermediaire de TVA'

    class depenses_tva_taux_intermediaire(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux intermediaire"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_intermediaire = menage('depenses_ht_tva_taux_intermediaire', period)
            taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_intermediaire * (1 + taux_intermediaire + augmentation)

    class tva_taux_intermediaire(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux intermediaire"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_intermediaire = menage('depenses_ht_tva_taux_intermediaire', period)
            taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_intermediaire * (taux_intermediaire + augmentation)

    def apply(self):
        self.update_variable(self.depenses_tva_taux_intermediaire)
        self.update_variable(self.tva_taux_intermediaire)
        self.modify_parameters(modifier_function = reform_modify_parameters)


class augmente_taux_reduit(Reform):
    name = u'Augmentation du taux reduit de TVA'

    class depenses_tva_taux_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_reduit = menage('depenses_ht_tva_taux_reduit', period)
            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_reduit * (1 + taux_reduit + augmentation)

    class tva_taux_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_reduit = menage('depenses_ht_tva_taux_reduit', period)
            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_reduit * (taux_reduit + augmentation)

    def apply(self):
        self.update_variable(self.depenses_tva_taux_reduit)
        self.update_variable(self.tva_taux_reduit)
        self.modify_parameters(modifier_function = reform_modify_parameters)


class augmente_taux_super_reduit(Reform):
    name = u'Augmentation du taux super_reduit de TVA'

    class depenses_tva_taux_super_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux super_reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_super_reduit = menage('depenses_ht_tva_taux_super_reduit', period)
            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_super_reduit * (1 + taux_super_reduit + augmentation)

    class tva_taux_super_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux super_reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_super_reduit = menage('depenses_ht_tva_taux_super_reduit', period)
            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_super_reduit * (taux_super_reduit + augmentation)

    def apply(self):
        self.update_variable(self.depenses_tva_taux_super_reduit)
        self.update_variable(self.tva_taux_super_reduit)
        self.modify_parameters(modifier_function = reform_modify_parameters)


class augmente_tous_les_taux(Reform):
    name = u'Augmentation de tous les taux de TVA (+1 p.p.)'

    class depenses_tva_taux_plein(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux plein"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_plein = menage('depenses_ht_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_plein * (1 + taux_plein + augmentation)

    class tva_taux_plein(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux plein"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_plein = menage('depenses_ht_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_plein * (taux_plein + augmentation)

    class depenses_tva_taux_intermediaire(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux intermediaire"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_intermediaire = menage('depenses_ht_tva_taux_intermediaire', period)
            taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_intermediaire * (1 + taux_intermediaire + augmentation)

    class tva_taux_intermediaire(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux intermediaire"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_intermediaire = menage('depenses_ht_tva_taux_intermediaire', period)
            taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_intermediaire * (taux_intermediaire + augmentation)

    class depenses_tva_taux_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_reduit = menage('depenses_ht_tva_taux_reduit', period)
            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_reduit * (1 + taux_reduit + augmentation)

    class tva_taux_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_reduit = menage('depenses_ht_tva_taux_reduit', period)
            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_reduit * (taux_reduit + augmentation)

    class depenses_tva_taux_super_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux super_reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_super_reduit = menage('depenses_ht_tva_taux_super_reduit', period)
            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_super_reduit * (1 + taux_super_reduit + augmentation)

    class tva_taux_super_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux super_reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_super_reduit = menage('depenses_ht_tva_taux_super_reduit', period)
            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_super_reduit * (taux_super_reduit + augmentation)

    def apply(self):
        self.update_variable(self.depenses_tva_taux_plein)
        self.update_variable(self.tva_taux_plein)
        self.update_variable(self.depenses_tva_taux_intermediaire)
        self.update_variable(self.tva_taux_intermediaire)
        self.update_variable(self.depenses_tva_taux_reduit)
        self.update_variable(self.tva_taux_reduit)
        self.update_variable(self.depenses_tva_taux_super_reduit)
        self.update_variable(self.tva_taux_super_reduit)
        self.modify_parameters(modifier_function = reform_modify_parameters)


class augmente_tous_les_taux_pass_through_0_8(Reform):
    name = u'Augmentation de tous les taux de TVA (+1 p.p.) avec un pass-through de 0.8'

    class depenses_ht_tva_taux_plein_reform(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses HT des biens acquittant la TVA acquitée à taux plein"

        def formula(menage, period, parameters):
            pass_through = 0.8
            depenses_ht_tva_taux_plein = menage('depenses_ht_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_plein * (1 + taux_plein + pass_through * augmentation) / (1 + taux_plein + augmentation)

    class depenses_tva_taux_plein(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux plein"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_plein_reform = menage('depenses_ht_tva_taux_plein_reform', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_plein_reform * (1 + taux_plein + augmentation)

    class tva_taux_plein(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux plein"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_plein_reform = menage('depenses_ht_tva_taux_plein_reform', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_plein_reform * (taux_plein + augmentation)

    class depenses_ht_tva_taux_intermediaire_reform(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses HT des biens acquittant la TVA acquitée à taux intermediaire"

        def formula(menage, period, parameters):
            pass_through = 0.8
            depenses_ht_tva_taux_intermediaire = menage('depenses_ht_tva_taux_intermediaire', period)
            taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_intermediaire * (1 + taux_intermediaire + pass_through * augmentation) / (1 + taux_intermediaire + augmentation)

    class depenses_tva_taux_intermediaire(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux intermediaire"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_intermediaire_reform = menage('depenses_ht_tva_taux_intermediaire_reform', period)
            taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_intermediaire_reform * (1 + taux_intermediaire + augmentation)

    class tva_taux_intermediaire(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux intermediaire"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_intermediaire_reform = menage('depenses_ht_tva_taux_intermediaire_reform', period)
            taux_intermediaire = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_intermediaire
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_intermediaire_reform * (taux_intermediaire + augmentation)

    class depenses_ht_tva_taux_reduit_reform(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses HT des biens acquittant la TVA acquitée à taux reduit"

        def formula(menage, period, parameters):
            pass_through = 0.8
            depenses_ht_tva_taux_reduit = menage('depenses_ht_tva_taux_reduit', period)
            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_reduit * (1 + taux_reduit + pass_through * augmentation) / (1 + taux_reduit + augmentation)

    class depenses_tva_taux_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_reduit_reform = menage('depenses_ht_tva_taux_reduit_reform', period)
            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_reduit_reform * (1 + taux_reduit + augmentation)

    class tva_taux_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_reduit_reform = menage('depenses_ht_tva_taux_reduit_reform', period)
            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_reduit_reform * (taux_reduit + augmentation)

    class depenses_ht_tva_taux_super_reduit_reform(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses HT des biens acquittant la TVA acquitée à taux super_reduit"

        def formula(menage, period, parameters):
            pass_through = 0.8
            depenses_ht_tva_taux_super_reduit = menage('depenses_ht_tva_taux_super_reduit', period)
            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_super_reduit * (1 + taux_super_reduit + pass_through * augmentation) / (1 + taux_super_reduit + augmentation)

    class depenses_tva_taux_super_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses TTC des biens acquittant la TVA acquitée à taux super_reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_super_reduit_reform = menage('depenses_ht_tva_taux_super_reduit_reform', period)
            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_super_reduit_reform * (1 + taux_super_reduit + augmentation)

    class tva_taux_super_reduit(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant de la TVA acquitée à taux super_reduit"

        def formula(menage, period, parameters):
            depenses_ht_tva_taux_super_reduit_reform = menage('depenses_ht_tva_taux_super_reduit_reform', period)
            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            augmentation = parameters(period.start).imposition_indirecte.tva.taux_de_tva.augmentation_tva_2025.delta_taux

            return depenses_ht_tva_taux_super_reduit_reform * (taux_super_reduit + augmentation)

    def apply(self):
        self.add_variable(self.depenses_ht_tva_taux_plein_reform)
        self.add_variable(self.depenses_ht_tva_taux_intermediaire_reform)
        self.add_variable(self.depenses_ht_tva_taux_reduit_reform)
        self.add_variable(self.depenses_ht_tva_taux_super_reduit_reform)
        self.update_variable(self.depenses_tva_taux_plein)
        self.update_variable(self.tva_taux_plein)
        self.update_variable(self.depenses_tva_taux_intermediaire)
        self.update_variable(self.tva_taux_intermediaire)
        self.update_variable(self.depenses_tva_taux_reduit)
        self.update_variable(self.tva_taux_reduit)
        self.update_variable(self.depenses_tva_taux_super_reduit)
        self.update_variable(self.tva_taux_super_reduit)
        self.modify_parameters(modifier_function = reform_modify_parameters)
