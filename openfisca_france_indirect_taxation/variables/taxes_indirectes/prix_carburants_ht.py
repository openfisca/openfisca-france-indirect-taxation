from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR


class prix_gazole_b7_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gazole B7 HT par litre avant remise'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_gazole_b7_ht', period)

    def formula_2022(menage, period, parameters):
        prix_gazole_b7_ht = menage('prix_gazole_b7_ht', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_gazole_b7_ht_avant_remise = prix_gazole_b7_ht + (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_gazole_b7_ht_avant_remise

    def formula_2023(menage, period):
        return menage('prix_gazole_b7_ht', period)


class prix_gazole_b7_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix du gazole B7 HT par litre"
    definition_period = YEAR
    default_value = 0
    reference = "https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000046489832/2022-10-27/"

    def formula(menage, period, parameters):
        prix_gazole_b7_ht_hectolitre = parameters(period.start).prix_carburants.diesel_ht
        prix_gazole_b7_ht = prix_gazole_b7_ht_hectolitre / 100
        return prix_gazole_b7_ht


class prix_gazole_b10_ht_avant_remise(Variable):  # Attention pas de prix dispo pour le diesel b10 on prend celui du diesel b7
    value_type = float
    entity = Menage
    label = 'prix du gazole B10 HT par litre avant remise'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_gazole_b10_ht', period)

    def formula_2022(menage, period, parameters):
        prix_gazole_b10_ht = menage('prix_gazole_b10_ht', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_gazole_b10_ht_avant_remise = prix_gazole_b10_ht + (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_gazole_b10_ht_avant_remise

    def formula_2023(menage, period):
        return menage('prix_gazole_b10_ht', period)


class prix_gazole_b10_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix du gazole B10 HT par litre"
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period, parameters):
        prix_gazole_b7_ht_hectolitre = parameters(period.start).prix_carburants.diesel_ht
        prix_gazole_b10_ht = prix_gazole_b7_ht_hectolitre / 100
        return prix_gazole_b10_ht


class prix_essence_sp95_e10_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 E10 HT par litre avant remise"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp95_e10_ht', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp95_e10_ht = menage('prix_essence_sp95_e10_ht', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_essence_sp95_e10_ht_avant_remise = prix_essence_sp95_e10_ht + (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_essence_sp95_e10_ht_avant_remise

    def formula_2023(menage, period):
        return menage('prix_essence_sp95_e10_ht', period)


class prix_essence_sp95_e10_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 E10 HT par litre "
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period, parameters):
        prix_essence_sp95_e10_ht_hectolitre = parameters(period.start).prix_carburants.super_95_e10_ht
        prix_essence_sp95_e10_ht = prix_essence_sp95_e10_ht_hectolitre / 100
        return prix_essence_sp95_e10_ht


class prix_essence_sp95_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 HT par litre avant remise"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp95_ht', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp95_ht = menage('prix_essence_sp95_ht', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_essence_sp95_ht_avant_remise = prix_essence_sp95_ht + (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_essence_sp95_ht_avant_remise

    def formula_2023(menage, period):
        return menage('prix_essence_sp95_ht_avant_remise', period)


class prix_essence_sp95_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 HT par litre"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_sp95_ht_hectolitre = parameters(period.start).prix_carburants.super_95_ht
        prix_essence_sp95_ht = prix_essence_sp95_ht_hectolitre / 100
        return prix_essence_sp95_ht


class prix_essence_sp98_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 HT par litre avant remise"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp98_ht', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp98_ht = menage('prix_essence_sp98_ht', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_essence_sp98_ht_avant_remise = prix_essence_sp98_ht + (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_essence_sp98_ht_avant_remise

    def formula_2023(menage, period):
        return menage('prix_essence_sp98_ht', period)


class prix_essence_sp98_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 HT par litre "
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_sp98_ht_hectolitre = parameters(period.start).prix_carburants.super_98_ht
        prix_essence_sp98_ht = prix_essence_sp98_ht_hectolitre / 100
        return prix_essence_sp98_ht


class prix_essence_super_plombe_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence super plombé HT par litre"
    definition_period = YEAR
    default_value = 0
    end = "2017-01-01"

    def formula(menage, period, parameters):
        prix_essence_super_plombe_ht_hectolitre = parameters(period.start).prix_carburants.super_plombe_ht
        prix_essence_super_plombe_ht = prix_essence_super_plombe_ht_hectolitre / 100
        return prix_essence_super_plombe_ht


class prix_essence_e85_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence E85 HT par litre avant remise"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_e85_ht', period)

    def formula_2022(menage, period, parameters):
        prix_essence_e85_ht = menage('prix_essence_e85_ht', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        prix_essence_e85_ht_avant_remise = prix_essence_e85_ht + (aide_exceptionnelle_gazole_essence_hl / 100)
        return prix_essence_e85_ht_avant_remise

    def formula_2023(menage, period):
        return menage('prix_essence_e85_ht', period)


class prix_essence_e85_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence E85 HT par litre"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period, parameters):
        prix_essence_e85_ht_hectolitre = parameters(period.start).prix_carburants.super_e85_ht
        prix_essence_e85_ht = prix_essence_e85_ht_hectolitre / 100
        return prix_essence_e85_ht


class prix_gpl_carburant_ht_avant_remise(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gaz de pétrole liquéfié - carburant HT par litre avant remise'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_gpl_carburant_ht', period)

    def formula_2022(menage, period, parameters):
        prix_gpl_carburant_ht = menage('prix_gpl_carburant_ht', period)
        aide_exceptionnelle_gpl_carburant_100kg = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gpl_carburant_100kg
        coefficient_conversion_kg_vers_litre = (1 / 0.525)
        aide_exceptionnelle_gpl_carburant_hectolitre = aide_exceptionnelle_gpl_carburant_100kg * coefficient_conversion_kg_vers_litre
        prix_gpl_carburant_ht_avant_remise = prix_gpl_carburant_ht + (aide_exceptionnelle_gpl_carburant_hectolitre / 100)
        return prix_gpl_carburant_ht_avant_remise

    def formula_2023(menage, period):
        return menage('prix_gpl_carburant_ht', period)


class prix_gpl_carburant_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix du gaz de pétrole liquéfié - carburant HT par litre"
    definition_period = YEAR
    default_value = 0
    reference = "https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000046489832/2022-10-27/"

    def formula(menage, period, parameters):
        prix_gpl_carburant_ht_hectolitre = parameters(period.start).prix_carburants.gplc_ht
        prix_gpl_carburant_ht = prix_gpl_carburant_ht_hectolitre / 100
        return prix_gpl_carburant_ht
