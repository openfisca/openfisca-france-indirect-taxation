# -*- coding: utf-8 -*-

import numpy

from openfisca_core.reforms import Reform
from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore
from openfisca_france_indirect_taxation.variables.revenus.revenus_menages import Deciles
from openfisca_france_indirect_taxation.projects.base import elasticite_tabac, nombre_paquets_cigarettes_by_year


def create_reforme_tabac_budgets_2018_2019(baseline_year = None):
    
    assert baseline_year is not None
    
    class reforme_tabac_budgets_2018_2019(Reform):
        key = 'reforme_tabac_budgets_2018_2019',
        name = "Réforme de la fiscalité tabac (tabac à rouler et cigarettes) prévue par les budgets 2018 et 2019",
    
        class depenses_cigarettes_calibre(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses cigarettes calibrées au niveau individuel"
    
            def formula(menage, period, parameters):
                prix_paquet = parameters("{}-01-01".format(baseline_year)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes
                paquets_par_menage = nombre_paquets_cigarettes_by_year[2017] / (menage('pondmen', period).sum())
                nombre_paquets_imputes = (
                    paquets_par_menage 
                    * (menage('depenses_cigarettes', period) * menage('pondmen', period) * len(menage('pondmen', period))) 
                    / ((menage('depenses_cigarettes', period) * menage('pondmen', period)).sum())
                    )
                return nombre_paquets_imputes * prix_paquet
    
        class depenses_cigarettes_calibre_par_decile(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses cigarettes calibrées au niveau du décile"
    
            def formula(menage, period, parameters):
                prix_paquet = parameters("{}-01-01".format(baseline_year)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes
                paquets_par_menage = nombre_paquets_cigarettes_by_year[2017] / (menage('pondmen', period).sum())
                decile = menage('niveau_vie_decile', period)
                depenses_cigarettes_totales = (menage('depenses_cigarettes', period) * menage('pondmen', period)).sum()
                depenses_cigarettes_decile = list()
                nombre_paquets_imputes = list()
                for i in range(1,11):
                    depenses_cigarettes_decile.append(
                        (
                        menage('depenses_cigarettes', period) 
                        * menage('pondmen', period) 
                        * (decile == i)
                        ).sum()
                        )
                    nombre_paquets_imputes.append(
                        (
                        paquets_par_menage 
                        * (depenses_cigarettes_decile[i-1] * 10) 
                        / depenses_cigarettes_totales
                        )
                        )
                return numpy.select(
                    [
                        (decile == Deciles.decile_1),
                        (decile == Deciles.decile_2),
                        (decile == Deciles.decile_3),
                        (decile == Deciles.decile_4),
                        (decile == Deciles.decile_5),
                        (decile == Deciles.decile_6),
                        (decile == Deciles.decile_7),
                        (decile == Deciles.decile_8),
                        (decile == Deciles.decile_9),
                        (decile == Deciles.decile_10),
                        ],
                    [
                        nombre_paquets_imputes[0] * prix_paquet,
                        nombre_paquets_imputes[1] * prix_paquet,
                        nombre_paquets_imputes[2] * prix_paquet,
                        nombre_paquets_imputes[3] * prix_paquet,
                        nombre_paquets_imputes[4] * prix_paquet,
                        nombre_paquets_imputes[5] * prix_paquet,
                        nombre_paquets_imputes[6] * prix_paquet,
                        nombre_paquets_imputes[7] * prix_paquet,
                        nombre_paquets_imputes[8] * prix_paquet,
                        nombre_paquets_imputes[9] * prix_paquet,
                        ],
                    default=0.0
                    )
    
        class depenses_cigarettes_calibre_apres_reforme_mars_2018(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses de cigarettes après prise en compte des réactions comportementales"
    
            def formula(menage, period, parameters):
                prix_paquet_baseline = parameters("{}-12-31".format(baseline_year)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes
                prix_paquet_reforme = parameters("2018-03-01").imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes 
                depenses_cigarettes_calibre = menage('depenses_cigarettes_calibre_par_decile', period)
                depenses_cigarettes_calibre_elast = (
                    depenses_cigarettes_calibre 
                    * (
                        1 + (1 + elasticite_tabac) * (
                        (prix_paquet_reforme - prix_paquet_baseline) / prix_paquet_baseline
                        )
                    ))
    
                return depenses_cigarettes_calibre_elast
    
    
        class depenses_cigarettes_calibre_apres_reforme_mars_2019(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses de cigarettes après prise en compte des réactions comportementales"
    
            def formula(menage, period, parameters):
                prix_paquet_baseline = parameters("{}-12-31".format(baseline_year)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes
                prix_paquet_reforme = parameters("2019-03-01").imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes 
                depenses_cigarettes_calibre = menage('depenses_cigarettes_calibre_par_decile', period)
                depenses_cigarettes_calibre_elast = (
                    depenses_cigarettes_calibre 
                    * (
                        1 + (1 + elasticite_tabac) * (
                        (prix_paquet_reforme - prix_paquet_baseline) / prix_paquet_baseline
                        )
                    ))
    
                return depenses_cigarettes_calibre_elast
    
        class depenses_cigarettes_calibre_apres_reforme_novembre_2019(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses de cigarettes après prise en compte des réactions comportementales"
    
            def formula(menage, period, parameters):
                prix_paquet_baseline = parameters("{}-12-31".format(baseline_year)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes
                prix_paquet_reforme = parameters("2019-11-01").imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes 
                depenses_cigarettes_calibre = menage('depenses_cigarettes_calibre_par_decile', period)
                depenses_cigarettes_calibre_elast = (
                    depenses_cigarettes_calibre 
                    * (
                        1 + (1 + elasticite_tabac) * (
                        (prix_paquet_reforme - prix_paquet_baseline) / prix_paquet_baseline
                        )
                    ))
    
                return depenses_cigarettes_calibre_elast
    
    
        class depenses_tabac_a_rouler_apres_reforme_mars_2018(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses de tabac à rouler après prise en compte des réactions comportementales"
    
            def formula(menage, period, parameters):
                prix_baseline = parameters("{}-12-31".format(baseline_year)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_bague_tabac
                prix_reforme = parameters("2018-03-01").imposition_indirecte.taxes_tabacs.prix_tabac.prix_bague_tabac 
                depenses_tabac_a_rouler = menage('depenses_tabac_a_rouler', period)
                depenses_tabac_a_rouler_elast = (
                    depenses_tabac_a_rouler 
                    * (
                        1 + (1 + elasticite_tabac) * (
                        (prix_reforme - prix_baseline) / prix_baseline
                        )
                    ))
    
                return depenses_tabac_a_rouler_elast
    
        class depenses_tabac_a_rouler_apres_reforme_mars_2019(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses de tabac à rouler après prise en compte des réactions comportementales"
    
            def formula(menage, period, parameters):
                prix_baseline = parameters("{}-12-31".format(baseline_year)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_bague_tabac
                prix_reforme = parameters("2019-03-01").imposition_indirecte.taxes_tabacs.prix_tabac.prix_bague_tabac 
                depenses_tabac_a_rouler = menage('depenses_tabac_a_rouler', period)
                depenses_tabac_a_rouler_elast = (
                    depenses_tabac_a_rouler 
                    * (
                        1 + (1 + elasticite_tabac) * (
                        (prix_reforme - prix_baseline) / prix_baseline
                        )
                    ))
    
                return depenses_tabac_a_rouler_elast
    
        class depenses_tabac_a_rouler_apres_reforme_novembre_2019(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses de tabac à rouler après prise en compte des réactions comportementales"
    
            def formula(menage, period, parameters):
                prix_baseline = parameters("{}-12-31".format(baseline_year)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_bague_tabac
                prix_reforme = parameters("2019-11-01").imposition_indirecte.taxes_tabacs.prix_tabac.prix_bague_tabac 
                depenses_tabac_a_rouler = menage('depenses_tabac_a_rouler', period)
                depenses_tabac_a_rouler_elast = (
                    depenses_tabac_a_rouler 
                    * (
                        1 + (1 + elasticite_tabac) * (
                        (prix_reforme - prix_baseline) / prix_baseline
                        )
                    ))
    
                return depenses_tabac_a_rouler_elast
    
    
        class depenses_tabac_calibre(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses de tabac contrefactuelles (après recalibration des dépenses de cigarettes)"
    
            def formula(menage, period):
    
                depenses_cigarettes_calibre = menage('depenses_cigarettes_calibre_par_decile', period) 
                depenses_tabac_a_rouler = menage('depenses_tabac_a_rouler', period) 
    
                return depenses_cigarettes_calibre + depenses_tabac_a_rouler
        
        
        class depenses_cigarettes_post_reforme(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses de cigarettes suite aux réformes introduites par le bugdet 2019 par rapport à la situation au 31/12/2018"
    
            def formula(menage, period):
    
                depenses_cigarettes = (
                    2 * menage('depenses_cigarettes_calibre_apres_reforme_mars_2018', period) # dépenses contrefactuelles (pas de réforme de janvier à février)
                    + 8 * menage('depenses_cigarettes_calibre_apres_reforme_mars_2019', period) # effet de mars à octobre
                    + 2 * menage('depenses_cigarettes_calibre_apres_reforme_novembre_2019', period) # effet de novembre à décembre
                    ) / 12
    
                return depenses_cigarettes
    
        class depenses_tabac_a_rouler_post_reforme(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses de tabac à rouler suite aux réformes introduites par le bugdet 2019 par rapport à la situation au 31/12/2018"
    
            def formula(menage, period):
    
                depenses_tabac_a_rouler = (
                    2 * menage('depenses_tabac_a_rouler_apres_reforme_mars_2018', period) # dépenses contrefactuelles (pas de réforme de janvier à février)
                    + 8 * menage('depenses_tabac_a_rouler_apres_reforme_mars_2019', period) # effet de mars à octobre
                    + 2 * menage('depenses_tabac_a_rouler_apres_reforme_novembre_2019', period) # effet de novembre à décembre
                    ) / 12
                
                return depenses_tabac_a_rouler
        
    
        class depenses_tabac_post_reforme(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses de tabac suite aux réformes introduites par le bugdet 2019 par rapport à la situation au 31/12/2018"
    
            def formula(menage, period):
                
                cigarettes = menage('depenses_cigarettes_post_reforme', period) 
                tabac_a_rouler = menage('depenses_tabac_a_rouler_post_reforme', period) 
                
                return cigarettes + tabac_a_rouler
    
    
        def apply(self):
            self.update_variable(self.depenses_cigarettes_calibre)
            self.update_variable(self.depenses_cigarettes_calibre_par_decile)
            self.update_variable(self.depenses_cigarettes_calibre_apres_reforme_mars_2018)
            self.update_variable(self.depenses_cigarettes_calibre_apres_reforme_mars_2019)
            self.update_variable(self.depenses_cigarettes_calibre_apres_reforme_novembre_2019)
            self.update_variable(self.depenses_tabac_a_rouler_apres_reforme_mars_2018)
            self.update_variable(self.depenses_tabac_a_rouler_apres_reforme_mars_2019)
            self.update_variable(self.depenses_tabac_a_rouler_apres_reforme_novembre_2019)
            self.update_variable(self.depenses_tabac_calibre)
            self.update_variable(self.depenses_cigarettes_post_reforme)
            self.update_variable(self.depenses_tabac_a_rouler_post_reforme)
            self.update_variable(self.depenses_tabac_post_reforme)
            

    return reforme_tabac_budgets_2018_2019
