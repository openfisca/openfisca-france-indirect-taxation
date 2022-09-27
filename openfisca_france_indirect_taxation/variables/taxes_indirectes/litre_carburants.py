from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR
import numpy as np

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
    label = 'nombre de litre de gazole B7 consommés par le ménage'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        depense_gazole_b7_ttc_entree = menage('depense_gazole_b7_ttc_entree', period)
        prix_gazole_b7_ttc = menage('prix_gazole_b7_ttc', period)
        nombre_litres_gazole_b7 = np.divide(depense_gazole_b7_ttc_entree, prix_gazole_b7_ttc, out=np.zeros_like(depense_gazole_b7_ttc_entree), where= prix_gazole_b7_ttc != 0)
        return nombre_litres_gazole_b7


class nombre_litres_gazole_b10(Variable):   # ATTENTION: pas de prix disponible pour gazole B10, on utilise prix du gazole B7
    value_type = float
    entity = Menage
    label = 'nombre de litre de gazole B10 consommés par le ménage'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        depense_gazole_b10_ttc_entree = menage('depense_gazole_b10_ttc_entree', period)
        prix_gazole_b10_ttc = menage('prix_gazole_b10_ttc', period)
        nombre_litres_gazole_b10 = np.divide(depense_gazole_b10_ttc_entree, prix_gazole_b10_ttc, out=np.zeros_like(depense_gazole_b10_ttc_entree), where= prix_gazole_b10_ttc != 0)
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
    label = "nombre de litre d'essence SP95 E10 consommés par le ménage"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period):
        depense_essence_sp95_e10_ttc_entree = menage('depense_essence_sp95_e10_ttc_entree', period)
        prix_essence_sp95_e10_ttc = menage('prix_essence_sp95_e10_ttc', period)
        nombre_litres_essence_sp95_e10 = np.divide(depense_essence_sp95_e10_ttc_entree, prix_essence_sp95_e10_ttc, out=np.zeros_like(depense_essence_sp95_e10_ttc_entree), where= prix_essence_sp95_e10_ttc != 0)
        return nombre_litres_essence_sp95_e10


class nombre_litres_essence_sp95(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence SP95 consommés par le ménage"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        depense_essence_sp95_ttc_entree = menage('depense_essence_sp95_ttc_entree', period)
        prix_essence_sp95_ttc = menage('prix_essence_sp95_ttc', period)
        nombre_litres_essence_sp95 = np.divide(depense_essence_sp95_ttc_entree, prix_essence_sp95_ttc, out=np.zeros_like(depense_essence_sp95_ttc_entree), where= prix_essence_sp95_ttc != 0)
        return nombre_litres_essence_sp95


class nombre_litres_essence_sp98(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence SP98 consommés par le ménage"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        depense_essence_sp98_ttc_entree = menage('depense_essence_sp98_ttc_entree', period)
        prix_essence_sp98_ttc = menage('prix_essence_sp98_ttc', period)
        nombre_litres_essence_sp98 = np.divide(depense_essence_sp98_ttc_entree, prix_essence_sp98_ttc, out=np.zeros_like(depense_essence_sp98_ttc_entree), where= prix_essence_sp98_ttc != 0)
        return nombre_litres_essence_sp98


class nombre_litres_essence_super_plombe(Variable):
    value_type = float
    entity = Menage
    label = 'nombre de litre de super plombé consommés par le ménage'
    definition_period = YEAR
    default_value = 0
    end = "2017-01-01"

    def formula(menage, period):
        depense_essence_super_plombe_ttc_entree = menage('depense_essence_super_plombe_ttc_entree', period)
        prix_essence_super_plombe_ttc = menage('prix_essence_super_plombe_ttc', period)
        nombre_litres_essence_super_plombe = np.divide(depense_essence_super_plombe_ttc_entree, prix_essence_super_plombe_ttc, out=np.zeros_like(depense_essence_super_plombe_ttc_entree), where= prix_essence_super_plombe_ttc != 0)
        return nombre_litres_essence_super_plombe


class nombre_litres_essence_e85(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence E85 par le ménage"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period):
        depense_essence_e85_ttc_entree = menage('depense_essence_e85_ttc_entree', period)
        prix_essence_e85_ttc = menage('prix_essence_e85_ttc', period)
        nombre_litres_essence_e85 = depense_essence_e85_ttc_entree / prix_essence_e85_ttc
        nombre_litres_essence_e85 = np.divide(depense_essence_e85_ttc_entree, prix_essence_e85_ttc, out=np.zeros_like(depense_essence_e85_ttc_entree), where= prix_essence_e85_ttc != 0)
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
    label = 'nombre de litre de gaz de pétrole liquéfié consommés par le ménage'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        depense_gpl_carburant_ttc_entree = menage('depense_gpl_carburant_ttc_entree', period)
        prix_gpl_carburant_ttc = menage('prix_gpl_carburant_ttc', period)
        nombre_litres_gpl_carburant = np.divide(depense_gpl_carburant_ttc_entree, prix_gpl_carburant_ttc, out=np.zeros_like(depense_gpl_carburant_ttc_entree), where= prix_gpl_carburant_ttc != 0)
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
