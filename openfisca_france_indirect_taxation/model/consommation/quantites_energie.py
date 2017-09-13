# -*- coding: utf-8 -*-

from __future__ import division


import numpy

from openfisca_france_indirect_taxation.model.base import * # noqa analysis:ignore


class quantites_diesel(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantités de diesel consommées par les ménages"

    def formula(self, simulation, period):
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        quantites_diesel = depenses_diesel / diesel_ttc * 100

        return quantites_diesel


class quantites_sp_e10(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantités consommées de sans plomb e10 par les ménages"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10 = depenses_essence * part_sp_e10
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        quantite_sp_e10 = depenses_sp_e10 / super_95_e10_ttc * 100

        return quantite_sp_e10


class quantites_sp95(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantités consommées de sans plomb 95 par les ménages"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp95 = depenses_essence * part_sp95
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        quantite_sp95 = depenses_sp95 / super_95_ttc * 100

        return quantite_sp95


class quantites_sp98(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantités consommées de sans plomb 98 par les ménages"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp98 = depenses_essence * part_sp98
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        quantites_sp98 = depenses_sp98 / super_98_ttc * 100

        return quantites_sp98


class quantites_super_plombe(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantités consommées de super plombé par les ménages"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe = depenses_essence * part_super_plombe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        quantite_super_plombe = depenses_super_plombe / super_plombe_ttc * 100

        return quantite_super_plombe


class quantites_essence(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantités d'essence consommées par les ménages"

    def formula_1990(self, simulation, period):
        quantites_sp95 = simulation.calculate('quantites_sp95', period)
        quantites_sp98 = simulation.calculate('quantites_sp98', period)
        quantites_super_plombe = simulation.calculate('quantites_super_plombe', period)
        quantites_essence = (quantites_sp95 + quantites_sp98 + quantites_super_plombe)
        return quantites_essence

    def formula_2007(self, simulation, period):

        quantites_sp95 = simulation.calculate('quantites_sp95', period)
        quantites_sp98 = simulation.calculate('quantites_sp98', period)
        quantites_essence = (quantites_sp95 + quantites_sp98)
        return quantites_essence

    def formula_2009(self, simulation, period):
        quantites_sp95 = simulation.calculate('quantites_sp95', period)
        quantites_sp98 = simulation.calculate('quantites_sp98', period)
        quantites_sp_e10 = simulation.calculate('quantites_sp_e10', period)
        quantites_essence = (quantites_sp95 + quantites_sp98 + quantites_sp_e10)
        return quantites_essence


# Not used
class quantites_electricite_3kva(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 3 kva"

    def formula(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_3_kva
        depenses_elect = simulation.calculate('poste_04_5_1_1_1_a', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_3_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


# Not used
class quantites_electricite_6kva(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 6 kva"

    def formula(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_6_kva
        depenses_elect = simulation.calculate('poste_04_5_1_1_1_a', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


# Not used
class quantites_electricite_9kva(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 9 kva"

    def formula(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_9_kva
        depenses_elect = simulation.calculate('poste_04_5_1_1_1_a', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


# Not used
class quantites_electricite_12kva(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 12 kva"

    def formula(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_12_kva
        depenses_elect = simulation.calculate('poste_04_5_1_1_1_a', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


# Not used
class quantites_electricite_15kva(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 15 kva"

    def formula(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_15_kva
        depenses_elect = simulation.calculate('poste_04_5_1_1_1_a', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


# Not used
class quantites_electricite_18kva(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 18 kva"

    def formula(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_18_kva
        depenses_elect = simulation.calculate('poste_04_5_1_1_1_a', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return quantite_elect


class quantites_gaz_contrat_base(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat de base"

    def formula(self, simulation, period):
        tarif_fixe_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.base_0_1000
        depenses_gaz = simulation.calculate('poste_04_5_2_1_1', period)
        depenses_sans_part_fixe = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_base_ttc
        quantite_gaz = depenses_sans_part_fixe / prix_unitaire_gaz

        return quantite_gaz


class quantites_gaz_contrat_b0(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat b0"

    def formula(self, simulation, period):
        tarif_fixe_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b0_1000_6000
        depenses_gaz = simulation.calculate('poste_04_5_2_1_1', period)
        depenses_sans_part_fixe = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b0_ttc
        quantite_gaz = depenses_sans_part_fixe / prix_unitaire_gaz

        return quantite_gaz


class quantites_gaz_contrat_b1(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat b1"

    def formula(self, simulation, period):
        tarif_fixe_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b1_6_30000
        depenses_gaz = simulation.calculate('poste_04_5_2_1_1', period)
        depenses_sans_part_fixe = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b1_ttc
        quantite_gaz = depenses_sans_part_fixe / prix_unitaire_gaz

        return quantite_gaz


class quantites_gaz_contrat_b2i(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat b2i"

    def formula(self, simulation, period):
        tarif_fixe_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b2i_30000
        depenses_gaz = simulation.calculate('poste_04_5_2_1_1', period)
        depenses_gaz_variables = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b2i_ttc
        quantite_gaz = depenses_gaz_variables / prix_unitaire_gaz

        return quantite_gaz


class quantites_gaz_contrat_optimal(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au meilleur contrat"

    def formula(self, simulation, period):
        quantite_base = simulation.calculate('quantites_gaz_contrat_base', period)
        quantite_b0 = simulation.calculate('quantites_gaz_contrat_b0', period)
        quantite_b1 = simulation.calculate('quantites_gaz_contrat_b1', period)
        quantite_b2i = simulation.calculate('quantites_gaz_contrat_b2i', period)
        quantite_optimale_base_b0 = numpy.maximum(quantite_base, quantite_b0)
        quantite_optimale_base_b1 = numpy.maximum(quantite_optimale_base_b0, quantite_b1)
        quantite_optimale_base_b2i = numpy.maximum(quantite_optimale_base_b1, quantite_b2i)
        quantite_optimale = numpy.maximum(quantite_optimale_base_b2i, 0)

        return quantite_optimale


class quantites_electricite_selon_compteur(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantité d'électricité (en kWh) consommée par les ménages d'après le compteur imputé"

    def formula(self, simulation, period):
        depenses_electricite_variables = simulation.calculate('depenses_electricite_variables', period)
        depenses_electricite_prix_unitaire = simulation.calculate('depenses_electricite_prix_unitaire', period)
        quantites_electricite_selon_compteur = depenses_electricite_variables / depenses_electricite_prix_unitaire
        quantites_electricite_selon_compteur = numpy.maximum(quantites_electricite_selon_compteur, 0)

        return quantites_electricite_selon_compteur


class quantites_combustibles_liquides(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantité de combustibles solides (en litres) consommée par les ménages"

    def formula(self, simulation, period):
        depenses_combustibles_liquides = simulation.calculate('depenses_combustibles_liquides', period)
        prix_combustibles_liquides = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
        
        quantite_combustibles_liquides = depenses_combustibles_liquides / prix_combustibles_liquides
        
        return quantite_combustibles_liquides
