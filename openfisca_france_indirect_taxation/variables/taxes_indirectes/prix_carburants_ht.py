from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR


class prix_gazole_b7_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gazole B7 HT par litre avant remise'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_gazole_b7_hors_remise_ttc = menage('prix_gazole_b7_hors_remise_ttc', period)
        accise_gazole_b7_total = menage('accise_gazole_b7', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b7_hors_tva = prix_gazole_b7_hors_remise_ttc * (1 / (1 + taux_plein_tva))
        prix_gazole_b7_ht_avant_remise = prix_gazole_b7_hors_tva - (accise_gazole_b7_total / 100)
        return prix_gazole_b7_ht_avant_remise


class prix_gazole_b7_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix du gazole B7 HT par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0
    reference = "https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000046489832/2022-10-27/"

    def formula(menage, period):
        return menage('prix_gazole_b7_ht_avant_remise', period)

    def formula_2022(menage, period, parameters):
        prix_gazole_b7_ht_avant_remise = menage('prix_gazole_b7_ht_avant_remise', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_gazole_b7_ht = prix_gazole_b7_ht_avant_remise - (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_gazole_b7_ht

    def formula_2023(menage, period):
        return menage('prix_gazole_b7_ht_avant_remise', period)


class prix_gazole_b10_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gazole B10 HT par litre avant remise'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period, parameters):
        prix_gazole_b10_hors_remise_ttc = menage('prix_gazole_b10_hors_remise_ttc', period)
        accise_gazole_b10_hectolitre = menage('accise_gazole_b10', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b10_hors_tva = prix_gazole_b10_hors_remise_ttc * (1 / (1 + taux_plein_tva))
        prix_gazole_b10_ht_avant_remise = prix_gazole_b10_hors_tva - (accise_gazole_b10_hectolitre / 100)
        return prix_gazole_b10_ht_avant_remise


class prix_gazole_b10_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix du gazole B10 HT par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_gazole_b10_ht_avant_remise', period)

    def formula_2022(menage, period, parameters):
        prix_gazole_b10_ht_avant_remise = menage('prix_gazole_b10_ht_avant_remise', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_gazole_b10_ht = prix_gazole_b10_ht_avant_remise - (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_gazole_b10_ht

    def formula_2023(menage, period):
        return menage('prix_gazole_b10_ht_avant_remise', period)


class prix_essence_sp95_e10_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 E10 HT par litre avant remise"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period, parameters):
        prix_essence_sp95_e10_hors_remise_ttc = menage('prix_essence_sp95_e10_hors_remise_ttc', period)
        accise_sp_e10_ticpe = menage('accise_essence_sp95_e10', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_e10_hors_tva = prix_essence_sp95_e10_hors_remise_ttc * (1 / (1 + taux_plein_tva))
        prix_essence_sp95_e10_ht_avant_remise = prix_essence_sp95_e10_hors_tva - (accise_sp_e10_ticpe / 100)
        return prix_essence_sp95_e10_ht_avant_remise


class prix_essence_sp95_e10_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 E10 HT par litre "
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp95_e10_ht_avant_remise', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp95_e10_ht_avant_remise = menage('prix_essence_sp95_e10_ht_avant_remise', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_essence_sp95_e10_hors_remise_ttc = prix_essence_sp95_e10_ht_avant_remise - (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_essence_sp95_e10_hors_remise_ttc

    def formula_2023(menage, period):
        return menage('prix_essence_sp95_e10_ht_avant_remise', period)


class prix_essence_sp95_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 HT par litre avant remise"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_sp95_hors_remise_ttc = menage('prix_essence_sp95_hors_remise_ttc', period)
        accise_sp95_ticpe = menage('accise_essence_sp95', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_hors_tva = prix_essence_sp95_hors_remise_ttc * (1 / (1 + taux_plein_tva))
        prix_essence_sp95_ht_avant_remise = prix_essence_sp95_hors_tva - (accise_sp95_ticpe / 100)
        return prix_essence_sp95_ht_avant_remise


class prix_essence_sp95_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 TTC par litre"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp95_ht_avant_remise', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp95_ht_avant_remise = menage('prix_essence_sp95_ht_avant_remise', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_essence_sp95_hors_remise_ttc = prix_essence_sp95_ht_avant_remise - (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_essence_sp95_hors_remise_ttc

    def formula_2023(menage, period):
        return menage('prix_essence_sp95_ht_avant_remise', period)


class prix_essence_sp98_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 HT par litre avant remise"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_sp98_hors_remise_ttc = menage('prix_essence_sp98_hors_remise_ttc', period)
        accise_sp98_ticpe = menage('accise_essence_sp98', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp98_hors_tva = prix_essence_sp98_hors_remise_ttc * (1 / (1 + taux_plein_tva))
        prix_essence_sp98_ht_avant_remise = prix_essence_sp98_hors_tva - (accise_sp98_ticpe / 100)
        return prix_essence_sp98_ht_avant_remise


class prix_essence_sp98_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 HT par litre "
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp98_ht_avant_remise', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp98_ht_avant_remise = menage('prix_essence_sp98_ht_avant_remise', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_essence_sp98_hors_remise_ttc = prix_essence_sp98_ht_avant_remise - (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_essence_sp98_hors_remise_ttc

    def formula_2023(menage, period):
        return menage('prix_essence_sp98_ht_avant_remise', period)


class prix_essence_super_plombe_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence super plombé HT par litre"
    definition_period = YEAR
    default_value = 0
    end = "2017-01-01"

    def formula(menage, period, parameters):
        prix_essence_super_plombe_ttc = menage('prix_essence_super_plombe_ttc', period)
        accise_super_plombe_ticpe = ('accise_essence_super_plombe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_super_plombe_hors_tva = prix_essence_super_plombe_ttc * (1 / (1 + taux_plein_tva))
        prix_essence_super_plombe_ht_avant_remise = prix_essence_super_plombe_hors_tva - (accise_super_plombe_ticpe / 100)
        return prix_essence_super_plombe_ht_avant_remise


class prix_essence_e85_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence E85 HT par litre avant remise"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period, parameters):
        prix_essence_e85_hors_remise_ttc = menage('prix_essence_e85_hors_remise_ttc', period)
        accise_e85_hectolitre = menage('accise_essence_e85', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_e85_hors_tva = prix_essence_e85_hors_remise_ttc * (1 / (1 + taux_plein_tva))
        prix_essence_e85_ht_avant_remise = prix_essence_e85_hors_tva - (accise_e85_hectolitre / 100)
        return prix_essence_e85_ht_avant_remise


class prix_essence_e85_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence E85 HT par litre"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_e85_ht_avant_remise', period)

    def formula_2022(menage, period, parameters):
        prix_essence_e85_ht_avant_remise = menage('prix_essence_e85_ht_avant_remise', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_essence_e85_ht = prix_essence_e85_ht_avant_remise - (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_essence_e85_ht

    def formula_2023(menage, period):
        return menage('prix_essence_e85_ht_avant_remise', period)


class prix_gpl_carburant_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gaz de pétrole liquéfié - carburant HT par litre avant remise'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_gpl_carburant_hors_remise_ttc = menage('prix_gpl_carburant_hors_remise_ttc', period)
        accise_gpl_carburant_hectolitre = menage('accise_gpl_carburant', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gpl_carburant_hors_tva = prix_gpl_carburant_hors_remise_ttc * (1 / (1 + taux_plein_tva))
        prix_gpl_carburant_ht_avant_remise = prix_gpl_carburant_hors_tva - (accise_gpl_carburant_hectolitre / 100)
        return prix_gpl_carburant_ht_avant_remise


class prix_gpl_carburant_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix du gaz de pétrole liquéfié - carburant HT par litre"
    definition_period = YEAR
    default_value = 0
    reference = "https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000046489832/2022-10-27/"

    def formula(menage, period):
        return menage('prix_gpl_carburant_ht_avant_remise', period)

    def formula_2022(menage, period, parameters):
        prix_gpl_carburant_ht_avant_remise = menage('prix_gpl_carburant_ht_avant_remise', period)
        aide_exceptionnelle_gpl_carburant_100kg = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gpl_carburant_100kg
        prix_gpl_carburant_ht = prix_gpl_carburant_ht_avant_remise - (aide_exceptionnelle_gpl_carburant_100kg / 100)
        return prix_gpl_carburant_ht

    def formula_2023(menage, period):
        return menage('prix_gpl_carburant_ht_avant_remise', period)
