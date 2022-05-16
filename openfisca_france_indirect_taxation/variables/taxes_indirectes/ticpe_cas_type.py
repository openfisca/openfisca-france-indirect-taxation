import numpy as np

from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

## ticpe diesel

class diesel_ticpe_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de TICPE sur le diesel"
    definition_period = YEAR

    def formula(menage, period, parameters):
        region = menage('region', period)
        accise_diesel = parameters(period).imposition_indirecte.produits_energetiques.ticpe.gazole
        major_ticpe_diesel = parameters(period).imposition_indirecte.produits_energetiques.major_regionale_ticpe_gazole
        major_regionale_ticpe_diesel = np.fromiter(
            (
                getattr(major_ticpe_diesel, region_cell, 0)
                for region_cell in region
            ),
            dtype=np.float32
        )
        accise_diesel_ticpe = accise_diesel + major_regionale_ticpe_diesel
        nombre_litres_diesel = menage('nombre_litres_diesel', period)
        montant_diesel_ticpe = nombre_litres_diesel * (accise_diesel_ticpe / 100)
        return montant_diesel_ticpe


## ticpe essence

class essence_ticpe_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur toutes les essences cumulées"
    definition_period = YEAR

    def formula_2009(menage, period):
        sp95_ticpe = menage('sp95_ticpe_cas_type', period)
        sp98_ticpe = menage('sp98_ticpe_cas_type', period)
        sp_e10_ticpe = menage('sp_e10_ticpe_cas_type', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe + sp_e10_ticpe)
        return essence_ticpe

    def formula_2007(menage, period):
        sp95_ticpe = menage('sp95_ticpe_cas_type', period)
        sp98_ticpe = menage('sp98_ticpe_cas_type', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe)
        return essence_ticpe

    def formula_1990(menage, period):
        sp95_ticpe = menage('sp95_ticpe_cas_type', period)
        sp98_ticpe = menage('sp98_ticpe_cas_type', period)
        super_plombe_ticpe = menage('super_plombe_ticpe_cas_type', period)
        essence_ticpe = (sp95_ticpe + sp98_ticpe + super_plombe_ticpe)
        return essence_ticpe


class sp_e10_ticpe_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur le SP E10"
    definition_period = YEAR

    def formula_2009(menage, period, parameters):
        region = menage('region', period)
        accise_super_e10 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_e10
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super
        majoration_ticpe_super_e10 = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in region
            ),
            dtype=np.float32
        )
        accise_sp_e10_ticpe = accise_super_e10 + majoration_ticpe_super_e10
        nombre_litres_sp_e10 = menage('nombre_litres_sp_e10', period)
        montant_sp_e10_ticpe = nombre_litres_sp_e10 * (accise_sp_e10_ticpe / 100)
        return montant_sp_e10_ticpe


class sp95_ticpe_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de TICPE sur le sp_95"
    definition_period = YEAR

    def formula(menage, period, parameters):
        region = menage('region', period)
        accise_super95 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_95_98
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super
        majoration_ticpe_super95 = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in region
            ),
            dtype=np.float32
        )
        accise_sp_95_ticpe = accise_super95 + majoration_ticpe_super95
        nombre_litres_sp_95 = menage('nombre_litres_sp_95', period)
        montant_sp95_ticpe = nombre_litres_sp_95 * (accise_sp_95_ticpe / 100)
        return montant_sp95_ticpe

class sp98_ticpe_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de TICPE sur le sp_98"
    definition_period = YEAR

    def formula(menage, period, parameters):
        region = menage('region', period)
        accise_super98 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_95_98
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super
        majoration_ticpe_super98 = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in region
            ),
            dtype=np.float32
        )
        accise_sp_98_ticpe = accise_super98 + majoration_ticpe_super98
        nombre_litres_sp_98 = menage('nombre_litres_sp_98', period)
        montant_sp98_ticpe = nombre_litres_sp_98 * (accise_sp_98_ticpe / 100)
        return montant_sp98_ticpe

class super_plombe_ticpe_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur le super plombé"
    definition_period = YEAR
    end = "2006-12-31"

    def formula(menage, period, parameters):
        accise_super_plombe_ticpe = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_plombe

        nombre_litres_super_plombe = menage('nombre_litres_super_plombe', period)

        montant_super_plombe_ticpe = nombre_litres_super_plombe * (accise_super_plombe_ticpe /100)

        return montant_super_plombe_ticpe

## ticpe combustibles liquides

class combustibles_liquides_ticpe_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de TICPE sur les combustibles liquides"
    definition_period = YEAR

    def formula(menage, period, parameters):
        nombre_litres_combustibles_liquides = menage('nombre_litres_combustibles_liquides', period)
        accise_combustibles_liquides = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole_fioul_domestique_hectolitre ##à verifier
        combustibles_liquides_ticpe = nombre_litres_combustibles_liquides * (accise_combustibles_liquides / 100)

        return combustibles_liquides_ticpe

## total taxs energies (ticpe diesel + ticpe essence + ticpe combustibles liquides)

class total_taxes_energies_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur tous les carburants cumulés"
    definition_period = YEAR

    def formula(menage, period):
        essence_ticpe = menage('essence_ticpe_cas_type', period)
        diesel_ticpe = menage('diesel_ticpe_cas_type', period)
        combustibles_liquides_ticpe = menage('combustibles_liquides_ticpe_cas_type', period)
        total_taxes_energies = diesel_ticpe + essence_ticpe + combustibles_liquides_ticpe

        return total_taxes_energies

## cout total hors taxe

class cout_total_carburant_ht_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du cout total du carburant (essence + diesel + combustibles liquides) hors taxes"
    definition_period = YEAR

    def formula(menage, period):
        nombre_litres_diesel = menage('nombre_litres_diesel', period)
        nombre_litres_sp_e10 = menage('nombre_litres_sp_e10', period)
        nombre_litres_sp_95 = menage('nombre_litres_sp_95', period)
        nombre_litres_sp_98 = menage('nombre_litres_sp_98', period)
        nombre_litres_super_plombe = menage('nombre_litres_super_plombe', period)
        nombre_litres_combustibles_liquides = menage('nombre_litres_combustibles_liquides', period)

        prix_litre_diesel_ht = menage('prix_litre_diesel_ht', period)
        prix_litre_super_e10_ht = menage('prix_litre_super_e10_ht', period)
        prix_litre_super_95_ht = menage('prix_litre_super_95_ht', period)
        prix_litre_super_98_ht = menage('prix_litre_super_98_ht', period)
        prix_litre_super_plombe_ht = menage('prix_litre_super_plombe_ht', period)
        prix_litre_gplc_ht = menage('prix_litre_gplc_ht', period)

        cout_diesel_ht = nombre_litres_diesel * prix_litre_diesel_ht
        cout_sp_e10_ht = nombre_litres_sp_e10 * prix_litre_super_e10_ht
        cout_sp_95_ht = nombre_litres_sp_95 * prix_litre_super_95_ht
        cout_sp_98_ht = nombre_litres_sp_98 * prix_litre_super_98_ht
        cout_super_plombe_ht = nombre_litres_super_plombe * prix_litre_super_plombe_ht
        cout_combustibles_liquides_ht = nombre_litres_combustibles_liquides * prix_litre_gplc_ht

        cout_total_ht = cout_diesel_ht + cout_sp_e10_ht + cout_sp_95_ht + cout_sp_98_ht + cout_super_plombe_ht + cout_combustibles_liquides_ht

        return cout_total_ht

## tva sur cout ht carburant

class tva_cout_carburant_ht_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la tva sur le cout total ht du carburant"
    definition_period = YEAR

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        cout_total_ht_cas_type = menage('cout_total_ht_cas_type', period)

        tva_cout_carburant_ht = taux_plein_tva * cout_total_ht_cas_type

        return tva_cout_carburant_ht

## tva sur ticpe carburant

class tva_ticpe_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la tva sur la TICPE du carburant"
    definition_period = YEAR

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        total_taxes_energies = menage('total_taxes_energies_cas_type', period)

        tva_ticpe = taux_plein_tva * total_taxes_energies

        return tva_ticpe

## tva total

class tva_carburant_total(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du cout total de la TVA sur le carburant pour le menage"
    definition_period = YEAR

    def formula(menage,period):
        tva_ticpe = menage('tva_ticpe_cas_type', period)
        tva_cout_carburant_ht = menage('tva_cout_carburant_ht_cas_type', period)
        tva_carburant_total = tva_ticpe + tva_cout_carburant_ht

        return tva_carburant_total

## cout total ttc

class cout_total_carburant_ttc_cas_type(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du cout total du carburant pour le menage (cout_carburant_ht + ticpe + tva_carburant_total )"
    definition_period = YEAR

    def formula(menage, period):
        total_taxes_energies = menage('total_taxes_energies_cas_type', period)
        cout_total_carburant_ht = menage('cout_total_carburant_ht_cas_type', period)
        tva_carburant_total = menage('tva_carburant_total', period)


        cout_total_carburant_ttc = total_taxes_energies + cout_total_carburant_ht + tva_carburant_total

        return cout_total_carburant_ttc
