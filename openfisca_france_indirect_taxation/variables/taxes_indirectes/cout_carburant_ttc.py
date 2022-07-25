from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

# cout different type de gazole ttc:


class cout_gazole_b7_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'cout du gazole B7 ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        cout_gazole_b7_ht = menage('cout_gazole_b7_ht', period)
        gazole_b7_ticpe = menage('gazole_b7_ticpe', period)
        tva_sur_gazole_b7 = menage('tva_sur_gazole_b7', period)
        cout_gazole_b7_ttc = cout_gazole_b7_ht + gazole_b7_ticpe + tva_sur_gazole_b7
        return cout_gazole_b7_ttc


class cout_gazole_b10_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'cout du gazole B10 ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        cout_gazole_b10_ht = menage('cout_gazole_b10_ht', period)
        gazole_b10_ticpe = menage('gazole_b10_ticpe', period)
        tva_sur_gazole_b10 = menage('tva_sur_gazole_b10', period)
        cout_gazole_b10_ttc = cout_gazole_b10_ht + gazole_b10_ticpe + tva_sur_gazole_b10
        return cout_gazole_b10_ttc


# cout gazole total ht:


class cout_gazole_total_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'cout total du gazole ttc'
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

    def formula_2009(menage, period):
        cout_essence_sp95_e10_ht = menage('cout_essence_sp95_e10_ht', period)
        essence_sp95_e10_ticpe = menage('essence_sp95_e10_ticpe', period)
        tva_sur_essence_sp95_e10 = menage('tva_sur_essence_sp95_e10', period)
        cout_essence_sp95_e10_ttc = cout_essence_sp95_e10_ht + essence_sp95_e10_ticpe + tva_sur_essence_sp95_e10
        return cout_essence_sp95_e10_ttc


class cout_essence_sp95_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'escence sp95 ttc"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period):
        cout_essence_sp95_ht = menage('cout_essence_sp95_ht', period)
        essence_sp95_ticpe = menage('essence_sp95_ticpe', period)
        tva_sur_essence_sp95 = menage('tva_sur_essence_sp95', period)
        cout_essence_sp95_ttc = cout_essence_sp95_ht + essence_sp95_ticpe + tva_sur_essence_sp95
        return cout_essence_sp95_ttc


class cout_essence_sp98_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'escence sp98 ttc"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period):
        cout_essence_sp98_ht = menage('cout_essence_sp98_ht', period)
        essence_sp98_ticpe = menage('essence_sp98_ticpe', period)
        tva_sur_essence_sp98 = menage('tva_sur_essence_sp98', period)
        cout_essence_sp98_ttc = cout_essence_sp98_ht + essence_sp98_ticpe + tva_sur_essence_sp98
        return cout_essence_sp98_ttc


class cout_essence_super_plombe_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'essence super plombé ttc"
    definition_period = YEAR
    default_value = 0
    end = "2007-01-01"

    def formula(menage, period):
        cout_essence_super_plombe_ht = menage('cout_essence_super_plombe_ht', period)
        essence_super_plombe_ticpe = menage('essence_super_plombe_ticpe', period)
        tva_sur_essence_super_plombe = menage('tva_sur_essence_super_plombe', period)
        cout_essence_super_plombe_ttc = cout_essence_super_plombe_ht + essence_super_plombe_ticpe + tva_sur_essence_super_plombe
        return cout_essence_super_plombe_ttc


class cout_essence_e85_ttc(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'essence e85 ttc"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period):
        cout_essence_e85_ht = menage('cout_essence_e85_ht', period)
        essence_e85_ticpe = menage('essence_e85_ticpe', period)
        tva_sur_essence_e85 = menage('tva_sur_essence_e85', period)
        cout_essence_e85_ttc = cout_essence_e85_ht + essence_e85_ticpe + tva_sur_essence_e85
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
        cout_essence_e85_ttc = menage('cout_essence_e85_ttc', period)
        cout_essence_sp95_e10_ttc = menage('cout_essence_sp95_e10_ttc', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_e85_ttc + cout_essence_sp95_e10_ttc)
        return cout_essence_total_ttc

    def formula_2007(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc', period)
        cout_essence_e85_ttc = menage('cout_essence_e85_ttc', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_e85_ttc)
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
    label = 'cout du gaz de pétrole liquéfié - carburant ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ht', period)
        gpl_carburant_ticpe = menage('gpl_carburant_ticpe', period)
        tva_sur_gpl_carburant = menage('tva_sur_gpl_carburant', period)
        cout_gpl_carburant_ttc = cout_gpl_carburant_ht + gpl_carburant_ticpe + tva_sur_gpl_carburant
        return cout_gpl_carburant_ttc


# cout carburant total ttc:

class cout_carburant_total_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant des couts sur tous les carburants cumulés ttc'
    definition_period = YEAR

    def formula(menage, period):
        cout_essence_total_ht = menage('cout_essence_total_ttc', period)
        cout_gazole_total_ht = menage('cout_gazole_total_ttc', period)
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ttc', period)
        cout_carburant_total_ht = cout_gazole_total_ht + cout_essence_total_ht + cout_gpl_carburant_ht
        return cout_carburant_total_ht


class cout_carburant_total_ttc_sans_distinction(Variable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant des couts sur tous les carburants cumulés ttc '
    definition_period = YEAR

    def formula_2017(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc', period)
        cout_essence_e85_ttc = menage('cout_essence_e85_ttc', period)
        cout_essence_sp95_e10_ttc = menage('cout_essence_sp95_e10_ttc', period)
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc', period)
        cout_gazole_b10_ttc = menage('cout_gazole_b10_ttc', period)
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ttc', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_e85_ttc
             + cout_essence_sp95_e10_ttc + cout_gazole_b7_ttc + cout_gazole_b10_ttc + cout_gpl_carburant_ht)
        return cout_essence_total_ttc

    def formula_2009(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc', period)
        cout_essence_e85_ttc = menage('cout_essence_e85_ttc', period)
        cout_essence_sp95_e10_ttc = menage('cout_essence_sp95_e10_ttc', period)
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc', period)
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ttc', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_e85_ttc
        + cout_essence_sp95_e10_ttc + cout_gazole_b7_ttc + cout_gpl_carburant_ht)
        return cout_essence_total_ttc

    def formula_2007(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc', period)
        cout_essence_e85_ttc = menage('cout_essence_e85_ttc', period)
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc', period)
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ttc', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_e85_ttc
        + cout_gazole_b7_ttc + cout_gpl_carburant_ht)
        return cout_essence_total_ttc

    def formula_1990(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc', period)
        cout_essence_super_plombe_ttc = menage('cout_essence_super_plombe_ttc', period)
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc', period)
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ttc', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_super_plombe_ttc
        + cout_gazole_b7_ttc + cout_gpl_carburant_ht)
        return cout_essence_total_ttc
