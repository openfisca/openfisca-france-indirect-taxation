# -*- coding: utf-8 -*-

from __future__ import division

from datetime import date
from openfisca_core.reforms import Reform, update_legislation

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore
from ..model.taxes_indirectes import tva, ticpe
from ..model.consommation import emissions_co2, quantites_energie

# from openfisca_core.columns import FloatCol
# from ..entities import Menages
# from openfisca_core.formulas import (dated_function)


# Réforme selon le prix du carbone : prix fixé à 50 euros par tonne de CO2. En utilisant nos données
# d'équivalence entre consommation et émission, on met en place les montants de taxe suivants :

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
                "values": [{'start': u'2010-01-01', 'stop': '2014-12-31', 'value': 0.0045}],
                },
            "essence": {
                "@type": "Parameter",
                "description": u"Surcroît de prix de l'essence (en euros par hectolitres)",
                "format": "float",
                "unit": 'currency',
                "values": [{'start': u'2010-01-01', 'stop': '2014-12-31', 'value': 12.1 - 1.694}],
                },
            "diesel": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du diesel (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2010-01-01', 'stop': '2014-12-31', 'value': 13.3 - 1.862}],
                },
            "fioul_domestique": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du diesel (en euros par litre)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2010-01-01', 'stop': '2014-12-31', 'value': 0.155 - 0.0217}],
                },
            "gaz": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du gaz (en euros par kWh)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2010-01-01', 'stop': '2014-12-31', 'value': 0.012 - 0.00168}],
                },
            "abaissement_tva_taux_plein": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.026}],
                },
            "abaissement_tva_taux_plein_bis": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.01}],
                },
            "abaissement_tva_taux_reduit": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.03}],
                },
            "abaissement_tva_taux_super_reduit": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.01}],
                },
            },
        }

    reference_legislation_json_copy['children']['taxe_carbone'] = reform_legislation_subtree
    return reference_legislation_json_copy


class depenses_diesel_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en diesel après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = simulation.legislation_at(period.start).taxe_carbone.diesel
        carburants_elasticite_prix = simulation.calculate('elas_price_1_1')
        depenses_diesel_ajustees_taxe_carbone = \
            depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

        return period, depenses_diesel_ajustees_taxe_carbone


class depenses_electricite_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en électricité après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_electricite_variables = simulation.calculate('depenses_electricite_variables', period)
        depenses_electricite_prix_unitaire = simulation.calculate('depenses_electricite_prix_unitaire', period)
        reforme_electricite = simulation.legislation_at(period.start).taxe_carbone.electricite
        electricite_elasticite_prix = simulation.calculate('elas_price_2_2')
        depenses_electricite_ajustees_variables = (
            depenses_electricite_variables *
            (1 + (1 + electricite_elasticite_prix) * reforme_electricite / depenses_electricite_prix_unitaire)
            )
        depenses_electricite_tarif_fixe = simulation.calculate('depenses_electricite_tarif_fixe', period)
        min_tarif_fixe = depenses_electricite_tarif_fixe.min()
        depenses_electricite_ajustees = depenses_electricite_ajustees_variables + depenses_electricite_tarif_fixe

        # We do not want to input the expenditure of the contract for those who consume nothing
        poste_coicop_451 = simulation.calculate('poste_coicop_451', period)
        depenses_electricite_ajustees = (
            depenses_electricite_ajustees * (poste_coicop_451 > min_tarif_fixe) +
            poste_coicop_451 * (poste_coicop_451 < min_tarif_fixe)
            )

        return period, depenses_electricite_ajustees


class depenses_essence_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en essence après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence', period)
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        carburants_elasticite_prix = simulation.calculate('elas_price_1_1')
        depenses_essence_ajustees_taxe_carbone = \
            depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence / super_95_ttc)

        return period, depenses_essence_ajustees_taxe_carbone


class depenses_fioul_domestique_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en fioul domestique après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_fioul = simulation.calculate('poste_04_5_3_1_1', period)
        prix_fioul_ttc = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
        reforme_fioul = simulation.legislation_at(period.start).taxe_carbone.fioul_domestique
        fioul_elasticite_prix = simulation.calculate('elas_price_2_2')
        depenses_fioul_ajustees_taxe_carbone = \
            depenses_fioul * (1 + (1 + fioul_elasticite_prix) * reforme_fioul / prix_fioul_ttc)

        return period, depenses_fioul_ajustees_taxe_carbone


class depenses_gaz_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en gaz après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_gaz_variables = simulation.calculate('depenses_gaz_variables', period)
        depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
        reforme_gaz = simulation.legislation_at(period.start).taxe_carbone.gaz
        gaz_elasticite_prix = simulation.calculate('elas_price_2_2')
        depenses_gaz_ajustees_variables = \
            depenses_gaz_variables * (1 + (1 + gaz_elasticite_prix) * reforme_gaz / depenses_gaz_prix_unitaire)
        depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
        depenses_gaz_ajustees = depenses_gaz_ajustees_variables + depenses_gaz_tarif_fixe
        depenses_gaz_ajustees[numpy.isnan(depenses_gaz_ajustees)] = 0
        depenses_gaz_ajustees[numpy.isinf(depenses_gaz_ajustees)] = 0

        return period, depenses_gaz_ajustees


class depenses_tva_taux_plein_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses sur les biens assujetis à la TVA à taux plein après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_plein
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_ajustees = \
            depenses_tva_taux_plein * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))

        return period, depenses_tva_taux_plein_ajustees


class depenses_tva_taux_plein_bis_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses sur les biens assujetis à la TVA à taux plein bis après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein_bis = simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_plein_bis
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_bis_ajustees = (
            depenses_tva_taux_plein *
            (1 + (1 + elasticite) * (- abaissement_tva_taux_plein_bis) / (1 + taux_plein))
            )

        return period, depenses_tva_taux_plein_bis_ajustees


class depenses_tva_taux_reduit_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses sur les biens assujetis à la TVA à taux reduit après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_tva_taux_reduit = simulation.calculate('depenses_tva_taux_reduit', period)
        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        abaissement_tva_taux_reduit = simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_reduit
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_reduit_ajustees = \
            depenses_tva_taux_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_reduit) / (1 + taux_reduit))

        return period, depenses_tva_taux_reduit_ajustees


class depenses_tva_taux_super_reduit_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses sur les biens assujetis à la TVA à taux super reduit après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_tva_taux_super_reduit = simulation.calculate('depenses_tva_taux_super_reduit', period)
        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        abaissement_tva_taux_super_reduit = simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_super_reduit
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_super_reduit_ajustees = \
            depenses_tva_taux_super_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_super_reduit) / (1 + taux_super_reduit))

        return period, depenses_tva_taux_super_reduit_ajustees


class diesel_ticpe(Variable):
    label = u"Calcul du montant de TICPE sur le diesel après réforme"
    reference = ticpe.diesel_ticpe

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        reforme_diesel = simulation.legislation_at(period.start).taxe_carbone.diesel
        accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
        taux_implicite_diesel_ajuste = (
            (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva)) /
            (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
            )

        depenses_diesel_ajustees_taxe_carbone = \
            simulation.calculate('depenses_diesel_ajustees_taxe_carbone', period)
        depenses_diesel_htva_ajustees = (
            depenses_diesel_ajustees_taxe_carbone -
            tax_from_expense_including_tax(depenses_diesel_ajustees_taxe_carbone, taux_plein_tva)
            )
        montant_diesel_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
            )

        return period, montant_diesel_ticpe_ajuste


class emissions_CO2_carburants(Variable):
    label = u"Emissions de CO2 des ménages via leur consommation de carburants après réforme, en kg de CO2"
    # reference = emissions_co2.emissions_CO2_carburants

    def function(self, simulation, period):
        quantites_diesel_ajustees = simulation.calculate('quantites_diesel', period)
        quantites_essence_ajustees = simulation.calculate('quantites_essence', period)
        emissions_diesel = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
        emissions_essence = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
        emissions_ajustees = (
            (quantites_diesel_ajustees * emissions_diesel) +
            (quantites_essence_ajustees * emissions_essence)
            )  # Source : Ademe

        return period, emissions_ajustees


class emissions_CO2_energies(Variable):
    label = u"Emissions de CO2 des ménages via leur conso d'énergies après taxe carbone, en kg de CO2"
    # # reference = emissions_co2.emissions_CO2_energies

    def function(self, simulation, period):
        emissions_carburants_ajustees = simulation.calculate('emissions_CO2_carburants', period)
        emissions_electricite_ajustees = simulation.calculate('emissions_CO2_electricite', period)
        emissions_fioul_domestique_ajustees = \
            simulation.calculate('emissions_CO2_fioul_domestique', period)
        emissions_gaz_ajustees = simulation.calculate('emissions_CO2_gaz', period)

        emissions_energies_ajustees = (
            emissions_carburants_ajustees + emissions_electricite_ajustees +
            emissions_fioul_domestique_ajustees + emissions_gaz_ajustees
            )
        return period, emissions_energies_ajustees


class emissions_CO2_electricite(Variable):
    label = u"Emissions de CO2 des ménages via leur consommation d'électricité après réforme, en kg de CO2"
    # reference = emissions_co2.emissions_CO2_electricite

    def function(self, simulation, period):
        quantites_electricite_ajustees = simulation.calculate('quantites_electricite_selon_compteur_ajustees_taxe_carbone', period)
        emissions_eletricite = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_electricite
        emissions_ajustees = quantites_electricite_ajustees * emissions_eletricite

        return period, emissions_ajustees


class emissions_CO2_fioul_domestique(Variable):
    label = u"Emissions de CO2 des ménages via leur consommation de fioul après réforme, en kg de CO2"
    # reference = emissions_co2.emissions_CO2_fioul_domestique

    def function(self, simulation, period):
        quantites_fioul_ajustees = simulation.calculate('quantites_fioul_domestique', period)
        emissions_fioul = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_fioul_domestique
        emissions_ajustees = quantites_fioul_ajustees * emissions_fioul

        return period, emissions_ajustees


class emissions_CO2_gaz(Variable):
    label = u"Emissions de CO2 des ménages via leur consommation de gaz après réforme, en kg de CO2"
    # reference = emissions_co2.emissions_CO2_gaz

    def function(self, simulation, period):
        quantites_gaz_ajustees = simulation.calculate('quantites_gaz_contrat_optimal_ajustees_taxe_carbone', period)
        emissions_gaz = \
            simulation.legislation_at(period.start).imposition_indirecte.emissions_CO2.energie_logement.CO2_gaz
        emissions_ajustees = quantites_gaz_ajustees * emissions_gaz

        return period, emissions_ajustees


class essence_ticpe(Variable):
    label = u"Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"
    reference = ticpe.essence_ticpe

    # @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe', period)
        super_plombe_ticpe_ajustee = simulation.calculate('super_plombe_ticpe', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    # @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
        return period, essence_ticpe_ajustee

    # @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        sp95_ticpe_ajustee = simulation.calculate('sp95_ticpe', period)
        sp98_ticpe_ajustee = simulation.calculate('sp98_ticpe', period)
        sp_e10_ticpe_ajustee = simulation.calculate('sp_e10_ticpe', period)
        essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
        return period, essence_ticpe_ajustee


class fioul_domestique_ticpe(Variable):
    label = u"Calcul du montant de TICPE sur le fioul domestique après réforme - taxe carbone"
    # reference = ticpe.fioul_domestique_ticpe

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        accise_fioul_ticpe = (
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.gazole_fioul_domestique_hectolitre / 100
            )
        reforme_fioul = simulation.legislation_at(period.start).taxe_carbone.fioul_domestique
        accise_fioul_ajustee = accise_fioul_ticpe + reforme_fioul
        prix_fioul_ttc = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
        prix_fioul_ttc_ajuste = prix_fioul_ttc + reforme_fioul

        taux_implicite_fioul_ajuste = (
            (accise_fioul_ajustee * (1 + taux_plein_tva)) /
            (prix_fioul_ttc_ajuste - accise_fioul_ajustee * (1 + taux_plein_tva))
            )

        depenses_fioul_ajustees = simulation.calculate('depenses_fioul_domestique_ajustees_taxe_carbone', period)
        depenses_fioul_ajustees_htva = \
            depenses_fioul_ajustees - tax_from_expense_including_tax(depenses_fioul_ajustees, taux_plein_tva)
        montant_fioul_ticpe_ajuste = \
            tax_from_expense_including_tax(depenses_fioul_ajustees_htva, taux_implicite_fioul_ajuste)

        return period, montant_fioul_ticpe_ajuste


class quantites_diesel(Variable):
    label = u"Quantités de diesel consommées après la réforme - taxe carbone "
    reference = quantites_energie.quantites_diesel

    def function(self, simulation, period):
        depenses_diesel_ajustees_taxe_carbone = \
            simulation.calculate('depenses_diesel_ajustees_taxe_carbone', period)
        diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        reforme_diesel = simulation.legislation_at(period.start).taxe_carbone.diesel
        quantites_diesel_ajustees = depenses_diesel_ajustees_taxe_carbone / (diesel_ttc + reforme_diesel) * 100

        return period, quantites_diesel_ajustees


class quantites_fioul_domestique(Variable):
    label = u"Quantités de fioul domestique consommées après la réforme - taxe carbone "
    # reference = quantites_energie.quantites_fioul_domestique

    def function(self, simulation, period):
        depenses_fioul_ajustees_taxe_carbone = \
            simulation.calculate('depenses_fioul_domestique_ajustees_taxe_carbone', period)
        prix_fioul_ttc = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_fioul_domestique.prix_annuel_moyen_du_fioul_domestique_ttc_livraisons_de_2000_a_4999_litres_en_euro_par_litre
        reforme_fioul = simulation.legislation_at(period.start).taxe_carbone.fioul_domestique
        quantites_fioul_ajustees = depenses_fioul_ajustees_taxe_carbone / (prix_fioul_ttc + reforme_fioul)

        return period, quantites_fioul_ajustees


class quantites_gaz_contrat_optimal_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity = Menage
    label = u"Quantités de gaz consommées après la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_gaz_ajustees_taxe_carbone = simulation.calculate('depenses_gaz_ajustees_taxe_carbone', period)
        depenses_gaz_tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)
        depenses_gaz_ajustees_variables = depenses_gaz_ajustees_taxe_carbone - depenses_gaz_tarif_fixe

        depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
        reforme_gaz = simulation.legislation_at(period.start).taxe_carbone.gaz

        quantites_gaz_ajustees = depenses_gaz_ajustees_variables / (depenses_gaz_prix_unitaire + reforme_gaz)

        return period, quantites_gaz_ajustees


class quantites_electricite_selon_compteur_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity = Menage
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


class quantites_sp_e10(Variable):
    label = u"Quantités consommées de sans plomb e10 par les ménages après réforme - taxe carbone"
    reference = quantites_energie.quantites_sp_e10

    def function(self, simulation, period):
        depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp_e10
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

        return period, quantite_sp_e10


class quantites_sp95(Variable):
    label = u"Quantités consommées de sans plomb 95 par les ménages après réforme"
    reference = quantites_energie.quantites_sp95

    def function(self, simulation, period):
        depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp95_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp95
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

        return period, quantites_sp95_ajustees


class quantites_sp98(Variable):
    label = u"Quantités consommées de sans plomb 98 par les ménages"
    reference = quantites_energie.quantites_sp98

    def function(self, simulation, period):
        depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp98_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp98
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

        return period, quantites_sp98_ajustees


class quantites_super_plombe(Variable):
    label = u"Quantités consommées de super plombé par les ménages après réforme"
    reference = quantites_energie.quantites_super_plombe

    def function(self, simulation, period):
        depenses_essence_ajustees_taxe_carbone = simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_taxe_carbone * part_super_plombe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

        return period, quantites_super_plombe_ajustees

class quantites_essence(Variable):
    label = u"Quantités d'essence consommées par les ménages après réforme"
    reference = quantites_energie.quantites_essence

    # @dated_function(start = date(1990, 1, 1), stop = date(2006, 12, 31))
    def function_90_06(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98', period)
        quantites_super_plombe_ajustees = \
            simulation.calculate('quantites_super_plombe', period)
        quantites_essence_ajustees = (
            quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
            )
        return period, quantites_essence_ajustees

    # @dated_function(start = date(2007, 1, 1), stop = date(2008, 12, 31))
    def function_07_08(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
        return period, quantites_essence_ajustees

    # @dated_function(start = date(2009, 1, 1), stop = date(2015, 12, 31))
    def function_09_15(self, simulation, period):

        quantites_sp95_ajustees = simulation.calculate('quantites_sp95', period)
        quantites_sp98_ajustees = simulation.calculate('quantites_sp98', period)
        quantites_sp_e10_ajustees = simulation.calculate('quantites_sp_e10', period)
        quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
        return period, quantites_essence_ajustees

class sp_e10_ticpe(Variable):
    label = u"Calcul du montant de la TICPE sur le SP E10 après réforme"
    reference = ticpe.sp_e10_ticpe

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        try:
            accise_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10
            majoration_ticpe_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
        except:
            accise_ticpe_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10

        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
        taux_implicite_sp_e10_ajuste = (
            (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva)) /
            (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxe_carbone = \
            simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        sp_e10_depenses_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp_e10
        sp_e10_depenses_htva_ajustees = \
            sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
        montant_sp_e10_ticpe_ajuste = \
            tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

        return period, montant_sp_e10_ticpe_ajuste

class sp95_ticpe(Variable):
    label = u"Calcul du montant de TICPE sur le sp_95 après réforme"
    reference = ticpe.sp95_ticpe

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        super_95_ttc_ajuste = super_95_ttc + reforme_essence
        taux_implicite_sp95_ajuste = (
            (accise_ticpe_super95_ajustee * (1 + taux_plein_tva)) /
            (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxe_carbone = \
            simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp95
        depenses_sp_95_htva_ajustees = (
            depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
            )
        montant_sp95_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
            )

        return period, montant_sp95_ticpe_ajuste

class sp98_ticpe(Variable):
    label = u"Calcul du montant de TICPE sur le sp_98 après réforme"
    reference = ticpe.sp98_ticpe

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        super_98_ttc_ajuste = super_98_ttc + reforme_essence
        taux_implicite_sp98_ajuste = (
            (accise_ticpe_super98_ajustee * (1 + taux_plein_tva)) /
            (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxe_carbone = \
            simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98_ajustees = depenses_essence_ajustees_taxe_carbone * part_sp98
        depenses_sp_98_htva_ajustees = (
            depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
            )
        montant_sp98_ticpe_ajuste = (
            tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
            )

        return period, montant_sp98_ticpe_ajuste

class super_plombe_ticpe(Variable):
    label = u"Calcul du montant de la TICPE sur le super plombé après réforme"
    reference = ticpe.super_plombe_ticpe

    def function(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

        reforme_essence = simulation.legislation_at(period.start).taxe_carbone.essence
        accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
        taux_implicite_super_plombe_ajuste = (
            (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva)) /
            (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
            )
        depenses_essence_ajustees_taxe_carbone = \
            simulation.calculate('depenses_essence_ajustees_taxe_carbone', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe_ajustees = depenses_essence_ajustees_taxe_carbone * part_super_plombe
        depenses_super_plombe_htva_ajustees = (
            depenses_super_plombe_ajustees -
            tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
            )
        montant_super_plombe_ticpe_ajuste = \
            tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

        return period, montant_super_plombe_ticpe_ajuste

class taxe_electricite(Variable):
    column = FloatCol
    entity = Menage
    label = u"Recettes de la taxe carbone sur la consommation d'électricité - ceteris paribus"
    # On considère que les contributions sur les taxes précédentes ne sont pas affectées

    def function(self, simulation, period):
        quantites_electricite_ajustees = simulation.calculate('quantites_electricite_selon_compteur_ajustees_taxe_carbone', period)
        reforme_electricite = simulation.legislation_at(period.start).taxe_carbone.electricite
        recettes_electricite = quantites_electricite_ajustees * reforme_electricite

        return period, recettes_electricite

class taxe_gaz(Variable):
    column = FloatCol
    entity = Menage
    label = u"Recettes de la taxe carbone sur la consommation de gaz - ceteris paribus"
    # On considère que les contributions sur les taxes précédentes ne sont pas affectées

    def function(self, simulation, period):
        quantites_gaz_ajustees = simulation.calculate('quantites_gaz_contrat_optimal_ajustees_taxe_carbone', period)
        reforme_gaz = simulation.legislation_at(period.start).taxe_carbone.gaz
        recettes_gaz = quantites_gaz_ajustees * reforme_gaz

        return period, recettes_gaz

class ticpe_totale(Variable):
    label = u"Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"
    reference = ticpe.ticpe_totale

    def function(self, simulation, period):
        essence_ticpe_ajustee = simulation.calculate('essence_ticpe', period)
        diesel_ticpe_ajustee = simulation.calculate('diesel_ticpe', period)
        ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

        return period, ticpe_totale_ajustee

class total_taxes_energies(Variable):
    label = u"Différence entre les contributions aux taxes sur l'énergie après la taxe carbone"
    # reference = ticpe.total_taxes_energies

    def function(self, simulation, period):
        taxe_diesel = simulation.calculate('diesel_ticpe', period)
        taxe_electricite = simulation.calculate('taxe_electricite', period)
        taxe_essence = simulation.calculate('essence_ticpe', period)
        taxe_fioul_domestique = simulation.calculate('fioul_domestique_ticpe', period)
        taxe_gaz = simulation.calculate('taxe_gaz', period)

        total = (
            taxe_diesel + taxe_electricite + taxe_essence + taxe_fioul_domestique + taxe_gaz
            )

        return period, total

class tva_taux_plein(Variable):
    label = u"Contribution sur la TVA à taux plein après réaction à la réforme - taxe carbone"
    reference = tva.tva_taux_plein

    def function(self, simulation, period):
        depenses_tva_taux_plein_ajustees = \
            simulation.calculate('depenses_tva_taux_plein_ajustees_taxe_carbone', period)

        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_plein
        nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

        return period, tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)

class tva_taux_plein_bis(Variable):
    column = FloatCol
    entity = Menage
    label = u"Contribution sur la TVA à taux plein après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_tva_taux_plein_ajustees = \
            simulation.calculate('depenses_tva_taux_plein_bis_ajustees_taxe_carbone', period)

        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = \
            simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_plein_bis
        nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

        return period, tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)

class tva_taux_reduit(Variable):
    label = u"Contribution sur la TVA à taux reduit après réaction à la réforme - taxe carbone"
    reference = tva.tva_taux_reduit

    def function(self, simulation, period):
        depenses_tva_taux_reduit_ajustees = \
            simulation.calculate('depenses_tva_taux_reduit_ajustees_taxe_carbone', period)

        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        abaissement_tva_taux_reduit = \
            simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_reduit
        nouveau_taux_reduit = taux_reduit - abaissement_tva_taux_reduit

        return period, tax_from_expense_including_tax(depenses_tva_taux_reduit_ajustees, nouveau_taux_reduit)

class tva_taux_super_reduit(Variable):
    label = u"Contribution sur la TVA à taux super reduit après réaction à la réforme - taxe carbone"
    reference = tva.tva_taux_super_reduit

    def function(self, simulation, period):
        depenses_tva_taux_super_reduit_ajustees = \
            simulation.calculate('depenses_tva_taux_super_reduit_ajustees_taxe_carbone', period)

        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        abaissement_tva_taux_super_reduit = \
            simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_super_reduit
        nouveau_taux_super_reduit = taux_super_reduit - abaissement_tva_taux_super_reduit

        return period, \
            tax_from_expense_including_tax(depenses_tva_taux_super_reduit_ajustees, nouveau_taux_super_reduit)

class tva_total(Variable):
    label = u"Différence de contribution sur la TVA après réaction à la réforme - taxes carburants"
    reference = tva.tva_total

    def function(self, simulation, period):
        taux_plein = simulation.calculate('tva_taux_plein_bis', period)
        taux_reduit = simulation.calculate('tva_taux_reduit', period)
        taux_super_reduit = simulation.calculate('tva_taux_super_reduit', period)
        taux_intermediaire = simulation.calculate('tva_taux_intermediaire', period)

        total = (taux_plein + taux_reduit + taux_super_reduit + taux_intermediaire)

        return period, total


class taxe_carbone(Reform):
    key = 'taxe_carbone',
    name = u"Réforme de l'imposition indirecte des énergies selon leur contenu carbone",


    def apply(self):
        self.modify_legislation_json(modifier_function = modify_legislation_json)
        variables = [
            depenses_diesel_ajustees_taxe_carbone,
            depenses_electricite_ajustees_taxe_carbone,
            depenses_essence_ajustees_taxe_carbone,
            depenses_fioul_domestique_ajustees_taxe_carbone,
            depenses_gaz_ajustees_taxe_carbone,
            depenses_tva_taux_plein_ajustees_taxe_carbone,
            depenses_tva_taux_plein_bis_ajustees_taxe_carbone,
            depenses_tva_taux_reduit_ajustees_taxe_carbone,
            depenses_tva_taux_super_reduit_ajustees_taxe_carbone,
            diesel_ticpe,
            emissions_CO2_carburants,
            emissions_CO2_energies,
            emissions_CO2_electricite,
            emissions_CO2_fioul_domestique,
            emissions_CO2_gaz,
            essence_ticpe,
            fioul_domestique_ticpe,
            quantites_diesel,
            quantites_fioul_domestique,
            quantites_gaz_contrat_optimal_ajustees_taxe_carbone,
            quantites_electricite_selon_compteur_ajustees_taxe_carbone,
            quantites_sp_e10,
            quantites_sp95,
            quantites_sp98,
            quantites_super_plombe,
            quantites_essence,
            sp_e10_ticpe,
            sp95_ticpe,
            sp98_ticpe,
            super_plombe_ticpe,
            taxe_electricite,
            taxe_gaz,
            ticpe_totale,
            total_taxes_energies,
            tva_taux_plein,
            tva_taux_plein_bis,
            tva_taux_reduit,
            tva_taux_super_reduit,
            tva_total,
            ]
        for variable in variables:
            self.add_variable(variable)
