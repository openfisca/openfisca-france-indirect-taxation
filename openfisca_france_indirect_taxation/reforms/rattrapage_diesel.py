# -*- coding: utf-8 -*-


import numpy

from openfisca_core.reforms import Reform


from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore
from openfisca_france_indirect_taxation.variables.taxes_indirectes import (
    ticpe,
    tva,
    )
from openfisca_france_indirect_taxation.variables.consommation import (
    emissions_co2, quantites_energie)


parameters_path = os.path.join(os.path.dirname(__file__), 'parameters')


def modify_parameters(parameters):
    file_path = os.path.join(parameters_path, 'rattrapage-diesel-parameters.yaml')
    reform_parameters_subtree = load_parameter_file(name='rattrapage_diesel', file_path=file_path)
    parameters.add_child('rattrapage_diesel', reform_parameters_subtree)
    return parameters


class reforme_rattrapage_diesel(Reform):
    key = 'rattrapage_diesel'
    name = "Reforme de l'imposition indirecte des carburants"

    # class depenses_carburants_ajustees_rattrapage_diesel(YearlyVariable):
    #    value_type = float
    #    entity = Menage
    #    label = u"Depenses en carburants après reaction a la reforme - taxes carburants"

    #    def formula(menage, period):
    #        depenses_diesel_ajustees = menage('depenses_diesel_ajustees_rattrapage_diesel', period)
    #        depenses_essence_ajustees = menage('depenses_essence_ajustees_rattrapage_diesel', period)
    #        depenses_carburants_ajustees = depenses_diesel_ajustees + depenses_essence_ajustees

    #        return depenses_carburants_ajustees

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
            total_taxes_energies_rattrapage_diesel = menage('total_taxes_energies_rattrapage_diesel', period)

            contribution = total_taxes_energies_rattrapage_diesel - total_taxes_energies

            return contribution

    class depenses_carburants_corrigees_ajustees_rattrapage_diesel(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Depenses en carburants après reaction a la reforme - taxes carburants"

        def formula(menage, period):
            depenses_diesel_ajustees = menage('depenses_diesel_corrigees_ajustees_rattrapage_diesel', period)
            depenses_essence_ajustees = menage('depenses_essence_corrigees_ajustees_rattrapage_diesel', period)
            depenses_carburants_ajustees = depenses_diesel_ajustees + depenses_essence_ajustees

            return depenses_carburants_ajustees

    # class depenses_diesel_ajustees_rattrapage_diesel(YearlyVariable):
    #    value_type = float
    #    entity = Menage
    #    label = u"Depenses en diesel après reaction a la reforme - taxes carburants"

    #    def formula(menage, period, parameters):
    #        depenses_diesel = menage('depenses_diesel', period)
    #        diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
    #        reforme_diesel = parameters(period.start).rattrapage_diesel.diesel
    #        carburants_elasticite_prix = menage('elas_price_1_1', period)
    #        depenses_diesel_ajustees_rattrapage_diesel = \
    #            depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

    #        return depenses_diesel_ajustees_rattrapage_diesel

    class depenses_diesel_corrigees_ajustees_rattrapage_diesel(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Depenses en diesel après reaction a la reforme - taxes carburants"

        def formula(menage, period, parameters):
            depenses_diesel = menage('depenses_diesel_corrigees', period)
            diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            reforme_diesel = parameters(period.start).rattrapage_diesel.diesel
            carburants_elasticite_prix = menage('elas_price_1_1', period)
            depenses_diesel_ajustees_rattrapage_diesel = \
                depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel / diesel_ttc)

            return depenses_diesel_ajustees_rattrapage_diesel

    class depenses_essence_ajustees_rattrapage_diesel(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Depenses en essence après reaction a la reforme - taxes carburants"

        def formula(menage, period, parameters):
            depenses_essence = menage('depenses_essence', period)
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            reforme_essence = parameters(period.start).rattrapage_diesel.essence
            carburants_elasticite_prix = menage('elas_price_1_1', period)
            print("reforme_essence", reforme_essence)
            print("super_95_ttc", super_95_ttc)
            depenses_essence_ajustees_rattrapage_diesel = \
                depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence / super_95_ttc)

            return depenses_essence_ajustees_rattrapage_diesel

    class depenses_essence_corrigees_ajustees_rattrapage_diesel(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Depenses en essence après reaction a la reforme - taxes carburants"

        def formula(menage, period, parameters):
            depenses_essence = menage('depenses_essence_corrigees', period)
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            reforme_essence = parameters(period.start).rattrapage_diesel.essence
            carburants_elasticite_prix = menage('elas_price_1_1', period)
            depenses_essence_ajustees_rattrapage_diesel = \
                depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence / super_95_ttc)

            return depenses_essence_ajustees_rattrapage_diesel

    class depenses_tva_taux_plein_ajustees_rattrapage_diesel(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Depenses sur les biens assujetis a la TVA a taux plein après reaction a la reforme - taxes carburants"

        def formula(menage, period, parameters):
            depenses_tva_taux_plein = menage('depenses_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein = parameters(period.start).rattrapage_diesel.abaissement_tva_taux_plein
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_plein_ajustees = (
                depenses_tva_taux_plein
                * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))
                )

            return depenses_tva_taux_plein_ajustees

    class depenses_tva_taux_plein_bis_ajustees_rattrapage_diesel(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Depenses sur les biens assujetis a la TVA a taux plein après reaction a la reforme - taxes carburants"

        def formula(menage, period, parameters):
            depenses_tva_taux_plein = menage('depenses_tva_taux_plein', period)
            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein = \
                parameters(period.start).rattrapage_diesel.abaissement_tva_taux_plein_bis
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_plein_ajustees = \
                depenses_tva_taux_plein * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))

            return depenses_tva_taux_plein_ajustees

    class depenses_tva_taux_reduit_ajustees_rattrapage_diesel(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Depenses sur les biens assujetis a la TVA a taux reduit après reaction a la reforme - taxes carburants"

        def formula(menage, period, parameters):
            depenses_tva_taux_reduit = menage('depenses_tva_taux_reduit', period)
            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            abaissement_tva_taux_reduit = \
                parameters(period.start).rattrapage_diesel.abaissement_tva_taux_reduit
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_reduit_ajustees = \
                depenses_tva_taux_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_reduit) / (1 + taux_reduit))

            return depenses_tva_taux_reduit_ajustees

    class depenses_tva_taux_super_reduit_ajustees_rattrapage_diesel(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Depenses sur les biens assujetis a la TVA tx super reduit après reaction a la reforme - taxes carburants"

        def formula(menage, period, parameters):
            depenses_tva_taux_super_reduit = menage('depenses_tva_taux_super_reduit', period)
            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            abaissement_tva_taux_super_reduit = \
                parameters(period.start).rattrapage_diesel.abaissement_tva_taux_super_reduit
            elasticite = menage('elas_price_3_3', period)
            depenses_tva_taux_super_reduit_ajustees = (
                depenses_tva_taux_super_reduit
                * (1 + (1 + elasticite) * (- abaissement_tva_taux_super_reduit) / (1 + taux_super_reduit))
                )
            return depenses_tva_taux_super_reduit_ajustees

    class diesel_ticpe(YearlyVariable):
        baseline_variable = ticpe.diesel_ticpe  #  TODO réintégrer ou effacer car update
        label = "Calcul du montant de TICPE sur le diesel après reforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            try:
                majoration_ticpe_diesel = \
                    parameters(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
                accise_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole
                accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
            except Exception:
                accise_diesel_ticpe = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole

            reforme_diesel = parameters(period.start).rattrapage_diesel.diesel
            accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
            prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
            taux_implicite_diesel_ajuste = (
                (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                / (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                )

            depenses_diesel_ajustees_rattrapage_diesel = \
                menage('depenses_diesel_corrigees_ajustees_rattrapage_diesel', period)
            depenses_diesel_htva_ajustees = (
                depenses_diesel_ajustees_rattrapage_diesel
                - tax_from_expense_including_tax(depenses_diesel_ajustees_rattrapage_diesel, taux_plein_tva)
                )
            montant_diesel_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
                )

            return montant_diesel_ticpe_ajuste

    class emissions_CO2_carburants(YearlyVariable):
        label = "Emissions de CO2 des menages via leur consommation de carburants après reforme, en kg de CO2"
        baseline_variable = emissions_co2.emissions_CO2_carburants

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

    class essence_ticpe(YearlyVariable):
        label = "Calcul du montant de la TICPE sur toutes les essences cumulees, après reforme"
        baseline_variable = ticpe.essence_ticpe

        def formula_2009(menage, period):
            sp95_ticpe_ajustee = menage('sp95_ticpe', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe', period)
            sp_e10_ticpe_ajustee = menage('sp_e10_ticpe', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_2007(menage, period):
            sp95_ticpe_ajustee = menage('sp95_ticpe', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_1990(menage, period):
            sp95_ticpe_ajustee = menage('sp95_ticpe', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe', period)
            super_plombe_ticpe_ajustee = menage('super_plombe_ticpe', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
            return essence_ticpe_ajustee

    class quantites_diesel(YearlyVariable):
        label = "Quantites de diesel consommees après la reforme - taxe carburants"
        baseline_variable = quantites_energie.quantites_diesel

        def formula(menage, period, parameters):
            depenses_diesel_ajustees_rattrapage_diesel = \
                menage('depenses_diesel_corrigees_ajustees_rattrapage_diesel', period)
            diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            reforme_diesel = parameters(period.start).rattrapage_diesel.diesel
            quantites_diesel_ajustees = depenses_diesel_ajustees_rattrapage_diesel / (diesel_ttc + reforme_diesel) * 100

            return quantites_diesel_ajustees

    class quantites_sp_e10(YearlyVariable):
        label = "Quantites consommees de sans plomb e10 par les menages après reforme - taxe carburants"
        baseline_variable = quantites_energie.quantites_sp_e10

        def formula(menage, period, parameters):
            depenses_essence_ajustees_rattrapage_diesel = \
                menage('depenses_essence_corrigees_ajustees_rattrapage_diesel', period)
            part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            depenses_sp_e10_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp_e10
            super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
            reforme_essence = parameters(period.start).rattrapage_diesel.essence
            quantite_sp_e10 = depenses_sp_e10_ajustees / (super_95_e10_ttc + reforme_essence) * 100

            return quantite_sp_e10

    class quantites_sp95(YearlyVariable):
        label = "Quantites consommees de sans plomb 95 par les menages après reforme"
        baseline_variable = quantites_energie.quantites_sp95

        def formula(menage, period, parameters):
            depenses_essence_ajustees_rattrapage_diesel = menage('depenses_essence_corrigees_ajustees_rattrapage_diesel', period)
            part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp95_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp95
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            reforme_essence = parameters(period.start).rattrapage_diesel.essence
            quantites_sp95_ajustees = depenses_sp95_ajustees / (super_95_ttc + reforme_essence) * 100

            return quantites_sp95_ajustees

    class quantites_sp98(YearlyVariable):
        label = "Quantites consommees de sans plomb 98 par les menages"
        baseline_variable = quantites_energie.quantites_sp98

        def formula(menage, period, parameters):
            depenses_essence_ajustees_rattrapage_diesel = menage('depenses_essence_corrigees_ajustees_rattrapage_diesel', period)
            part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp98_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp98
            super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
            reforme_essence = parameters(period.start).rattrapage_diesel.essence
            quantites_sp98_ajustees = depenses_sp98_ajustees / (super_98_ttc + reforme_essence) * 100

            return quantites_sp98_ajustees

    class quantites_super_plombe(YearlyVariable):
        label = "Quantites consommees de super plombe par les menages après reforme"
        baseline_variable = quantites_energie.quantites_super_plombe

        def formula(menage, period, parameters):
            depenses_essence_ajustees_rattrapage_diesel = menage('depenses_essence_corrigees_ajustees_rattrapage_diesel', period)
            part_super_plombe = \
                parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_super_plombe
            super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
            reforme_essence = parameters(period.start).rattrapage_diesel.essence
            quantites_super_plombe_ajustees = depenses_super_plombe_ajustees / (super_plombe_ttc + reforme_essence) * 100

            return quantites_super_plombe_ajustees

    class quantites_essence(YearlyVariable):
        label = "Quantites d'essence consommees par les menages après reforme"
        baseline_variable = quantites_energie.quantites_essence
        definition_period = YEAR

        def formula_2009(menage, period):
            quantites_sp95_ajustees = menage('quantites_sp95', period)
            quantites_sp98_ajustees = menage('quantites_sp98', period)
            quantites_sp_e10_ajustees = menage('quantites_sp_e10', period)
            quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_sp_e10_ajustees)
            return quantites_essence_ajustees

        def formula_2007(menage, period):
            quantites_sp95_ajustees = menage('quantites_sp95', period)
            quantites_sp98_ajustees = menage('quantites_sp98', period)
            quantites_essence_ajustees = (quantites_sp95_ajustees + quantites_sp98_ajustees)
            return quantites_essence_ajustees

        def formula_1990(menage, period):
            quantites_sp95_ajustees = menage('quantites_sp95', period)
            quantites_sp98_ajustees = menage('quantites_sp98', period)
            quantites_super_plombe_ajustees = \
                menage('quantites_super_plombe', period)
            quantites_essence_ajustees = (
                quantites_sp95_ajustees + quantites_sp98_ajustees + quantites_super_plombe_ajustees
                )
            return quantites_essence_ajustees

    class sp_e10_ticpe(YearlyVariable):
        label = "Calcul du montant de la TICPE sur le SP E10 après reforme"
        baseline_variable = ticpe.sp_e10_ticpe

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

            reforme_essence = parameters(period.start).rattrapage_diesel.essence
            accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
            super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
            super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence
            taux_implicite_sp_e10_ajuste = (
                (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
                / (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_rattrapage_diesel = \
                menage('depenses_essence_corrigees_ajustees_rattrapage_diesel', period)
            part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            sp_e10_depenses_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp_e10
            sp_e10_depenses_htva_ajustees = \
                sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
            montant_sp_e10_ticpe_ajuste = \
                tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

            return montant_sp_e10_ticpe_ajuste

    class sp95_ticpe(YearlyVariable):
        label = "Calcul du montant de TICPE sur le sp_95 après reforme"
        baseline_variable = ticpe.sp95_ticpe

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            try:
                accise_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
                majoration_ticpe_super95 = \
                    parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
                accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
            except Exception:
                accise_ticpe_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98

            reforme_essence = parameters(period.start).rattrapage_diesel.essence
            accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            super_95_ttc_ajuste = super_95_ttc + reforme_essence
            taux_implicite_sp95_ajuste = (
                (accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
                / (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_rattrapage_diesel = \
                menage('depenses_essence_corrigees_ajustees_rattrapage_diesel', period)
            part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp_95_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp95
            depenses_sp_95_htva_ajustees = (
                depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
                )
            montant_sp95_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
                )

            return montant_sp95_ticpe_ajuste

    class sp98_ticpe(YearlyVariable):
        label = "Calcul du montant de TICPE sur le sp_98 après reforme"
        baseline_variable = ticpe.sp98_ticpe

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            try:
                accise_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
                majoration_ticpe_super98 = \
                    parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
                accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
            except Exception:
                accise_ticpe_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98

            reforme_essence = parameters(period.start).rattrapage_diesel.essence
            accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
            super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
            super_98_ttc_ajuste = super_98_ttc + reforme_essence
            taux_implicite_sp98_ajuste = (
                (accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
                / (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_rattrapage_diesel = \
                menage('depenses_essence_corrigees_ajustees_rattrapage_diesel', period)
            part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp_98_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_sp98
            depenses_sp_98_htva_ajustees = (
                depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
                )
            montant_sp98_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
                )

            return montant_sp98_ticpe_ajuste

    class super_plombe_ticpe(YearlyVariable):
        label = "Calcul du montant de la TICPE sur le super plombe après reforme"
        baseline_variable = ticpe.super_plombe_ticpe

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            accise_super_plombe_ticpe = \
                parameters(period.start).imposition_indirecte.ticpe.super_plombe_ticpe

            reforme_essence = parameters(period.start).rattrapage_diesel.essence
            accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
            super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
            super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence
            taux_implicite_super_plombe_ajuste = (
                (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
                / (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_ajustees_rattrapage_diesel = \
                menage('depenses_essence_corrigees_ajustees_rattrapage_diesel', period)
            part_super_plombe = \
                parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_ajustees_rattrapage_diesel * part_super_plombe
            depenses_super_plombe_htva_ajustees = (
                depenses_super_plombe_ajustees
                - tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
                )
            montant_super_plombe_ticpe_ajuste = \
                tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

            return montant_super_plombe_ticpe_ajuste

    class ticpe_totale(YearlyVariable):
        label = "Calcul du montant de la TICPE sur tous les carburants cumules, après reforme"
        baseline_variable = ticpe.ticpe_totale

        def formula(menage, period):
            essence_ticpe = menage('essence_ticpe', period)
            diesel_ticpe = menage('diesel_ticpe', period)
            ticpe_totale = diesel_ticpe + essence_ticpe

            return ticpe_totale

    class total_taxes_energies_rattrapage_diesel(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Différence entre les contributions aux taxes sur l'énergie après la taxe carbone"

        def formula(menage, period):
            taxe_diesel = menage('diesel_ticpe', period)
            taxe_essence = menage('essence_ticpe', period)
            taxe_combustibles_liquides = menage('combustibles_liquides_ticpe', period)

            total = (
                taxe_diesel + taxe_essence + taxe_combustibles_liquides
                )

            return total

    class tva_taux_plein(YearlyVariable):
        label = "Contribution sur la TVA a taux plein après reaction a la reforme - taxes carburants"
        baseline_variable = tva.tva_taux_plein

        def formula(menage, period, parameters):
            depenses_tva_taux_plein_ajustees = \
                menage('depenses_tva_taux_plein_ajustees_rattrapage_diesel', period)

            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein = parameters(period.start).rattrapage_diesel.abaissement_tva_taux_plein
            nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

            return tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)

    class tva_taux_plein_bis(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Contribution sur la TVA a taux plein après reaction a la reforme - taxes carburants"

        def formula(menage, period, parameters):
            depenses_tva_taux_plein_ajustees = \
                menage('depenses_tva_taux_plein_bis_ajustees_rattrapage_diesel', period)

            taux_plein = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            abaissement_tva_taux_plein = \
                parameters(period.start).rattrapage_diesel.abaissement_tva_taux_plein_bis
            nouveau_taux_plein = taux_plein - abaissement_tva_taux_plein

            return tax_from_expense_including_tax(depenses_tva_taux_plein_ajustees, nouveau_taux_plein)

    class tva_taux_reduit(YearlyVariable):
        label = "Contribution sur la TVA a taux reduit après reaction a la reforme - taxes carburants"
        baseline_variable = tva.tva_taux_reduit

        def formula(menage, period, parameters):
            depenses_tva_taux_reduit_ajustees = \
                menage('depenses_tva_taux_reduit_ajustees_rattrapage_diesel', period)

            taux_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_reduit
            abaissement_tva_taux_reduit = \
                parameters(period.start).rattrapage_diesel.abaissement_tva_taux_reduit
            nouveau_taux_reduit = taux_reduit - abaissement_tva_taux_reduit

            return tax_from_expense_including_tax(depenses_tva_taux_reduit_ajustees, nouveau_taux_reduit)

    class tva_taux_super_reduit(YearlyVariable):
        label = "Contribution sur la TVA a taux super reduit après reaction a la reforme - taxes carburants"
        baseline_variable = tva.tva_taux_super_reduit

        def formula(menage, period, parameters):
            depenses_tva_taux_super_reduit_ajustees = \
                menage('depenses_tva_taux_super_reduit_ajustees_rattrapage_diesel', period)

            taux_super_reduit = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_particulier_super_reduit
            abaissement_tva_taux_super_reduit = \
                parameters(period.start).rattrapage_diesel.abaissement_tva_taux_super_reduit
            nouveau_taux_super_reduit = taux_super_reduit - abaissement_tva_taux_super_reduit

            return tax_from_expense_including_tax(depenses_tva_taux_super_reduit_ajustees, nouveau_taux_super_reduit)

    class tva_total(YearlyVariable):
        label = "Difference de contribution sur la TVA après reaction a la reforme - rattrapage diesel"
        baseline_variable = tva.tva_total

        def formula(menage, period):
            taux_plein = menage('tva_taux_plein_bis', period)
            taux_reduit = menage('tva_taux_reduit', period)
            taux_super_reduit = menage('tva_taux_super_reduit', period)
            taux_intermediaire = menage('tva_taux_intermediaire', period)

            total = (taux_plein + taux_reduit + taux_super_reduit + taux_intermediaire)

            return total

    def apply(self):
        self.modify_parameters(modifier_function = modify_parameters)
        self.update_variable(self.cheques_energie)
        self.update_variable(self.contributions_reforme)
        self.update_variable(self.depenses_carburants_corrigees_ajustees_rattrapage_diesel)
        self.update_variable(self.depenses_diesel_corrigees_ajustees_rattrapage_diesel)
        self.update_variable(self.depenses_essence_corrigees_ajustees_rattrapage_diesel)
        self.update_variable(self.depenses_tva_taux_plein_ajustees_rattrapage_diesel)
        self.update_variable(self.depenses_tva_taux_plein_bis_ajustees_rattrapage_diesel)
        self.update_variable(self.depenses_tva_taux_reduit_ajustees_rattrapage_diesel)
        self.update_variable(self.depenses_tva_taux_super_reduit_ajustees_rattrapage_diesel)
        self.update_variable(self.diesel_ticpe)
        self.update_variable(self.emissions_CO2_carburants)
        self.update_variable(self.essence_ticpe)
        self.update_variable(self.quantites_diesel)
        self.update_variable(self.quantites_sp_e10)
        self.update_variable(self.quantites_sp95)
        self.update_variable(self.quantites_sp98)
        self.update_variable(self.quantites_super_plombe)
        self.update_variable(self.quantites_essence)
        self.update_variable(self.sp_e10_ticpe)
        self.update_variable(self.sp95_ticpe)
        self.update_variable(self.sp98_ticpe)
        self.update_variable(self.super_plombe_ticpe)
        self.update_variable(self.ticpe_totale)
        self.update_variable(self.total_taxes_energies_rattrapage_diesel)
        self.update_variable(self.tva_taux_plein)
        self.update_variable(self.tva_taux_plein_bis)
        self.update_variable(self.tva_taux_reduit)
        self.update_variable(self.tva_taux_super_reduit)
        self.update_variable(self.tva_total)

        self.update_variable(self.depenses_essence_ajustees_rattrapage_diesel)
