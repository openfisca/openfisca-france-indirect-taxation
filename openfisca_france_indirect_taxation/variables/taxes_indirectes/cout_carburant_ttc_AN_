import numpy as np

from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

# cout different type de gazole ttc:
class cout_gazole_b7_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout du gazole B7 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        nombre_litres_gazole_b7 = menage('nombre_litres_gazole_b7', period)
        prix_gazole_b7_hectolitre_ttc = parameters(period).prix_carburants.diesel_ttc   ### à modifier avec le nouveau CSV + litre?
        cout_gazole_b7_ttc = nombre_litres_gazole_b7 * ( prix_gazole_b7_hectolitre_ttc / 100)
        return cout_gazole_b7_ttc

class cout_gazole_b10_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix du gazole B10 ttc"
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period, parameters):
        nombre_litres_gazole_b10 = menage('nombre_litres_gazole_b10', period)
        prix_gazole_b10_hectolitre_ttc = parameters(period).prix_carburants.diesel_ttc   ### à modifier avec le nouveau CSV + litre?
        cout_gazole_b10_ttc = nombre_litres_gazole_b10 * ( prix_gazole_b10_hectolitre_ttc / 100)
        return cout_gazole_b10_ttc

# cout gazole total ht:
class cout_gazole_total_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout total du gazole ttc"
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc', period)
        cout_gazole_b10_ttc = menage('cout_gazole_b10_ttc', period)
        cout_gazole_total_ttc = (cout_gazole_b7_ttc + cout_gazole_b10_ttc)
        return cout_gazole_total_ttc

    def formula(menage, period):
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc', period)
        cout_gazole_total_ttc = cout_gazole_b7_ttc
        return cout_gazole_total_ttc


# cout different type d'essence ttc:

class cout_essence_sp95_e10_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'escence sp95 e10 ttc"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period, parameters):
        nombre_litres_essence_sp95_e10 = menage('nombre_litres_essence_sp95_e10', period)
        prix_essence_sp95_e10_hectolitre_ttc = parameters(period).prix_carburants.super_95_e10_ttc ### à modifier avec le nouveau CSV + litre?
        cout_essence_sp95_e10_ttc = nombre_litres_essence_sp95_e10 * ( prix_essence_sp95_e10_hectolitre_ttc / 100)
        return cout_essence_sp95_e10_ttc

class cout_essence_sp95_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'escence sp95 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        nombre_litres_essence_sp95 = menage('nombre_litres_essence_sp95', period)
        prix_essence_sp95_hectolitre_ttc = parameters(period).prix_carburants.super_95_ttc ### à modifier avec le nouveau CSV + litre?
        cout_essence_sp95_ttc = nombre_litres_essence_sp95 * ( prix_essence_sp95_hectolitre_ttc / 100)
        return cout_essence_sp95_ttc

class cout_essence_sp98_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'escence sp98 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        nombre_litres_essence_sp98 = menage('nombre_litres_essence_sp98', period)
        prix_essence_sp98_hectolitre_ttc = parameters(period).prix_carburants.super_98_ttc ### à modifier avec le nouveau CSV + litre?
        cout_essence_sp98_ttc = nombre_litres_essence_sp98 * ( prix_essence_sp98_hectolitre_ttc / 100)
        return cout_essence_sp98_ttc

class cout_essence_super_plombe_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'essence super plombé ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        nombre_litres_essence_super_plombe = menage('nombre_litres_essence_super_plombe', period)
        prix_essence_essence_super_plombe_hectolitre_ttc = parameters(period).prix_carburants.super_95_e10_ttc ### à modifier avec le nouveau CSV + litre?
        cout_essence_essence_super_plombe_ttc = nombre_litres_essence_super_plombe * ( prix_essence_essence_super_plombe_hectolitre_ttc / 100)
        return cout_essence_essence_super_plombe_ttc

class cout_essence_e85_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'essence e85 ttc"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period, parameters):
        nombre_litres_essence_e85 = menage('nombre_litres_essence_e85', period)
        prix_essence_e85_hectolitre_ttc = parameters(period).prix_carburants.super_95_ttc ### à modifier avec le nouveau CSV + FAUX CAR SP95
        cout_essence_e85_ttc = nombre_litres_essence_e85 * ( prix_essence_e85_hectolitre_ttc / 100)
        return cout_essence_e85_ttc

# cout essence total ttc:
class cout_essence_total_ttc(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant des couts sur tous les types d'essences cumulés ttc"
    definition_period = YEAR

    def formula_2009(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc', period)
        cout_essence_essence_e85_ttc = menage('cout_essence_essence_e85_ttc', period)
        cout_essence_sp95_e10_ttc = menage('cout_essence_sp95_e10_ttc', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_essence_e85_ttc + cout_essence_sp95_e10_ttc)
        return cout_essence_total_ttc

    def formula_2007(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc', period)
        cout_essence_essence_e85_ttc = menage('cout_essence_essence_e85_ttc', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_essence_e85_ttc)
        return cout_essence_total_ttc

    def formula_1990(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc', period)
        cout_essence_super_plombe_ttc = menage('cout_essence_super_plombe_ttc', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_super_plombe_ttc)
        return cout_essence_total_ttc

# cout gaz de pétrole liquéfié carburant ttc:

class cout_gpl_carburant_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout du gaz de pétrole liquéfié - carburant ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        nombre_litres_gpl_carburant = menage('nombre_litres_gpl_carburant', period)
        prix_gpl_carburant_ttc = parameters(period).prix_carburants.gplc_ttc ### à modifier avec le nouveau CSV + litre?
        cout_gpl_carburant_ttc = nombre_litres_gpl_carburant * ( prix_gpl_carburant_ttc / 100)
        return cout_gpl_carburant_ttc

# cout carburant total ht:
class cout_carburant_total_ht(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant des couts sur tous les carburants cumulés ttc"
    definition_period = YEAR

    def formula(menage, period):
        cout_essence_total_ht = menage('cout_essence_total_ht', period)
        cout_gazole_total_ht = menage('cout_gazole_total_ht', period)
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ht', period)
        cout_carburant_total_ht = cout_gazole_total_ht + cout_essence_total_ht + cout_gpl_carburant_ht
        return cout_carburant_total_ht
