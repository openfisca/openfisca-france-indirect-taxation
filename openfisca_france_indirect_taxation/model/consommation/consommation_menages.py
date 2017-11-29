# -*- coding: utf-8 -*-


from __future__ import division


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class depenses_assurance_sante(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en assurances liées aux transports"

    def formula(self, simulation, period):
        depenses_assurance_sante = simulation.calculate('poste_12_5_3_1_1', period)
        return depenses_assurance_sante


class depenses_assurance_transport(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en assurances liées aux transports"

    def formula(self, simulation, period):
        depenses_assurance_transport = simulation.calculate('poste_12_5_4_1_1', period)
        return depenses_assurance_transport


class depenses_autres_assurances(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en assurances liées aux transports"

    def formula(self, simulation, period):
        depenses_assurance_vie_deces = simulation.calculate('poste_12_5_1_1_1', period)
        depenses_assurance_logement = simulation.calculate('poste_12_5_2_1_1', period)
        depenses_assurance_reste = simulation.calculate('poste_12_5_5_1_1', period)

        depenses_assurance_autres = \
            depenses_assurance_vie_deces + depenses_assurance_logement + depenses_assurance_reste

        return depenses_assurance_autres


class depenses_ticpe(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Consommation de carburants"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return simulation.calculate('depenses_ht_ticpe', period) * (1 + taux_plein_tva)
        # This is equivalent to call directly poste_07_2_2_1_1

class depenses_essence_recalculees(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en essence recalculées à partir du prix ht"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_sp_e10_ht = simulation.calculate('depenses_sp_e10_ht', period)
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_super_plombe_ht = simulation.calculate('depenses_super_plombe_ht', period)


class depenses_tot(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Somme des dépenses du ménage"

    def formula(self, simulation, period):
        postes_agreges = ['poste_agrege_{}'.format(index) for index in
            ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12"]
            ]
        depenses_tot = 0
        for poste in postes_agreges:
            depenses_tot += simulation.calculate('{}'.format(poste), period)

        return depenses_tot


class depenses_totales(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Consommation totale du ménage"

    def formula(self, simulation, period):
        depenses_tva_taux_super_reduit = simulation.calculate('depenses_tva_taux_super_reduit', period)
        depenses_tva_taux_reduit = simulation.calculate('depenses_tva_taux_reduit', period)
        depenses_tva_taux_intermediaire = simulation.calculate('depenses_tva_taux_intermediaire', period)
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        return (
            depenses_tva_taux_super_reduit +
            depenses_tva_taux_reduit +
            depenses_tva_taux_intermediaire +
            depenses_tva_taux_plein
            )


class distance_routiere_hebdomadaire_teg(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Distance routière parcourue par le ménage pour se rendre à son teg par semaine"


class duree_moyenne_trajet_aller_retour_teg(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Durée moyenne de l'aller-retour pour le teg"


class quantite_diesel(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantité de diesel consommée (en hecto-litres)"


class quantite_supercarburants(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Quantité de supercarburants (super 95, super98 et superE10) consommée (en hecto-litres)"


class somme_coicop12(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Somme des postes coicop12"

    def formula(self, simulation, period):
        return sum(
            simulation.calculate('coicop12_{}'.format(idx), period)
            for idx in xrange(1, 13)
            )


class somme_coicop12_conso(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Somme des postes coicop12 de 1 à 8"

    def formula(self, simulation, period):
        return sum(
            simulation.calculate('coicop12_{}'.format(idx), period)
            for idx in xrange(1, 9)
            )
