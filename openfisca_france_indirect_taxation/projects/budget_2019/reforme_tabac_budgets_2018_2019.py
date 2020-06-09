# -*- coding: utf-8 -*-

from openfisca_core.reforms import Reform
from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore
from openfisca_france_indirect_taxation.projects.base import elasticite_tabac


def create_reforme_tabac_budgets_2018_2019(baseline_year = None):
    
    assert baseline_year is not None

    class reforme_tabac_budgets_2018_2019(Reform):
        key = 'reforme_tabac_budgets_2018_2019',
        name = "Réforme de la fiscalité tabac (tabac à rouler et cigarettes) prévue par les budgets 2018 et 2019",
    
    
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
