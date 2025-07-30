import numpy

from openfisca_core.reforms import Reform
from openfisca_france_indirect_taxation.variables.base import *
from openfisca_france_indirect_taxation.variables.revenus.revenus_menages import Deciles


def create_reforme_calage_depenses_cigarettes(
        agregat_depenses = None,
        niveau_calage = None,
        year_calage = None,
        ):

    assert agregat_depenses is not None
    assert niveau_calage in ['decile', 'individuel']
    assert year_calage is not None

    class calage_depenses_cigarettes(Reform):
        key = 'calage_depenses_cigarettes',
        name = 'Réforme qui recale les dépenses de cigarettes pour atteindre un certain niveau agrégé',

        if niveau_calage == 'individuel':
            class depenses_cigarettes(Variable):
                value_type = float
                entity = Menage
                definition_period = MONTH
                set_input = set_input_divide_by_period

                def formula(menage, period, parameters):
                    prix_paquet = parameters('{}-12-31'.format(year_calage)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes
                    paquets_par_menage = agregat_depenses / 12 / (menage('pondmen', period.this_year).sum())
                    nombre_paquets_imputes = (
                        paquets_par_menage
                        * (menage('poste_02_2_1', period, options = [DIVIDE]) * menage('pondmen', period.this_year) * len(menage('pondmen', period.this_year)))
                        / ((menage('poste_02_2_1', period, options = [DIVIDE]) * menage('pondmen', period.this_year)).sum())
                        )
                    return nombre_paquets_imputes * prix_paquet

        elif niveau_calage == 'decile':
            class depenses_cigarettes(Variable):
                value_type = float
                entity = Menage
                definition_period = MONTH
                set_input = set_input_divide_by_period

                def formula(menage, period, parameters):
                    prix_paquet = parameters('{}-12-31'.format(year_calage)).imposition_indirecte.taxes_tabacs.prix_tabac.prix_paquet_cigarettes
                    paquets_par_menage = agregat_depenses / 12 / (menage('pondmen', period.this_year).sum())
                    decile = menage('niveau_vie_decile', period.this_year)
                    depenses_cigarettes_totales = (menage('poste_02_2_1', period, options = [DIVIDE]) * menage('pondmen', period.this_year)).sum()
                    depenses_cigarettes_decile = list()
                    nombre_paquets_imputes = list()
                    for i in range(1, 11):
                        depenses_cigarettes_decile.append(
                            (
                                menage('poste_02_2_1', period, options = [DIVIDE])
                                * menage('pondmen', period.this_year)
                                * (decile == i)
                                ).sum()
                            )
                        nombre_paquets_imputes.append(
                            (
                                paquets_par_menage
                                * (depenses_cigarettes_decile[i - 1] * 10)
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
                        default = 0.0
                        )

        def apply(self):
            self.update_variable(self.depenses_cigarettes)

    return calage_depenses_cigarettes


def create_reforme_calage_depenses_tabac(
        agregat_depenses = None,
        year_calage = None,
        ):

    assert agregat_depenses is not None
    assert year_calage is not None

    class calage_depenses(Reform):
        key = 'calage_depenses_cigarettes',
        name = 'Réforme qui recale les dépenses de cigarettes pour atteindre un certain niveau agrégé',

        class depenses_cigarettes(Variable):
            value_type = float
            entity = Menage
            definition_period = MONTH
            set_input = set_input_divide_by_period

            def formula(menage, period, parameters):
                agregats_bdf = (
                    ((menage('poste_02_2_1', period, options = [DIVIDE]) * menage('pondmen', period.this_year))
                    + (menage('poste_02_2_2', period, options = [DIVIDE]) * menage('pondmen', period.this_year))
                    + (menage('poste_02_2_3', period, options = [DIVIDE]) * menage('pondmen', period.this_year))).sum()
                    )

                return menage('poste_02_2_1', period, options = [DIVIDE]) * (agregat_depenses / 12 / agregats_bdf)

        class depenses_cigares(Variable):
            value_type = float
            entity = Menage
            set_input = set_input_divide_by_period

            def formula(menage, period):
                agregats_bdf = (
                    ((menage('poste_02_2_1', period, options = [DIVIDE]) * menage('pondmen', period.this_year))
                    + (menage('poste_02_2_2', period, options = [DIVIDE]) * menage('pondmen', period.this_year))
                    + (menage('poste_02_2_3', period, options = [DIVIDE]) * menage('pondmen', period.this_year))).sum()
                    )

                return menage('poste_02_2_2', period, options = [DIVIDE]) * (agregat_depenses / 12 / agregats_bdf)

        class depenses_tabac_a_rouler(Variable):
            value_type = float
            entity = Menage
            definition_period = MONTH
            set_input = set_input_divide_by_period

            def formula(menage, period):
                agregats_bdf = (
                    ((menage('poste_02_2_1', period, options = [DIVIDE]) * menage('pondmen', period.this_year))
                    + (menage('poste_02_2_2', period, options = [DIVIDE]) * menage('pondmen', period.this_year))
                    + (menage('poste_02_2_3', period, options = [DIVIDE]) * menage('pondmen', period.this_year))).sum()
                    )

                return menage('poste_02_2_3', period, options = [DIVIDE]) * (agregat_depenses / 12 / agregats_bdf)

        def apply(self):
            self.update_variable(self.depenses_cigarettes)
            self.update_variable(self.depenses_cigares)
            self.update_variable(self.depenses_tabac_a_rouler)

    return calage_depenses
