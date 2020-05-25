# -*- coding: utf-8 -*-


from openfisca_core.reforms import Reform
import numpy

from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore

# Montants de taxe prévus par la loi Contribution climat-énergie. 7€ en 2014, 14,5€ en 2015, 22€ en 2016,
# 30,5€ en 2017, 39€ en 2018 et 47.5€ en 2019 En utilisant nos données d'équivalence entre consommation et émission,
# on met en place les montants de taxe suivants :
# Dans cette réforme on suppose qu'on impute à la législation de 2014 une augmentation équivalente à ce qui est prévu
# par la loi pour les années à venir.


def modify_parameters(parameters):
    node = ParameterNode(
        "cce_2016_in_2014",
        data = {
            "description": "cce_2016_in_2014",
            "diesel_2014_2016": {
                "description": "Surcroît de prix du diesel (en euros par hectolitres)",
                # TODO "unit": '?',
                "unit": 'currency',
                "values": {'2014-01-01': 5.852 - 1.862}
                },
            "essence_2014_2016": {
                "description": "Surcroît de prix de l'essence (en euros par hectolitres)",
                "unit": 'currency',
                "values": {'2014-01-01': 5.324 - 1.694},
                },
            "combustibles_liquides_2014_2016": {
                "description": "Surcroît de prix du fioul domestique (en euros par litre)",
                "unit": 'currency',
                "values": {'2014-01-01': 0.0682 - 0.0217},
                },
            "gaz_2014_2016": {
                "description": "Surcroît de prix du gaz (en euros par kWh)",
                # TODO "unit": '?',
                "unit": 'currency',
                "values": {'2014-01-01': 0.00528 - 0.00168},
                },
            "abaissement_tva_taux_plein_2014_2016": {
                "description": "Baisse de la TVA à taux plein pour obtenir un budget constant",
                # TODO "unit": '?',
                "values": {'2010-01-01': 0.008},
                },
            "abaissement_tva_taux_plein_bis_2014_2016": {
                "description": "Baisse de la TVA à taux plein pour obtenir un budget constant",
                # TODO "unit": '?',
                "values": {'2010-01-01': 0.005},
                },
            "abaissement_tva_taux_reduit_2014_2016": {
                "description": "Baisse de la TVA à taux plein pour obtenir un budget constant",
                # TODO "unit": '?',
                "values": {'2010-01-01': 0.006},
                },
            "abaissement_tva_taux_super_reduit_2014_2016": {
                "description": "Baisse de la TVA à taux plein pour obtenir un budget constant",
                # TODO "unit": '?',
                "values": {'2010-01-01': 0.006},
                },
            },
        )
    parameters.add_child('cce_2016_in_2014', node)
    return parameters


class cce_2016_in_2014(Reform):
    key = 'cce_2016_in_2014',
    name = "Augmentation des taux de la contribution climat energie aux taux de 2016 sur les données de 2014",

    class cheques_energie(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des chèques énergie (indexés par uc) - taxe carbone"

        def formula(menage, period):
            contribution = menage('contributions_reforme', period)
            ocde10 = menage('ocde10', period)
            pondmen = menage('pondmen', period)

            somme_contributions = numpy.sum(contribution * pondmen)
            contribution_uc = somme_contributions / numpy.sum(ocde10 * pondmen)

            cheque = contribution_uc * ocde10

            return cheque

    class contributions_reforme(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Changement de contribution aux taxes énergétiques suite à la réforme - taxe carbone"

        def formula(menage, period):
            total_taxes_energies = menage('total_taxes_energies', period)
            total_taxes_energies_cce = menage('total_taxes_energies_cce_2016_in_2014', period)

            contribution = total_taxes_energies_cce - total_taxes_energies

            return contribution

    class depenses_carburants_corrigees_ajustees_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Depenses en carburants après reaction a la reforme - taxes carburants"

        def formula(menage, period):
            depenses_diesel_ajustees = menage('depenses_diesel_corrigees_ajustees_cce_2016_in_2014', period)
            depenses_essence_ajustees = menage('depenses_essence_corrigees_ajustees_cce_2016_in_2014', period)
            depenses_carburants_ajustees = depenses_diesel_ajustees + depenses_essence_ajustees

            return depenses_carburants_ajustees

    class depenses_diesel_corrigees_ajustees_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en diesel après réaction à la réforme - contribution climat énergie, hausse de 2014 à 2016"

        def formula(menage, period, parameters):
            depenses_diesel = menage('depenses_diesel', period)
            diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            reforme_diesel = parameters(period.start).cce_2016_in_2014.diesel_2014_2016
            carburants_elasticite_prix = menage('elas_price_1_1', period)
            depenses_diesel_ajustees_cce_2016_in_2014 = \
                depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

            return depenses_diesel_ajustees_cce_2016_in_2014

    class depenses_energies_logement_ajustees_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en électricité sans inclure dépenses jointes avec le gaz"

        def formula(menage, period, parameters):
            depenses_electricite_ajustees = menage('depenses_electricite', period)
            depenses_gaz_ville_ajustees = menage('depenses_gaz_ville_ajustees_cce_2016_in_2014', period)
            depenses_gaz_liquefie = menage('depenses_gaz_liquefie', period)
            depenses_combustibles_liquides_ajustees = menage('depenses_combustibles_liquides_ajustees_cce_2016_in_2014', period)
            depenses_combustibles_solides = menage('depenses_combustibles_solides', period)
            depenses_energie_thermique = menage('depenses_energie_thermique', period)
            depenses_energies_logement_ajustees_cce_2016_in_2014 = (
                depenses_electricite_ajustees + depenses_gaz_ville_ajustees + depenses_gaz_liquefie
                + depenses_combustibles_liquides_ajustees + depenses_combustibles_solides + depenses_energie_thermique
                )

            return depenses_energies_logement_ajustees_cce_2016_in_2014

    class depenses_essence_corrigees_ajustees_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en essence après réaction à la réforme - contribution climat énergie, hausse de 2014 à 2016"

        def formula(menage, period, parameters):
            depenses_essence = menage('depenses_essence', period)
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            reforme_essence = parameters(period.start).cce_2016_in_2014.essence_2014_2016
            carburants_elasticite_prix = menage('elas_price_1_1', period)
            depenses_essence_ajustees_cce_2016_in_2014 = \
                depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence / super_95_ttc)

            return depenses_essence_ajustees_cce_2016_in_2014

    class depenses_combustibles_liquides_ajustees_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en combustibles_liquides après réaction à la réforme - contribution climat énergie, hausse de 2014 à 2016"

        def formula(menage, period, parameters):
            depenses_combustibles_liquides = menage('depenses_combustibles_liquides', period)
            prix_fioul_ttc = \
                parameters(period.start).tarifs_energie.prix_fioul_domestique.prix_annuel_moyen_fioul_domestique_ttc_livraisons_2000_4999_litres_en_euro_par_litre
            reforme_combustibles_liquides = \
                parameters(period.start).cce_2016_in_2014.combustibles_liquides_2014_2016
            combustibles_liquides_elasticite_prix = menage('elas_price_2_2', period)
            depenses_combustibles_liquides_ajustees_cce_2016_in_2014 = \
                depenses_combustibles_liquides * (1 + (1 + combustibles_liquides_elasticite_prix) * reforme_combustibles_liquides / prix_fioul_ttc)

            return depenses_combustibles_liquides_ajustees_cce_2016_in_2014

    class depenses_gaz_ville_ajustees_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en gaz après réaction à la réforme - contribution climat énergie, hausse de 2014 à 2016"

        def formula(menage, period, parameters):
            depenses_gaz_variables = menage('depenses_gaz_variables', period)
            depenses_gaz_prix_unitaire = menage('depenses_gaz_prix_unitaire', period)
            reforme_gaz = \
                parameters(period.start).cce_2016_in_2014.gaz_2014_2016
            gaz_elasticite_prix = menage('elas_price_2_2', period)
            depenses_gaz_ajustees_variables = \
                depenses_gaz_variables * (1 + (1 + gaz_elasticite_prix) * reforme_gaz / depenses_gaz_prix_unitaire)
            depenses_gaz_tarif_fixe = menage('depenses_gaz_tarif_fixe', period)
            depenses_gaz_ajustees = depenses_gaz_ajustees_variables + depenses_gaz_tarif_fixe
            depenses_gaz_ajustees[numpy.isnan(depenses_gaz_ajustees)] = 0
            depenses_gaz_ajustees[numpy.isinf(depenses_gaz_ajustees)] = 0

            return depenses_gaz_ajustees

    class depenses_tva_taux_plein_ajustees_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses sur les biens assujetis à la TVA à taux plein après réaction à la réforme - cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_tva_taux_plein = menage('depenses_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein = (
                parameters(period.start).cce_2016_in_2014.abaissement_tva_taux_plein_2014_2016
                )
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_plein_ajustees = \
                depenses_tva_taux_plein * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))

            return depenses_tva_taux_plein_ajustees

    class depenses_tva_taux_plein_bis_ajustees_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses sur les biens assujetis à la TVA à taux plei bis après réaction à la réforme - cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_tva_taux_plein = menage('depenses_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein_bis = (
                parameters(period.start).cce_2016_in_2014.abaissement_tva_taux_plein_bis_2014_2016
                )
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_plein_bis_ajustees = (
                depenses_tva_taux_plein
                * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein_bis) / (1 + taux_plein))
                )

            return depenses_tva_taux_plein_bis_ajustees

    class depenses_tva_taux_reduit_ajustees_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses sur les biens assujetis à la TVA à taux reduit après réaction à la réforme - cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_tva_taux_reduit = menage('depenses_tva_taux_reduit', period)
            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            abaissement_tva_taux_reduit = (
                parameters(period.start).cce_2016_in_2014.abaissement_tva_taux_reduit_2014_2016
                )
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_reduit_ajustees = \
                depenses_tva_taux_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_reduit) / (1 + taux_reduit))

            return depenses_tva_taux_reduit_ajustees

    class depenses_tva_taux_super_reduit_ajustees_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses sur les biens assujetis à la TVA à taux super reduit après réaction à la réforme - cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_tva_taux_super_reduit = menage('depenses_tva_taux_super_reduit', period)
            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            abaissement_tva_taux_super_reduit = (
                parameters(period.start).cce_2016_in_2014.abaissement_tva_taux_super_reduit_2014_2016
                )
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_super_reduit_ajustees = \
                depenses_tva_taux_super_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_super_reduit) / (1 + taux_super_reduit))

            return depenses_tva_taux_super_reduit_ajustees

    class diesel_ticpe(YearlyVariable):
        label = "Calcul du montant de TICPE sur le diesel après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            try:
                majoration_ticpe_diesel = \
                    parameters(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
                accise_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole
                accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
            except Exception:
                accise_diesel_ticpe = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole

            reforme_diesel = parameters(period.start).cce_2016_in_2014.diesel_2014_2016
            accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
            prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
            taux_implicite_diesel_ajuste = (
                (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                / (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                )

            depenses_diesel_ajustees_cce_2016_in_2014 = \
                menage('depenses_diesel_corrigees_ajustees_cce_2016_in_2014', period)
            depenses_diesel_htva_ajustees = (
                depenses_diesel_ajustees_cce_2016_in_2014
                - tax_from_expense_including_tax(depenses_diesel_ajustees_cce_2016_in_2014, taux_plein_tva)
                )
            montant_diesel_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
                )

            return montant_diesel_ticpe_ajuste

    class emissions_CO2_carburants(YearlyVariable):
        label = "Emissions de CO2 des ménages via leur conso de carburants après réforme - cce 2014-2016 - en kg de CO2"

        def formula(menage, period, parameters):
            quantites_diesel_ajustees = menage('quantites_diesel', period)
            quantites_essence_ajustees = menage('quantites_essence', period)
            emissions_diesel = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
            emissions_essence = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
            emissions_ajustees = (
                (quantites_diesel_ajustees * emissions_diesel)
                + (quantites_essence_ajustees * emissions_essence)
                )  # Source : Ademe

            return emissions_ajustees

    class emissions_CO2_energies_totales(YearlyVariable):
        label = "Emissions de CO2 des ménages via leur conso d'énergies après hausse cce 14-15, en kg de CO2"

        def formula(menage, period):
            emissions_carburants_ajustees = menage('emissions_CO2_carburants', period)
            emissions_electricite_ajustees = menage('emissions_CO2_electricite', period)
            emissions_combustibles_liquides_ajustees = \
                menage('emissions_CO2_combustibles_liquides', period)
            emissions_gaz_ajustees = menage('emissions_CO2_gaz_ville', period)

            emissions_energies_ajustees = (
                emissions_carburants_ajustees + emissions_electricite_ajustees
                + emissions_combustibles_liquides_ajustees + emissions_gaz_ajustees
                )
            return emissions_energies_ajustees

    class emissions_CO2_combustibles_liquides(YearlyVariable):
        label = "Emissions de CO2 des ménages via leur conso de fioul après réforme - hausse cce 2014-2016 - en kg de CO2"

        def formula(menage, period, parameters):
            quantites_combustibles_liquides_ajustees = menage('quantites_combustibles_liquides', period)
            emissions_combustibles_liquides = \
                parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_combustibles_liquides
            emissions_ajustees = quantites_combustibles_liquides_ajustees * emissions_combustibles_liquides

            return emissions_ajustees

    class emissions_CO2_gaz_ville(YearlyVariable):
        label = "Emissions de CO2 des ménages via leur conso de gaz après réforme - hausse cce 2014-2016 - en kg de CO2"

        def formula(menage, period, parameters):
            quantites_gaz_ajustees = menage('quantites_gaz_final_ajustees_cce_2016_in_2014', period)
            emissions_gaz = \
                parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_gaz_ville
            emissions_ajustees = quantites_gaz_ajustees * emissions_gaz

            return emissions_ajustees

    class essence_ticpe(YearlyVariable):
        label = "Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"
        definition_period = YEAR

        def formula_2009(menage, period):
            sp95_ticpe_ajustee = menage('sp95_ticpe', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe', period)
            sp_e10_ticpe_ajustee = menage('sp_e10_ticpe', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_2007(menage, period, parameters):
            sp95_ticpe_ajustee = menage('sp95_ticpe', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_1990(menage, period, parameters):
            sp95_ticpe_ajustee = menage('sp95_ticpe', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe', period)
            super_plombe_ticpe_ajustee = menage('super_plombe_ticpe', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
            return essence_ticpe_ajustee

    class combustibles_liquides_ticpe(YearlyVariable):
        label = "Calcul du montant de TICPE sur le combustibles_liquides domestique après réforme - hausse cce 2014-2016"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            accise_combustibles_liquides_ticpe = (
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole_fioul_domestique_hectolitre / 100
                )
            reforme_combustibles_liquides = \
                parameters(period.start).cce_2016_in_2014.combustibles_liquides_2014_2016
            accise_combustibles_liquides_ajustee = accise_combustibles_liquides_ticpe + reforme_combustibles_liquides
            prix_fioul_ttc = \
                parameters(period.start).tarifs_energie.prix_fioul_domestique.prix_annuel_moyen_fioul_domestique_ttc_livraisons_2000_4999_litres_en_euro_par_litre
            prix_fioul_ttc_ajuste = prix_fioul_ttc + reforme_combustibles_liquides

            taux_implicite_combustibles_liquides_ajuste = (
                (accise_combustibles_liquides_ajustee * (1 + taux_plein_tva))
                / (prix_fioul_ttc_ajuste - accise_combustibles_liquides_ajustee * (1 + taux_plein_tva))
                )

            depenses_combustibles_liquides_ajustees = menage('depenses_combustibles_liquides_ajustees_cce_2016_in_2014', period)
            depenses_combustibles_liquides_ajustees_htva = \
                depenses_combustibles_liquides_ajustees - tax_from_expense_including_tax(depenses_combustibles_liquides_ajustees, taux_plein_tva)
            montant_combustibles_liquides_ticpe_ajuste = \
                tax_from_expense_including_tax(depenses_combustibles_liquides_ajustees_htva, taux_implicite_combustibles_liquides_ajuste)

            return montant_combustibles_liquides_ticpe_ajuste

    class quantites_diesel(YearlyVariable):
        label = "Quantités de diesel consommées après la réforme - contribution climat énergie, hausse de 2014 à 2016"

        def formula(menage, period, parameters):
            depenses_diesel_ajustees_cce_2016_in_2014 = \
                menage('depenses_diesel_corrigees_ajustees_cce_2016_in_2014', period)
            diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            reforme_diesel = parameters(period.start).cce_2016_in_2014.diesel_2014_2016
            quantites_diesel_ajustees = depenses_diesel_ajustees_cce_2016_in_2014 / (diesel_ttc + reforme_diesel) * 100

            return quantites_diesel_ajustees

    class quantites_combustibles_liquides(YearlyVariable):
        label = "Quantités de combustibles_liquides consommées après la réforme - contribution climat énergie, hausse de 2014 à 2016 "

        def formula(menage, period, parameters):
            depenses_combustibles_liquides_ajustees_cce_2016_in_2014 = \
                menage('depenses_combustibles_liquides_ajustees_cce_2016_in_2014', period)
            prix_fioul_ttc = \
                parameters(period.start).tarifs_energie.prix_fioul_domestique.prix_annuel_moyen_fioul_domestique_ttc_livraisons_2000_4999_litres_en_euro_par_litre
            reforme_combustibles_liquides = \
                parameters(period.start).cce_2016_in_2014.combustibles_liquides_2014_2016
            quantites_combustibles_liquides_ajustees = depenses_combustibles_liquides_ajustees_cce_2016_in_2014 / (prix_fioul_ttc + reforme_combustibles_liquides)

            return quantites_combustibles_liquides_ajustees

    class quantites_gaz_final_ajustees_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités de gaz consommées après la réforme - contribution climat énergie, hausse de 2014 à 2016"

        def formula(menage, period, parameters):
            depenses_gaz_ville_ajustees_cce_2016_in_2014 = menage('depenses_gaz_ville_ajustees_cce_2016_in_2014', period)
            depenses_gaz_tarif_fixe = menage('depenses_gaz_tarif_fixe', period)
            depenses_gaz_ajustees_variables = depenses_gaz_ville_ajustees_cce_2016_in_2014 - depenses_gaz_tarif_fixe

            depenses_gaz_prix_unitaire = menage('depenses_gaz_prix_unitaire', period)
            reforme_gaz = \
                parameters(period.start).cce_2016_in_2014.gaz_2014_2016

            quantites_gaz_ajustees = depenses_gaz_ajustees_variables / (depenses_gaz_prix_unitaire + reforme_gaz)

            return quantites_gaz_ajustees

    class quantites_sp_e10(YearlyVariable):
        label = "Quantités consommées de sans plomb e10 par les ménages après réforme - hausse cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_essence_ajustees_cce_2016_in_2014 = \
                menage('depenses_essence_corrigees_ajustees_cce_2016_in_2014', period)
            part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            depenses_sp_e10_ajustees = depenses_essence_ajustees_cce_2016_in_2014 * part_sp_e10
            super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
            reforme_essence = parameters(period.start).cce_2016_in_2014.essence_2014_2016
            quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

            return quantite_sp_e10

    class quantites_sp95(YearlyVariable):
        label = "Quantités consommées de sans plomb 95 par les ménages après réforme - hausse cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_essence_ajustees_cce_2016_in_2014 = \
                menage('depenses_essence_corrigees_ajustees_cce_2016_in_2014', period)
            part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp95_ajustees = depenses_essence_ajustees_cce_2016_in_2014 * part_sp95
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            reforme_essence = parameters(period.start).cce_2016_in_2014.essence_2014_2016
            quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

            return quantites_sp95_ajustees

    class quantites_sp98(YearlyVariable):
        label = "Quantités consommées de sans plomb 98 par les ménages - hausse cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_essence_ajustees_cce_2016_in_2014 = \
                menage('depenses_essence_corrigees_ajustees_cce_2016_in_2014', period)
            part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp98_ajustees = depenses_essence_ajustees_cce_2016_in_2014 * part_sp98
            super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
            reforme_essence = parameters(period.start).cce_2016_in_2014.essence_2014_2016
            quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

            return quantites_sp98_ajustees

    class quantites_super_plombe(YearlyVariable):
        label = "Quantités consommées de super plombé par les ménages après réforme - hausse cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_essence_ajustees_cce_2016_in_2014 = \
                menage('depenses_essence_corrigees_ajustees_cce_2016_in_2014', period)
            part_super_plombe = \
                parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_ajustees_cce_2016_in_2014 * part_super_plombe
            super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
            reforme_essence = parameters(period.start).cce_2016_in_2014.essence_2014_2016
            quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

            return quantites_super_plombe_ajustees

    class quantites_essence(YearlyVariable):
        label = "Quantités d'essence consommées par les ménages après réforme - hausse cce 2014-2016"

        definition_period = YEAR

        def formula_2009(menage, period):
            quantites_sp95_ajustees = menage('quantites_sp95', period)
            quantites_sp98_ajustees = menage('quantites_sp98', period)
            quantites_sp_e10_ajustees = menage('quantites_sp_e10', period)
            quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
            return quantites_essence_ajustees

        def formula_2007(menage, period, parameters):
            quantites_sp95_ajustees = menage('quantites_sp95', period)
            quantites_sp98_ajustees = menage('quantites_sp98', period)
            quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
            return quantites_essence_ajustees

        def formula_1990(menage, period, parameters):
            quantites_sp95_ajustees = menage('quantites_sp95', period)
            quantites_sp98_ajustees = menage('quantites_sp98', period)
            quantites_super_plombe_ajustees = \
                menage('quantites_super_plombe', period)
            quantites_essence_ajustees = (
                quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
                )
            return quantites_essence_ajustees

    class sp_e10_ticpe(YearlyVariable):
        label = "Calcul du montant de la TICPE sur le SP E10 après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            try:
                accise_super_e10 = \
                    parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e10
                majoration_ticpe_super_e10 = \
                    parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
                accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
            except Exception:
                accise_ticpe_super_e10 = \
                    parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e10

            reforme_essence = parameters(period.start).cce_2016_in_2014.essence_2014_2016
            accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
            super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
            super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
            taux_implicite_sp_e10_ajuste = (
                (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
                / (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_cce_2016_in_2014 = \
                menage('depenses_essence_corrigees_ajustees_cce_2016_in_2014', period)
            part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            sp_e10_depenses_ajustees = depenses_essence_ajustees_cce_2016_in_2014 * part_sp_e10
            sp_e10_depenses_htva_ajustees = \
                sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
            montant_sp_e10_ticpe_ajuste = \
                tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

            return montant_sp_e10_ticpe_ajuste

    class sp95_ticpe(YearlyVariable):
        label = "Calcul du montant de TICPE sur le sp_95 après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            try:
                accise_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
                majoration_ticpe_super95 = \
                    parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
                accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
            except Exception:
                accise_ticpe_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98

            reforme_essence = parameters(period.start).cce_2016_in_2014.essence_2014_2016
            accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            super_95_ttc_ajuste = super_95_ttc + reforme_essence
            taux_implicite_sp95_ajuste = (
                (accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
                / (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_cce_2016_in_2014 = \
                menage('depenses_essence_corrigees_ajustees_cce_2016_in_2014', period)
            part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp_95_ajustees = depenses_essence_ajustees_cce_2016_in_2014 * part_sp95
            depenses_sp_95_htva_ajustees = (
                depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
                )
            montant_sp95_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
                )

            return montant_sp95_ticpe_ajuste

    class sp98_ticpe(YearlyVariable):
        label = "Calcul du montant de TICPE sur le sp_98 après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            try:
                accise_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
                majoration_ticpe_super98 = \
                    parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
                accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
            except Exception:
                accise_ticpe_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98

            reforme_essence = parameters(period.start).cce_2016_in_2014.essence_2014_2016
            accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
            super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
            super_98_ttc_ajuste = super_98_ttc + reforme_essence
            taux_implicite_sp98_ajuste = (
                (accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
                / (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_cce_2016_in_2014 = \
                menage('depenses_essence_corrigees_ajustees_cce_2016_in_2014', period)
            part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp_98_ajustees = depenses_essence_ajustees_cce_2016_in_2014 * part_sp98
            depenses_sp_98_htva_ajustees = (
                depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
                )
            montant_sp98_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
                )

            return montant_sp98_ticpe_ajuste

    class super_plombe_ticpe(YearlyVariable):
        label = "Calcul du montant de la TICPE sur le super plombé après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            accise_super_plombe_ticpe = \
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_plombe

            reforme_essence = parameters(period.start).cce_2016_in_2014.essence_2014_2016
            accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
            super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
            super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
            taux_implicite_super_plombe_ajuste = (
                (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
                / (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_cce_2016_in_2014 = \
                menage('depenses_essence_corrigees_ajustees_cce_2016_in_2014', period)
            part_super_plombe = \
                parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_ajustees_cce_2016_in_2014 * part_super_plombe
            depenses_super_plombe_htva_ajustees = (
                depenses_super_plombe_ajustees
                - tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
                )
            montant_super_plombe_ticpe_ajuste = \
                tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

            return montant_super_plombe_ticpe_ajuste

    class taxe_gaz_ville(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Recettes de la hausse de cce 2014-2016 sur la consommation de gaz - ceteris paribus"
        # On considère que les contributions sur les taxes précédentes ne sont pas affectées

        def formula(menage, period, parameters):
            quantites_gaz_ajustees = menage('quantites_gaz_final_ajustees_cce_2016_in_2014', period)
            reforme_gaz = parameters(period.start).cce_2016_in_2014.gaz_2014_2016
            recettes_gaz = quantites_gaz_ajustees * reforme_gaz

            return recettes_gaz

    class ticpe_totale(YearlyVariable):
        label = "Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

        def formula(menage, period):
            essence_ticpe_ajustee = menage('essence_ticpe', period)
            diesel_ticpe_ajustee = menage('diesel_ticpe', period)
            ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

            return ticpe_totale_ajustee

    class total_taxes_energies_cce_2016_in_2014(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Différence entre les contributions aux taxes sur l'énergie après la hausse cce 2014-2016"

        def formula(menage, period):
            taxe_diesel = menage('diesel_ticpe', period)
            taxe_essence = menage('essence_ticpe', period)
            taxe_combustibles_liquides = menage('combustibles_liquides_ticpe', period)
            taxe_gaz_ville = menage('taxe_gaz_ville', period)

            total = (
                taxe_diesel + taxe_essence + taxe_combustibles_liquides + taxe_gaz_ville
                )

            return total

    class tva_taux_plein(YearlyVariable):
        label = "Contribution sur la TVA à taux plein après réaction à la réforme - cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_tva_taux_plein_ajustees = \
                menage('depenses_tva_taux_plein_ajustees_cce_2016_in_2014', period)

            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein = (
                parameters(period.start).cce_2016_in_2014.abaissement_tva_taux_plein_2014_2016
                )
            nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

            return tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)

    class tva_taux_plein_bis(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Contribution sur la TVA à taux plein après réaction à la réforme - cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_tva_taux_plein_ajustees = \
                menage('depenses_tva_taux_plein_bis_ajustees_cce_2016_in_2014', period)

            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein = (
                parameters(period.start).cce_2016_in_2014.abaissement_tva_taux_plein_bis_2014_2016
                )
            nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

            return tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)

    class tva_taux_reduit(YearlyVariable):
        label = "Contribution sur la TVA à taux reduit après réaction à la réforme - cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_tva_taux_reduit_ajustees = \
                menage('depenses_tva_taux_reduit_ajustees_cce_2016_in_2014', period)

            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            abaissement_tva_taux_reduit = \
                parameters(period.start).cce_2016_in_2014.abaissement_tva_taux_reduit_2014_2016
            nouveau_taux_reduit = taux_reduit - abaissement_tva_taux_reduit

            return tax_from_expense_including_tax(depenses_tva_taux_reduit_ajustees, nouveau_taux_reduit)

    class tva_taux_super_reduit(YearlyVariable):
        label = "Contribution sur la TVA à taux super reduit après réaction à la réforme - cce 2014-2016"

        def formula(menage, period, parameters):
            depenses_tva_taux_super_reduit_ajustees = \
                menage('depenses_tva_taux_super_reduit_ajustees_cce_2016_in_2014', period)

            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            abaissement_tva_taux_super_reduit = \
                parameters(period.start).cce_2016_in_2014.abaissement_tva_taux_super_reduit_2014_2016
            nouveau_taux_super_reduit = taux_super_reduit - abaissement_tva_taux_super_reduit

            return \
                tax_from_expense_including_tax(depenses_tva_taux_super_reduit_ajustees, nouveau_taux_super_reduit)

    class tva_total(YearlyVariable):
        label = "Différence de contribution sur la TVA après réaction à la réforme - taxes carburants"

        def formula(menage, period):
            taux_plein = menage('tva_taux_plein_bis', period)
            taux_reduit = menage('tva_taux_reduit', period)
            taux_super_reduit = menage('tva_taux_super_reduit', period)
            taux_intermediaire = menage('tva_taux_intermediaire', period)

            total = (taux_plein + taux_reduit + taux_super_reduit + taux_intermediaire)

            return total

    def apply(self):
        self.update_variable(self.cheques_energie)
        self.update_variable(self.contributions_reforme)
        self.update_variable(self.depenses_carburants_corrigees_ajustees_cce_2016_in_2014)
        self.update_variable(self.depenses_diesel_corrigees_ajustees_cce_2016_in_2014)
        self.update_variable(self.depenses_energies_logement_ajustees_cce_2016_in_2014)
        self.update_variable(self.depenses_essence_corrigees_ajustees_cce_2016_in_2014)
        self.update_variable(self.depenses_combustibles_liquides_ajustees_cce_2016_in_2014)
        self.update_variable(self.depenses_gaz_ville_ajustees_cce_2016_in_2014)
        self.update_variable(self.depenses_tva_taux_plein_ajustees_cce_2016_in_2014)
        self.update_variable(self.depenses_tva_taux_plein_bis_ajustees_cce_2016_in_2014)
        self.update_variable(self.depenses_tva_taux_reduit_ajustees_cce_2016_in_2014)
        self.update_variable(self.depenses_tva_taux_super_reduit_ajustees_cce_2016_in_2014)
        self.update_variable(self.diesel_ticpe)
        self.update_variable(self.emissions_CO2_carburants)
        self.update_variable(self.emissions_CO2_energies_totales)
        self.update_variable(self.emissions_CO2_combustibles_liquides)
        self.update_variable(self.emissions_CO2_gaz_ville)
        self.update_variable(self.essence_ticpe)
        self.update_variable(self.combustibles_liquides_ticpe)
        self.update_variable(self.quantites_diesel)
        self.update_variable(self.quantites_combustibles_liquides)
        self.update_variable(self.quantites_gaz_final_ajustees_cce_2016_in_2014)
        self.update_variable(self.quantites_sp_e10)
        self.update_variable(self.quantites_sp95)
        self.update_variable(self.quantites_sp98)
        self.update_variable(self.quantites_super_plombe)
        self.update_variable(self.quantites_essence)
        self.update_variable(self.sp_e10_ticpe)
        self.update_variable(self.sp95_ticpe)
        self.update_variable(self.sp98_ticpe)
        self.update_variable(self.super_plombe_ticpe)
        self.update_variable(self.taxe_gaz_ville)
        self.update_variable(self.ticpe_totale)
        self.update_variable(self.total_taxes_energies_cce_2016_in_2014)
        self.update_variable(self.tva_taux_plein)
        self.update_variable(self.tva_taux_plein_bis)
        self.update_variable(self.tva_taux_reduit)
        self.update_variable(self.tva_taux_super_reduit)
        self.update_variable(self.tva_total)
        self.modify_parameters(modifier_function = modify_parameters)
