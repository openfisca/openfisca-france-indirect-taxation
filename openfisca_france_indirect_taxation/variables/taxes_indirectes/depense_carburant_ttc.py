from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

# depense different type de gazole ttc:


class depense_gazole_b7_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'depense du gazole B7 ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        depense_gazole_b7_ht = menage('depense_gazole_b7_ht', period)
        gazole_b7_ticpe = menage('gazole_b7_ticpe', period)
        tva_sur_gazole_b7 = menage('tva_sur_gazole_b7', period)
        depense_gazole_b7_ttc = depense_gazole_b7_ht + gazole_b7_ticpe + tva_sur_gazole_b7
        return depense_gazole_b7_ttc


class depense_gazole_b10_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'depense du gazole B10 ttc'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        depense_gazole_b10_ht = menage('depense_gazole_b10_ht', period)
        gazole_b10_ticpe = menage('gazole_b10_ticpe', period)
        tva_sur_gazole_b10 = menage('tva_sur_gazole_b10', period)
        depense_gazole_b10_ttc = depense_gazole_b10_ht + gazole_b10_ticpe + tva_sur_gazole_b10
        return depense_gazole_b10_ttc


# depense gazole total ht:


class depense_gazole_total_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'depense total du gazole ttc'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc', period)
        depense_gazole_b10_ttc = menage('depense_gazole_b10_ttc', period)
        depense_gazole_total_ttc = (depense_gazole_b7_ttc + depense_gazole_b10_ttc)
        return depense_gazole_total_ttc

    def formula(menage, period):
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc', period)
        depense_gazole_total_ttc = depense_gazole_b7_ttc
        return depense_gazole_total_ttc

# depense different type d'essence ttc:


class depense_essence_sp95_e10_ttc(Variable):
    value_type = float
    entity = Menage
    label = "Dépense en essence sp95 e10 ttc"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period):
        depense_essence_sp95_e10_ht = menage('depense_essence_sp95_e10_ht', period)
        essence_sp95_e10_ticpe = menage('essence_sp95_e10_ticpe', period)
        tva_sur_essence_sp95_e10 = menage('tva_sur_essence_sp95_e10', period)
        depense_essence_sp95_e10_ttc = depense_essence_sp95_e10_ht + essence_sp95_e10_ticpe + tva_sur_essence_sp95_e10
        return depense_essence_sp95_e10_ttc


class depense_essence_sp95_ttc(Variable):
    value_type = float
    entity = Menage
    label = "Dépense en essence sp95 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        depense_essence_sp95_ht = menage('depense_essence_sp95_ht', period)
        essence_sp95_ticpe = menage('essence_sp95_ticpe', period)
        tva_sur_essence_sp95 = menage('tva_sur_essence_sp95', period)
        depense_essence_sp95_ttc = depense_essence_sp95_ht + essence_sp95_ticpe + tva_sur_essence_sp95
        return depense_essence_sp95_ttc


class depense_essence_sp98_ttc(Variable):
    value_type = float
    entity = Menage
    label = "Dépense en essence sp98 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        depense_essence_sp98_ht = menage('depense_essence_sp98_ht', period)
        essence_sp98_ticpe = menage('essence_sp98_ticpe', period)
        tva_sur_essence_sp98 = menage('tva_sur_essence_sp98', period)
        depense_essence_sp98_ttc = depense_essence_sp98_ht + essence_sp98_ticpe + tva_sur_essence_sp98
        return depense_essence_sp98_ttc


class depense_essence_super_plombe_ttc(Variable):
    value_type = float
    entity = Menage
    label = "depense de l'essence super plombé ttc"
    definition_period = YEAR
    default_value = 0
    end = "2007-01-01"

    def formula(menage, period):
        depense_essence_super_plombe_ht = menage('depense_essence_super_plombe_ht', period)
        essence_super_plombe_ticpe = menage('essence_super_plombe_ticpe', period)
        tva_sur_essence_super_plombe = menage('tva_sur_essence_super_plombe', period)
        depense_essence_super_plombe_ttc = depense_essence_super_plombe_ht + essence_super_plombe_ticpe + tva_sur_essence_super_plombe
        return depense_essence_super_plombe_ttc


class depense_essence_e85_ttc(Variable):
    value_type = float
    entity = Menage
    label = "depense de l'essence e85 ttc"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period):
        depense_essence_e85_ht = menage('depense_essence_e85_ht', period)
        essence_e85_ticpe = menage('essence_e85_ticpe', period)
        tva_sur_essence_e85 = menage('tva_sur_essence_e85', period)
        depense_essence_e85_ttc = depense_essence_e85_ht + essence_e85_ticpe + tva_sur_essence_e85
        return depense_essence_e85_ttc


# depense essence total ttc:

class depense_essence_total_ttc(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant des depenses sur tous les types d'essences cumulés ttc"
    definition_period = YEAR

    def formula_2009(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc', period)
        depense_essence_e85_ttc = menage('depense_essence_e85_ttc', period)
        depense_essence_sp95_e10_ttc = menage('depense_essence_sp95_e10_ttc', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_e85_ttc + depense_essence_sp95_e10_ttc)
        return depense_essence_total_ttc

    def formula_2007(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc', period)
        depense_essence_e85_ttc = menage('depense_essence_e85_ttc', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_e85_ttc)
        return depense_essence_total_ttc

    def formula_1990(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc', period)
        depense_essence_super_plombe_ttc = menage('depense_essence_super_plombe_ttc', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_super_plombe_ttc)
        return depense_essence_total_ttc

# depense gaz de pétrole liquéfié carburant ttc:


class depense_gpl_carburant_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'depense du gaz de pétrole liquéfié - carburant ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ht', period)
        gpl_carburant_ticpe = menage('gpl_carburant_ticpe', period)
        tva_sur_gpl_carburant = menage('tva_sur_gpl_carburant', period)
        depense_gpl_carburant_ttc = depense_gpl_carburant_ht + gpl_carburant_ticpe + tva_sur_gpl_carburant
        return depense_gpl_carburant_ttc


# depense carburant total ttc:

class depense_carburant_total_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant des depenses sur tous les carburants cumulés ttc'
    definition_period = YEAR

    def formula(menage, period):
        depense_essence_total_ht = menage('depense_essence_total_ttc', period)
        depense_gazole_total_ht = menage('depense_gazole_total_ttc', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc', period)
        depense_carburant_total_ht = depense_gazole_total_ht + depense_essence_total_ht + depense_gpl_carburant_ht
        return depense_carburant_total_ht


class depense_carburant_total_ttc_sans_distinction(Variable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant des depenses sur tous les carburants cumulés ttc '
    definition_period = YEAR

    def formula_2017(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc', period)
        depense_essence_e85_ttc = menage('depense_essence_e85_ttc', period)
        depense_essence_sp95_e10_ttc = menage('depense_essence_sp95_e10_ttc', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc', period)
        depense_gazole_b10_ttc = menage('depense_gazole_b10_ttc', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_e85_ttc
             + depense_essence_sp95_e10_ttc + depense_gazole_b7_ttc + depense_gazole_b10_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc

    def formula_2009(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc', period)
        depense_essence_e85_ttc = menage('depense_essence_e85_ttc', period)
        depense_essence_sp95_e10_ttc = menage('depense_essence_sp95_e10_ttc', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_e85_ttc
        + depense_essence_sp95_e10_ttc + depense_gazole_b7_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc

    def formula_2007(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc', period)
        depense_essence_e85_ttc = menage('depense_essence_e85_ttc', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_e85_ttc
        + depense_gazole_b7_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc

    def formula_1990(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc', period)
        depense_essence_super_plombe_ttc = menage('depense_essence_super_plombe_ttc', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_super_plombe_ttc
        + depense_gazole_b7_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc
