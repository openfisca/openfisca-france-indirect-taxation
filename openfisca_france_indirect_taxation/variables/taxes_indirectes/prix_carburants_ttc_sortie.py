from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR


class prix_gazole_b7_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gazole B7 TTC par litre à la pompe'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_gazole_b7_ht = menage('prix_gazole_b7_ht', period)
        accise_gazole_b7_total = menage('accise_gazole_b7', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal

        prix_gazole_b7_hors_tva = prix_gazole_b7_ht + (accise_gazole_b7_total / 100)
        prix_gazole_b7_ttc = prix_gazole_b7_hors_tva * (1 + taux_plein_tva)
        return prix_gazole_b7_ttc


class prix_gazole_b7_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix du gazole B7 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_gazole_b7_ttc_sortie', period)

    def formula_2022(menage, period, parameters):
        prix_gazole_b7_ttc = menage('prix_gazole_b7_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b7_hors_remise_ttc = prix_gazole_b7_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_gazole_b7_hors_remise_ttc

    def formula_2023(menage, period):
        return menage('prix_gazole_b7_ttc_sortie', period)


class prix_gazole_b10_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gazole B10 TTC par litre à la pompe'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period, parameters):
        prix_gazole_b10_ht = menage('prix_gazole_b10_ht', period)
        accise_gazole_b10_hectolitre = menage('accise_gazole_b10', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b10_hors_tva = prix_gazole_b10_ht + (accise_gazole_b10_hectolitre / 100)
        prix_gazole_b10_ttc_sortie = prix_gazole_b10_hors_tva * (1 + taux_plein_tva)
        return prix_gazole_b10_ttc_sortie


class prix_gazole_b10_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix du gazole B10 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_gazole_b10_ttc_sortie', period)

    def formula_2022(menage, period, parameters):
        prix_gazole_b10_ttc = menage('prix_gazole_b10_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b10_hors_remise_ttc = prix_gazole_b10_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_gazole_b10_hors_remise_ttc

    def formula_2023(menage, period):
        return menage('prix_gazole_b10_ttc_sortie', period)


class prix_essence_sp95_e10_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 E10 TTC par litre à la pompe"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period, parameters):
        prix_essence_sp95_e10_ht = menage('prix_essence_sp95_e10_ht', period)
        accise_sp_e10_ticpe = menage('accise_essence_sp95_e10', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_e10_hors_tva = prix_essence_sp95_e10_ht + (accise_sp_e10_ticpe / 100)
        prix_essence_sp95_e10_ttc_sortie = prix_essence_sp95_e10_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp95_e10_ttc_sortie


class prix_essence_sp95_e10_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 E10 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp95_e10_ttc_sortie', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp95_e10_ttc = menage('prix_essence_sp95_e10_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_e10_ttc = prix_essence_sp95_e10_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_sp95_e10_ttc

    def formula_2023(menage, period):
        return menage('prix_essence_sp95_e10_ttc_sortie', period)


class prix_essence_sp95_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 TTC par litre à la pompe"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_sp95_ht = menage('prix_essence_sp95_ht', period)
        accise_sp95_ticpe = menage('accise_essence_sp95', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_hors_tva = prix_essence_sp95_ht + (accise_sp95_ticpe / 100)
        prix_essence_sp95_ttc_sortie = prix_essence_sp95_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp95_ttc_sortie


class prix_essence_sp95_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp95_ttc_sortie', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp95_ttc = menage('prix_essence_sp95_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_ttc = prix_essence_sp95_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_sp95_ttc

    def formula_2023(menage, period):
        return menage('prix_essence_sp95_ttc_sortie', period)


class prix_essence_sp98_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 TTC par litre à la pompe"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_sp98_ht = menage('prix_essence_sp98_ht', period)
        accise_sp98_ticpe = menage('accise_essence_sp98', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp98_hors_tva = prix_essence_sp98_ht + (accise_sp98_ticpe / 100)
        prix_essence_sp98_ttc_sortie = prix_essence_sp98_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp98_ttc_sortie


class prix_essence_sp98_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp98_ttc_sortie', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp98_ttc = menage('prix_essence_sp98_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp98_ttc = prix_essence_sp98_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_sp98_ttc

    def formula_2023(menage, period):
        return menage('prix_essence_sp98_ttc_sortie', period)


class prix_essence_super_plombe_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence super plombé TTC par litre à la pompe"
    definition_period = YEAR
    default_value = 0
    end = "2017-01-01"

    def formula(menage, period, parameters):
        prix_essence_super_plombe_ht = menage('prix_essence_super_plombe_ht', period)
        accise_super_plombe_ticpe = ('accise_essence_super_plombe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_super_plombe_hors_tva = prix_essence_super_plombe_ht + (accise_super_plombe_ticpe / 100)
        prix_essence_super_plombe_ttc_sortie = prix_essence_super_plombe_hors_tva * (1 + taux_plein_tva)
        return prix_essence_super_plombe_ttc_sortie


class prix_essence_e85_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence E85 TTC par litre à la pompe"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period, parameters):
        prix_essence_e85_ht = menage('prix_essence_e85_ht', period)
        accise_e85_hectolitre = menage('accise_essence_e85', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal

        prix_essence_e85_hors_tva = prix_essence_e85_ht + (accise_e85_hectolitre / 100)
        prix_essence_e85_ttc_sortie = prix_essence_e85_hors_tva * (1 + taux_plein_tva)
        return prix_essence_e85_ttc_sortie


class prix_essence_e85_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence E85 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_e85_ttc_sortie', period)

    def formula_2022(menage, period, parameters):
        prix_essence_e85_ttc = menage('prix_essence_e85_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_e85_hors_remise_ttc = prix_essence_e85_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_e85_hors_remise_ttc

    def formula_2023(menage, period):
        return menage('prix_essence_e85_ttc_sortie', period)


class prix_gpl_carburant_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gaz de pétrole liquéfié - carburant  par litre à la pompe'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_gpl_carburant_ht = menage('prix_gpl_carburant_ht', period)
        accise_gpl_carburant_hectolitre = menage('accise_gpl_carburant', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gpl_carburant_hors_tva = prix_gpl_carburant_ht + (accise_gpl_carburant_hectolitre / 100)
        prix_gpl_carburant_ttc_sortie = prix_gpl_carburant_hors_tva * (1 + taux_plein_tva)
        return prix_gpl_carburant_ttc_sortie


class prix_gpl_carburant_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix du GPL TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_gpl_carburant_ttc_sortie', period)

    def formula_2022(menage, period, parameters):
        prix_gpl_carburant_ttc = menage('prix_gpl_carburant_ttc_sortie', period)
        aide_exceptionnelle_gpl_carburant_100kg = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gpl_carburant_100kg
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gpl_carburant_hors_remise_ttc = prix_gpl_carburant_ttc + (aide_exceptionnelle_gpl_carburant_100kg / 100) * (1 + taux_plein_tva)
        return prix_gpl_carburant_hors_remise_ttc

    def formula_2023(menage, period):
        return menage('prix_gpl_carburant_ttc_sortie', period)
