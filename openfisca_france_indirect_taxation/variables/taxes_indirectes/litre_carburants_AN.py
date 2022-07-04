from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR


# caracteristiques menages


class code_region(Variable):
    value_type = str
    entity = Menage
    label = 'code region du menage'
    definition_period = YEAR


# nombre de litres par type de gazole

class nombre_litres_gazole_b7(Variable):
    value_type = float
    entity = Menage
    label = 'nombre de litre de gasoil B7 consommés par le menage'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        cout_gazole_b7_ttc_entree = menage('cout_gazole_b7_ttc_entree', period)
        prix_gazole_b7_ttc = menage('prix_gazole_b7_ttc', period)
        nombre_litres_gazole_b7 = cout_gazole_b7_ttc_entree / prix_gazole_b7_ttc
        return nombre_litres_gazole_b7


class nombre_litres_gazole_b10(Variable):   # ATTENTION: pas de prix disponible pour gazole B10, on utilise prix du gazole B7
    value_type = float
    entity = Menage
    label = 'nombre de litre de gasoil B10 consommés par le menage'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        cout_gazole_b10_ttc_entree = menage('cout_gazole_b10_ttc_entree', period)
        prix_gazole_b10_ttc = menage('prix_gazole_b10_ttc', period)
        nombre_litres_gazole_b10 = cout_gazole_b10_ttc_entree / prix_gazole_b10_ttc
        return nombre_litres_gazole_b10

# nombre de litre de gazole total:


class nombre_litres_gazole_total(Variable):
    value_type = float
    entity = Menage
    label = 'nombre de litre de gazole total'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        nombre_litres_gazole_b7 = menage('nombre_litres_gazole_b7', period)
        nombre_litres_gazole_b10 = menage('nombre_litres_gazole_b10', period)
        nombre_litres_gazole_total = (nombre_litres_gazole_b7 + nombre_litres_gazole_b10)
        return nombre_litres_gazole_total

    def formula(menage, period):
        nombre_litres_gazole_b7 = menage('nombre_litres_gazole_b7', period)
        nombre_litres_gazole_total = nombre_litres_gazole_b7
        return nombre_litres_gazole_total


# nombre litres essence


class nombre_litres_essence_sp95_e10(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence super e10 consommés par le menage"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period):
        cout_essence_sp95_e10_ttc_entree = menage('cout_essence_sp95_e10_ttc_entree', period)
        prix_essence_sp95_e10_ttc = menage('prix_essence_sp95_e10_ttc', period)
        nombre_litres_essence_sp95_e10 = cout_essence_sp95_e10_ttc_entree / prix_essence_sp95_e10_ttc
        return nombre_litres_essence_sp95_e10


class nombre_litres_essence_sp95(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence sp95 consommés par le menage"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        cout_essence_sp95_ttc_entree = menage('cout_essence_sp95_ttc_entree', period)
        prix_essence_sp95_ttc = menage('prix_essence_sp95_ttc', period)
        nombre_litres_essence_sp95 = cout_essence_sp95_ttc_entree / prix_essence_sp95_ttc
        return nombre_litres_essence_sp95


class nombre_litres_essence_sp98(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence sp98 consommés par le menage"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        cout_essence_sp98_ttc_entree = menage('cout_essence_sp98_ttc_entree', period)
        prix_essence_sp98_ttc = menage('prix_essence_sp98_ttc', period)
        nombre_litres_essence_sp98 = cout_essence_sp98_ttc_entree / prix_essence_sp98_ttc
        return nombre_litres_essence_sp98


class nombre_litres_essence_super_plombe(Variable):
    value_type = float
    entity = Menage
    label = 'nombre de litre de super plombé consommés par le menage'
    definition_period = YEAR
    default_value = 0
    end = "2017-01-01"

    def formula(menage, period):
        cout_essence_super_plombe_ttc_entree = menage('cout_essence_super_plombe_ttc_entree', period)
        prix_essence_super_plombe_ttc = menage('prix_essence_super_plombe_ttc', period)
        nombre_litres_essence_super_plombe = cout_essence_super_plombe_ttc_entree / prix_essence_super_plombe_ttc
        return nombre_litres_essence_super_plombe


class nombre_litres_essence_e85(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence e85 par le menage"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period):
        cout_essence_e85_ttc_entree = menage('cout_essence_e85_ttc_entree', period)
        prix_essence_e85_ttc = menage('prix_essence_e85_ttc', period)
        nombre_litres_essence_e85 = cout_essence_e85_ttc_entree / prix_essence_e85_ttc
        return nombre_litres_essence_e85


# montant TVA total sur l'essence

class nombre_litres_essence_total(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence total"
    definition_period = YEAR

    def formula_2009(menage, period):
        nombre_litres_essence_sp95 = menage('nombre_litres_essence_sp95', period)
        nombre_litres_essence_sp98 = menage('nombre_litres_essence_sp98', period)
        nombre_litres_essence_e85 = menage('nombre_litres_essence_e85', period)
        nombre_litres_essence_sp95_e10 = menage('nombre_litres_essence_sp95_e10', period)
        nombre_litres_essence_total = (nombre_litres_essence_sp95 + nombre_litres_essence_sp98 + nombre_litres_essence_e85 + nombre_litres_essence_sp95_e10)
        return nombre_litres_essence_total

    def formula_2007(menage, period):
        nombre_litres_essence_sp95 = menage('nombre_litres_essence_sp95', period)
        nombre_litres_essence_sp98 = menage('nombre_litres_essence_sp98', period)
        nombre_litres_essence_e85 = menage('nombre_litres_essence_e85', period)
        nombre_litres_essence_total = (nombre_litres_essence_sp95 + nombre_litres_essence_sp98 + nombre_litres_essence_e85)
        return nombre_litres_essence_total

    def formula_1990(menage, period):
        nombre_litres_essence_sp95 = menage('nombre_litres_essence_sp95', period)
        nombre_litres_essence_sp98 = menage('nombre_litres_essence_sp98', period)
        nombre_litres_essence_super_plombe = menage('nombre_litres_essence_super_plombe', period)
        nombre_litres_essence_total = (nombre_litres_essence_sp95 + nombre_litres_essence_sp98 + nombre_litres_essence_super_plombe)
        return nombre_litres_essence_total


# nombre litres combustibles liquides


class nombre_litres_gpl_carburant(Variable):
    value_type = float
    entity = Menage
    label = 'nombre de litre de gaz de pétrole liquéfié consommés par le menage'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        cout_gpl_carburant_ttc_entree = menage('cout_gpl_carburant_ttc_entree', period)
        prix_gpl_carburant_ttc = menage('prix_gpl_carburant_ttc', period)
        nombre_litres_gpl_carburant = cout_gpl_carburant_ttc_entree / prix_gpl_carburant_ttc
        return nombre_litres_gpl_carburant


# nombre de litre total:


class nombre_litres_total(Variable):
    value_type = float
    entity = Menage
    label = 'nombre de litre total'
    definition_period = YEAR

    def formula(menage, period):
        nombre_litres_essence_total = menage('nombre_litres_essence_total', period)
        nombre_litres_gazole_total = menage('nombre_litres_gazole_total', period)
        nombre_litres_gpl_carburant = menage('nombre_litres_gpl_carburant', period)
        nombre_litres_total = nombre_litres_gazole_total + nombre_litres_essence_total + nombre_litres_gpl_carburant
        return nombre_litres_total
