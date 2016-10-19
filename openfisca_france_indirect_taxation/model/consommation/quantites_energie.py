# -*- coding: utf-8 -*-

from __future__ import division


from datetime import date
import numpy

from openfisca_france_indirect_taxation.model.base import *


class quantites_diesel(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités de diesel consommées par les ménages"

    def function(self, simulation, period):
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        quantites_diesel = depenses_diesel / diesel_ttc * 100

        return period, quantites_diesel


class quantites_sp_e10(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb e10 par les ménages"

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10 = depenses_essence * part_sp_e10
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        quantite_sp_e10 = depenses_sp_e10 / super_95_e10_ttc * 100

        return period, quantite_sp_e10


class quantites_sp95(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb 95 par les ménages"

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp95 = depenses_essence * part_sp95
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        quantite_sp95 = depenses_sp95 / super_95_ttc * 100

        return period, quantite_sp95


class quantites_sp98(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb 98 par les ménages"

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp98 = depenses_essence * part_sp98
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        quantites_sp98 = depenses_sp98 / super_98_ttc * 100

        return period, quantites_sp98


class quantites_super_plombe(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de super plombé par les ménages"

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe = depenses_essence * part_super_plombe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        quantite_super_plombe = depenses_super_plombe / super_plombe_ttc * 100

        return period, quantite_super_plombe


class quantites_essence(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités d'essence consommées par les ménages"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        quantites_sp95 = simulation.calculate('quantites_sp95', period)
        quantites_sp98 = simulation.calculate('quantites_sp98', period)
        quantites_super_plombe = simulation.calculate('quantites_super_plombe', period)
        quantites_essence = (quantites_sp95 + quantites_sp98 + quantites_super_plombe)
        return period, quantites_essence

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        quantites_sp95 = simulation.calculate('quantites_sp95', period)
        quantites_sp98 = simulation.calculate('quantites_sp98', period)
        quantites_essence = (quantites_sp95 + quantites_sp98)
        return period, quantites_essence

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        quantites_sp95 = simulation.calculate('quantites_sp95', period)
        quantites_sp98 = simulation.calculate('quantites_sp98', period)
        quantites_sp_e10 = simulation.calculate('quantites_sp_e10', period)
        quantites_essence = (quantites_sp95 + quantites_sp98 + quantites_sp_e10)
        return period, quantites_essence


class quantites_electricite_3kva(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 3 kva"

    def function(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_3_kva
        depenses_elect = simulation.calculate('poste_coicop_451', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_3_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return period, quantite_elect


class quantites_electricite_6kva(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 6 kva"

    def function(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_6_kva
        depenses_elect = simulation.calculate('poste_coicop_451', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return period, quantite_elect


class quantites_electricite_9kva(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 9 kva"

    def function(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_9_kva
        depenses_elect = simulation.calculate('poste_coicop_451', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return period, quantite_elect


class quantites_electricite_12kva(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 12 kva"

    def function(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_12_kva
        depenses_elect = simulation.calculate('poste_coicop_451', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return period, quantite_elect


class quantites_electricite_15kva(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 15 kva"

    def function(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_15_kva
        depenses_elect = simulation.calculate('poste_coicop_451', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return period, quantite_elect


class quantites_electricite_18kva(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantite d'électricité (en kWh) consommée par les ménages si leur compteur est de 18 kva"

    def function(self, simulation, period):
        tarif_fixe_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_18_kva
        depenses_elect = simulation.calculate('poste_coicop_451', period)
        depenses_sans_part_fixe = depenses_elect - tarif_fixe_elect
        prix_unitaire_elect = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva
        quantite_elect = depenses_sans_part_fixe / prix_unitaire_elect

        return period, quantite_elect


class quantites_gaz_contrat_base(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat de base"

    def function(self, simulation, period):
        tarif_fixe_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.base_0_1000
        depenses_gaz = simulation.calculate('poste_coicop_452', period)
        depenses_sans_part_fixe = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_base_ttc
        quantite_gaz = depenses_sans_part_fixe / prix_unitaire_gaz

        return period, quantite_gaz


class quantites_gaz_contrat_b0(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat b0"

    def function(self, simulation, period):
        tarif_fixe_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b0_1000_6000
        depenses_gaz = simulation.calculate('poste_coicop_452', period)
        depenses_sans_part_fixe = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b0_ttc
        quantite_gaz = depenses_sans_part_fixe / prix_unitaire_gaz

        return period, quantite_gaz


class quantites_gaz_contrat_b1(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat b1"

    def function(self, simulation, period):
        tarif_fixe_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b1_6_30000
        depenses_gaz = simulation.calculate('poste_coicop_452', period)
        depenses_sans_part_fixe = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b1_ttc
        quantite_gaz = depenses_sans_part_fixe / prix_unitaire_gaz

        return period, quantite_gaz


class quantites_gaz_contrat_b2i(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au contrat b2i"

    def function(self, simulation, period):
        tarif_fixe_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b2i_30000
        depenses_gaz = simulation.calculate('poste_coicop_452', period)
        depenses_gaz_variables = depenses_gaz - tarif_fixe_gaz
        prix_unitaire_gaz = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b2i_ttc
        quantite_gaz = depenses_gaz_variables / prix_unitaire_gaz

        return period, quantite_gaz


class quantites_gaz_contrat_optimal(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantité de gaz (en kWh) consommée par les ménages s'ils ont souscrit au meilleur contrat"

    def function(self, simulation, period):
        quantite_base = simulation.calculate('quantites_gaz_contrat_base', period)
        quantite_b0 = simulation.calculate('quantites_gaz_contrat_b0', period)
        quantite_b1 = simulation.calculate('quantites_gaz_contrat_b1', period)
        quantite_b2i = simulation.calculate('quantites_gaz_contrat_b2i', period)
        quantite_optimale_base_b0 = numpy.maximum(quantite_base, quantite_b0)
        quantite_optimale_base_b1 = numpy.maximum(quantite_optimale_base_b0, quantite_b1)
        quantite_optimale_base_b2i = numpy.maximum(quantite_optimale_base_b1, quantite_b2i)
        quantite_optimale = numpy.maximum(quantite_optimale_base_b2i, 0)

        return period, quantite_optimale


class quantites_electricite_selon_compteur(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantité d'électricité (en kWh) consommée par les ménages d'après le compteur imputé"

    def function(self, simulation, period):
        depenses_electricite_variables = simulation.calculate('depenses_electricite_variables', period)
        depenses_electricite_prix_unitaire = simulation.calculate('depenses_electricite_prix_unitaire', period)
        quantites_electricite_selon_compteur = depenses_electricite_variables / depenses_electricite_prix_unitaire
        quantites_electricite_selon_compteur = numpy.maximum(quantites_electricite_selon_compteur, 0)

        return period, quantites_electricite_selon_compteur


class quantites_fioul_domestique(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantité de fuel domestique consommée par les ménages, en litres"

    def function(self, simulation, period):
        depenses_fioul = simulation.calculate('poste_coicop_453', period)
        prix_fioul_ttc = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
        quantites_fioul = depenses_fioul / prix_fioul_ttc

        return period, quantites_fioul
