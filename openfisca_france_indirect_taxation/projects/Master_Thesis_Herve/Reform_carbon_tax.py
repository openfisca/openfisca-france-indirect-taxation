import numpy

from openfisca_core.reforms import Reform
from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore

DIESEL_KG_CO2_PAR_HL = 264.5
ESSENCE_KG_CO2_PAR_HL = 228.4

def modify_parameters(parameters):
    node = ParameterNode(
        'carbon_tax_rv',
        data = {
            "description": "carbon_tax_rv",
            "diesel_with_carbon_tax_rv": {
                "description": "Surcroît de prix du diesel (en euros par hectolitres)",
                "unit": 'currency',
                "values": {'2018-01-01': (55.0 - 44.63) / 1e3 * ESSENCE_KG_CO2_PAR_HL}  # test
                },
            "essence_with_carbon_tax_rv": {
                "description": "Surcroît de prix de l'essence (en euros par hectolitres)",
                "unit": 'currency',
                "values": {'2018-01-01': 2.6 + (55.0 - 44.6) / 1e3 * DIESEL_KG_CO2_PAR_HL} # test
                }
            }
        )

    parameters.add_child('carbon_tax_rv', node)
    parameters.prestations.add_child('cheque_energie_reforme', FranceIndirectTaxationTaxBenefitSystem().parameters.prestations.cheque_energie)

    return parameters


class carbon_tax_rv(Reform):
    key = 'carbon_tax_rv',
    name = "Réforme de la fiscalité des énergies de 2019 par rapport aux taux de 20168",

    class cheques_energie(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant des chèques énergie tels que prévus par la loi"

        def formula(menage, period, parameters):
            revenu_fiscal = numpy.maximum(0.0, menage('revdecm', period) / 1.22)
            ocde10 = menage('ocde10', period)
            revenu_fiscal_uc = revenu_fiscal / ocde10
            bareme_cheque_energie_reforme = parameters(period).prestations.cheque_energie_reforme

            return numpy.select(
                [
                    (ocde10 == 1),
                    ((ocde10 > 1) * (ocde10 < 2)),
                    (ocde10 >= 2),
                    ],
                [
                    bareme_cheque_energie_reforme.menage_avec_1_uc.calc(revenu_fiscal_uc),
                    bareme_cheque_energie_reforme.menage_entre_1_et_2_uc.calc(revenu_fiscal_uc),
                    bareme_cheque_energie_reforme.menage_avec_2_uc_et_plus.calc(revenu_fiscal_uc),
                    ],
                default = 0.0
                )
    
    class bonus_cheques_energie(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Montant du bonus de chèques énergie réparti uniformément (indexés par uc) - taxe carbone"

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
        label = "Changement de contribution à la taxe carbone suite à la réforme "

        def formula(menage, period):
            total_ticpe = menage('ticpe_totale',period)
            total_ticpe_carbon_tax_rv = menage('ticpe_totale_carbon_tax_rv',period)

            contribution = total_ticpe_carbon_tax_rv - total_ticpe

            return contribution
                
    class depenses_carburants_corrigees_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Depenses en carburants après reaction a la reforme"

        def formula(menage, period, parameters):
            depenses_diesel_ajustees = menage('depenses_diesel_corrigees_carbon_tax_rv', period)
            depenses_essence_ajustees = menage('depenses_essence_corrigees_carbon_tax_rv', period)
            depenses_carburants_ajustees = depenses_diesel_ajustees + depenses_essence_ajustees

            return depenses_carburants_ajustees

    class depenses_diesel_corrigees_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en diesel après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_diesel = menage('depenses_diesel', period)
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            reforme_diesel = parameters(period.start).carbon_tax_rv.diesel_with_carbon_tax_rv
            carburants_elasticite_prix = menage('elas_price_1_1', period)
            depenses_diesel_carbon_tax_rv = \
                depenses_diesel * (1 + (1 + carburants_elasticite_prix) * reforme_diesel * (1 + taux_plein_tva) / diesel_ttc)

            return depenses_diesel_carbon_tax_rv

    class depenses_essence_corrigees_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Dépenses en essence après réaction à la réforme"

        def formula(menage, period, parameters):
            depenses_essence = menage('depenses_essence', period)
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            reforme_essence = parameters(period.start).carbon_tax_rv.essence_with_carbon_tax_rv
            carburants_elasticite_prix = menage('elas_price_1_1', period)
            depenses_essence_carbon_tax_rv = \
                depenses_essence * (1 + (1 + carburants_elasticite_prix) * reforme_essence * (1 + taux_plein_tva) / super_95_ttc)

            return depenses_essence_carbon_tax_rv
        
    class diesel_ticpe_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de TICPE sur le diesel après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            # If the parameter does not have a defined value, it returns None
            majoration_ticpe_diesel = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_gazole.alsace

            accise_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole

            accise_diesel_ticpe = (
                accise_diesel + majoration_ticpe_diesel
                if majoration_ticpe_diesel is not None
                else accise_diesel
                )

            reforme_diesel = parameters(period.start).carbon_tax_rv.diesel_with_carbon_tax_rv
            accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
            prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel * (1 + taux_plein_tva)
            taux_implicite_diesel_ajuste = (
                (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                / (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                )

            depenses_diesel_carbon_tax_rv = \
                menage('depenses_diesel_corrigees_carbon_tax_rv', period)
            depenses_diesel_htva_ajustees = (
                depenses_diesel_carbon_tax_rv
                - tax_from_expense_including_tax(depenses_diesel_carbon_tax_rv, taux_plein_tva)
                )
            montant_diesel_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
                )

            return montant_diesel_ticpe_ajuste

    class diesel_ticpe_test(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de TICPE sur le diesel sans réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            # If the parameter does not have a defined value, it returns None
            majoration_ticpe_diesel = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_gazole.alsace

            accise_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole

            accise_diesel_ticpe = (
                accise_diesel + majoration_ticpe_diesel
                if majoration_ticpe_diesel is not None
                else accise_diesel
                )

            accise_diesel_ticpe_ajustee = accise_diesel_ticpe
            prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc
            taux_implicite_diesel_ajuste = (
                (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                / (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                )

            depenses_diesel_carbon_tax_rv = \
                menage('depenses_diesel', period)
            depenses_diesel_htva_ajustees = (
                depenses_diesel_carbon_tax_rv
                - tax_from_expense_including_tax(depenses_diesel_carbon_tax_rv, taux_plein_tva)
                )
            montant_diesel_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
                )

            return montant_diesel_ticpe_ajuste

    class quantite_diesel_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul des quantités de diesel après réforme"

        def formula(menage, period, parameters):
            reforme_diesel = parameters(period.start).carbon_tax_rv.diesel_with_carbon_tax_rv
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel * (1 + taux_plein_tva)

            depenses_diesel_carbon_tax_rv = \
                menage('depenses_diesel_corrigees_carbon_tax_rv', period)

            return depenses_diesel_carbon_tax_rv / prix_diesel_ttc_ajuste

    class diesel_ticpe_rattrapage_integral(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de TICPE sur le diesel après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            # If the parameter does not have a defined value, it returns None
            majoration_ticpe_diesel = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_gazole.alsace

            accise_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole

            accise_diesel_ticpe = (
                accise_diesel + majoration_ticpe_diesel
                if majoration_ticpe_diesel is not None
                else accise_diesel
                )

            taxe_essence = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            taxe_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole
            reforme_diesel = taxe_essence - taxe_diesel
            accise_diesel_ticpe_ajustee = accise_diesel_ticpe + reforme_diesel
            prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
            prix_diesel_ttc_ajuste = prix_diesel_ttc + reforme_diesel
            taux_implicite_diesel_ajuste = (
                (accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                / (prix_diesel_ttc_ajuste - accise_diesel_ticpe_ajustee * (1 + taux_plein_tva))
                )

            depenses_diesel_rattrapage_integral = \
                menage('depenses_diesel_corrigees_rattrapage_integral', period)
            depenses_diesel_htva_ajustees = (
                depenses_diesel_rattrapage_integral
                - tax_from_expense_including_tax(depenses_diesel_rattrapage_integral, taux_plein_tva)
                )
            montant_diesel_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_diesel_htva_ajustees, taux_implicite_diesel_ajuste)
                )

            return montant_diesel_ticpe_ajuste

    class essence_ticpe_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur toutes les essences cumulées, après réforme"

        def formula_2009(menage, period):
            sp95_ticpe_ajustee = menage('sp95_ticpe_carbon_tax_rv', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe_carbon_tax_rv', period)
            sp_e10_ticpe_ajustee = menage('sp_e10_ticpe_carbon_tax_rv', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_2007(menage, period):
            sp95_ticpe_ajustee = menage('sp95_ticpe_carbon_tax_rv', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe_carbon_tax_rv', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_1990(menage, period, parameters):
            sp95_ticpe_ajustee = menage('sp95_ticpe_carbon_tax_rv', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe_carbon_tax_rv', period)
            super_plombe_ticpe_ajustee = menage('super_plombe_ticpe_carbon_tax_rv', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
            return essence_ticpe_ajustee

    class essence_ticpe_test(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur toutes les essences cumulées, sans réforme"

        def formula_2009(menage, period):
            sp95_ticpe_ajustee = menage('sp95_ticpe_test', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe_test', period)
            sp_e10_ticpe_ajustee = menage('sp_e10_ticpe_test', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + sp_e10_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_2007(menage, period):
            sp95_ticpe_ajustee = menage('sp95_ticpe_test', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe_test', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee)
            return essence_ticpe_ajustee

        def formula_1990(menage, period, parameters):
            sp95_ticpe_ajustee = menage('sp95_ticpe_test', period)
            sp98_ticpe_ajustee = menage('sp98_ticpe_test', period)
            super_plombe_ticpe_ajustee = menage('super_plombe_ticpe_test', period)
            essence_ticpe_ajustee = (sp95_ticpe_ajustee + sp98_ticpe_ajustee + super_plombe_ticpe_ajustee)
            return essence_ticpe_ajustee

    class quantite_essence_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul des qauntités de toutes les essences cumulées, après réforme"

        def formula_2009(menage, period):
            quantite_sp95_ajustee = menage('quantite_sp95_carbon_tax_rv', period)
            quantite_sp98_ajustee = menage('quantite_sp98_carbon_tax_rv', period)
            quantite_sp_e10_ajustee = menage('quantite_sp_e10_carbon_tax_rv', period)
            quantite_essence_ajustee = (quantite_sp95_ajustee + quantite_sp98_ajustee + quantite_sp_e10_ajustee)
            return quantite_essence_ajustee

        def formula_2007(menage, period):
            quantite_sp95_ajustee = menage('quantite_sp95_carbon_tax_rv', period)
            quantite_sp98_ajustee = menage('quantite_sp98_carbon_tax_rv', period)
            quantite_essence_ajustee = (quantite_sp95_ajustee + quantite_sp98_ajustee)
            return quantite_essence_ajustee

        def formula_1990(menage, period, parameters):
            quantite_sp95_ajustee = menage('quantite_sp95_carbon_tax_rv', period)
            quantite_sp98_ajustee = menage('quantite_sp98_carbon_tax_rv', period)
            quantite_super_plombe_ajustee = menage('quantite_super_plombe_carbon_tax_rv', period)
            quantite_essence_ajustee = (quantite_sp95_ajustee + quantite_sp98_ajustee + quantite_super_plombe_ajustee)
            return quantite_essence_ajustee

    class emissions_CO2_carburants(YearlyVariable):
        label = "Emissions de CO2 des ménages via leur consommation de carburants après réforme, en kg de CO2"
        # use_baseline =emissions_co2.emissions_CO2_carburants

        def formula(menage, period, parameters):
            quantites_diesel_ajustees = menage('quantite_diesel_carbon_tax_rv', period)
            quantites_essence_ajustees = menage('quantite_essence_carbon_tax_rv', period)
            emissions_diesel = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_diesel
            emissions_essence = \
                parameters(period.start).imposition_indirecte.emissions_CO2.carburants.CO2_essence
            emissions_ajustees = (
                (quantites_diesel_ajustees * emissions_diesel)
                + (quantites_essence_ajustees * emissions_essence)
                )  # Source : Ademe

            return emissions_ajustees
    
    class revenu_reforme_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Revenu généré par la réforme officielle 2018 avant redistribution"

        def formula(menage, period):
            total_ticpe = menage('ticpe_totale',period)
            total_ticpe_carbon_tax_rv = menage('ticpe_totale_carbon_tax_rv',period)
            total_gains_tva_carburants_carbon_tax_rv = menage('gains_tva_carburants_carbon_tax_rv', period)

            revenu_reforme = (total_ticpe_carbon_tax_rv - total_ticpe) + total_gains_tva_carburants_carbon_tax_rv                

            return revenu_reforme
        
    class gains_tva_carburants_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Recettes en TVA sur les carburants de la réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            depenses_essence_corrigees_carbon_tax_rv = \
                menage('depenses_essence_corrigees_carbon_tax_rv', period)
            depenses_diesel_corrigees_carbon_tax_rv = \
                menage('depenses_diesel_corrigees_carbon_tax_rv', period)
            tva_depenses_carburants_corrigees_carbon_tax_rv = (
                (taux_plein_tva / (1 + taux_plein_tva))
                * (depenses_essence_corrigees_carbon_tax_rv + depenses_diesel_corrigees_carbon_tax_rv)
                )
            depenses_essence = \
                menage('depenses_essence', period)
            depenses_diesel = \
                menage('depenses_diesel', period)
            tva_depenses_carburants_corrigees = (
                (taux_plein_tva / (1 + taux_plein_tva))
                * (depenses_essence + depenses_diesel)
                )
            gains_tva_carburants = (
                tva_depenses_carburants_corrigees_carbon_tax_rv
                - tva_depenses_carburants_corrigees
                )
            return gains_tva_carburants

    class ticpe_totale_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

        def formula(menage, period):
            essence_ticpe_ajustee = menage('essence_ticpe_carbon_tax_rv', period)
            diesel_ticpe_ajustee = menage('diesel_ticpe_carbon_tax_rv', period)
            ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

            return ticpe_totale_ajustee

    class ticpe_totale_test(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur tous les carburants cumulés, après réforme"

        def formula(menage, period):
            essence_ticpe_ajustee = menage('essence_ticpe_test', period)
            diesel_ticpe_ajustee = menage('diesel_ticpe_test', period)
            ticpe_totale_ajustee = diesel_ticpe_ajustee + essence_ticpe_ajustee

            return ticpe_totale_ajustee

    class sp_e10_ticpe_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur le SP E10 après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            accise_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e10
            # If the parameter does not have a defined value, it returns None
            majoration_ticpe_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace

            accise_ticpe_super_e10 = (
                accise_super_e10 + majoration_ticpe_super_e10
                if majoration_ticpe_super_e10 is not None
                else accise_super_e10
                )

            reforme_essence = parameters(period.start).carbon_tax_rv.essence_with_carbon_tax_rv
            accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10 + reforme_essence
            super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
            super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence * (1 + taux_plein_tva)
            taux_implicite_sp_e10_ajuste = (
                (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
                / (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence_corrigees_carbon_tax_rv', period)
            part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            sp_e10_depenses_ajustees = depenses_essence_carbon_tax_rv * part_sp_e10
            sp_e10_depenses_htva_ajustees = \
                sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
            montant_sp_e10_ticpe_ajuste = \
                tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

            return montant_sp_e10_ticpe_ajuste

    class sp_e10_ticpe_test(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur le SP E10 sans réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            accise_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e10
            # If the parameter does not have a defined value, it returns None
            majoration_ticpe_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace

            accise_ticpe_super_e10 = (
                accise_super_e10 + majoration_ticpe_super_e10
                if majoration_ticpe_super_e10 is not None
                else accise_super_e10
                )

            accise_ticpe_super_e10_ajustee = accise_ticpe_super_e10
            super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
            super_95_e10_ttc_ajuste = super_95_e10_ttc
            taux_implicite_sp_e10_ajuste = (
                (accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
                / (super_95_e10_ttc_ajuste - accise_ticpe_super_e10_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence', period)
            part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            sp_e10_depenses_ajustees = depenses_essence_carbon_tax_rv * part_sp_e10
            sp_e10_depenses_htva_ajustees = \
                sp_e10_depenses_ajustees - tax_from_expense_including_tax(sp_e10_depenses_ajustees, taux_plein_tva)
            montant_sp_e10_ticpe_ajuste = \
                tax_from_expense_including_tax(sp_e10_depenses_htva_ajustees, taux_implicite_sp_e10_ajuste)

            return montant_sp_e10_ticpe_ajuste

    class quantite_sp_e10_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur le SP E10 après réforme"

        def formula(menage, period, parameters):
            reforme_essence = parameters(period.start).carbon_tax_rv.essence_with_carbon_tax_rv
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
            super_95_e10_ttc_ajuste = super_95_e10_ttc + reforme_essence * (1 + taux_plein_tva)
            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence_corrigees_carbon_tax_rv', period)
            part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
            sp_e10_depenses_ajustees = depenses_essence_carbon_tax_rv * part_sp_e10

            return sp_e10_depenses_ajustees / super_95_e10_ttc_ajuste

    class sp95_ticpe_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de TICPE sur le sp_95 après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            accise_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            majoration_ticpe_super95 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = (
                accise_super95 + majoration_ticpe_super95
                if majoration_ticpe_super95 is not None
                else accise_super95
                )

            reforme_essence = parameters(period.start).carbon_tax_rv.essence_with_carbon_tax_rv
            accise_ticpe_super95_ajustee = accise_ticpe_super95 + reforme_essence
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            super_95_ttc_ajuste = super_95_ttc + reforme_essence * (1 + taux_plein_tva)
            taux_implicite_sp95_ajuste = (
                (accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
                / (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence_corrigees_carbon_tax_rv', period)
            part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp_95_ajustees = depenses_essence_carbon_tax_rv * part_sp95
            depenses_sp_95_htva_ajustees = (
                depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
                )
            montant_sp95_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
                )

            return montant_sp95_ticpe_ajuste

    class sp95_ticpe_test(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de TICPE sur le sp_95 sans réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            accise_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            majoration_ticpe_super95 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = (
                accise_super95 + majoration_ticpe_super95
                if majoration_ticpe_super95 is not None
                else accise_super95
                )

            accise_ticpe_super95_ajustee = accise_ticpe_super95
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            super_95_ttc_ajuste = super_95_ttc
            taux_implicite_sp95_ajuste = (
                (accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
                / (super_95_ttc_ajuste - accise_ticpe_super95_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence', period)
            part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp_95_ajustees = depenses_essence_carbon_tax_rv * part_sp95
            depenses_sp_95_htva_ajustees = (
                depenses_sp_95_ajustees - tax_from_expense_including_tax(depenses_sp_95_ajustees, taux_plein_tva)
                )
            montant_sp95_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_95_htva_ajustees, taux_implicite_sp95_ajuste)
                )

            return montant_sp95_ticpe_ajuste

    class quantite_sp95_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de TICPE sur le sp_95 après réforme"

        def formula(menage, period, parameters):
            reforme_essence = parameters(period.start).carbon_tax_rv.essence_with_carbon_tax_rv
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
            super_95_ttc_ajuste = super_95_ttc + reforme_essence * (1 + taux_plein_tva)
            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence_corrigees_carbon_tax_rv', period)
            part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
            depenses_sp_95_ajustees = depenses_essence_carbon_tax_rv * part_sp95

            return depenses_sp_95_ajustees / super_95_ttc_ajuste

    class sp98_ticpe_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de TICPE sur le sp_98 après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            accise_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            majoration_ticpe_super98 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = (
                accise_super98 + majoration_ticpe_super98
                if majoration_ticpe_super98 is not None
                else accise_super98
                )

            reforme_essence = parameters(period.start).carbon_tax_rv.essence_with_carbon_tax_rv
            accise_ticpe_super98_ajustee = accise_ticpe_super98 + reforme_essence
            super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
            super_98_ttc_ajuste = super_98_ttc + reforme_essence * (1 + taux_plein_tva)
            taux_implicite_sp98_ajuste = (
                (accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
                / (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence_corrigees_carbon_tax_rv', period)
            part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp_98_ajustees = depenses_essence_carbon_tax_rv * part_sp98
            depenses_sp_98_htva_ajustees = (
                depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
                )
            montant_sp98_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
                )

            return montant_sp98_ticpe_ajuste

    class sp98_ticpe_test(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de TICPE sur le sp_98 sans réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

            accise_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            majoration_ticpe_super98 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = (
                accise_super98 + majoration_ticpe_super98
                if majoration_ticpe_super98 is not None
                else accise_super98
                )

            accise_ticpe_super98_ajustee = accise_ticpe_super98
            super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
            super_98_ttc_ajuste = super_98_ttc
            taux_implicite_sp98_ajuste = (
                (accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
                / (super_98_ttc_ajuste - accise_ticpe_super98_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence', period)
            part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp_98_ajustees = depenses_essence_carbon_tax_rv * part_sp98
            depenses_sp_98_htva_ajustees = (
                depenses_sp_98_ajustees - tax_from_expense_including_tax(depenses_sp_98_ajustees, taux_plein_tva)
                )
            montant_sp98_ticpe_ajuste = (
                tax_from_expense_including_tax(depenses_sp_98_htva_ajustees, taux_implicite_sp98_ajuste)
                )

            return montant_sp98_ticpe_ajuste

    class quantite_sp98_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de TICPE sur le sp_98 après réforme"

        def formula(menage, period, parameters):
            reforme_essence = parameters(period.start).carbon_tax_rv.essence_with_carbon_tax_rv
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
            super_98_ttc_ajuste = super_98_ttc + reforme_essence * (1 + taux_plein_tva)

            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence_corrigees_carbon_tax_rv', period)
            part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
            depenses_sp_98_ajustees = depenses_essence_carbon_tax_rv * part_sp98

            return depenses_sp_98_ajustees / super_98_ttc_ajuste

    class super_plombe_ticpe_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur le super plombé après réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            accise_super_plombe_ticpe = \
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_plombe

            reforme_essence = parameters(period.start).carbon_tax_rv.essence_with_carbon_tax_rv
            accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe + reforme_essence
            super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
            super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence * (1 + taux_plein_tva)
            taux_implicite_super_plombe_ajuste = (
                (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
                / (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence_corrigees_carbon_tax_rv', period)
            part_super_plombe = \
                parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_carbon_tax_rv * part_super_plombe
            depenses_super_plombe_htva_ajustees = (
                depenses_super_plombe_ajustees
                - tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
                )
            montant_super_plombe_ticpe_ajuste = \
                tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

            return montant_super_plombe_ticpe_ajuste

    class super_plombe_ticpe_test(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur le super plombé sans réforme"

        def formula(menage, period, parameters):
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            accise_super_plombe_ticpe = \
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_plombe

            accise_super_plombe_ticpe_ajustee = accise_super_plombe_ticpe
            super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
            super_plombe_ttc_ajuste = super_plombe_ttc
            taux_implicite_super_plombe_ajuste = (
                (accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
                / (super_plombe_ttc_ajuste - accise_super_plombe_ticpe_ajustee * (1 + taux_plein_tva))
                )
            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence', period)
            part_super_plombe = \
                parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_carbon_tax_rv * part_super_plombe
            depenses_super_plombe_htva_ajustees = (
                depenses_super_plombe_ajustees
                - tax_from_expense_including_tax(depenses_super_plombe_ajustees, taux_plein_tva)
                )
            montant_super_plombe_ticpe_ajuste = \
                tax_from_expense_including_tax(depenses_super_plombe_htva_ajustees, taux_implicite_super_plombe_ajuste)

            return montant_super_plombe_ticpe_ajuste

    class quantite_super_plombe_carbon_tax_rv(YearlyVariable):
        value_type = float
        entity = Menage
        label = "Calcul du montant de la TICPE sur le super plombé après réforme"

        def formula(menage, period, parameters):
            reforme_essence = parameters(period.start).carbon_tax_rv.essence_with_carbon_tax_rv
            taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
            super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
            super_plombe_ttc_ajuste = super_plombe_ttc + reforme_essence * (1 + taux_plein_tva)
            depenses_essence_carbon_tax_rv = \
                menage('depenses_essence_corrigees_carbon_tax_rv', period)
            part_super_plombe = \
                parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
            depenses_super_plombe_ajustees = depenses_essence_carbon_tax_rv * part_super_plombe
            return depenses_super_plombe_ajustees / super_plombe_ttc_ajuste
        
    def apply(self):
        self.update_variable(self.cheques_energie)
        self.update_variable(self.bonus_cheques_energie)
        self.update_variable(self.contributions_reforme)
        self.update_variable(self.depenses_carburants_corrigees_carbon_tax_rv)
        self.update_variable(self.depenses_diesel_corrigees_carbon_tax_rv)
        self.update_variable(self.depenses_essence_corrigees_carbon_tax_rv)
        self.update_variable(self.diesel_ticpe_carbon_tax_rv)
        self.update_variable(self.diesel_ticpe_test)
        self.update_variable(self.quantite_diesel_carbon_tax_rv)
        self.update_variable(self.essence_ticpe_carbon_tax_rv)
        self.update_variable(self.essence_ticpe_test)
        self.update_variable(self.quantite_essence_carbon_tax_rv)
        self.update_variable(self.emissions_CO2_carburants)
        self.update_variable(self.revenu_reforme_carbon_tax_rv)
        self.update_variable(self.gains_tva_carburants_carbon_tax_rv)
        self.update_variable(self.ticpe_totale_carbon_tax_rv)
        self.update_variable(self.ticpe_totale_test)
        self.update_variable(self.sp_e10_ticpe_carbon_tax_rv)
        self.update_variable(self.sp_e10_ticpe_test)
        self.update_variable(self.quantite_sp_e10_carbon_tax_rv)
        self.update_variable(self.sp95_ticpe_carbon_tax_rv)
        self.update_variable(self.sp95_ticpe_test)
        self.update_variable(self.quantite_sp95_carbon_tax_rv)
        self.update_variable(self.sp98_ticpe_carbon_tax_rv)
        self.update_variable(self.sp98_ticpe_test)
        self.update_variable(self.quantite_sp98_carbon_tax_rv)
        self.update_variable(self.super_plombe_ticpe_carbon_tax_rv)
        self.update_variable(self.super_plombe_ticpe_test)
        self.update_variable(self.quantite_super_plombe_carbon_tax_rv)
        self.modify_parameters(modifier_function = modify_parameters)