# -*- coding: utf-8 -*-


import numpy

from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class quantites_combustibles_liquides(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantité de combustibles solides (en litres) consommée par les ménages"

    def formula(menage, period, parameters):
        depenses_combustibles_liquides = menage('depenses_combustibles_liquides', period)
        prix_combustibles_liquides = \
            parameters(period.start).tarifs_energie.prix_fioul_domestique.prix_annuel_moyen_fioul_domestique_ttc_livraisons_2000_4999_litres_en_euro_par_litre

        quantite_combustibles_liquides = depenses_combustibles_liquides / prix_combustibles_liquides

        return quantite_combustibles_liquides


class quantites_diesel(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités de diesel consommées par les ménages"

    def formula(menage, period, parameters):
        depenses_diesel = menage('depenses_diesel', period)
        diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
        quantites_diesel = depenses_diesel / diesel_ttc * 100

        return quantites_diesel


# Not used
class quantites_electricite_3kva(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 3 kva"

    def formula(menage, period, parameters):
        tarif_fixe_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_3_kva
        depenses_elect = menage('depenses_electricite', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.prix_unitaire_base_edf_ttc.prix_kwh_3_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


# Not used
class quantites_electricite_6kva(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 6 kva"

    def formula(menage, period, parameters):
        tarif_fixe_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_6_kva
        depenses_elect = menage('depenses_electricite', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.prix_unitaire_base_edf_ttc.prix_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


# Not used
class quantites_electricite_9kva(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 9 kva"

    def formula(menage, period, parameters):
        tarif_fixe_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_9_kva
        depenses_elect = menage('depenses_electricite', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.prix_unitaire_base_edf_ttc.prix_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


# Not used
class quantites_electricite_12kva(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 12 kva"

    def formula(menage, period, parameters):
        tarif_fixe_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_12_kva
        depenses_elect = menage('depenses_electricite', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.prix_unitaire_base_edf_ttc.prix_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


# Not used
class quantites_electricite_15kva(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 15 kva"

    def formula(menage, period, parameters):
        tarif_fixe_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_15_kva
        depenses_elect = menage('depenses_electricite', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.prix_unitaire_base_edf_ttc.prix_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


# Not used
class quantites_electricite_18kva(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 18 kva"

    def formula(menage, period, parameters):
        tarif_fixe_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_18_kva
        depenses_elect = menage('depenses_electricite', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.prix_unitaire_base_edf_ttc.prix_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


class quantites_essence(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités d'essence consommées par les ménages"

    def formula_1990(menage, period):
        quantites_sp95 = menage('quantites_sp95', period)
        quantites_sp98 = menage('quantites_sp98', period)
        quantites_super_plombe = menage('quantites_super_plombe', period)
        quantites_essence = (quantites_sp95 + quantites_sp98 + quantites_super_plombe)
        return quantites_essence

    def formula_2007(menage, period):

        quantites_sp95 = menage('quantites_sp95', period)
        quantites_sp98 = menage('quantites_sp98', period)
        quantites_essence = (quantites_sp95 + quantites_sp98)
        return quantites_essence

    def formula_2009(menage, period):
        quantites_sp95 = menage('quantites_sp95', period)
        quantites_sp98 = menage('quantites_sp98', period)
        quantites_sp_e10 = menage('quantites_sp_e10', period)
        quantites_essence = (quantites_sp95 + quantites_sp98 + quantites_sp_e10)
        return quantites_essence


class quantites_gaz_contrat_base(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat de base"

    def formula(menage, period, parameters):
        tarif_fixe_gaz = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.base_0_1000
        depenses_gaz = menage('depenses_gaz_ville', period)
        depenses_sans_part_fixe = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_base_ttc
        quantite_gaz = depenses_sans_part_fixe / prix_unitaire_gaz

        return quantite_gaz


class quantites_gaz_contrat_b0(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat b0"

    def formula(menage, period, parameters):
        tarif_fixe_gaz = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.b0_1000_6000
        depenses_gaz = menage('depenses_gaz_ville', period)
        depenses_sans_part_fixe = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_b0_ttc
        quantite_gaz = depenses_sans_part_fixe / prix_unitaire_gaz

        return quantite_gaz


class quantites_gaz_contrat_b1(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat b1"

    def formula(menage, period, parameters):
        tarif_fixe_gaz = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.b1_6_30000
        depenses_gaz = menage('depenses_gaz_ville', period)
        depenses_sans_part_fixe = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_b1_ttc
        quantite_gaz = depenses_sans_part_fixe / prix_unitaire_gaz

        return quantite_gaz


class quantites_gaz_contrat_b2i(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat b2i"

    def formula(menage, period, parameters):
        tarif_fixe_gaz = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.b2i_30000
        depenses_gaz = menage('depenses_gaz_ville', period)
        depenses_gaz_variables = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_b2i_ttc
        quantite_gaz = depenses_gaz_variables / prix_unitaire_gaz

        return quantite_gaz


class quantites_gaz_contrat_optimal(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au meilleur contrat"

    def formula(menage, period):
        quantite_base = menage('quantites_gaz_contrat_base', period)
        quantite_b0 = menage('quantites_gaz_contrat_b0', period)
        quantite_b1 = menage('quantites_gaz_contrat_b1', period)
        quantite_b2i = menage('quantites_gaz_contrat_b2i', period)
        quantite_optimale_base_b0 = numpy.maximum(quantite_base, quantite_b0)
        quantite_optimale_base_b1 = numpy.maximum(quantite_optimale_base_b0, quantite_b1)
        quantite_optimale_base_b2i = numpy.maximum(quantite_optimale_base_b1, quantite_b2i)
        quantite_optimale = numpy.maximum(quantite_optimale_base_b2i, 0)

        return quantite_optimale


class quantites_gaz_final(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au meilleur contrat"

    def formula(menage, period):
        quantites_gaz_contrat_optimal = menage('quantites_gaz_contrat_optimal', period)
        depenses_gaz_prix_unitaire = menage('depenses_gaz_prix_unitaire', period)
        tarifs_sociaux_gaz = menage('tarifs_sociaux_gaz', period)

        # Ceux qui ne consomment pas de gaz ayant depenses_gaz_prix_unitaire = 0, on remplace 0 par 1 pour éviter de diviser par zéro
        depenses_gaz_prix_unitaire = depenses_gaz_prix_unitaire + 1 * (depenses_gaz_prix_unitaire == 0)
        quantites_gaz_finale = quantites_gaz_contrat_optimal + (tarifs_sociaux_gaz / depenses_gaz_prix_unitaire * (depenses_gaz_prix_unitaire != 0))

        return quantites_gaz_finale


class quantites_electricite_selon_compteur(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantité d'électricité (en kWh) consommée par les ménages d'après le compteur imputé"

    def formula(menage, period):
        depenses_electricite_variables = menage('depenses_electricite_variables', period)
        depenses_electricite_prix_unitaire = menage('depenses_electricite_prix_unitaire', period)
        # On inclut ici les dépenses non facturées aux ménages (provenant des TPN) pour refleter leur "vraie" consommation
        tarifs_sociaux_electricite = menage('tarifs_sociaux_electricite', period)
        quantites_electricite_selon_compteur = (depenses_electricite_variables + tarifs_sociaux_electricite) / depenses_electricite_prix_unitaire
        quantites_electricite_selon_compteur = numpy.maximum(quantites_electricite_selon_compteur, 0)

        return quantites_electricite_selon_compteur


class quantites_gaz_liquefie(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantité de gaz liquefie (en kWh) consommée par les ménages d'après SOeS Phébus 2013"

    def formula(menage, period):
        depenses_gaz_liquefie = menage('depenses_gaz_liquefie', period)
        pondmen = menage('pondmen', period)

        population = numpy.sum(pondmen)
        total_gpl_phebus = population * 0.19  # quantité annuelle moyenne consommée par les ménages
        # en MWh d'après la conversion des tep donnés par SOeS Phébus
        total_gpl_bdf = numpy.sum(depenses_gaz_liquefie * pondmen)

        quantites_gaz_liquefie = depenses_gaz_liquefie * total_gpl_phebus / total_gpl_bdf

        return quantites_gaz_liquefie * 1000  # en KWh


class quantites_sp_e10(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités consommées de sans plomb e10 par les ménages"

    def formula(menage, period, parameters):
        depenses_essence = menage('depenses_essence', period)
        part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10 = depenses_essence * part_sp_e10
        super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
        quantite_sp_e10 = depenses_sp_e10 / super_95_e10_ttc * 100

        return quantite_sp_e10


class quantites_sp95(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités consommées de sans plomb 95 par les ménages"

    def formula(menage, period, parameters):
        depenses_essence = menage('depenses_essence', period)
        part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp95 = depenses_essence * part_sp95
        super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
        quantite_sp95 = depenses_sp95 / super_95_ttc * 100

        return quantite_sp95


class quantites_sp98(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités consommées de sans plomb 98 par les ménages"

    def formula(menage, period, parameters):
        depenses_essence = menage('depenses_essence', period)
        part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp98 = depenses_essence * part_sp98
        super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
        quantites_sp98 = depenses_sp98 / super_98_ttc * 100

        return quantites_sp98


class quantites_super_plombe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantités consommées de super plombé par les ménages"

    def formula(menage, period, parameters):
        depenses_essence = menage('depenses_essence', period)
        part_super_plombe = \
            parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe = depenses_essence * part_super_plombe
        super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
        quantite_super_plombe = depenses_super_plombe / super_plombe_ttc * 100

        return quantite_super_plombe
