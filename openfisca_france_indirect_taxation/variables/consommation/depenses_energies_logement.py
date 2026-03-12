# -*- coding: utf-8 -*-

import logging
import numpy
from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore

log = logging.getLogger(__name__)


class depenses_combustibles_liquides(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Dépenses en combustibles liquides'

    def formula(menage, period):
        depenses_combustibles_liquides = menage('poste_04_5_3_1', period)

        return depenses_combustibles_liquides


class depenses_combustibles_solides(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Dépenses en combustibles solides'

    def formula(menage, period):
        depenses_combustibles_solides = menage('poste_04_5_4_1', period)
        return depenses_combustibles_solides


class depenses_electricite(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Dépenses en électricité totale après imputation factures jointes'

    def formula(menage, period):
        depenses_electricite = menage('poste_04_5_1_1', period)

        return depenses_electricite


class depenses_electricite_percentile(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Classement par percentile des dépenses d'électricité"

    def formula(menage, period):
        depenses_electricite = menage('depenses_electricite', period)
        depenses_electricite_rank = depenses_electricite.argsort().argsort()
        depenses_electricite_percentile = depenses_electricite_rank / len(depenses_electricite_rank) * 100

        return depenses_electricite_percentile


class depenses_electricite_prix_unitaire(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Prix unitaire de l'électricité de chaque ménage, après affectation d'un compteur"

    def formula(menage, period, parameters):
        depenses_electricite_percentile = menage('depenses_electricite_percentile', period)

        # Note : les barèmes ne donnent que les prix unitaires pour 3 et 6 kva. Pour les puissances supérieures,
        # les valeurs sont assez proches de celles du compteur 6kva que nous utilisons comme proxy.
        prix_unitaire_3kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.prix_unitaire_base_edf_ttc.prix_kwh_3_kva
        prix_unitaire_6kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.prix_unitaire_base_edf_ttc.prix_kwh_6_kva

        prix_unitaire = (
            (depenses_electricite_percentile < 4) * prix_unitaire_3kva
            + (depenses_electricite_percentile > 4) * prix_unitaire_6kva
            )

        return prix_unitaire


class depenses_electricite_tarif_fixe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en électricité des ménages sur le coût fixe de l'abonnement, après affectation d'un compteur"

    def formula(menage, period, parameters):
        depenses_electricite_percentile = menage('depenses_electricite_percentile', period)

        tarif_fixe_3kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_3_kva
        tarif_fixe_6kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_6_kva
        tarif_fixe_9kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_9_kva
        tarif_fixe_12kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_12_kva
        tarif_fixe_15kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_15_kva

        tarif_fixe = (
            (depenses_electricite_percentile < 4) * tarif_fixe_3kva
            + (depenses_electricite_percentile > 4) * (depenses_electricite_percentile < 52) * tarif_fixe_6kva
            + (depenses_electricite_percentile > 52) * (depenses_electricite_percentile < 78) * tarif_fixe_9kva
            + (depenses_electricite_percentile > 78) * (depenses_electricite_percentile < 88) * tarif_fixe_12kva
            + (depenses_electricite_percentile > 88) * tarif_fixe_15kva
            )

        return tarif_fixe


class depenses_electricite_variables(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en électricité des ménages, hors coût fixe de l'abonnement"

    def formula(menage, period):
        depenses_electricite = menage('depenses_electricite', period)
        depenses_electricite_tarif_fixe = menage('depenses_electricite_tarif_fixe', period)
        depenses_electricite_variables = depenses_electricite - depenses_electricite_tarif_fixe
        depenses_electricite_variables = numpy.maximum(depenses_electricite_variables, 0)

        return depenses_electricite_variables


class depenses_energies_logement(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Dépenses en électricité sans inclure dépenses jointes avec le gaz'

    def formula(menage, period):
        depenses_electricite = menage('depenses_electricite', period)
        depenses_gaz_ville = menage('depenses_gaz_ville', period)
        depenses_gaz_liquefie = menage('depenses_gaz_liquefie', period)
        depenses_combustibles_liquides = menage('depenses_combustibles_liquides', period)
        depenses_combustibles_solides = menage('depenses_combustibles_solides', period)
        depenses_energie_thermique = menage('depenses_energie_thermique', period)
        depenses_energies_logement = (
            depenses_electricite + depenses_gaz_ville + depenses_gaz_liquefie + depenses_combustibles_liquides
            + depenses_combustibles_solides + depenses_energie_thermique
            )

        return depenses_energies_logement


class depenses_energie_thermique(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Dépenses en énergie thermique'

    def formula(menage, period):
        depenses_energie_thermique = menage('poste_04_5_5_1_1', period)

        return depenses_energie_thermique


class depenses_energies_totales(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Dépenses en électricité sans inclure dépenses jointes avec le gaz'

    def formula(menage, period):
        depenses_energies_logement = menage('depenses_energies_logement', period)
        depenses_carburants = menage('depenses_carburants', period)
        depenses_energies_totales = (
            depenses_energies_logement + depenses_carburants
            )

        return depenses_energies_totales


class depenses_gaz_liquefie(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Dépenses en gaz liquéfié'

    def formula(menage, period):
        depenses_gaz_liquefie = menage('poste_04_5_2_2_1', period)

        return depenses_gaz_liquefie


class depenses_gaz_prix_unitaire(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Prix unitaire du gaz rencontré par les ménages'

    def formula(menage, period, parameters):
        quantite_base = menage('quantites_gaz_contrat_base', period)
        quantite_b0 = menage('quantites_gaz_contrat_b0', period)
        quantite_b1 = menage('quantites_gaz_contrat_b1', period)
        quantite_b2i = menage('quantites_gaz_contrat_b2i', period)
        quantite_optimale = menage('quantites_gaz_contrat_optimal', period)

        prix_unitaire_base = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_base_ttc
        prix_unitaire_b0 = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_b0_ttc
        prix_unitaire_b1 = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_b1_ttc
        prix_unitaire_b2i = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_b2i_ttc

        prix_unitaire_optimal = (
            (quantite_base == quantite_optimale) * prix_unitaire_base
            + (quantite_b0 == quantite_optimale) * prix_unitaire_b0
            + (quantite_b1 == quantite_optimale) * prix_unitaire_b1
            + (quantite_b2i == quantite_optimale) * (quantite_b1 != quantite_optimale) * prix_unitaire_b2i
            )

        return prix_unitaire_optimal


class depenses_gaz_ville(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Dépenses en gaz de ville'

    def formula(menage, period):
        depenses_gaz_ville = menage('poste_04_5_2_1', period)

        return depenses_gaz_ville


class depenses_gaz_tarif_fixe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en gaz des ménages sur le coût fixe de l'abonnement"

    def formula(menage, period, parameters):
        quantite_base = menage('quantites_gaz_contrat_base', period)
        quantite_b0 = menage('quantites_gaz_contrat_b0', period)
        quantite_b1 = menage('quantites_gaz_contrat_b1', period)
        quantite_b2i = menage('quantites_gaz_contrat_b2i', period)
        quantite_optimale = menage('quantites_gaz_contrat_optimal', period)

        tarif_fixe_base = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.base_0_1000
        tarif_fixe_b0 = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.b0_1000_6000
        tarif_fixe_b1 = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.b1_6_30000
        tarif_fixe_b2i = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.b2i_30000

        tarif_fixe_optimal = (
            (quantite_base == quantite_optimale) * tarif_fixe_base
            + (quantite_b0 == quantite_optimale) * tarif_fixe_b0
            + (quantite_b1 == quantite_optimale) * tarif_fixe_b1
            + (quantite_b2i == quantite_optimale) * (quantite_b1 != quantite_optimale) * tarif_fixe_b2i
            )

        return tarif_fixe_optimal


class depenses_gaz_variables(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en gaz des ménages, hors coût fixe de l'abonnement"

    def formula(menage, period):
        depenses_gaz = menage('depenses_gaz_ville', period)
        tarif_fixe = menage('depenses_gaz_tarif_fixe', period)

        depenses_gaz_variables = depenses_gaz - tarif_fixe
        depenses_gaz_variables = numpy.maximum(depenses_gaz_variables, 0)

        return depenses_gaz_variables


class combustibles_liquides(YearlyVariable):
    value_type = float
    entity = Menage
    label = '=1 si le ménage consomme des combustibles liquides'

    def formula(menage, period):
        depenses_combustibles_liquides = menage('depenses_combustibles_liquides', period)
        combustibles_liquides = 1 * (depenses_combustibles_liquides > 0)

        return combustibles_liquides


class electricite(YearlyVariable):
    value_type = float
    entity = Menage
    label = "=1 si le ménage consomme de l'électricité"

    def formula(menage, period):
        depenses_electricite = menage('depenses_electricite', period)
        electricite = 1 * (depenses_electricite > 0)

        return electricite


class gaz_ville(YearlyVariable):
    value_type = float
    entity = Menage
    label = '=1 si le ménage consomme du gaz'

    def formula(menage, period):
        depenses_gaz_ville = menage('depenses_gaz_ville', period)
        gaz_ville = 1 * (depenses_gaz_ville > 0)

        return gaz_ville
