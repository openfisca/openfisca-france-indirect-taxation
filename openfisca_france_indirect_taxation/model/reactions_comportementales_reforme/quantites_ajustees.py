# -*- coding: utf-8 -*-

from __future__ import division


from datetime import date

from ..base import * # noqa analysis:ignore


class quantites_diesel_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités de diesel consommées après la réforme - contribution climat énergie, hausse de 2014 à 2015"

    def function(self, simulation, period):
        depenses_diesel_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_diesel_ajustees_cce_2014_2015', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = simulation.legislation_at(period.start).contribution_climat_energie_reforme.diesel_2014_2015
        quantites_diesel_ajustees = depenses_diesel_ajustees_cce_2014_2015 / (diesel_ttc + reforme_diesel) * 100

        return period, quantites_diesel_ajustees


class quantites_diesel_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités de diesel consommées après la réforme - contribution climat énergie, hausse de 2014 à 2016"

    def function(self, simulation, period):
        depenses_diesel_ajustees_cce_2014_2016 = \
            simulation.calculate('depenses_diesel_ajustees_cce_2014_2016', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = simulation.legislation_at(period.start).contribution_climat_energie_reforme.diesel_2014_2016
        quantites_diesel_ajustees = depenses_diesel_ajustees_cce_2014_2016 / (diesel_ttc + reforme_diesel) * 100

        return period, quantites_diesel_ajustees


class quantites_diesel_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités de diesel consommées après la réforme - taxe carbone "

    def function(self, simulation, period):
        depenses_diesel_ajustees_taxe_carbone = \
            simulation.calculate('depenses_diesel_ajustees_taxe_carbone', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = simulation.legislation_at(period.start).taxe_carbone.diesel
        quantites_diesel_ajustees = depenses_diesel_ajustees_taxe_carbone / (diesel_ttc + reforme_diesel) * 100

        return period, quantites_diesel_ajustees


class quantites_diesel_ajustees_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités de diesel consommées après la réforme - taxe carburants"

    def function(self, simulation, period):
        depenses_diesel_ajustees_taxes_carburants = \
            simulation.calculate('depenses_diesel_ajustees_taxes_carburants', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = simulation.legislation_at(period.start).taxes_carburants.diesel
        quantites_diesel_ajustees = depenses_diesel_ajustees_taxes_carburants / (diesel_ttc + reforme_diesel) * 100

        return period, quantites_diesel_ajustees


class quantites_fioul_domestique_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités de fioul consommées après la réforme - contribution climat énergie, hausse de 2014 à 2015 "

    def function(self, simulation, period):
        depenses_fioul_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_fioul_domestique_ajustees_cce_2014_2015', period)
        prix_fioul_ttc = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
        reforme_fioul = \
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.fioul_domestique_2014_2015
        quantites_fioul_ajustees = depenses_fioul_ajustees_cce_2014_2015 / (prix_fioul_ttc + reforme_fioul)

        return period, quantites_fioul_ajustees


class quantites_fioul_domestique_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités de fioul consommées après la réforme - contribution climat énergie, hausse de 2014 à 2016 "

    def function(self, simulation, period):
        depenses_fioul_ajustees_cce_2014_2016 = \
            simulation.calculate('depenses_fioul_domestique_ajustees_cce_2014_2016', period)
        prix_fioul_ttc = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
        reforme_fioul = \
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.fioul_domestique_2014_2016
        quantites_fioul_ajustees = depenses_fioul_ajustees_cce_2014_2016 / (prix_fioul_ttc + reforme_fioul)

        return period, quantites_fioul_ajustees


class quantites_fioul_domestique_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités de fioul domestique consommées après la réforme - taxe carbone "

    def function(self, simulation, period):
        depenses_fioul_ajustees_taxe_carbone = \
            simulation.calculate('depenses_fioul_domestique_ajustees_taxe_carbone', period)
        prix_fioul_ttc = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
        reforme_fioul = simulation.legislation_at(period.start).taxe_carbone.fioul_domestique
        quantites_fioul_ajustees = depenses_fioul_ajustees_taxe_carbone / (prix_fioul_ttc + reforme_fioul)

        return period, quantites_fioul_ajustees


class quantites_gaz_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités de gaz consommées après la réforme - contribution climat énergie, hausse de 2014 à 2015"

    def function(self, simulation, period):
        depenses_gaz_ajustees_cce_2014_2015 = simulation.calculate('depenses_gaz_ajustees_cce_2014_2015', period)
        depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
        depenses_gaz_ajustees_variables = depenses_gaz_ajustees_cce_2014_2015 - depenses_gaz_tarif_fixe

        depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
        reforme_gaz = \
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.gaz_2014_2015

        quantites_gaz_ajustees = depenses_gaz_ajustees_variables / (depenses_gaz_prix_unitaire + reforme_gaz)

        return period, quantites_gaz_ajustees


class quantites_gaz_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités de gaz consommées après la réforme - contribution climat énergie, hausse de 2014 à 2016"

    def function(self, simulation, period):
        depenses_gaz_ajustees_cce_2014_2016 = simulation.calculate('depenses_gaz_ajustees_cce_2014_2016', period)
        depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
        depenses_gaz_ajustees_variables = depenses_gaz_ajustees_cce_2014_2016 - depenses_gaz_tarif_fixe

        depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
        reforme_gaz = \
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.gaz_2014_2016

        quantites_gaz_ajustees = depenses_gaz_ajustees_variables / (depenses_gaz_prix_unitaire + reforme_gaz)

        return period, quantites_gaz_ajustees


class quantites_gaz_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités de gaz consommées après la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_gaz_ajustees_taxe_carbone = simulation.calculate('depenses_gaz_ajustees_taxe_carbone', period)
        depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
        depenses_gaz_ajustees_variables = depenses_gaz_ajustees_taxe_carbone - depenses_gaz_tarif_fixe

        depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
        reforme_gaz = simulation.legislation_at(period.start).taxe_carbone.gaz

        quantites_gaz_ajustees = depenses_gaz_ajustees_variables / (depenses_gaz_prix_unitaire + reforme_gaz)

        return period, quantites_gaz_ajustees


class quantites_electricite_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités d'électricité consommées après la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_electricite_ajustees_taxe_carbone = \
            simulation.calculate('depenses_electricite_ajustees_taxe_carbone', period)
        depenses_electricite_tarif_fixe = simulation.calculate('depenses_electricite_tarif_fixe', period)
        depenses_electricite_ajustees_variables = \
            depenses_electricite_ajustees_taxe_carbone - depenses_electricite_tarif_fixe

        depenses_electricite_prix_unitaire = simulation.calculate('depenses_electricite_prix_unitaire', period)
        reforme_electricite = simulation.legislation_at(period.start).taxe_carbone.electricite

        quantites_electricite_ajustees = \
            depenses_electricite_ajustees_variables / (depenses_electricite_prix_unitaire + reforme_electricite)

        quantites_electricite_avant_reforme = simulation.calculate('quantites_electricite_selon_compteur', period)
        quantites_electricite_ajustees = (
            quantites_electricite_ajustees * (quantites_electricite_avant_reforme > 0)
            )

        return period, quantites_electricite_ajustees


class quantites_sp_e10_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb e10 par les ménages après réforme - hausse cce 2014-2015"

    def function(self, simulation, period):
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_sp_e10
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

        return period, quantite_sp_e10


class quantites_sp_e10_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb e10 par les ménages après réforme - hausse cce 2014-2016"

    def function(self, simulation, period):
        depenses_essence_ajustees_cce_2014_2016 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2016', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10_ajustees = depenses_essence_ajustees_cce_2014_2016 * part_sp_e10
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2016
        quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

        return period, quantite_sp_e10


class quantites_sp_e10_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb e10 par les ménages après réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp_e10
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

        return period, quantite_sp_e10


class quantites_sp_e10_ajustees_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb e10 par les ménages après réforme - taxe carburants"

    def function(self, simulation, period):
        depenses_essence_ajustees_taxes_carburants = \
            simulation.calculate('depenses_essence_ajustees_taxes_carburants', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10_ajustees = depenses_essence_ajustees_taxes_carburants * part_sp_e10
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

        return period, quantite_sp_e10


class quantites_sp95_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb 95 par les ménages après réforme - hausse cce 2014-2015"

    def function(self, simulation, period):
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp95_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_sp95
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

        return period, quantites_sp95_ajustees


class quantites_sp95_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb 95 par les ménages après réforme - hausse cce 2014-2016"

    def function(self, simulation, period):
        depenses_essence_ajustees_cce_2014_2016 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2016', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp95_ajustees = depenses_essence_ajustees_cce_2014_2016 * part_sp95
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2016
        quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

        return period, quantites_sp95_ajustees


class quantites_sp95_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb 95 par les ménages après réforme"

    def function(self, simulation, period):
        depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp95_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp95
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

        return period, quantites_sp95_ajustees


class quantites_sp95_ajustees_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb 95 par les ménages après réforme"

    def function(self, simulation, period):
        depenses_essence_ajustees_taxes_carburants = simulation.calculate('depenses_essence_ajustees_taxes_carburants', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp95_ajustees = depenses_essence_ajustees_taxes_carburants * part_sp95
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

        return period, quantites_sp95_ajustees


class quantites_sp98_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb 98 par les ménages - hausse cce 2014-2015"

    def function(self, simulation, period):
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp98_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_sp98
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

        return period, quantites_sp98_ajustees


class quantites_sp98_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb 98 par les ménages - hausse cce 2014-2016"

    def function(self, simulation, period):
        depenses_essence_ajustees_cce_2014_2016 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2016', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp98_ajustees = depenses_essence_ajustees_cce_2014_2016 * part_sp98
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2016
        quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

        return period, quantites_sp98_ajustees


class quantites_sp98_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb 98 par les ménages"

    def function(self, simulation, period):
        depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp98_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp98
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

        return period, quantites_sp98_ajustees


class quantites_sp98_ajustees_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de sans plomb 98 par les ménages"

    def function(self, simulation, period):
        depenses_essence_ajustees_taxes_carburants = simulation.calculate('depenses_essence_ajustees_taxes_carburants', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp98_ajustees = depenses_essence_ajustees_taxes_carburants * part_sp98
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

        return period, quantites_sp98_ajustees


class quantites_super_plombe_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de super plombé par les ménages après réforme - hausse cce 2014-2015"

    def function(self, simulation, period):
        depenses_essence_ajustees_cce_2014_2015 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2015', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_cce_2014_2015 * part_super_plombe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2015
        quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

        return period, quantites_super_plombe_ajustees


class quantites_super_plombe_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de super plombé par les ménages après réforme - hausse cce 2014-2016"

    def function(self, simulation, period):
        depenses_essence_ajustees_cce_2014_2016 = \
            simulation.calculate('depenses_essence_ajustees_cce_2014_2016', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_cce_2014_2016 * part_super_plombe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        reforme_essence = simulation.legislation_at(period.start).contribution_climat_energie_reforme.essence_2014_2016
        quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

        return period, quantites_super_plombe_ajustees


class quantites_super_plombe_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de super plombé par les ménages après réforme"

    def function(self, simulation, period):
        depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_taxe_carbone * part_super_plombe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

        return period, quantites_super_plombe_ajustees


class quantites_super_plombe_ajustees_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités consommées de super plombé par les ménages après réforme"

    def function(self, simulation, period):
        depenses_essence_ajustees_taxes_carburants = simulation.calculate('depenses_essence_ajustees_taxes_carburants', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_taxes_carburants * part_super_plombe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        reforme_essence = simulation.legislation_at(period.start).taxes_carburants.essence
        quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

        return period, quantites_super_plombe_ajustees


class quantites_essence_ajustees_cce_2014_2015(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités d'essence consommées par les ménages après réforme - hausse cce 2014-2015"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_cce_2014_2015', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_cce_2014_2015', period)
        quantites_super_plombe_ajustees = \
            simulation.calculate('quantites_super_plombe_ajustees_cce_2014_2015', period)
        quantites_essence_ajustees = (
            quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
            )
        return period, quantites_essence_ajustees

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_cce_2014_2015', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_cce_2014_2015', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
        return period, quantites_essence_ajustees

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_cce_2014_2015', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_cce_2014_2015', period)
        quantites_sp_e10_ajustees = simulation.calculate('quantites_sp_e10_ajustees_cce_2014_2015', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
        return period, quantites_essence_ajustees


class quantites_essence_ajustees_cce_2014_2016(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités d'essence consommées par les ménages après réforme - hausse cce 2014-2016"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_cce_2014_2016', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_cce_2014_2016', period)
        quantites_super_plombe_ajustees = \
            simulation.calculate('quantites_super_plombe_ajustees_cce_2014_2016', period)
        quantites_essence_ajustees = (
            quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
            )
        return period, quantites_essence_ajustees

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_cce_2014_2016', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_cce_2014_2016', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
        return period, quantites_essence_ajustees

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_cce_2014_2016', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_cce_2014_2016', period)
        quantites_sp_e10_ajustees = simulation.calculate('quantites_sp_e10_ajustees_cce_2014_2016', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
        return period, quantites_essence_ajustees


class quantites_essence_ajustees_taxe_carbone(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités d'essence consommées par les ménages après réforme"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_taxe_carbone', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_taxe_carbone', period)
        quantites_super_plombe_ajustees = \
            simulation.calculate('quantites_super_plombe_ajustees_taxe_carbone', period)
        quantites_essence_ajustees = (
            quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
            )
        return period, quantites_essence_ajustees

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_taxe_carbone', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_taxe_carbone', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
        return period, quantites_essence_ajustees

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_taxe_carbone', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_taxe_carbone', period)
        quantites_sp_e10_ajustees = simulation.calculate('quantites_sp_e10_ajustees_taxe_carbone', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
        return period, quantites_essence_ajustees


class quantites_essence_ajustees_taxes_carburants(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Quantités d'essence consommées par les ménages après réforme"

    @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_taxes_carburants', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_taxes_carburants', period)
        quantites_super_plombe_ajustees = \
            simulation.calculate('quantites_super_plombe_ajustees_taxes_carburants', period)
        quantites_essence_ajustees = (
            quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
            )
        return period, quantites_essence_ajustees

    @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_taxes_carburants', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_taxes_carburants', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
        return period, quantites_essence_ajustees

    @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95_ajustees_taxes_carburants', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98_ajustees_taxes_carburants', period)
        quantites_sp_e10_ajustees = simulation.calculate('quantites_sp_e10_ajustees_taxes_carburants', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
        return period, quantites_essence_ajustees
