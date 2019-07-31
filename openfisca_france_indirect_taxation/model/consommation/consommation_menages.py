# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class depenses_assurance_sante(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en assurances liées aux transports"

    def formula(menage, period):
        depenses_assurance_sante = menage('poste_12_5_3_1_1', period)
        return depenses_assurance_sante


class depenses_assurance_transport(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en assurances liées aux transports"

    def formula(menage, period):
        depenses_assurance_transport = menage('poste_12_5_4_1_1', period)
        return depenses_assurance_transport


class depenses_autres_assurances(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en assurances liées aux transports"

    def formula(menage, period):
        depenses_assurance_vie_deces = menage('poste_12_5_1_1_1', period)
        depenses_assurance_logement = menage('poste_12_5_2_1_1', period)
        depenses_assurance_reste = menage('poste_12_5_5_1_1', period)

        depenses_assurance_autres = \
            depenses_assurance_vie_deces + depenses_assurance_logement + depenses_assurance_reste

        return depenses_assurance_autres


class depenses_ticpe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Consommation de carburants"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        returnmenage('depenses_ht_ticpe', period) * (1 + taux_plein_tva)
        # This is equivalent to call directly poste_07_2_2_1_1


class depenses_essence_recalculees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en essence recalculées à partir du prix ht"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        depenses_sp_e10_ht = menage('depenses_sp_e10_ht', period)
        depenses_sp_95_ht = menage('depenses_sp_95_ht', period)
        depenses_sp_98_ht = menage('depenses_sp_98_ht', period)
        depenses_super_plombe_ht = menage('depenses_super_plombe_ht', period)


class depenses_tot(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Somme des dépenses du ménage"

    def formula(menage, period):
        postes_agreges = ['poste_agrege_{}'.format(index) for index in
            ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12"]
            ]
        depenses_tot = 0
        for poste in postes_agreges:
            depenses_tot += menage('{}'.format(poste), period)

        return depenses_tot


class depenses_totales(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Consommation totale du ménage"

    def formula(menage, period):
        depenses_tva_taux_super_reduit = menage('depenses_tva_taux_super_reduit', period)
        depenses_tva_taux_reduit = menage('depenses_tva_taux_reduit', period)
        depenses_tva_taux_intermediaire = menage('depenses_tva_taux_intermediaire', period)
        depenses_tva_taux_plein = menage('depenses_tva_taux_plein', period)
        return (
            depenses_tva_taux_super_reduit +
            depenses_tva_taux_reduit +
            depenses_tva_taux_intermediaire +
            depenses_tva_taux_plein
            )


class distance(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Distance annuelle parcourue imputée de l'ENTD"


class distance_routiere_hebdomadaire_teg(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Distance routière parcourue par le ménage pour se rendre à son teg par semaine"


class duree_moyenne_trajet_aller_retour_teg(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Durée moyenne de l'aller-retour pour le teg"


class quantite_diesel(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantité de diesel consommée (en hecto-litres)"


class quantite_supercarburants(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Quantité de supercarburants (super 95, super98 et superE10) consommée (en hecto-litres)"


class somme_coicop12(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Somme des postes coicop12"

    def formula(menage, period):
        return sum(
            menage('coicop12_{}'.format(idx), period)
            for idx in range(1, 13)
            )


class somme_coicop12_conso(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Somme des postes coicop12 de 1 à 8"

    def formula(menage, period):
        return sum(
            menage('coicop12_{}'.format(idx), period)
            for idx in range(1, 9)
            )
