import numpy

from openfisca_core.reforms import Reform
from openfisca_france_indirect_taxation.variables.base import *
from openfisca_france_indirect_taxation.variables.revenus.revenus_menages import Deciles


def create_reforme_calage_depenses_cigarettes(
    agregat_depenses = None,
    year_calage = None
    ):
    
    assert agregat_depenses is not None
    assert year_calage is not None

    class calage_depenses_cigarettes(Reform):
        key = 'calage_depenses_cigarettes',
        name = "Réforme qui recale les dépenses de cigarettes pour atteindre un certain niveau agrégé",

        class depenses_cigarettes_calibre(YearlyVariable):
            value_type = float
            entity = Menage
            label = "Dépenses cigarettes calibrées au niveau individuel"

            def formula(menage, period, parameters):
                prix_paquet = parameters("{}-12-31".format(year_calage)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes
                paquets_par_menage = agregat_depenses / (menage('pondmen', period).sum())
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
                prix_paquet = parameters("{}-12-31".format(year_calage)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes
                paquets_par_menage = agregat_depenses / (menage('pondmen', period).sum())
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

        def apply(self):
            self.update_variable(self.depenses_cigarettes_calibre)
            self.update_variable(self.depenses_cigarettes_calibre_par_decile)

    return calage_depenses_cigarettes