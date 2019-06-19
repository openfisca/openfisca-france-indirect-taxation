# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core.reforms import Reform, update_legislation
import numpy

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore
from ..model.taxes_indirectes import tva, ticpe
from ..model.consommation import emissions_co2, quantites_energie


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "taxe_carbone",
        "children": {
            "electricite": {
                "@type": "Parameter",
                "description": u"Surcroît de prix de l'électricité (en euros par kWh)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2010-01-01', 'value': 0.0045}],
                },
            "essence": {
                "@type": "Parameter",
                "description": u"Surcroît de prix de l'essence (en euros par hectolitres)",
                "format": "float",
                "unit": 'currency',
                "values": [{'start': u'2010-01-01', 'value': 12.1 - 1.694}],
                },
            "diesel": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du diesel (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2010-01-01', 'value': 13.3 - 1.862}],
                },
            "combustibles_liquides": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du diesel (en euros par litre)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2010-01-01', 'value': 0.155 - 0.0217}],
                },
            "gaz": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du gaz (en euros par kWh)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2010-01-01', 'value': 0.012 - 0.00168}],
                },
            "abaissement_tva_taux_plein": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'value': 0.026}],
                },
            "abaissement_tva_taux_plein_bis": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'value': 0.01}],
                },
            "abaissement_tva_taux_reduit": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'value': 0.03}],
                },
            "abaissement_tva_taux_super_reduit": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'value': 0.01}],
                },
            },
        }

    reference_legislation_json_copy['children']['taxe_carbone'] = reform_legislation_subtree
    return reference_legislation_json_copy



class taxe_carbone(Reform):
    key = 'taxe_carbone',
    name = u"Réforme de l'imposition indirecte des énergies selon leur contenu carbone",


    class cheques_energie(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Montant des chèques énergie (indexés par uc) - taxe carbone"

        def formula(self, simulation, period):
            contribution = simulation.calculate('contributions_reforme', period)
            ocde10 = simulation.calculate('ocde10', period)
            pondmen = simulation.calculate('pondmen', period)

            somme_contributions = numpy.sum(contribution * pondmen)
            contribution_uc = somme_contributions / numpy.sum(ocde10 * pondmen)

            cheque = contribution_uc * ocde10

            return cheque


    class contributions_reforme(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Changement de contribution aux taxes énergétiques suite à la réforme - taxe carbone"

        def formula(self, simulation, period):
            total_taxes_energies = simulation.calculate('total_taxes_energies', period)
            total_taxes_energies_taxe_carbone = simulation.calculate('total_taxes_energies_taxe_carbone', period)

            contribution = total_taxes_energies_taxe_carbone - total_taxes_energies

            return contribution


    class depenses_carburants_corrigees_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Dépenses en carburants après réaction à la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_diesel_ajustees = simulation.calculate('depenses_diesel_corrigees_ajustees_taxe_carbone', period)
            depenses_essence_ajustees = simulation.calculate('depenses_essence_corrigees_ajustees_taxe_carbone', period)
            depenses_carburants_ajustees = depenses_diesel_ajustees + depenses_essence_ajustees

            return depenses_carburants_ajustees


    class depenses_diesel_corrigees_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Dépenses en diesel après réaction à la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_diesel = simulation.calculate('depenses_diesel_corrigees', period)
            diesel_ttc = parameters(period.start).imposition_indirecte.prix_carburants.diesel_ttc
            reforme_diesel = parameters(period.start).taxe_carbone.diesel
            carburants_elasticite_prix = simulation.calculate('elas_price_1_1', period)
            depenses_diesel_ajustees_taxe_carbone = \
                depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

            return depenses_diesel_ajustees_taxe_carbone


    class depenses_electricite_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Dépenses en électricité après réaction à la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_electricite_variables = simulation.calculate('depenses_electricite_variables', period)
            depenses_electricite_prix_unitaire = simulation.calculate('depenses_electricite_prix_unitaire', period)
            reforme_electricite = parameters(period.start).taxe_carbone.electricite
            electricite_elasticite_prix = simulation.calculate('elas_price_2_2', period)
            depenses_electricite_ajustees_variables = (
                depenses_electricite_variables *
                (1 + (1 + electricite_elasticite_prix) * reforme_electricite / depenses_electricite_prix_unitaire)
                )
            depenses_electricite_tarif_fixe = simulation.calculate('depenses_electricite_tarif_fixe', period)
            min_tarif_fixe = depenses_electricite_tarif_fixe.min()
            depenses_electricite_ajustees = depenses_electricite_ajustees_variables + depenses_electricite_tarif_fixe

            # We do not want to input the expenditure of the contract for those who consume nothing
            depenses_electricite = simulation.calculate('depenses_electricite', period)
            depenses_electricite_ajustees = (
                depenses_electricite_ajustees * (depenses_electricite > min_tarif_fixe) +
                depenses_electricite * (depenses_electricite < min_tarif_fixe)
                )

            return depenses_electricite_ajustees


    class depenses_energies_logement_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Dépenses en électricité sans inclure dépenses jointes avec le gaz"

        def formula(self, simulation, period):
            depenses_electricite_ajustees = simulation.calculate('depenses_electricite_ajustees_taxe_carbone', period)
            depenses_gaz_ville_ajustees = simulation.calculate('depenses_gaz_ville_ajustees_taxe_carbone', period)
            depenses_gaz_liquefie = simulation.calculate('depenses_gaz_liquefie', period)
            depenses_combustibles_liquides_ajustees = simulation.calculate('depenses_combustibles_liquides_ajustees_taxe_carbone', period)
            depenses_combustibles_solides = simulation.calculate('depenses_combustibles_solides', period)
            depenses_energie_thermique = simulation.calculate('depenses_energie_thermique', period)
            depenses_energies_logement_ajustees_taxe_carbone = (
                depenses_electricite_ajustees + depenses_gaz_ville_ajustees + depenses_gaz_liquefie +
                depenses_combustibles_liquides_ajustees + depenses_combustibles_solides + depenses_energie_thermique
                )

            return depenses_energies_logement_ajustees_taxe_carbone


    class depenses_essence_corrigees_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Dépenses en essence après réaction à la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_essence = simulation.calculate('depenses_essence_corrigees', period)
            super_95_ttc = parameters(period.start).imposition_indirecte.prix_carburants.super_95_ttc
            reforme_essence = parameters(period.start).taxe_carbone.essence
            carburants_elasticite_prix = simulation.calculate('elas_price_1_1', period)
            depenses_essence_ajustees_taxe_carbone = \
                depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence / super_95_ttc)

            return depenses_essence_ajustees_taxe_carbone


    class depenses_combustibles_liquides_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Dépenses en fioul domestique après réaction à la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_combustibles_liquides = simulation.calculate('depenses_combustibles_liquides', period)
            prix_fioul_ttc = \
                parameters(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
            reforme_fioul = parameters(period.start).taxe_carbone.combustibles_liquides
            combustibles_liquides_elasticite_prix = simulation.calculate('elas_price_2_2', period)
            depenses_combustibles_liquides_ajustees_taxe_carbone = \
                depenses_combustibles_liquides * (1 + (1 + combustibles_liquides_elasticite_prix) * reforme_fioul / prix_fioul_ttc)

            return depenses_combustibles_liquides_ajustees_taxe_carbone


    class depenses_gaz_ville_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Dépenses en gaz après réaction à la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_gaz_variables = simulation.calculate('depenses_gaz_variables', period)
            depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
            reforme_gaz = parameters(period.start).taxe_carbone.gaz
            gaz_elasticite_prix = simulation.calculate('elas_price_2_2', period)
            depenses_gaz_ajustees_variables = \
                depenses_gaz_variables * (1 + (1 + gaz_elasticite_prix) * reforme_gaz / depenses_gaz_prix_unitaire)
            depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
            depenses_gaz_ajustees = depenses_gaz_ajustees_variables + depenses_gaz_tarif_fixe
            depenses_gaz_ajustees[numpy.isnan(depenses_gaz_ajustees)] = 0
            depenses_gaz_ajustees[numpy.isinf(depenses_gaz_ajustees)] = 0

            return depenses_gaz_ajustees


    class depenses_tva_taux_plein_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Dépenses sur les biens assujetis à la TVA à taux plein après réaction à la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein = parameters(period.start).taxe_carbone.abaissement_tva_taux_plein
            elasticite = simulation.calculate('elas_price_3_3', period)
            depenses_tva_taux_plein_ajustees = \
                depenses_tva_taux_plein * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))

            return depenses_tva_taux_plein_ajustees


    class depenses_tva_taux_plein_bis_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Dépenses sur les biens assujetis à la TVA à taux plein bis après réaction à la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein_bis = parameters(period.start).taxe_carbone.abaissement_tva_taux_plein_bis
            elasticite = simulation.calculate('elas_price_3_3', period)
            depenses_tva_taux_plein_bis_ajustees = (
                depenses_tva_taux_plein *
                (1 + (1 + elasticite) * (- abaissement_tva_taux_plein_bis) / (1 + taux_plein))
                )

            return depenses_tva_taux_plein_bis_ajustees


    class depenses_tva_taux_reduit_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Dépenses sur les biens assujetis à la TVA à taux reduit après réaction à la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_tva_taux_reduit = simulation.calculate('depenses_tva_taux_reduit', period)
            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            abaissement_tva_taux_reduit = parameters(period.start).taxe_carbone.abaissement_tva_taux_reduit
            elasticite = simulation.calculate('elas_price_3_3', period)
            depenses_tva_taux_reduit_ajustees = \
                depenses_tva_taux_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_reduit) / (1 + taux_reduit))

            return depenses_tva_taux_reduit_ajustees


    class depenses_tva_taux_super_reduit_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Dépenses sur les biens assujetis à la TVA à taux super reduit après réaction à la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_tva_taux_super_reduit = simulation.calculate('depenses_tva_taux_super_reduit', period)
            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            abaissement_tva_taux_super_reduit = parameters(period.start).taxe_carbone.abaissement_tva_taux_super_reduit
            elasticite = simulation.calculate('elas_price_3_3', period)
            depenses_tva_taux_super_reduit_ajustees = \
                depenses_tva_taux_super_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_super_reduit) / (1 + taux_super_reduit))

            return depenses_tva_taux_super_reduit_ajustees


    class diesel_ticpe(YearlyVariable):
        label = u"Calcul du montant de TICPE sur le diesel après réforme"
        use_baseline =ticpe.diesel_ticpe

        def formula(self, simulation, period):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            try:
                majoration_ticpe_diesel = \
                    parameters(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
                accise_diesel = parameters(period.start).imposition_indirecte.ticpe.ticpe_gazole
                accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
            except:
                accise_diesel_ticpe = parameters(period.start).imposition_indirecte.ticpe.ticpe_gazole

            reforme_diesel = parameters(period.start).taxe_carbone.diesel
            accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
            prix_diesel_ttc = parameters(period.start).imposition_indirecte.prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
            taux_implicite_diesel_ajuste = (
                (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
                (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                )

            depenses_diesel_ajustees_taxe_carbone = \
                simulation.calculate('depenses_diesel_corrigees_ajustees_taxe_carbone', period)
            depenses_diesel_htva_ajustees = (
                depenses_diesel_ajustees_taxe_carbone -
                tax_from_expense_including_tax(depenses_diesel_ajustees_taxe_carbone, taux_plein_tva)
                )
            montant_diesel_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
                )

            return montant_diesel_ticpe_ajuste


    class emissions_CO2_carburants(YearlyVariable):
        label = u"Emissions de CO2 des ménages via leur consommation de carburants après réforme, en kg de CO2"
        # use_baseline =emissions_co2.emissions_CO2_carburants

        def formula(self, simulation, period):
            quantites_diesel_ajustees = simulation.calculate('quantites_diesel', period)
            quantites_essence_ajustees = simulation.calculate('quantites_essence', period)
            emissions_diesel = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
            emissions_essence = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
            emissions_ajustees = (
                (quantites_diesel_ajustees * emissions_diesel) +
                (quantites_essence_ajustees * emissions_essence)
                )  # Source : Ademe

            return emissions_ajustees


    class emissions_CO2_energies_totales(YearlyVariable):
        label = u"Emissions de CO2 des ménages via leur conso d'énergies après taxe carbone, en kg de CO2"
        use_baseline =emissions_co2.emissions_CO2_energies_totales

        def formula(self, simulation, period):
            emissions_carburants_ajustees = simulation.calculate('emissions_CO2_carburants', period)
            emissions_electricite_ajustees = simulation.calculate('emissions_CO2_electricite', period)
            emissions_combustibles_liquides_ajustees = \
                simulation.calculate('emissions_CO2_combustibles_liquides', period)
            emissions_gaz_ajustees = simulation.calculate('emissions_CO2_gaz_ville', period)

            emissions_energies_ajustees = (
                emissions_carburants_ajustees + emissions_electricite_ajustees +
                emissions_combustibles_liquides_ajustees + emissions_gaz_ajustees
                )
            return emissions_energies_ajustees


    class emissions_CO2_electricite(YearlyVariable):
        label = u"Emissions de CO2 des ménages via leur consommation d'électricité après réforme, en kg de CO2"
        use_baseline =emissions_co2.emissions_CO2_electricite

        def formula(self, simulation, period):
            quantites_electricite_ajustees = simulation.calculate('quantites_electricite_selon_compteur_ajustees_taxe_carbone', period)
            emissions_eletricite = \
                parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_electricite
            emissions_ajustees = quantites_electricite_ajustees * emissions_eletricite

            return emissions_ajustees


    class emissions_CO2_combustibles_liquides(YearlyVariable):
        label = u"Emissions de CO2 des ménages via leur consommation de fioul après réforme, en kg de CO2"
        use_baseline =emissions_co2.emissions_CO2_combustibles_liquides

        def formula(self, simulation, period):
            quantites_combustibles_liquides_ajustees = simulation.calculate('quantites_combustibles_liquides', period)
            emissions_combustibles_liquides = \
                parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_combustibles_liquides
            emissions_ajustees = quantites_combustibles_liquides_ajustees * emissions_combustibles_liquides

            return emissions_ajustees


    class emissions_CO2_gaz_ville(YearlyVariable):
        label = u"Emissions de CO2 des ménages via leur consommation de gaz après réforme, en kg de CO2"
        use_baseline =emissions_co2.emissions_CO2_gaz_ville

        def formula(self, simulation, period):
            quantites_gaz_ajustees = simulation.calculate('quantites_gaz_final_ajustees_taxe_carbone', period)
            emissions_gaz = \
                parameters(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_gaz_ville
            emissions_ajustees = quantites_gaz_ajustees * emissions_gaz

            return emissions_ajustees


    class essence_ticpe(YearlyVariable):
        label = u"Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"
        use_baseline =ticpe.essence_ticpe
        definition_period = YEAR

        def formula_2009(self, simulation, period):
            sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe', period)
            sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe', period)
            sp_e10_ticpe_ajustee = simulation.calculate('sp_e10_ticpe', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_2007(self, simulation, period):
            sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe', period)
            sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_1990(self, simulation, period):
            sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe', period)
            sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe', period)
            super_plombe_ticpe_ajustee = simulation.calculate('super_plombe_ticpe', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
            return essence_ticpe_ajustee


    class combustibles_liquides_ticpe(YearlyVariable):
        label = u"Calcul du montant de TICPE sur le fioul domestique après réforme - taxe carbone"
        use_baseline =ticpe.combustibles_liquides_ticpe

        def formula(self, simulation, period):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            accise_fioul_ticpe = (
                parameters(period.start).imposition_indirecte.ticpe.gazole_fioul_domestique_hectolitre / 100
                )
            reforme_fioul = parameters(period.start).taxe_carbone.combustibles_liquides
            accise_fioul_ajustee = accise_fioul_ticpe + reforme_fioul
            prix_fioul_ttc = \
                parameters(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
            prix_fioul_ttc_ajuste = prix_fioul_ttc + reforme_fioul

            taux_implicite_fioul_ajuste = (
                (accise_fioul_ajustee * (1 + taux_plein_tva)) /
                (prix_fioul_ttc_ajuste - accise_fioul_ajustee * (1 + taux_plein_tva))
                )

            depenses_fioul_ajustees = simulation.calculate('depenses_combustibles_liquides_ajustees_taxe_carbone', period)
            depenses_fioul_ajustees_htva = \
                depenses_fioul_ajustees - tax_from_expense_including_tax(depenses_fioul_ajustees, taux_plein_tva)
            montant_fioul_ticpe_ajuste = \
                tax_from_expense_including_tax(depenses_fioul_ajustees_htva, taux_implicite_fioul_ajuste)

            return montant_fioul_ticpe_ajuste


    class quantites_diesel(YearlyVariable):
        label = u"Quantités de diesel consommées après la réforme - taxe carbone "
        use_baseline =quantites_energie.quantites_diesel

        def formula(self, simulation, period):
            depenses_diesel_ajustees_taxe_carbone = \
                simulation.calculate('depenses_diesel_corrigees_ajustees_taxe_carbone', period)
            diesel_ttc = parameters(period.start).imposition_indirecte.prix_carburants.diesel_ttc
            reforme_diesel = parameters(period.start).taxe_carbone.diesel
            quantites_diesel_ajustees = depenses_diesel_ajustees_taxe_carbone / (diesel_ttc + reforme_diesel) * 100

            return quantites_diesel_ajustees


    class quantites_combustibles_liquides(YearlyVariable):
        label = u"Quantités de fioul domestique consommées après la réforme - taxe carbone "
        use_baseline =quantites_energie.quantites_combustibles_liquides

        def formula(self, simulation, period):
            depenses_combustibles_liquides_ajustees_taxe_carbone = \
                simulation.calculate('depenses_combustibles_liquides_ajustees_taxe_carbone', period)
            prix_fioul_ttc = \
                parameters(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
            reforme_fioul = parameters(period.start).taxe_carbone.combustibles_liquides
            quantites_combustibles_liquides_ajustees = depenses_combustibles_liquides_ajustees_taxe_carbone / (prix_fioul_ttc + reforme_fioul)

            return quantites_combustibles_liquides_ajustees


    class quantites_gaz_final_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Quantités de gaz consommées après la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_gaz_ajustees_taxe_carbone = simulation.calculate('depenses_gaz_ville_ajustees_taxe_carbone', period)
            depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
            depenses_gaz_ajustees_variables = depenses_gaz_ajustees_taxe_carbone - depenses_gaz_tarif_fixe

            depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
            reforme_gaz = parameters(period.start).taxe_carbone.gaz

            quantites_gaz_ajustees = depenses_gaz_ajustees_variables / (depenses_gaz_prix_unitaire + reforme_gaz)

            return quantites_gaz_ajustees


    class quantites_electricite_selon_compteur_ajustees_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Quantités d'électricité consommées après la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_electricite_ajustees_taxe_carbone = \
                simulation.calculate('depenses_electricite_ajustees_taxe_carbone', period)
            depenses_electricite_tarif_fixe = simulation.calculate('depenses_electricite_tarif_fixe', period)
            depenses_electricite_ajustees_variables = \
                depenses_electricite_ajustees_taxe_carbone - depenses_electricite_tarif_fixe

            depenses_electricite_prix_unitaire = simulation.calculate('depenses_electricite_prix_unitaire', period)
            reforme_electricite = parameters(period.start).taxe_carbone.electricite

            quantites_electricite_ajustees = \
                depenses_electricite_ajustees_variables / (depenses_electricite_prix_unitaire + reforme_electricite)

            quantites_electricite_avant_reforme = simulation.calculate('quantites_electricite_selon_compteur', period)
            quantites_electricite_ajustees = (
                quantites_electricite_ajustees * (quantites_electricite_avant_reforme > 0)
                )

            return quantites_electricite_ajustees


    class quantites_sp_e10(YearlyVariable):
        label = u"Quantités consommées de sans plomb e10 par les ménages après réforme - taxe carbone"
        use_baseline =quantites_energie.quantites_sp_e10

        def formula(self, simulation, period):
            depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_corrigees_ajustees_taxe_carbone', period)
            part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            depenses_sp_e10_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp_e10
            super_95_e10_ttc = parameters(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
            reforme_essence = parameters(period.start).taxe_carbone.essence
            quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

            return quantite_sp_e10


    class quantites_sp95(YearlyVariable):
        label = u"Quantités consommées de sans plomb 95 par les ménages après réforme"
        use_baseline =quantites_energie.quantites_sp95

        def formula(self, simulation, period):
            depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_corrigees_ajustees_taxe_carbone', period)
            part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp95_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp95
            super_95_ttc = parameters(period.start).imposition_indirecte.prix_carburants.super_95_ttc
            reforme_essence = parameters(period.start).taxe_carbone.essence
            quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

            return quantites_sp95_ajustees


    class quantites_sp98(YearlyVariable):
        label = u"Quantités consommées de sans plomb 98 par les ménages"
        use_baseline =quantites_energie.quantites_sp98

        def formula(self, simulation, period):
            depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_corrigees_ajustees_taxe_carbone', period)
            part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp98_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp98
            super_98_ttc = parameters(period.start).imposition_indirecte.prix_carburants.super_98_ttc
            reforme_essence = parameters(period.start).taxe_carbone.essence
            quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

            return quantites_sp98_ajustees


    class quantites_super_plombe(YearlyVariable):
        label = u"Quantités consommées de super plombé par les ménages après réforme"
        use_baseline =quantites_energie.quantites_super_plombe

        def formula(self, simulation, period):
            depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_corrigees_ajustees_taxe_carbone', period)
            part_super_plombe = \
                parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_ajustees_taxe_carbone * part_super_plombe
            super_plombe_ttc = parameters(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
            reforme_essence = parameters(period.start).taxe_carbone.essence
            quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

            return quantites_super_plombe_ajustees

    class quantites_essence(YearlyVariable):
        label = u"Quantités d'essence consommées par les ménages après réforme"
        use_baseline =quantites_energie.quantites_essence
        definition_period = YEAR

        def formula_2009(self, simulation, period):
            quantites_sp95_ajustees = simulation.calculate('quantites_sp95', period)
            quantites_sp98_ajustees = simulation.calculate('quantites_sp98', period)
            quantites_sp_e10_ajustees = simulation.calculate('quantites_sp_e10', period)
            quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
            return quantites_essence_ajustees

        def formula_2007(self, simulation, period):
            quantites_sp95_ajustees = simulation.calculate('quantites_sp95', period)
            quantites_sp98_ajustees = simulation.calculate('quantites_sp98', period)
            quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
            return quantites_essence_ajustees

        def formula_1990(self, simulation, period):
            quantites_sp95_ajustees = simulation.calculate('quantites_sp95', period)
            quantites_sp98_ajustees = simulation.calculate('quantites_sp98', period)
            quantites_super_plombe_ajustees = \
                simulation.calculate('quantites_super_plombe', period)
            quantites_essence_ajustees = (
                quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
                )
            return quantites_essence_ajustees


    class sp_e10_ticpe(YearlyVariable):
        label = u"Calcul du montant de la TICPE sur le SP E10 après réforme"
        use_baseline =ticpe.sp_e10_ticpe

        def formula(self, simulation, period):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            try:
                accise_super_e10 = \
                    parameters(period.start).imposition_indirecte.ticpe.ticpe_super_e10
                majoration_ticpe_super_e10 = \
                    parameters(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
                accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
            except:
                accise_ticpe_super_e10 = \
                    parameters(period.start).imposition_indirecte.ticpe.ticpe_super_e10

            reforme_essence = parameters(period.start).taxe_carbone.essence
            accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
            super_95_e10_ttc = parameters(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
            super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
            taux_implicite_sp_e10_ajuste = (
                (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva)) /
                (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_taxe_carbone = \
                simulation.calculate('depenses_essence_corrigees_ajustees_taxe_carbone', period)
            part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            sp_e10_depenses_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp_e10
            sp_e10_depenses_htva_ajustees = \
                sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
            montant_sp_e10_ticpe_ajuste = \
                tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

            return montant_sp_e10_ticpe_ajuste

    class sp95_ticpe(YearlyVariable):
        label = u"Calcul du montant de TICPE sur le sp_95 après réforme"
        use_baseline =ticpe.sp95_ticpe

        def formula(self, simulation, period):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            try:
                accise_super95 = parameters(period.start).imposition_indirecte.ticpe.ticpe_super9598
                majoration_ticpe_super95 = \
                    parameters(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
                accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
            except:
                accise_ticpe_super95 = parameters(period.start).imposition_indirecte.ticpe.ticpe_super9598

            reforme_essence = parameters(period.start).taxe_carbone.essence
            accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
            super_95_ttc = parameters(period.start).imposition_indirecte.prix_carburants.super_95_ttc
            super_95_ttc_ajuste = super_95_ttc + reforme_essence
            taux_implicite_sp95_ajuste = (
                (accise_ticpe_super95_ajustee * (1 + taux_plein_tva)) /
                (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_taxe_carbone = \
                simulation.calculate('depenses_essence_corrigees_ajustees_taxe_carbone', period)
            part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp_95_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp95
            depenses_sp_95_htva_ajustees = (
                depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
                )
            montant_sp95_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
                )

            return montant_sp95_ticpe_ajuste

    class sp98_ticpe(YearlyVariable):
        label = u"Calcul du montant de TICPE sur le sp_98 après réforme"
        use_baseline =ticpe.sp98_ticpe

        def formula(self, simulation, period):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            try:
                accise_super98 = parameters(period.start).imposition_indirecte.ticpe.ticpe_super9598
                majoration_ticpe_super98 = \
                    parameters(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
                accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
            except:
                accise_ticpe_super98 = parameters(period.start).imposition_indirecte.ticpe.ticpe_super9598

            reforme_essence = parameters(period.start).taxe_carbone.essence
            accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
            super_98_ttc = parameters(period.start).imposition_indirecte.prix_carburants.super_98_ttc
            super_98_ttc_ajuste = super_98_ttc + reforme_essence
            taux_implicite_sp98_ajuste = (
                (accise_ticpe_super98_ajustee * (1 + taux_plein_tva)) /
                (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_taxe_carbone = \
                simulation.calculate('depenses_essence_corrigees_ajustees_taxe_carbone', period)
            part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp_98_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp98
            depenses_sp_98_htva_ajustees = (
                depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
                )
            montant_sp98_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
                )

            return montant_sp98_ticpe_ajuste

    class super_plombe_ticpe(YearlyVariable):
        label = u"Calcul du montant de la TICPE sur le super plombé après réforme"
        use_baseline =ticpe.super_plombe_ticpe

        def formula(self, simulation, period):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            accise_super_plombe_ticpe = \
                parameters(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

            reforme_essence = parameters(period.start).taxe_carbone.essence
            accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
            super_plombe_ttc = parameters(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
            super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
            taux_implicite_super_plombe_ajuste = (
                (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva)) /
                (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_taxe_carbone = \
                simulation.calculate('depenses_essence_corrigees_ajustees_taxe_carbone', period)
            part_super_plombe = \
                parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_ajustees_taxe_carbone * part_super_plombe
            depenses_super_plombe_htva_ajustees = (
                depenses_super_plombe_ajustees -
                tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
                )
            montant_super_plombe_ticpe_ajuste = \
                tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

            return montant_super_plombe_ticpe_ajuste

    class taxe_electricite(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Recettes de la taxe carbone sur la consommation d'électricité - ceteris paribus"
        # On considère que les contributions sur les taxes précédentes ne sont pas affectées

        def formula(self, simulation, period):
            quantites_electricite_ajustees = simulation.calculate('quantites_electricite_selon_compteur_ajustees_taxe_carbone', period)
            reforme_electricite = parameters(period.start).taxe_carbone.electricite
            recettes_electricite = quantites_electricite_ajustees * reforme_electricite

            return recettes_electricite

    class taxe_gaz(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Recettes de la taxe carbone sur la consommation de gaz - ceteris paribus"
        # On considère que les contributions sur les taxes précédentes ne sont pas affectées

        def formula(self, simulation, period):
            quantites_gaz_ajustees = simulation.calculate('quantites_gaz_final_ajustees_taxe_carbone', period)
            reforme_gaz = parameters(period.start).taxe_carbone.gaz
            recettes_gaz = quantites_gaz_ajustees * reforme_gaz

            return recettes_gaz

    class ticpe_totale(YearlyVariable):
        label = u"Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"
        use_baseline =ticpe.ticpe_totale

        def formula(self, simulation, period):
            essence_ticpe_ajustee = simulation.calculate('essence_ticpe', period)
            diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe', period)
            ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

            return ticpe_totale_ajustee

    class total_taxes_energies_taxe_carbone(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Différence entre les contributions aux taxes sur l'énergie après la taxe carbone"

        def formula(self, simulation, period):
            taxe_diesel = simulation.calculate('diesel_ticpe', period)
            taxe_electricite = simulation.calculate('taxe_electricite', period)
            taxe_essence = simulation.calculate('essence_ticpe', period)
            taxe_combustibles_liquides = simulation.calculate('combustibles_liquides_ticpe', period)
            taxe_gaz = simulation.calculate('taxe_gaz', period)

            total = (
                taxe_diesel + taxe_electricite + taxe_essence + taxe_combustibles_liquides + taxe_gaz
                )

            return total

    class tva_taux_plein(YearlyVariable):
        label = u"Contribution sur la TVA à taux plein après réaction à la réforme - taxe carbone"
        use_baseline =tva.tva_taux_plein

        def formula(self, simulation, period):
            depenses_tva_taux_plein_ajustees = \
                simulation.calculate('depenses_tva_taux_plein_ajustees_taxe_carbone', period)

            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein = parameters(period.start).taxe_carbone.abaissement_tva_taux_plein
            nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

            return tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)

    class tva_taux_plein_bis(YearlyVariable):
        value_type = float
        entity = Menage
        label = u"Contribution sur la TVA à taux plein après réaction à la réforme - taxe carbone"

        def formula(self, simulation, period):
            depenses_tva_taux_plein_ajustees = \
                simulation.calculate('depenses_tva_taux_plein_bis_ajustees_taxe_carbone', period)

            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein = \
                parameters(period.start).taxe_carbone.abaissement_tva_taux_plein_bis
            nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

            return tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)

    class tva_taux_reduit(YearlyVariable):
        label = u"Contribution sur la TVA à taux reduit après réaction à la réforme - taxe carbone"
        use_baseline =tva.tva_taux_reduit

        def formula(self, simulation, period):
            depenses_tva_taux_reduit_ajustees = \
                simulation.calculate('depenses_tva_taux_reduit_ajustees_taxe_carbone', period)

            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            abaissement_tva_taux_reduit = \
                parameters(period.start).taxe_carbone.abaissement_tva_taux_reduit
            nouveau_taux_reduit = taux_reduit - abaissement_tva_taux_reduit

            return tax_from_expense_including_tax(depenses_tva_taux_reduit_ajustees, nouveau_taux_reduit)

    class tva_taux_super_reduit(YearlyVariable):
        label = u"Contribution sur la TVA à taux super reduit après réaction à la réforme - taxe carbone"
        use_baseline =tva.tva_taux_super_reduit

        def formula(self, simulation, period):
            depenses_tva_taux_super_reduit_ajustees = \
                simulation.calculate('depenses_tva_taux_super_reduit_ajustees_taxe_carbone', period)

            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            abaissement_tva_taux_super_reduit = \
                parameters(period.start).taxe_carbone.abaissement_tva_taux_super_reduit
            nouveau_taux_super_reduit = taux_super_reduit - abaissement_tva_taux_super_reduit

            return \
                tax_from_expense_including_tax(depenses_tva_taux_super_reduit_ajustees, nouveau_taux_super_reduit)

    class tva_total(YearlyVariable):
        label = u"Différence de contribution sur la TVA après réaction à la réforme - taxes carburants"
        use_baseline =tva.tva_total

        def formula(self, simulation, period):
            taux_plein = simulation.calculate('tva_taux_plein_bis', period)
            taux_reduit = simulation.calculate('tva_taux_reduit', period)
            taux_super_reduit = simulation.calculate('tva_taux_super_reduit', period)
            taux_intermediaire = simulation.calculate('tva_taux_intermediaire', period)

            total = (taux_plein + taux_reduit + taux_super_reduit + taux_intermediaire)

            return total


    def apply(self):
        self.update_variable(self.cheques_energie)
        self.update_variable(self.contributions_reforme)
        self.update_variable(self.depenses_carburants_corrigees_ajustees_taxe_carbone)
        self.update_variable(self.depenses_diesel_corrigees_ajustees_taxe_carbone)
        self.update_variable(self.depenses_electricite_ajustees_taxe_carbone)
        self.update_variable(self.depenses_essence_corrigees_ajustees_taxe_carbone)
        self.update_variable(self.depenses_combustibles_liquides_ajustees_taxe_carbone)
        self.update_variable(self.depenses_gaz_ville_ajustees_taxe_carbone)
        self.update_variable(self.depenses_energies_logement_ajustees_taxe_carbone)
        self.update_variable(self.depenses_tva_taux_plein_ajustees_taxe_carbone)
        self.update_variable(self.depenses_tva_taux_plein_bis_ajustees_taxe_carbone)
        self.update_variable(self.depenses_tva_taux_reduit_ajustees_taxe_carbone)
        self.update_variable(self.depenses_tva_taux_super_reduit_ajustees_taxe_carbone)
        self.update_variable(self.diesel_ticpe)
        self.update_variable(self.emissions_CO2_carburants)
        self.update_variable(self.emissions_CO2_energies_totales)
        self.update_variable(self.emissions_CO2_electricite)
        self.update_variable(self.emissions_CO2_combustibles_liquides)
        self.update_variable(self.emissions_CO2_gaz_ville)
        self.update_variable(self.essence_ticpe)
        self.update_variable(self.combustibles_liquides_ticpe)
        self.update_variable(self.quantites_diesel)
        self.update_variable(self.quantites_combustibles_liquides)
        self.update_variable(self.quantites_gaz_final_ajustees_taxe_carbone)
        self.update_variable(self.quantites_electricite_selon_compteur_ajustees_taxe_carbone)
        self.update_variable(self.quantites_sp_e10)
        self.update_variable(self.quantites_sp95)
        self.update_variable(self.quantites_sp98)
        self.update_variable(self.quantites_super_plombe)
        self.update_variable(self.quantites_essence)
        self.update_variable(self.sp_e10_ticpe)
        self.update_variable(self.sp95_ticpe)
        self.update_variable(self.sp98_ticpe)
        self.update_variable(self.super_plombe_ticpe)
        self.update_variable(self.taxe_electricite)
        self.update_variable(self.taxe_gaz)
        self.update_variable(self.ticpe_totale)
        self.update_variable(self.total_taxes_energies_taxe_carbone)
        self.update_variable(self.tva_taux_plein)
        self.update_variable(self.tva_taux_plein_bis)
        self.update_variable(self.tva_taux_reduit)
        self.update_variable(self.tva_taux_super_reduit)
        self.update_variable(self.tva_total)
        self.modify_legislation_json(modifier_function = modify_legislation_json)
