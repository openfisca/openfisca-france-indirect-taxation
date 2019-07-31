# -*- coding: utf-8 -*-


from openfisca_core.reforms import Reform
import numpy

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore
from ..model.taxes_indirectes import tva, ticpe
from ..model.consommation import emissions_co2, quantites_energie

parameters_path = os.path.join(os.path.dirname(__file__), 'parameters')

# 44,6€ la tonne de CO2 en 2018 (au lieu des 39€ initialement prévus par la CCE), contre 22€ en 2016.
# Le rattrapage de la fiscalité du diesel prévoit une hausse de 2,6€ par an (par hectolitre)
# pendant 4 ans, en plus de la hausse de la composante carbone.

# En utilisant nos données d'équivalence entre consommation et émission,
# on met en place les montants de taxe suivants :

# On calcul les variables ajustées selon le scénario officiel et plusieurs alternatives :
# 1) une hausse de la CSPE sur l'électricité, 2) un rattrapage intégral de la fiscalité diesel,
# 3) la hausse de la composante carbone sans le rattrapage du diesel


def modify_parameters(parameters):
    node = ParameterNode(
        'officielle_2018_in_2016',
        data = {
            "description": "officielle_2018_in_2016",
            "diesel_2016_2018": {
                "description": "Surcroît de prix du diesel (en euros par hectolitres)",
                "unit": "currency",
                "values": {
                    "2016-01-01": 2.6 + 266 * (0.0446 - 0.022)
                    },
                },
            "diesel_cce_seulement": {
                "description": "Surcroît de prix du diesel (en euros par hectolitres) rattrapage exclut (i.e. cce seulement)",
                "unit": "currency",
                "values": {
                    "2016-01-01": 266 * (0.0446 - 0.022)
                    },
                },
            "essence_2016_2018": {
                "description": "Surcroît de prix de lessence (en euros par hectolitres)",
                "unit": "currency",
                "values": {
                    "2016-01-01": 242 * (0.0446 - 0.022)
                    }
                },
            "combustibles_liquides_2016_2018": {
                "description": "Surcroît de prix du fioul domestique (en euros par litre)",
                "unit": "currency",
                "values": {
                    "2016-01-01": 3.24 * (0.0446 - 0.022),
                    }
                },
            "electricite_cspe": {
                "description": "Surcroît de prix de lélectricité (en euros par kWh) en ajoutant la différence avec un prix de 10€ sur le marché EU-ETS",
                "unit": "currency",
                "values": {
                    "2016-01-01": 0.09 * (0.0446 - 0.01),  # Différence entre prix de la réforme et prix (environ 10€) sur le marché EU-ETS
                    },
                },
            "gaz_ville_2016_2018": {
                "description": "Surcroît de prix du gaz (en euros par kWh)",
                "unit": "currency",
                "values":
                    {"2016-01-01": 0.241 * (0.0446 - 0.022)}
                },
            "abaissement_tva_taux_plein_2016_2018": {
                "description": "Baisse de la TVA à taux plein pour obtenir un budget constantœ",
                "values": {
                    "2010-01-01": 0
                    },
                },
            "abaissement_tva_taux_plein_bis_2016_2018": {
                "description": "Baisse de la TVA à taux plein pour obtenir un budget constant",
                "values": {
                    "2010-01-01": 0
                    },
                },
            "abaissement_tva_taux_reduit_2016_2018": {
                "description": "Baisse de la TVA à taux plein pour obtenir un budget constant",
                "values": {
                    "2010-01-01": 0
                    },
                },
            "abaissement_tva_taux_super_reduit_2016_2018": {
                "description": "Baisse de la TVA à taux plein pour obtenir un budget constant",
                "values": {
                    "2010-01-01": 0
                    }
                }
            }
        )
    parameters.add_child('officielle_2018_in_2016', node)
    return parameters


class reforme_officielle_2018_in_2016(Reform):
    key = 'officielle_2018_in_2016',
    name = "Réforme de la fiscalité des énergies de 2018 par rapport aux taux de 2016",

    class cheques_energie_integral_inconditionnel_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des chèques énergie (indexés par uc) avec redistribution intégrale et inconditionnelle"

        def formula(menage, period):
            revenu_reforme = \
                menage('revenu_reforme_officielle_2018_in_2016', period)
            ocde10 = menage('ocde10', period)
            pondmen = menage('pondmen', period)

            somme_revenu = numpy.sum(revenu_reforme * pondmen)
            revenu_uc = somme_revenu / numpy.sum(ocde10 * pondmen)

            cheque = revenu_uc * ocde10

            return cheque

    class cheques_energie_integral_inconditionnel_officielle_2018_in_2016_plus_cspe(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des chèques énergie (indexés par uc) avec redistribution intégrale et inconditionnelle"

        def formula(menage, period):
            revenu_reforme = \
                menage('revenu_reforme_officielle_2018_in_2016_plus_cspe', period)
            ocde10 = menage('ocde10', period)
            pondmen = menage('pondmen', period)

            somme_revenu = numpy.sum(revenu_reforme * pondmen)
            revenu_uc = somme_revenu / numpy.sum(ocde10 * pondmen)

            cheque = revenu_uc * ocde10

            return cheque

    class cheques_energie_integral_inconditionnel_cce_seulement(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des chèques énergie (indexés par uc) avec redistribution intégrale et inconditionnelle"

        def formula(menage, period):
            revenu_reforme = \
                menage('revenu_reforme_cce_seulement', period)
            ocde10 = menage('ocde10', period)
            pondmen = menage('pondmen', period)

            somme_revenu = numpy.sum(revenu_reforme * pondmen)
            revenu_uc = somme_revenu / numpy.sum(ocde10 * pondmen)

            cheque = revenu_uc * ocde10

            return cheque

    class cheques_energie_integral_inconditionnel_rattrapage_integral(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des chèques énergie (indexés par uc) avec redistribution intégrale et inconditionnelle"

        def formula(menage, period):
            revenu_reforme = \
                menage('revenu_reforme_rattrapage_integral', period)
            ocde10 = menage('ocde10', period)
            pondmen = menage('pondmen', period)

            somme_revenu = numpy.sum(revenu_reforme * pondmen)
            revenu_uc = somme_revenu / numpy.sum(ocde10 * pondmen)

            cheque = revenu_uc * ocde10

            return cheque

    class cheques_energie_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des chèques énergie tels que prévus par la loi"

        def formula(menage, period):
            revenu_fiscal = menage('revdecm', period)
            ocde10 = menage('ocde10', period)
            revenu_fiscal_uc = revenu_fiscal / ocde10

            cheque = (
                0
                + 144 * (revenu_fiscal_uc < 5600) * (ocde10 == 1)
                + 190 * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2)
                + 227 * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2))
                + 96 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 == 1)
                + 126 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2)
                + 152 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2))
                + 48 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 == 1)
                + 63 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 > 1) * (ocde10 < 2)
                + 76 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * ((ocde10 == 2) + (ocde10 > 2))
                )

            return cheque

    class cheques_energie_ruraux_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des chèques énergie tels que prévus par la loi"

        def formula(menage, period):
            revenu_fiscal = menage('revdecm', period)
            ocde10 = menage('ocde10', period)
            pondmen = menage('pondmen', period)
            revenu_fiscal_uc = revenu_fiscal / ocde10
            strate = menage('strate', period)
            urbains = 1 * (strate > 0)

            eligibles = 1 * (revenu_fiscal_uc < 7700)
            ruraux_eligibles = (1 - urbains) * eligibles
            cheque_ruraux = 10 * ruraux_eligibles * ocde10

            somme_cheques_ruraux = numpy.sum(cheque_ruraux * pondmen)

            cheque = (
                0
                + 144 * (revenu_fiscal_uc < 5600) * (ocde10 == 1)
                + 190 * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2)
                + 227 * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2))
                + 96 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 == 1)
                + 126 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2)
                + 152 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2))
                + 48 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 == 1)
                + 63 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 > 1) * (ocde10 < 2)
                + 76 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * ((ocde10 == 2) + (ocde10 > 2))
                )

            somme_cheques = numpy.sum(cheque * pondmen)
            ratio_ruraux = somme_cheques_ruraux / somme_cheques

            cheque_final = (cheque * (1 - ratio_ruraux)) + cheque_ruraux

            return cheque_final

    class cheques_energie_by_energy_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des chèques énergie tels que prévus par la loi"

        def formula(menage, period):
            revenu_fiscal = menage('revdecm', period)
            ocde10 = menage('ocde10', period)
            pondmen = menage('pondmen', period)
            revenu_fiscal_uc = revenu_fiscal / ocde10
            combustibles_liquides = menage('combustibles_liquides', period)
            gaz_ville = menage('gaz_ville', period)
            by_energy = 1 * ((combustibles_liquides + gaz_ville) > 0)

            eligibles = 1 * (revenu_fiscal_uc < 7700)
            eligibles_by_energy = by_energy * eligibles
            cheque_by_energy = 70 * eligibles_by_energy * ocde10

            somme_cheques_by_energy = numpy.sum(cheque_by_energy * pondmen)

            cheque = (
                0
                + 144 * (revenu_fiscal_uc < 5600) * (ocde10 == 1)
                + 190 * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2)
                + 227 * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2))
                + 96 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 == 1)
                + 126 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2)
                + 152 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2))
                + 48 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 == 1)
                + 63 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 > 1) * (ocde10 < 2)
                + 76 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * ((ocde10 == 2) + (ocde10 > 2))
                )

            somme_cheques = numpy.sum(cheque * pondmen)
            ratio_by_energy = somme_cheques_by_energy / somme_cheques

            cheque_final = (cheque * (1 - ratio_by_energy)) + cheque_by_energy

            return cheque_final

    class cheques_energie_ruraux_by_energy_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des chèques énergie tels que prévus par la loi"

        def formula(menage, period):
            revenu_fiscal = menage('revdecm', period)
            ocde10 = menage('ocde10', period)
            pondmen = menage('pondmen', period)
            revenu_fiscal_uc = revenu_fiscal / ocde10
            strate = menage('strate', period)
            urbains = 1 * (strate > 0)

            eligibles = 1 * (revenu_fiscal_uc < 7700)

            ruraux_eligibles = (1 - urbains) * eligibles
            cheque_ruraux = 10 * ruraux_eligibles * ocde10
            somme_cheques_ruraux = numpy.sum(cheque_ruraux * pondmen)

            combustibles_liquides = menage('combustibles_liquides', period)
            gaz_ville = menage('gaz_ville', period)
            by_energy = 1 * ((combustibles_liquides + gaz_ville) > 0)

            eligibles_by_energy = by_energy * eligibles
            cheque_by_energy = 70 * eligibles_by_energy * ocde10
            somme_cheques_by_energy = numpy.sum(cheque_by_energy * pondmen)

            cheque = (
                0
                + 144 * (revenu_fiscal_uc < 5600) * (ocde10 == 1)
                + 190 * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2)
                + 227 * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2))
                + 96 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 == 1)
                + 126 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2)
                + 152 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2))
                + 48 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 == 1)
                + 63 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 > 1) * (ocde10 < 2)
                + 76 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * ((ocde10 == 2) + (ocde10 > 2))
                )

            somme_cheques = numpy.sum(cheque * pondmen)
            ratio_ruraux = somme_cheques_ruraux / somme_cheques
            ratio_by_energy = somme_cheques_by_energy / somme_cheques

            cheque_final = (
                (cheque * (1 - ratio_ruraux - ratio_by_energy))
                + cheque_ruraux
                + cheque_by_energy
                )

            return cheque_final

    class combustibles_liquides_ticpe_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de TICPE sur le combustibles_liquides domestique après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            accise_combustibles_liquides_ticpe = (
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole_fioul_domestique_hectolitre / 100
                )
            reforme_combustibles_liquides = \
                parameters(period.start).officielle_2018_in_2016.combustibles_liquides_2016_2018
            accise_combustibles_liquides_ajustee = accise_combustibles_liquides_ticpe + reforme_combustibles_liquides
            prix_fioul_ttc = \
                parameters(period.start).tarifs_energie.prix_fioul_domestique.prix_annuel_moyen_fioul_domestique_ttc_livraisons_2000_4999_litres_en_euro_par_litre
            prix_fioul_ttc_ajuste = prix_fioul_ttc + reforme_combustibles_liquides

            taux_implicite_combustibles_liquides_ajuste = (
                (accise_combustibles_liquides_ajustee * (1 + taux_plein_tva)) /
                (prix_fioul_ttc_ajuste - accise_combustibles_liquides_ajustee * (1 + taux_plein_tva))
                )

            depenses_combustibles_liquides_ajustees = menage('depenses_combustibles_liquides_officielle_2018_in_2016', period)
            depenses_combustibles_liquides_htva = \
                depenses_combustibles_liquides_ajustees - tax_from_expense_including_tax(depenses_combustibles_liquides_ajustees, taux_plein_tva)
            montant_combustibles_liquides_ticpe_ajuste = \
                tax_from_expense_including_tax(depenses_combustibles_liquides_htva, taux_implicite_combustibles_liquides_ajuste)

            return montant_combustibles_liquides_ticpe_ajuste

    class depenses_carburants_corrigees_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Depenses en carburants après reaction a la reforme"

        def formula(menage, period):
            depenses_diesel_ajustees = menage('depenses_diesel_corrigees_officielle_2018_in_2016', period)
            depenses_essence_ajustees = menage('depenses_essence_corrigees_officielle_2018_in_2016', period)
            depenses_carburants_ajustees = depenses_diesel_ajustees + depenses_essence_ajustees

            return depenses_carburants_ajustees

    class depenses_combustibles_liquides_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en combustibles_liquides après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_combustibles_liquides = menage('depenses_combustibles_liquides', period)
            prix_fioul_ttc = \
                parameters(period.start).tarifs_energie.prix_fioul_domestique.prix_annuel_moyen_fioul_domestique_ttc_livraisons_2000_4999_litres_en_euro_par_litre
            reforme_combustibles_liquides = \
                parameters(period.start).officielle_2018_in_2016.combustibles_liquides_2016_2018
            combustibles_liquides_elasticite_prix = menage('elas_price_2_2', period)
            depenses_combustibles_liquides_officielle_2018_in_2016 = \
                depenses_combustibles_liquides * (1 + (1 + combustibles_liquides_elasticite_prix) * reforme_combustibles_liquides / prix_fioul_ttc)

            return depenses_combustibles_liquides_officielle_2018_in_2016

    class depenses_diesel_corrigees_cce_seulement(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en diesel après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_diesel = menage('depenses_diesel_corrigees', period)
            diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            reforme_diesel = parameters(period.start).officielle_2018_in_2016.diesel_cce_seulement
            carburants_elasticite_prix = menage('elas_price_1_1', period)
            depenses_diesel_cce_seulement = \
                depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

            return depenses_diesel_cce_seulement

    class depenses_diesel_corrigees_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en diesel après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_diesel = menage('depenses_diesel_corrigees', period)
            diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            reforme_diesel = parameters(period.start).officielle_2018_in_2016.diesel_2016_2018
            carburants_elasticite_prix = menage('elas_price_1_1', period)
            depenses_diesel_officielle_2018_in_2016 = \
                depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

            return depenses_diesel_officielle_2018_in_2016

    class depenses_diesel_corrigees_rattrapage_integral(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en diesel après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_diesel = menage('depenses_diesel_corrigees', period)
            diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            taxe_essence = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            taxe_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole
            reforme_diesel = taxe_essence - taxe_diesel
            carburants_elasticite_prix = menage('elas_price_1_1', period)
            depenses_diesel_rattrapage_integral = \
                depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

            return depenses_diesel_rattrapage_integral

    class depenses_electricite_cspe(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en électricité après réaction à la hausse de la CSPE"

        def formula(menage, period, parameters):
            depenses_electricite_variables = menage('depenses_electricite_variables', period)
            tarifs_sociaux_electricite = menage('tarifs_sociaux_electricite', period)
            # Avec la réforme ces tarifs disparaissent, de nouvelles consommations entrent dans les dépenses des ménages :
            depenses_electricite_variables = depenses_electricite_variables + tarifs_sociaux_electricite

            depenses_electricite_prix_unitaire = menage('depenses_electricite_prix_unitaire', period)
            reforme_electricite = parameters(period.start).officielle_2018_in_2016.electricite_cspe
            electricite_elasticite_prix = menage('elas_price_2_2', period)
            depenses_electricite_ajustees_variables = (
                depenses_electricite_variables
                * (1 + (1 + electricite_elasticite_prix) * reforme_electricite / depenses_electricite_prix_unitaire)
                )
            depenses_electricite_tarif_fixe = menage('depenses_electricite_tarif_fixe', period)
            min_tarif_fixe = depenses_electricite_tarif_fixe.min()
            depenses_electricite_ajustees = depenses_electricite_ajustees_variables + depenses_electricite_tarif_fixe

            # We do not want to input the expenditure of the contract for those who consume nothing
            depenses_electricite = menage('depenses_electricite', period)
            depenses_electricite_ajustees = (
                depenses_electricite_ajustees * (depenses_electricite > min_tarif_fixe)
                + depenses_electricite * (depenses_electricite < min_tarif_fixe)
                )

            return depenses_electricite_ajustees

    class depenses_energies_logement_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en énergies dans le logement après la réforme"

        def formula(menage, period):
            depenses_electricite = menage('depenses_electricite', period)
            tarifs_sociaux_electricite = menage('tarifs_sociaux_electricite', period)
            depenses_gaz_ville_ajustees = menage('depenses_gaz_ville_officielle_2018_in_2016', period)
            depenses_gaz_liquefie = menage('depenses_gaz_liquefie', period)
            depenses_combustibles_liquides_ajustees = menage('depenses_combustibles_liquides_officielle_2018_in_2016', period)
            depenses_combustibles_solides = menage('depenses_combustibles_solides', period)
            depenses_energie_thermique = menage('depenses_energie_thermique', period)
            depenses_energies_logement_officielle_2018_in_2016 = (
                depenses_electricite + tarifs_sociaux_electricite + depenses_gaz_ville_ajustees + depenses_gaz_liquefie
                + depenses_combustibles_liquides_ajustees + depenses_combustibles_solides + depenses_energie_thermique
                )

            return depenses_energies_logement_officielle_2018_in_2016

    class depenses_energies_logement_officielle_2018_in_2016_plus_cspe(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en énergies logement après réforme avec hausse de la CSPE"

        def formula(menage, period):
            depenses_electricite_ajustees = menage('depenses_electricite_cspe', period)
            depenses_gaz_ville_ajustees = menage('depenses_gaz_ville_officielle_2018_in_2016', period)
            depenses_gaz_liquefie = menage('depenses_gaz_liquefie', period)
            depenses_combustibles_liquides_ajustees = menage('depenses_combustibles_liquides_officielle_2018_in_2016', period)
            depenses_combustibles_solides = menage('depenses_combustibles_solides', period)
            depenses_energie_thermique = menage('depenses_energie_thermique', period)
            depenses_energies_logement_officielle_2018_in_2016 = (
                depenses_electricite_ajustees + depenses_gaz_ville_ajustees + depenses_gaz_liquefie
                + depenses_combustibles_liquides_ajustees + depenses_combustibles_solides + depenses_energie_thermique
                )

            return depenses_energies_logement_officielle_2018_in_2016

    class depenses_essence_corrigees_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en essence après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_essence = menage('depenses_essence_corrigees', period)
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            reforme_essence = parameters(period.start).officielle_2018_in_2016.essence_2016_2018
            carburants_elasticite_prix = menage('elas_price_1_1', period)
            depenses_essence_officielle_2018_in_2016 = \
                depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence / super_95_ttc)

            return depenses_essence_officielle_2018_in_2016

    class depenses_gaz_ville_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en gaz après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_gaz_variables = menage('depenses_gaz_variables', period)
            # Avec la réforme ces tarifs disparaissent, de nouvelles consommations entrent dans les dépenses des ménages :
            tarifs_sociaux_gaz = menage('tarifs_sociaux_gaz', period)
            depenses_gaz_variables = depenses_gaz_variables + tarifs_sociaux_gaz

            depenses_gaz_prix_unitaire = menage('depenses_gaz_prix_unitaire', period)
            reforme_gaz = \
                parameters(period.start).officielle_2018_in_2016.gaz_ville_2016_2018
            gaz_elasticite_prix = menage('elas_price_2_2', period)
            depenses_gaz_variables = \
                depenses_gaz_variables * (1 + (1 + gaz_elasticite_prix) * reforme_gaz / depenses_gaz_prix_unitaire)
            depenses_gaz_tarif_fixe = menage('depenses_gaz_tarif_fixe', period)
            depenses_gaz_ajustees = depenses_gaz_variables + depenses_gaz_tarif_fixe
            depenses_gaz_ajustees = numpy.array(depenses_gaz_ajustees, dtype = float)
            depenses_gaz_ajustees[numpy.isnan(depenses_gaz_ajustees)] = 0
            depenses_gaz_ajustees[numpy.isinf(depenses_gaz_ajustees)] = 0

            return depenses_gaz_ajustees

    class depenses_tva_taux_plein_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses sur les biens assujetis à la TVA à taux plein après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_tva_taux_plein = menage('depenses_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein = (
                parameters(period.start).officielle_2018_in_2016.abaissement_tva_taux_plein_2016_2018
                )
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_plein_ajustees = \
                depenses_tva_taux_plein * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))

            return depenses_tva_taux_plein_ajustees

    class depenses_tva_taux_plein_bis_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses sur les biens assujetis à la TVA à taux plein bis après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_tva_taux_plein = menage('depenses_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein_bis = (
                parameters(period.start).officielle_2018_in_2016.abaissement_tva_taux_plein_bis_2016_2018
                )
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_plein_bis_ajustees = (
                depenses_tva_taux_plein
                * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein_bis) / (1 + taux_plein))
                )

            return depenses_tva_taux_plein_bis_ajustees

    class depenses_tva_taux_reduit_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses sur les biens assujetis à la TVA à taux reduit après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_tva_taux_reduit = menage('depenses_tva_taux_reduit', period)
            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            abaissement_tva_taux_reduit = (
                parameters(period.start).officielle_2018_in_2016.abaissement_tva_taux_reduit_2016_2018
                )
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_reduit_ajustees = \
                depenses_tva_taux_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_reduit) / (1 + taux_reduit))

            return depenses_tva_taux_reduit_ajustees

    class depenses_tva_taux_super_reduit_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses sur les biens assujetis à la TVA à taux super reduit après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_tva_taux_super_reduit = menage('depenses_tva_taux_super_reduit', period)
            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            abaissement_tva_taux_super_reduit = (
                parameters(period.start).officielle_2018_in_2016.abaissement_tva_taux_super_reduit_2016_2018
                )
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_super_reduit_ajustees = \
                depenses_tva_taux_super_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_super_reduit) / (1 + taux_super_reduit))

            return depenses_tva_taux_super_reduit_ajustees

    class diesel_ticpe_cce_seulement(YearlyVariable):
        value_type = float
        entity = Menage
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

            reforme_diesel = parameters(period.start).officielle_2018_in_2016.diesel_cce_seulement
            accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
            prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
            taux_implicite_diesel_ajuste = (
                (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
                (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                )

            depenses_diesel_cce_seulement = \
                menage('depenses_diesel_corrigees_cce_seulement', period)
            depenses_diesel_htva_ajustees = (
                depenses_diesel_cce_seulement -
                tax_from_expense_including_tax(depenses_diesel_cce_seulement, taux_plein_tva)
                )
            montant_diesel_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
                )

            return montant_diesel_ticpe_ajuste

    class diesel_ticpe_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
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

            reforme_diesel = parameters(period.start).officielle_2018_in_2016.diesel_2016_2018
            accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
            prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
            taux_implicite_diesel_ajuste = (
                (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
                (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                )

            depenses_diesel_officielle_2018_in_2016 = \
                menage('depenses_diesel_corrigees_officielle_2018_in_2016', period)
            depenses_diesel_htva_ajustees = (
                depenses_diesel_officielle_2018_in_2016 -
                tax_from_expense_including_tax(depenses_diesel_officielle_2018_in_2016, taux_plein_tva)
                )
            montant_diesel_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
                )

            return montant_diesel_ticpe_ajuste

    class diesel_ticpe_rattrapage_integral(YearlyVariable):
        value_type = float
        entity = Menage
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

            taxe_essence = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            taxe_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole
            reforme_diesel = taxe_essence - taxe_diesel
            accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
            prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
            taux_implicite_diesel_ajuste = (
                (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
                (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                )

            depenses_diesel_rattrapage_integral = \
                menage('depenses_diesel_corrigees_rattrapage_integral', period)
            depenses_diesel_htva_ajustees = (
                depenses_diesel_rattrapage_integral -
                tax_from_expense_including_tax(depenses_diesel_rattrapage_integral, taux_plein_tva)
                )
            montant_diesel_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
                )

            return montant_diesel_ticpe_ajuste

    class emissions_CO2_carburants_cce_seulement(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Emissions de CO2 des ménages via leur conso de carburants après réforme CCE sans rattrapage diesel, en kg de CO2"

        def formula(menage, period, parameters):
            quantites_diesel_ajustees = menage('quantites_diesel_cce_seulement', period)
            quantites_essence_ajustees = menage('quantites_essence_officielle_2018_in_2016', period)
            emissions_diesel = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
            emissions_essence = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
            emissions_ajustees = (
                (quantites_diesel_ajustees * emissions_diesel)
                + (quantites_essence_ajustees * emissions_essence)
                )

            return emissions_ajustees

    class emissions_CO2_carburants_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Emissions de CO2 des ménages via leur conso de carburants après réforme, en kg de CO2"

        def formula(menage, period, parameters):
            quantites_diesel_ajustees = menage('quantites_diesel_officielle_2018_in_2016', period)
            quantites_essence_ajustees = menage('quantites_essence_officielle_2018_in_2016', period)
            emissions_diesel = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
            emissions_essence = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
            emissions_ajustees = (
                (quantites_diesel_ajustees * emissions_diesel)
                + (quantites_essence_ajustees * emissions_essence)
                )

            return emissions_ajustees

    class emissions_CO2_carburants_rattrapage_integral(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Emissions de CO2 des ménages via leur conso de carburants après rattrapage intégral fisalité diesel, en kg de CO2"

        def formula(menage, period, parameters):
            quantites_diesel_ajustees = menage('quantites_diesel_rattrapage_integral', period)
            quantites_essence_ajustees = menage('quantites_essence', period)
            emissions_diesel = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
            emissions_essence = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
            emissions_ajustees = (
                (quantites_diesel_ajustees * emissions_diesel)
                + (quantites_essence_ajustees * emissions_essence)
                )

            return emissions_ajustees

    class emissions_CO2_combustibles_liquides_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Emissions de CO2 des ménages via leur conso de fioul après réforme - en kg de CO2"

        def formula(menage, period, parameters):
            quantites_combustibles_liquides_ajustees = menage('quantites_combustibles_liquides_officielle_2018_in_2016', period)
            emissions_combustibles_liquides = \
                parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_combustibles_liquides
            emissions_ajustees = quantites_combustibles_liquides_ajustees * emissions_combustibles_liquides

            return emissions_ajustees

    class emissions_CO2_diesel_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Emissions de CO2 des ménages via leur conso de diesel après réforme, en kg de CO2"

        def formula(menage, period, parameters):
            quantites_diesel_ajustees = menage('quantites_diesel_officielle_2018_in_2016', period)
            emissions_diesel = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
            emissions_ajustees = quantites_diesel_ajustees * emissions_diesel

            return emissions_ajustees

    class emissions_CO2_electricite_cspe(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Emissions de CO2 des ménages via leur consommation d'électricité après réforme cspe, en kg de CO2"

        def formula(menage, period, parameters):
            quantites_electricite_ajustees = menage('quantites_electricite_selon_compteur_cspe', period)
            emissions_eletricite = \
                parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_electricite
            emissions_ajustees = quantites_electricite_ajustees * emissions_eletricite

            return emissions_ajustees

    class emissions_CO2_energies_totales_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Emissions de CO2 des ménages via leur conso d'énergies après hausse cce 16-18, en kg de CO2"

        def formula(menage, period):
            emissions_carburants_ajustees = menage('emissions_CO2_carburants_officielle_2018_in_2016', period)
            emissions_electricite = menage('emissions_CO2_electricite', period)
            emissions_combustibles_liquides_ajustees = \
                menage('emissions_CO2_combustibles_liquides_officielle_2018_in_2016', period)
            emissions_gaz_ajustees = menage('emissions_CO2_gaz_ville_officielle_2018_in_2016', period)

            emissions_energies_ajustees = (
                emissions_carburants_ajustees + emissions_electricite
                + emissions_combustibles_liquides_ajustees + emissions_gaz_ajustees
                )
            return emissions_energies_ajustees

    class emissions_CO2_energies_totales_officielle_2018_in_2016_plus_cspe(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Emissions de CO2 des ménages via leur conso d'énergies après hausse cce 16-18, en kg de CO2"

        def formula(menage, period):
            emissions_carburants_ajustees = menage('emissions_CO2_carburants_officielle_2018_in_2016', period)
            emissions_electricite_ajustees = menage('emissions_CO2_electricite_cspe', period)
            emissions_combustibles_liquides_ajustees = \
                menage('emissions_CO2_combustibles_liquides_officielle_2018_in_2016', period)
            emissions_gaz_ajustees = menage('emissions_CO2_gaz_ville_officielle_2018_in_2016', period)

            emissions_energies_ajustees = (
                emissions_carburants_ajustees + emissions_electricite_ajustees
                + emissions_combustibles_liquides_ajustees + emissions_gaz_ajustees
                )
            return emissions_energies_ajustees

    class emissions_CO2_essence_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Emissions de CO2 des ménages via leur conso d'essence après réforme, en kg de CO2"

        def formula(menage, period, parameters):
            quantites_essence_ajustees = menage('quantites_essence_officielle_2018_in_2016', period)
            emissions_essence = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
            emissions_ajustees = quantites_essence_ajustees * emissions_essence

            return emissions_ajustees

    class emissions_CO2_gaz_ville_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Emissions de CO2 des ménages via leur conso de gaz après réforme - en kg de CO2"

        def formula(menage, period, parameters):
            quantites_gaz_ajustees = menage('quantites_gaz_final_officielle_2018_in_2016', period)
            emissions_gaz = \
                parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_gaz_ville
            emissions_ajustees = quantites_gaz_ajustees * emissions_gaz

            return emissions_ajustees

    class essence_ticpe_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"

        def formula_2009(menage, period):
            sp95_ticpe_ajustee = menage('sp95_ticpe_officielle_2018_in_2016', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe_officielle_2018_in_2016', period)
            sp_e10_ticpe_ajustee = menage('sp_e10_ticpe_officielle_2018_in_2016', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_2007(menage, period):
            sp95_ticpe_ajustee = menage('sp95_ticpe_officielle_2018_in_2016', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe_officielle_2018_in_2016', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_1990(menage, period):
            sp95_ticpe_ajustee = menage('sp95_ticpe_officielle_2018_in_2016', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe_officielle_2018_in_2016', period)
            super_plombe_ticpe_ajustee = menage('super_plombe_ticpe_officielle_2018_in_2016', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
            return essence_ticpe_ajustee

    class gains_tva_carburants_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Recettes en TVA sur les carburants de la réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            depenses_carburants_corrigees_officielle_2018_in_2016 = \
                menage('depenses_carburants_corrigees_officielle_2018_in_2016', period)
            tva_depenses_carburants_corrigees_officielle_2018_in_2016 = (
                (taux_plein_tva / (1 + taux_plein_tva))
                * depenses_carburants_corrigees_officielle_2018_in_2016
                )
            depenses_carburants_corrigees = \
                menage('depenses_carburants_corrigees', period)
            tva_depenses_carburants_corrigees = (
                (taux_plein_tva / (1 + taux_plein_tva))
                * depenses_carburants_corrigees
                )
            gains_tva_carburants = (
                tva_depenses_carburants_corrigees_officielle_2018_in_2016 -
                tva_depenses_carburants_corrigees
                )
            return gains_tva_carburants

    class gains_tva_combustibles_liquides_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Recettes de la réforme en TVA sur les combustibles liquides"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            depenses_combustibles_liquides_officielle_2018_in_2016 = \
                menage('depenses_combustibles_liquides_officielle_2018_in_2016', period)
            tva_depenses_combustibles_liquides_officielle_2018_in_2016 = (
                (taux_plein_tva / (1 + taux_plein_tva))
                * depenses_combustibles_liquides_officielle_2018_in_2016
                )
            depenses_combustibles_liquides = \
                menage('depenses_combustibles_liquides', period)
            tva_depenses_combustibles_liquides = (
                (taux_plein_tva / (1 + taux_plein_tva))
                * depenses_combustibles_liquides
                )
            gains_tva_combustibles_liquides = (
                tva_depenses_combustibles_liquides_officielle_2018_in_2016 -
                tva_depenses_combustibles_liquides
                )
            return gains_tva_combustibles_liquides

    class gains_tva_gaz_ville_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Recettes de la réforme en TVA sur le gaz naturel"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            depenses_gaz_tarif_fixe = menage('depenses_gaz_tarif_fixe', period)
            depenses_gaz_ville_officielle_2018_in_2016 = \
                menage('depenses_gaz_ville_officielle_2018_in_2016', period)
            tva_depenses_gaz_ville_officielle_2018_in_2016 = (
                (taux_plein_tva / (1 + taux_plein_tva))
                * (depenses_gaz_ville_officielle_2018_in_2016 - depenses_gaz_tarif_fixe)
                )
            depenses_gaz_ville = \
                menage('depenses_gaz_ville', period)
            tva_depenses_gaz_ville = (
                (taux_plein_tva / (1 + taux_plein_tva))
                * (depenses_gaz_ville - depenses_gaz_tarif_fixe)
                )
            gains_tva_gaz_ville = (
                tva_depenses_gaz_ville_officielle_2018_in_2016 -
                tva_depenses_gaz_ville
                )
            return gains_tva_gaz_ville

    class gains_tva_total_energies_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Recettes de la réforme en TVA sur toutes les énergies"

        def formula(menage, period):
            gains_carburants = menage('gains_tva_carburants_officielle_2018_in_2016', period)
            gains_combustibles_liquides = menage('gains_tva_combustibles_liquides_officielle_2018_in_2016', period)
            gains_gaz_ville = menage('gains_tva_gaz_ville_officielle_2018_in_2016', period)

            somme_gains = gains_carburants + gains_combustibles_liquides + gains_gaz_ville
            return somme_gains

    # Vérifier que rien n'est oublié ici
    class pertes_financieres_avant_redistribution_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant total des pertes financières dues à la réforme, avant redistribution"

        def formula(menage, period):
            depenses_energies_totales = menage('depenses_energies_totales', period)
            depenses_energies_logement_officielle_2018_in_2016 = \
                menage('depenses_energies_logement_officielle_2018_in_2016', period)
            depenses_carburants_officielle_2018_in_2016 = \
                menage('depenses_carburants_corrigees_officielle_2018_in_2016', period)

            pertes = (
                depenses_energies_logement_officielle_2018_in_2016
                + depenses_carburants_officielle_2018_in_2016 -
                depenses_energies_totales
                )

            return pertes

    class pertes_financieres_avant_redistribution_officielle_2018_in_2016_plus_cspe(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant total des pertes financières dues à la réforme, avant redistribution"

        def formula(menage, period):
            depenses_energies_totales = menage('depenses_energies_totales', period)
            depenses_energies_logement_officielle_2018_in_2016_plus_cspe = \
                menage('depenses_energies_logement_officielle_2018_in_2016_plus_cspe', period)
            depenses_carburants_officielle_2018_in_2016 = \
                menage('depenses_carburants_corrigees_officielle_2018_in_2016', period)

            pertes = (
                depenses_energies_logement_officielle_2018_in_2016_plus_cspe
                + depenses_carburants_officielle_2018_in_2016 -
                depenses_energies_totales
                )

            return pertes

    class quantites_combustibles_liquides_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités de combustibles_liquides consommées après la réforme"

        def formula(menage, period, parameters):
            depenses_combustibles_liquides_officielle_2018_in_2016 = \
                menage('depenses_combustibles_liquides_officielle_2018_in_2016', period)
            prix_fioul_ttc = \
                parameters(period.start).tarifs_energie.prix_fioul_domestique.prix_annuel_moyen_fioul_domestique_ttc_livraisons_2000_4999_litres_en_euro_par_litre
            reforme_combustibles_liquides = \
                parameters(period.start).officielle_2018_in_2016.combustibles_liquides_2016_2018
            quantites_combustibles_liquides_ajustees = depenses_combustibles_liquides_officielle_2018_in_2016 / (prix_fioul_ttc + reforme_combustibles_liquides)

            return quantites_combustibles_liquides_ajustees

    class quantites_diesel_cce_seulement(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités de diesel consommées après la réforme - contribution climat énergie, hausse de 2016 à 2018"

        def formula(menage, period, parameters):
            depenses_diesel_officielle_2018_in_2016 = \
                menage('depenses_diesel_corrigees_cce_seulement', period)
            diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            reforme_diesel = parameters(period.start).officielle_2018_in_2016.diesel_cce_seulement
            quantites_diesel_ajustees = depenses_diesel_officielle_2018_in_2016 / (diesel_ttc + reforme_diesel) * 100

            return quantites_diesel_ajustees

    class quantites_diesel_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités de diesel consommées après la réforme"

        def formula(menage, period, parameters):
            depenses_diesel_officielle_2018_in_2016 = \
                menage('depenses_diesel_corrigees_officielle_2018_in_2016', period)
            diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            reforme_diesel = parameters(period.start).officielle_2018_in_2016.diesel_2016_2018
            quantites_diesel_ajustees = depenses_diesel_officielle_2018_in_2016 / (diesel_ttc + reforme_diesel) * 100

            return quantites_diesel_ajustees

    class quantites_diesel_rattrapage_integral(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités de diesel consommées après la réforme"

        def formula(menage, period, parameters):
            depenses_diesel_officielle_2018_in_2016 = \
                menage('depenses_diesel_corrigees_rattrapage_integral', period)
            diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            taxe_essence = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            taxe_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole
            reforme_diesel = taxe_essence - taxe_diesel
            quantites_diesel_ajustees = depenses_diesel_officielle_2018_in_2016 / (diesel_ttc + reforme_diesel) * 100

            return quantites_diesel_ajustees

    class quantites_electricite_selon_compteur_cspe(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités d'électricité consommées après la réforme cspe"

        def formula(menage, period):
            depenses_electricite_ajustees = \
                menage('depenses_electricite_cspe', period)
            depenses_electricite_tarif_fixe = menage('depenses_electricite_tarif_fixe', period)
            depenses_electricite_ajustees_variables = \
                depenses_electricite_ajustees - depenses_electricite_tarif_fixe

            depenses_electricite_prix_unitaire = menage('depenses_electricite_prix_unitaire', period)
            reforme_electricite = parameters(period.start).officielle_2018_in_2016.electricite_cspe

            quantites_electricite_ajustees = \
                depenses_electricite_ajustees_variables / (depenses_electricite_prix_unitaire + reforme_electricite)

            quantites_electricite_avant_reforme = menage('quantites_electricite_selon_compteur', period)
            quantites_electricite_ajustees = (
                quantites_electricite_ajustees * (quantites_electricite_avant_reforme > 0)
                )

            return quantites_electricite_ajustees

    class quantites_essence_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités d'essence consommées par les ménages après réforme"
        definition_period = YEAR

        def formula_2009(menage, period):
            quantites_sp95_ajustees = menage('quantites_sp95_officielle_2018_in_2016', period)
            quantites_sp98_ajustees = menage('quantites_sp98_officielle_2018_in_2016', period)
            quantites_sp_e10_ajustees = menage('quantites_sp_e10_officielle_2018_in_2016', period)
            quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
            return quantites_essence_ajustees

        def formula_2007(menage, period):
            quantites_sp95_ajustees = menage('quantites_sp95_officielle_2018_in_2016', period)
            quantites_sp98_ajustees = menage('quantites_sp98_officielle_2018_in_2016', period)
            quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
            return quantites_essence_ajustees

        def formula_1990(menage, period):
            quantites_sp95_ajustees = menage('quantites_sp95_officielle_2018_in_2016', period)
            quantites_sp98_ajustees = menage('quantites_sp98_officielle_2018_in_2016', period)
            quantites_super_plombe_ajustees = \
                menage('quantites_super_plombe_officielle_2018_in_2016', period)
            quantites_essence_ajustees = (
                quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
                )
            return quantites_essence_ajustees

    class quantites_gaz_final_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités de gaz consommées après la réforme"

        def formula(menage, period, parameters):
            depenses_gaz_ville_officielle_2018_in_2016 = menage('depenses_gaz_ville_officielle_2018_in_2016', period)
            depenses_gaz_tarif_fixe = menage('depenses_gaz_tarif_fixe', period)
            depenses_gaz_variables = depenses_gaz_ville_officielle_2018_in_2016 - depenses_gaz_tarif_fixe

            depenses_gaz_prix_unitaire = menage('depenses_gaz_prix_unitaire', period)
            reforme_gaz = \
                parameters(period.start).officielle_2018_in_2016.gaz_ville_2016_2018

            quantites_gaz_ajustees = depenses_gaz_variables / (depenses_gaz_prix_unitaire + reforme_gaz)

            return quantites_gaz_ajustees

    class quantites_sp_e10_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités consommées de sans plomb e10 par les ménages après réforme"

        def formula(menage, period, parameters):
            depenses_essence_officielle_2018_in_2016 = \
                menage('depenses_essence_corrigees_officielle_2018_in_2016', period)
            part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            depenses_sp_e10_ajustees = depenses_essence_officielle_2018_in_2016 * part_sp_e10
            super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
            reforme_essence = parameters(period.start).officielle_2018_in_2016.essence_2016_2018
            quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

            return quantite_sp_e10

    class quantites_sp95_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités consommées de sans plomb 95 par les ménages après réforme"

        def formula(menage, period, parameters):
            depenses_essence_officielle_2018_in_2016 = \
                menage('depenses_essence_corrigees_officielle_2018_in_2016', period)
            part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp95_ajustees = depenses_essence_officielle_2018_in_2016 * part_sp95
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            reforme_essence = parameters(period.start).officielle_2018_in_2016.essence_2016_2018
            quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

            return quantites_sp95_ajustees

    class quantites_sp98_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités consommées de sans plomb 98 par les ménages"

        def formula(menage, period, parameters):
            depenses_essence_officielle_2018_in_2016 = \
                menage('depenses_essence_corrigees_officielle_2018_in_2016', period)
            part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp98_ajustees = depenses_essence_officielle_2018_in_2016 * part_sp98
            super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
            reforme_essence = parameters(period.start).officielle_2018_in_2016.essence_2016_2018
            quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

            return quantites_sp98_ajustees

    class quantites_super_plombe_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Quantités consommées de super plombé par les ménages après réforme"

        def formula(menage, period, parameters):
            depenses_essence_officielle_2018_in_2016 = \
                menage('depenses_essence_corrigees_officielle_2018_in_2016', period)
            part_super_plombe = \
                parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_officielle_2018_in_2016 * part_super_plombe
            super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
            reforme_essence = parameters(period.start).officielle_2018_in_2016.essence_2016_2018
            quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

            return quantites_super_plombe_ajustees

    # A modifier : prendre en compte uniquement le reste des cheques, et faire quelque chose de neutre
    class reste_transferts_neutre_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des transferts additionnels à imputer pour avoir une réforme à budget neutre, sans biaiser les effets distributifs"

        def formula(menage, period):
            ocde10 = menage('ocde10', period)
            pondmen = menage('pondmen', period)

            revenu_reforme = \
                menage('revenu_reforme_officielle_2018_in_2016', period)
            somme_revenu = numpy.sum(revenu_reforme * pondmen)
            cheque = menage('cheques_energie_officielle_2018_in_2016', period)
            somme_cheque = numpy.sum(cheque * pondmen)
            revenu_restant = somme_revenu - somme_cheque

            revenu_uc = revenu_restant / numpy.sum(ocde10 * pondmen)
            reste_transferts = revenu_uc * ocde10

            return reste_transferts

    class reste_transferts_neutre_officielle_2018_in_2016_plus_cspe(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des transferts additionnels à imputer pour avoir une réforme à budget neutre, sans biaiser les effets distributifs"

        def formula(menage, period):
            ocde10 = menage('ocde10', period)
            pondmen = menage('pondmen', period)

            revenu_reforme = \
                menage('revenu_reforme_officielle_2018_in_2016_plus_cspe', period)
            somme_revenu = numpy.sum(revenu_reforme * pondmen)
            cheque = menage('cheques_energie_officielle_2018_in_2016', period)
            somme_cheque = numpy.sum(cheque * pondmen)
            revenu_restant = somme_revenu - somme_cheque

            revenu_uc = revenu_restant / numpy.sum(ocde10 * pondmen)
            reste_transferts = revenu_uc * ocde10

            return reste_transferts

    class revenu_reforme_cce_seulement(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Revenu généré par la réforme de la cce, avant redistribution"

        def formula(menage, period):
            total_taxes_energies = menage('total_taxes_energies', period)
            total_taxes_energies_cce_seulement = \
                menage('total_taxes_energies_cce_seulement', period)
            tarifs_sociaux_electricite = menage('tarifs_sociaux_electricite', period)
            tarifs_sociaux_gaz = menage('tarifs_sociaux_gaz', period)

            revenu_reforme = (
                total_taxes_energies_cce_seulement - total_taxes_energies
                + tarifs_sociaux_electricite + tarifs_sociaux_gaz
                )

            return revenu_reforme

    class revenu_reforme_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Revenu généré par la réforme officielle 2018 avant redistribution"

        def formula(menage, period):
            total_taxes_energies = menage('total_taxes_energies', period)
            total_taxes_energies_officielle_2018_in_2016 = \
                menage('total_taxes_energies_officielle_2018_in_2016', period)
            gains_tva_total_energies = menage('gains_tva_total_energies_officielle_2018_in_2016', period)
            tarifs_sociaux_electricite = menage('tarifs_sociaux_electricite', period)
            tarifs_sociaux_gaz = menage('tarifs_sociaux_gaz', period)

            revenu_reforme = (
                total_taxes_energies_officielle_2018_in_2016 - total_taxes_energies
                + gains_tva_total_energies + tarifs_sociaux_electricite + tarifs_sociaux_gaz
                )

            return revenu_reforme

    class revenu_reforme_officielle_2018_in_2016_plus_cspe(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Revenu généré par la réforme officielle 2018 plus cspe, avant redistribution"

        def formula(menage, period):
            total_taxes_energies = menage('total_taxes_energies', period)
            total_taxes_energies_officielle_2018_in_2016_plus_cspe = \
                menage('total_taxes_energies_officielle_2018_in_2016_plus_cspe', period)

            tarifs_sociaux_electricite = menage('tarifs_sociaux_electricite', period)
            tarifs_sociaux_gaz = menage('tarifs_sociaux_gaz', period)

            revenu_reforme = (
                total_taxes_energies_officielle_2018_in_2016_plus_cspe - total_taxes_energies
                + tarifs_sociaux_electricite + tarifs_sociaux_gaz
                )

            return revenu_reforme

    class revenu_reforme_rattrapage_integral(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Revenu généré par le rattrapage intégral, avant redistribution"

        def formula(menage, period):
            total_taxes_energies = menage('total_taxes_energies', period)
            total_taxes_energies_rattrapage_integral = \
                menage('total_taxes_energies_rattrapage_integral', period)

            tarifs_sociaux_electricite = menage('tarifs_sociaux_electricite', period)
            tarifs_sociaux_gaz = menage('tarifs_sociaux_gaz', period)

            revenu_reforme = (
                total_taxes_energies_rattrapage_integral - total_taxes_energies
                + tarifs_sociaux_electricite + tarifs_sociaux_gaz
                )

            return revenu_reforme

    class sp_e10_ticpe_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
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

            reforme_essence = parameters(period.start).officielle_2018_in_2016.essence_2016_2018
            accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
            super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
            super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
            taux_implicite_sp_e10_ajuste = (
                (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva)) /
                (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_officielle_2018_in_2016 = \
                menage('depenses_essence_corrigees_officielle_2018_in_2016', period)
            part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            sp_e10_depenses_ajustees = depenses_essence_officielle_2018_in_2016 * part_sp_e10
            sp_e10_depenses_htva_ajustees = \
                sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
            montant_sp_e10_ticpe_ajuste = \
                tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

            return montant_sp_e10_ticpe_ajuste

    class sp95_ticpe_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
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

            reforme_essence = parameters(period.start).officielle_2018_in_2016.essence_2016_2018
            accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            super_95_ttc_ajuste = super_95_ttc + reforme_essence
            taux_implicite_sp95_ajuste = (
                (accise_ticpe_super95_ajustee * (1 + taux_plein_tva)) /
                (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_officielle_2018_in_2016 = \
                menage('depenses_essence_corrigees_officielle_2018_in_2016', period)
            part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp_95_ajustees = depenses_essence_officielle_2018_in_2016 * part_sp95
            depenses_sp_95_htva_ajustees = (
                depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
                )
            montant_sp95_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
                )

            return montant_sp95_ticpe_ajuste

    class sp98_ticpe_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
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

            reforme_essence = parameters(period.start).officielle_2018_in_2016.essence_2016_2018
            accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
            super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
            super_98_ttc_ajuste = super_98_ttc + reforme_essence
            taux_implicite_sp98_ajuste = (
                (accise_ticpe_super98_ajustee * (1 + taux_plein_tva)) /
                (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_officielle_2018_in_2016 = \
                menage('depenses_essence_corrigees_officielle_2018_in_2016', period)
            part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp_98_ajustees = depenses_essence_officielle_2018_in_2016 * part_sp98
            depenses_sp_98_htva_ajustees = (
                depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
                )
            montant_sp98_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
                )

            return montant_sp98_ticpe_ajuste

    class super_plombe_ticpe_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur le super plombé après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            accise_super_plombe_ticpe = \
                parameters(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

            reforme_essence = parameters(period.start).officielle_2018_in_2016.essence_2016_2018
            accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
            super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
            super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
            taux_implicite_super_plombe_ajuste = (
                (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva)) /
                (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_officielle_2018_in_2016 = \
                menage('depenses_essence_corrigees_officielle_2018_in_2016', period)
            part_super_plombe = \
                parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_officielle_2018_in_2016 * part_super_plombe
            depenses_super_plombe_htva_ajustees = (
                depenses_super_plombe_ajustees -
                tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
                )
            montant_super_plombe_ticpe_ajuste = \
                tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

            return montant_super_plombe_ticpe_ajuste

    class taxe_electricite_cspe(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Recettes de l'augmentation de la CSPE sur la consommation d'électricité - ceteris paribus"
        # On considère que les contributions sur les taxes précédentes ne sont pas affectées

        def formula(menage, period, parameters):
            quantites_electricite_ajustees = menage('quantites_electricite_selon_compteur_cspe', period)
            reforme_electricite = parameters(period.start).officielle_2018_in_2016.electricite_cspe
            recettes_electricite = quantites_electricite_ajustees * reforme_electricite

            return recettes_electricite

    class taxe_gaz_ville_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Recettes de la taxe sur la consommation de gaz - ceteris paribus"
        # On considère que les contributions sur les taxes précédentes ne sont pas affectées

        def formula(menage, period, parameters):
            quantites_gaz_ajustees = menage('quantites_gaz_final_officielle_2018_in_2016', period)
            reforme_gaz = parameters(period.start).officielle_2018_in_2016.gaz_ville_2016_2018
            recettes_gaz = quantites_gaz_ajustees * reforme_gaz

            return recettes_gaz

    class ticpe_totale_cce_seulement(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

        def formula(menage, period):
            essence_ticpe_ajustee = menage('essence_ticpe_officielle_2018_in_2016', period)
            diesel_ticpe_ajustee = menage('diesel_ticpe_cce_seulement', period)
            ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

            return ticpe_totale_ajustee

    class ticpe_totale_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

        def formula(menage, period):
            essence_ticpe_ajustee = menage('essence_ticpe_officielle_2018_in_2016', period)
            diesel_ticpe_ajustee = menage('diesel_ticpe_officielle_2018_in_2016', period)
            ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

            return ticpe_totale_ajustee

    class ticpe_totale_rattrapage_integral(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

        def formula(menage, period):
            essence_ticpe_ajustee = menage('essence_ticpe', period)
            diesel_ticpe_ajustee = menage('diesel_ticpe_rattrapage_integral', period)
            ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

            return ticpe_totale_ajustee

    class total_taxes_energies_cce_seulement(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Différence entre les contributions aux taxes sur l'énergie après la hausse cce 2016-2018"

        def formula(menage, period):
            taxe_diesel = menage('diesel_ticpe_cce_seulement', period)
            taxe_essence = menage('essence_ticpe_officielle_2018_in_2016', period)
            taxe_combustibles_liquides = menage('combustibles_liquides_ticpe_officielle_2018_in_2016', period)
            taxe_gaz_ville = menage('taxe_gaz_ville_officielle_2018_in_2016', period)

            total = (
                taxe_diesel + taxe_essence + taxe_combustibles_liquides + taxe_gaz_ville
                )

            return total

    class total_taxes_energies_officielle_2018_in_2016(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Différence entre les contributions aux taxes sur l'énergie après la hausse cce 2016-2018"

        def formula(menage, period):
            taxe_diesel = menage('diesel_ticpe_officielle_2018_in_2016', period)
            taxe_essence = menage('essence_ticpe_officielle_2018_in_2016', period)
            taxe_combustibles_liquides = menage('combustibles_liquides_ticpe_officielle_2018_in_2016', period)
            taxe_gaz_ville = menage('taxe_gaz_ville_officielle_2018_in_2016', period)

            total = (
                taxe_diesel + taxe_essence + taxe_combustibles_liquides + taxe_gaz_ville
                )

            return total

    class total_taxes_energies_officielle_2018_in_2016_plus_cspe(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Différence entre les contributions aux taxes sur l'énergie après la hausse 2016-2018"

        def formula(menage, period):
            taxe_diesel = menage('diesel_ticpe_officielle_2018_in_2016', period)
            taxe_electricite_cspe = menage('taxe_electricite_cspe', period)
            taxe_essence = menage('essence_ticpe_officielle_2018_in_2016', period)
            taxe_combustibles_liquides = menage('combustibles_liquides_ticpe_officielle_2018_in_2016', period)
            taxe_gaz_ville = menage('taxe_gaz_ville_officielle_2018_in_2016', period)

            total = (
                taxe_diesel + taxe_electricite_cspe + taxe_essence + taxe_combustibles_liquides + taxe_gaz_ville
                )

            return total

    class total_taxes_energies_rattrapage_integral(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Différence entre les contributions aux taxes sur l'énergie après la hausse cce 2016-2018"

        def formula(menage, period):
            taxe_diesel = menage('diesel_ticpe_rattrapage_integral', period)
            taxe_essence = menage('essence_ticpe', period)
            taxe_combustibles_liquides = menage('combustibles_liquides_ticpe', period)

            total = (
                taxe_diesel + taxe_essence + taxe_combustibles_liquides
                )

            return total

    def apply(self):
        self.update_variable(self.cheques_energie_officielle_2018_in_2016)
        self.update_variable(self.cheques_energie_integral_inconditionnel_cce_seulement)
        self.update_variable(self.cheques_energie_integral_inconditionnel_officielle_2018_in_2016)
        self.update_variable(self.cheques_energie_integral_inconditionnel_officielle_2018_in_2016_plus_cspe)
        self.update_variable(self.cheques_energie_integral_inconditionnel_rattrapage_integral)
        self.update_variable(self.cheques_energie_ruraux_officielle_2018_in_2016)
        self.update_variable(self.cheques_energie_by_energy_officielle_2018_in_2016)
        self.update_variable(self.cheques_energie_ruraux_by_energy_officielle_2018_in_2016)
        self.update_variable(self.combustibles_liquides_ticpe_officielle_2018_in_2016)
        self.update_variable(self.depenses_carburants_corrigees_officielle_2018_in_2016)
        self.update_variable(self.depenses_combustibles_liquides_officielle_2018_in_2016)
        self.update_variable(self.depenses_diesel_corrigees_cce_seulement)
        self.update_variable(self.depenses_diesel_corrigees_officielle_2018_in_2016)
        self.update_variable(self.depenses_diesel_corrigees_rattrapage_integral)
        self.update_variable(self.depenses_electricite_cspe)
        self.update_variable(self.depenses_energies_logement_officielle_2018_in_2016)
        self.update_variable(self.depenses_energies_logement_officielle_2018_in_2016_plus_cspe)
        self.update_variable(self.depenses_essence_corrigees_officielle_2018_in_2016)
        self.update_variable(self.depenses_gaz_ville_officielle_2018_in_2016)
        self.update_variable(self.depenses_tva_taux_plein_officielle_2018_in_2016)
        self.update_variable(self.depenses_tva_taux_plein_bis_officielle_2018_in_2016)
        self.update_variable(self.depenses_tva_taux_reduit_officielle_2018_in_2016)
        self.update_variable(self.depenses_tva_taux_super_reduit_officielle_2018_in_2016)
        self.update_variable(self.diesel_ticpe_cce_seulement)
        self.update_variable(self.diesel_ticpe_officielle_2018_in_2016)
        self.update_variable(self.diesel_ticpe_rattrapage_integral)
        self.update_variable(self.emissions_CO2_carburants_cce_seulement)
        self.update_variable(self.emissions_CO2_carburants_officielle_2018_in_2016)
        self.update_variable(self.emissions_CO2_carburants_rattrapage_integral)
        self.update_variable(self.emissions_CO2_combustibles_liquides_officielle_2018_in_2016)
        self.update_variable(self.emissions_CO2_diesel_officielle_2018_in_2016)
        self.update_variable(self.emissions_CO2_electricite_cspe)
        self.update_variable(self.emissions_CO2_energies_totales_officielle_2018_in_2016)
        self.update_variable(self.emissions_CO2_energies_totales_officielle_2018_in_2016_plus_cspe)
        self.update_variable(self.emissions_CO2_essence_officielle_2018_in_2016)
        self.update_variable(self.emissions_CO2_gaz_ville_officielle_2018_in_2016)
        self.update_variable(self.essence_ticpe_officielle_2018_in_2016)
        self.update_variable(self.gains_tva_carburants_officielle_2018_in_2016)
        self.update_variable(self.gains_tva_combustibles_liquides_officielle_2018_in_2016)
        self.update_variable(self.gains_tva_gaz_ville_officielle_2018_in_2016)
        self.update_variable(self.gains_tva_total_energies_officielle_2018_in_2016)
        self.update_variable(self.pertes_financieres_avant_redistribution_officielle_2018_in_2016)
        self.update_variable(self.pertes_financieres_avant_redistribution_officielle_2018_in_2016_plus_cspe)
        self.update_variable(self.quantites_combustibles_liquides_officielle_2018_in_2016)
        self.update_variable(self.quantites_diesel_cce_seulement)
        self.update_variable(self.quantites_diesel_officielle_2018_in_2016)
        self.update_variable(self.quantites_diesel_rattrapage_integral)
        self.update_variable(self.quantites_electricite_selon_compteur_cspe)
        self.update_variable(self.quantites_essence_officielle_2018_in_2016)
        self.update_variable(self.quantites_gaz_final_officielle_2018_in_2016)
        self.update_variable(self.quantites_sp_e10_officielle_2018_in_2016)
        self.update_variable(self.quantites_sp95_officielle_2018_in_2016)
        self.update_variable(self.quantites_sp98_officielle_2018_in_2016)
        self.update_variable(self.quantites_super_plombe_officielle_2018_in_2016)
        self.update_variable(self.reste_transferts_neutre_officielle_2018_in_2016)
        self.update_variable(self.reste_transferts_neutre_officielle_2018_in_2016_plus_cspe)
        self.update_variable(self.revenu_reforme_cce_seulement)
        self.update_variable(self.revenu_reforme_officielle_2018_in_2016)
        self.update_variable(self.revenu_reforme_officielle_2018_in_2016_plus_cspe)
        self.update_variable(self.revenu_reforme_rattrapage_integral)
        self.update_variable(self.sp_e10_ticpe_officielle_2018_in_2016)
        self.update_variable(self.sp95_ticpe_officielle_2018_in_2016)
        self.update_variable(self.sp98_ticpe_officielle_2018_in_2016)
        self.update_variable(self.super_plombe_ticpe_officielle_2018_in_2016)
        self.update_variable(self.taxe_electricite_cspe)
        self.update_variable(self.taxe_gaz_ville_officielle_2018_in_2016)
        self.update_variable(self.ticpe_totale_cce_seulement)
        self.update_variable(self.ticpe_totale_officielle_2018_in_2016)
        self.update_variable(self.ticpe_totale_rattrapage_integral)
        self.update_variable(self.total_taxes_energies_cce_seulement)
        self.update_variable(self.total_taxes_energies_officielle_2018_in_2016)
        self.update_variable(self.total_taxes_energies_officielle_2018_in_2016_plus_cspe)
        self.update_variable(self.total_taxes_energies_rattrapage_integral)
        self.modify_parameters(modifier_function = modify_parameters)
