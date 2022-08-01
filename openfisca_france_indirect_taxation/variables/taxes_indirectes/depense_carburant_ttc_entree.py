from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

# depense different type de gazole ttc:


class depense_gazole_b7_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = 'depense du gazole B7 ttc'
    definition_period = YEAR
    default_value = 0


class depense_gazole_b10_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = 'depense du gazole B10 ttc'
    definition_period = YEAR
    default_value = 0


# depense different type d'essence ttc:


class depense_essence_sp95_e10_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "depense de l'escence sp95 e10 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        depenses_sp_e10 = menage('depenses_sp_e10', period)
        return depenses_sp_e10


class depense_essence_sp95_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "depense de l'escence sp95 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        depenses_sp_95 = menage('depenses_sp_95', period)
        return depenses_sp_95


class depense_essence_sp98_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "depense de l'escence sp98 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        depenses_sp_98 = menage('depenses_sp_98', period)
        return depenses_sp_98


class depense_essence_super_plombe_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "depense de l'essence super plombé ttc"
    definition_period = YEAR
    default_value = 0
    end = "2007-01-01"


class depense_essence_e85_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "depense de l'essence e85 ttc"
    definition_period = YEAR
    default_value = 0


# depense essence total ttc:


# depense gaz de pétrole liquéfié carburant ttc:


class depense_gpl_carburant_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = 'depense du gaz de pétrole liquéfié - carburant ttc'
    definition_period = YEAR
    default_value = 0


class depense_carburant_total_ttc_sans_distinction_entree(Variable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant des depenses sur tous les carburants cumulés ttc '
    definition_period = YEAR

    def formula_2017(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc_entree', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc_entree', period)
        depense_essence_e85_ttc = menage('depense_essence_e85_ttc_entree', period)
        depense_essence_sp95_e10_ttc = menage('depense_essence_sp95_e10_ttc_entree', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc_entree', period)
        depense_gazole_b10_ttc = menage('depense_gazole_b10_ttc_entree', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc_entree', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_e85_ttc
        + depense_essence_sp95_e10_ttc + depense_gazole_b7_ttc + depense_gazole_b10_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc

    def formula_2009(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc_entree', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc_entree', period)
        depense_essence_e85_ttc = menage('depense_essence_e85_ttc_entree', period)
        depense_essence_sp95_e10_ttc = menage('depense_essence_sp95_e10_ttc_entree', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc_entree', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc_entree', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_e85_ttc
        + depense_essence_sp95_e10_ttc + depense_gazole_b7_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc

    def formula_2007(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc_entree', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc_entree', period)
        depense_essence_e85_ttc = menage('depense_essence_e85_ttc_entree', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc_entree', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc_entree', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_e85_ttc
        + depense_gazole_b7_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc

    def formula_1990(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc_entree', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc_entree', period)
        depense_essence_super_plombe_ttc = menage('depense_essence_super_plombe_ttc_entree', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc_entree', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc_entree', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_super_plombe_ttc
        + depense_gazole_b7_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc
