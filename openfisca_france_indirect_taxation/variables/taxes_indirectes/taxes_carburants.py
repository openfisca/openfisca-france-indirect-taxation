from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR


# Taxe sur les différents types de gazole:


class taxes_gazole_b7(Variable):
    value_type = float
    entity = Menage
    label = 'Taxes prélevées sur le diesel (gazole B7) en station service'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        gazole_b7_ticpe = menage('gazole_b7_ticpe', period)
        tva_sur_gazole_b7 = menage('tva_sur_gazole_b7', period)
        taxes_gazole_b7 = gazole_b7_ticpe + tva_sur_gazole_b7
        return taxes_gazole_b7


class taxes_gazole_b10(Variable):
    value_type = float
    entity = Menage
    label = 'Taxes prélevées sur le diesel (gazole B10) en station service'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        gazole_b10_ticpe = menage('gazole_b10_ticpe', period)
        tva_sur_gazole_b10 = menage('tva_sur_gazole_b10', period)
        taxes_gazole_b10 = gazole_b10_ticpe + tva_sur_gazole_b10
        return taxes_gazole_b10

# Total des taxes (TICPE + TVA)


class taxes_gazole_total(Variable):
    value_type = float
    entity = Menage
    label = 'Taxes prélevées sur le diesel (gazole B7 et B10) en station service'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        ticpe_gazole_total = menage('gazole_ticpe_total', period)
        tva_gazole_total = menage('tva_sur_gazole_total', period)
        taxes_gazole_total = ticpe_gazole_total + tva_gazole_total
        return taxes_gazole_total

# Taxe sur les differents types d'essence (SP95-E10, SP95, SP98, Super plombe, E85):


class taxes_essence_sp95_e10(Variable):
    value_type = float
    entity = Menage
    label = "Taxes prélevées sur l'essence sans plomb 95 E10 en station service"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period):
        essence_sp95_e10_ticpe = menage('essence_sp95_e10_ticpe', period)
        tva_sur_essence_sp95_e10 = menage('tva_sur_essence_sp95_e10', period)
        taxes_essence_sp95_e10 = essence_sp95_e10_ticpe + tva_sur_essence_sp95_e10
        return taxes_essence_sp95_e10


class taxes_essence_sp95(Variable):
    value_type = float
    entity = Menage
    label = "Taxes prélevées sur l'essence sans plomb 95 en station service"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        essence_sp95_ticpe = menage('essence_sp95_ticpe', period)
        tva_sur_essence_sp95 = menage('tva_sur_essence_sp95', period)
        taxes_essence_sp95 = essence_sp95_ticpe + tva_sur_essence_sp95
        return taxes_essence_sp95


class taxes_essence_sp98(Variable):
    value_type = float
    entity = Menage
    label = "Taxes prélevées sur l'essence sans plomb 98 en station service"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        essence_sp98_ticpe = menage('essence_sp98_ticpe', period)
        tva_sur_essence_sp98 = menage('tva_sur_essence_sp98', period)
        taxes_essence_sp98 = essence_sp98_ticpe + tva_sur_essence_sp98
        return taxes_essence_sp98


class taxes_essence_super_plombe(Variable):
    value_type = float
    entity = Menage
    label = "Taxes prélevées sur l'essence super plombé en station service"
    definition_period = YEAR
    default_value = 0
    end = '2006-12-31'

    def formula(menage, period):
        essence_super_plombe_ticpe = menage('essence_super_plombe_ticpe', period)
        tva_sur_essence_super_plombe = menage('tva_sur_essence_super_plombe', period)
        taxes_essence_super_plombe = essence_super_plombe_ticpe + tva_sur_essence_super_plombe
        return taxes_essence_super_plombe


class taxes_essence_e85(Variable):
    value_type = float
    entity = Menage
    label = "Taxes prélevées sur l'essence super ethanol 85 en station service"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period):
        essence_e85_ticpe = menage('essence_e85_ticpe', period)
        tva_sur_essence_e85 = menage('tva_sur_essence_e85', period)
        taxes_essence_e85 = essence_e85_ticpe + tva_sur_essence_e85
        return taxes_essence_e85


class taxes_essence_total(Variable):
    value_type = float
    entity = Menage
    label = "Taxes prélevées sur l'essence en station service"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        ticpe_essence_total = menage('essence_ticpe_total', period)
        tva_essence_total = menage('tva_sur_essence_total', period)
        taxes_essence_total = ticpe_essence_total + tva_essence_total
        return taxes_essence_total


# Taxe sur GPL carburant:


class taxes_gpl_carburant(Variable):
    value_type = float
    entity = Menage
    label = "Taxes prélevées sur le GPL carburant en station service"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        gpl_carburant_ticpe = menage('gpl_carburant_ticpe', period)
        tva_sur_gpl_carburant = menage('tva_sur_gpl_carburant', period)
        taxes_gpl_carburant = gpl_carburant_ticpe + tva_sur_gpl_carburant
        return taxes_gpl_carburant


# Total taxes (TICPE + TVA) sur tous les carburants


class taxes_carburant_total(Variable):
    value_type = float
    entity = Menage
    label = "Taxes prélevées sur les carburants en station service"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        taxes_gazole_total = menage('taxes_gazole_total', period)
        taxes_essence_total = menage('taxes_essence_total', period)
        taxes_gpl_carburant = menage('taxes_gpl_carburant', period)
        taxes_tous_carburants = taxes_gazole_total + taxes_essence_total + taxes_gpl_carburant
        return taxes_tous_carburants
