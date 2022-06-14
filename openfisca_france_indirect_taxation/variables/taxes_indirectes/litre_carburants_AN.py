from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR
#from openfisca_france_indirect_taxation.yearly_variable import YearlyVariable

## caracteristiques menages

class region(Variable):
    value_type = str
    entity = Menage
    label = "region du menage"
    definition_period = YEAR


## nombre litres diesel

class nombre_litres_gazole_b7(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre de gasoil B7 consommés par le menage"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc', period)
        prix_gazole_b7_hectolitre_ttc = parameters(period).prix_carburants.diesel_ttc   ### à modifier avec le nouveau CSV + litre?
        nombre_litres_gazole_b7 = cout_gazole_b7_ttc / ( prix_gazole_b7_hectolitre_ttc / 100 )
        return nombre_litres_gazole_b7

class nombre_litres_gazole_b7(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre de gasoil B7 consommés par le menage"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gazole_b10_ttc = menage('cout_gazole_b10_ttc', period)
        prix_gazole_b10_hectolitre_ttc = parameters(period).prix_carburants.diesel_ttc   ### à modifier avec le nouveau CSV + litre?
        nombre_litres_gazole_b10 = cout_gazole_b10_ttc / ( prix_gazole_b10_hectolitre_ttc / 100 )
        return nombre_litres_gazole_b10

## nombre litres essence

class nombre_litres_essence_sp95_e10(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence super e10 consommés par le menage"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period, parameters):
        cout_essence_sp95_e10_ttc = menage('cout_essence_sp95_e10_ttc', period)
        prix_essence_sp95_e10_hectolitre_ttc = parameters(period).prix_carburants.super_95_e10_ttc ### à modifier avec le nouveau CSV + litre?
        nombre_litres_essence_sp95_e10 = cout_essence_sp95_e10_ttc / ( prix_essence_sp95_e10_hectolitre_ttc / 100 )
        return nombre_litres_essence_sp95_e10

class nombre_litres_essence_sp95(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence sp95 consommés par le menage"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc', period)
        prix_essence_sp95_ttc_hectolitre = parameters(period).prix_carburants.super_95_ttc   ### à modifier avec le nouveau CSV
        nombre_litres_essence_sp95 = cout_essence_sp95_ttc / ( prix_essence_sp95_ttc_hectolitre / 100 )
        return nombre_litres_essence_sp95

class nombre_litres_essence_sp98(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence sp98 consommés par le menage"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc', period)
        prix_essence_sp98_ttc_hectolitre = parameters(period).prix_carburants.super_98_ttc   ### à modifier avec le nouveau CSV
        nombre_litres_essence_sp98 = cout_essence_sp98_ttc / ( prix_essence_sp98_ttc_hectolitre / 100 )
        return nombre_litres_essence_sp98

class nombre_litres_essence_super_plombe(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre de super plombé consommés par le menage"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_super_plombe_ttc = menage('cout_essence_super_plombe_ttc', period)
        prix_essence_super_plombe_ttc_hectolitre = parameters(period).prix_carburants.super_plombe_ttc   ### à modifier avec le nouveau CSV
        nombre_litres_essence_super_plombe = cout_essence_super_plombe_ttc / ( prix_essence_super_plombe_ttc_hectolitre / 100 )
        return nombre_litres_essence_super_plombe

class nombre_litres_essence_e85(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre d'essence e85 par le menage"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period, parameters):
        cout_essence_e85_ttc = menage('cout_essence_e85_ttc', period)
        prix_essence_e85_ttc_hectolitre = parameters(period).prix_carburants.super_95_ttc   ### à modifier avec le nouveau CSV car n'existe pas (pour le moment sp95)
        nombre_litres_essence_e85 = cout_essence_e85_ttc / ( prix_essence_e85_ttc_hectolitre / 100 )
        return nombre_litres_essence_e85

## nombre litres combustibles liquides

class nombre_litres_gpl_carburant(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litre de gaz de pétrole liquéfié consommés par le menage"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gpl_carburant_ttc = menage('cout_gpl_carburant_ttc', period)
        prix_cout_gpl_carburant_ttc_hectolitre = parameters(period).prix_carburants.gplc_ttc   ### à modifier avec le nouveau CSV car n'existe pas (pour le moment sp95)
        nombre_litres_gpl_carburant = cout_gpl_carburant_ttc / ( prix_cout_gpl_carburant_ttc_hectolitre / 100 )
        return nombre_litres_gpl_carburant