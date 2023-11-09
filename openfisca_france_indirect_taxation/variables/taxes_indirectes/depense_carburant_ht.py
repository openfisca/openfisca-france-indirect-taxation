from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR


# dépense differents types de gazole HT:


class depense_gazole_b7_ht(Variable):
    value_type = float
    entity = Menage
    label = 'dépense en gazole B7 HT'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        nombre_litres_gazole_b7 = menage('nombre_litres_gazole_b7', period)
        prix_gazole_b7_ht = menage('prix_gazole_b7_ht', period)
        depense_gazole_b7_ht = nombre_litres_gazole_b7 * prix_gazole_b7_ht
        return depense_gazole_b7_ht


class depense_gazole_b10_ht(Variable):
    value_type = float
    entity = Menage
    label = 'dépense en gazole B10 HT'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        nombre_litres_gazole_b10 = menage('nombre_litres_gazole_b10', period)
        prix_gazole_b10_ht = menage('prix_gazole_b10_ht', period)
        depense_gazole_b10_ht = nombre_litres_gazole_b10 * prix_gazole_b10_ht
        return depense_gazole_b10_ht


# dépense gazole total HT:

class depense_gazole_total_ht(Variable):
    value_type = float
    entity = Menage
    label = 'dépense totale en gazole HT'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        depense_gazole_b7_ht = menage('depense_gazole_b7_ht', period)
        depense_gazole_b10_ht = menage('depense_gazole_b10_ht', period)
        depense_gazole_total_ht = (depense_gazole_b7_ht + depense_gazole_b10_ht)
        return depense_gazole_total_ht

    def formula(menage, period):
        depense_gazole_b7_ht = menage('depense_gazole_b7_ht', period)
        depense_gazole_total_ht = depense_gazole_b7_ht
        return depense_gazole_total_ht


# dépense differents types d'essence HT:


class depense_essence_sp95_e10_ht(Variable):
    value_type = float
    entity = Menage
    label = "dépense en essence SP95 E10 HT"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period):
        nombre_litres_essence_sp95_e10 = menage('nombre_litres_essence_sp95_e10', period)
        prix_essence_sp95_e10_ht = menage('prix_essence_sp95_e10_ht', period)
        depense_essence_sp95_e10_ht = nombre_litres_essence_sp95_e10 * prix_essence_sp95_e10_ht
        return depense_essence_sp95_e10_ht


class depense_essence_sp95_ht(Variable):
    value_type = float
    entity = Menage
    label = "dépense en essence SP95 HT"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        nombre_litres_essence_sp95 = menage('nombre_litres_essence_sp95', period)
        prix_essence_sp95_ht = menage('prix_essence_sp95_ht', period)
        depense_essence_sp95_ht = nombre_litres_essence_sp95 * prix_essence_sp95_ht
        return depense_essence_sp95_ht


class depense_essence_sp98_ht(Variable):
    value_type = float
    entity = Menage
    label = "dépense en essence SP98 HT"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        nombre_litres_essence_sp98 = menage('nombre_litres_essence_sp98', period)
        prix_essence_sp98_ht = menage('prix_essence_sp98_ht', period)
        depense_essence_sp98_ht = nombre_litres_essence_sp98 * prix_essence_sp98_ht
        return depense_essence_sp98_ht


class depense_essence_super_plombe_ht(Variable):
    value_type = float
    entity = Menage
    label = "dépense en essence super plombé HT"
    definition_period = YEAR
    default_value = 0
    end = "2017-01-01"

    def formula(menage, period):
        nombre_litres_essence_super_plombe = menage('nombre_litres_essence_super_plombe', period)
        prix_essence_super_plombe_ht = menage('prix_essence_super_plombe_ht', period)
        depense_essence_super_plombe_ht = nombre_litres_essence_super_plombe * prix_essence_super_plombe_ht
        return depense_essence_super_plombe_ht


class depense_essence_e85_ht(Variable):
    value_type = float
    entity = Menage
    label = "dépense en essence E85 HT"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period):
        nombre_litres_essence_e85 = menage('nombre_litres_essence_e85', period)
        prix_essence_e85_ht = menage('prix_essence_e85_ht', period)
        depense_essence_e85_ht = nombre_litres_essence_e85 * prix_essence_e85_ht
        return depense_essence_e85_ht


# dépense essence total HT:

class depense_essence_total_ht(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant des dépenses sur tous les types d'essences cumulés HT"
    definition_period = YEAR

    def formula_2009(menage, period):
        depense_essence_sp95_ht = menage('depense_essence_sp95_ht', period)
        depense_essence_sp98_ht = menage('depense_essence_sp98_ht', period)
        depense_essence_e85_ht = menage('depense_essence_e85_ht', period)
        depense_essence_sp95_e10_ht = menage('depense_essence_sp95_e10_ht', period)
        depense_essence_total_ht = (depense_essence_sp95_ht + depense_essence_sp98_ht + depense_essence_e85_ht + depense_essence_sp95_e10_ht)
        return depense_essence_total_ht

    def formula_2007(menage, period):
        depense_essence_sp95_ht = menage('depense_essence_sp95_ht', period)
        depense_essence_sp98_ht = menage('depense_essence_sp98_ht', period)
        depense_essence_e85_ht = menage('depense_essence_e85_ht', period)
        depense_essence_total_ht = (depense_essence_sp95_ht + depense_essence_sp98_ht + depense_essence_e85_ht)
        return depense_essence_total_ht

    def formula_1990(menage, period):
        depense_essence_sp95_ht = menage('depense_essence_sp95_ht', period)
        depense_essence_sp98_ht = menage('depense_essence_sp98_ht', period)
        depense_essence_super_plombe_ht = menage('depense_essence_super_plombe_ht', period)
        depense_essence_total_ht = (depense_essence_sp95_ht + depense_essence_sp98_ht + depense_essence_super_plombe_ht)
        return depense_essence_total_ht


# dépense gaz de pétrole liquéfié carburant HT:


class depense_gpl_carburant_ht(Variable):
    value_type = float
    entity = Menage
    label = 'dépense en gaz de pétrole liquéfié - carburant HT'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        nombre_litres_gpl_carburant = menage('nombre_litres_gpl_carburant', period)
        prix_gpl_carburant_ht = menage('prix_gpl_carburant_ht', period)
        depense_gpl_carburant_ht = nombre_litres_gpl_carburant * prix_gpl_carburant_ht
        return depense_gpl_carburant_ht


# dépense carburant total HT:


class depense_carburant_total_ht(Variable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant des dépenses sur tous les carburants cumulés HT'
    definition_period = YEAR

    def formula(menage, period):
        depense_essence_total_ht = menage('depense_essence_total_ht', period)
        depense_gazole_total_ht = menage('depense_gazole_total_ht', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ht', period)
        depense_carburant_total_ht = depense_gazole_total_ht + depense_essence_total_ht + depense_gpl_carburant_ht
        return depense_carburant_total_ht
