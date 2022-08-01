from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR


# depense different type de gazole ht:


class depense_gazole_b7_ht(Variable):
    value_type = float
    entity = Menage
    label = 'depense du gazole B7 ht'
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
    label = 'depense du gazole B10 ht'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        nombre_litres_gazole_b10 = menage('nombre_litres_gazole_b10', period)
        prix_gazole_b10_ht = menage('prix_gazole_b10_ht', period)
        depense_gazole_b10_ht = nombre_litres_gazole_b10 * prix_gazole_b10_ht
        return depense_gazole_b10_ht


# depense gazole total ht:

class depense_gazole_total_ht(Variable):
    value_type = float
    entity = Menage
    label = 'depense total du gazole ht'
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


# depense different type d'essence ht:


class depense_essence_sp95_e10_ht(Variable):
    value_type = float
    entity = Menage
    label = "depense de l'essence SP95 E10 ht"
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
    label = "depense de l'essence SP95 ht"
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
    label = "depense de l'essence SP98 ht"
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
    label = "depense de l'essence super plombé ht"
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
    label = "depense de l'essence e85 ht"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period):
        nombre_litres_essence_e85 = menage('nombre_litres_essence_e85', period)
        prix_essence_e85_ht = menage('prix_essence_e85_ht', period)
        depense_essence_e85_ht = nombre_litres_essence_e85 * prix_essence_e85_ht
        return depense_essence_e85_ht


# depense essence total ht:

class depense_essence_total_ht(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant des depenses sur tous les types d'essences cumulés ht"
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


# depense gaz de pétrole liquéfié carburant ht:


class depense_gpl_carburant_ht(Variable):
    value_type = float
    entity = Menage
    label = 'depense du gaz de pétrole liquéfié - carburant ht'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        nombre_litres_gpl_carburant = menage('nombre_litres_gpl_carburant', period)
        prix_gpl_carburant_ht = menage('prix_gpl_carburant_ht', period)
        depense_gpl_carburant_ht = nombre_litres_gpl_carburant * prix_gpl_carburant_ht
        return depense_gpl_carburant_ht


# depense carburant total ht:


class depense_carburant_total_ht(Variable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant des depenses sur tous les carburants cumulés ht'
    definition_period = YEAR

    def formula(menage, period):
        depense_essence_total_ht = menage('depense_essence_total_ht', period)
        depense_gazole_total_ht = menage('depense_gazole_total_ht', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ht', period)
        depense_carburant_total_ht = depense_gazole_total_ht + depense_essence_total_ht + depense_gpl_carburant_ht
        return depense_carburant_total_ht
