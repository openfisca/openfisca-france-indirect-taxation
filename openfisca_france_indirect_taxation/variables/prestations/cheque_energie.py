import numpy

from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class cheques_energie(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Montant des chèques énergie tels que prévus par la loi'

    def formula(menage, period, parameters):
        revenu_fiscal = numpy.maximum(0.0, menage('revdecm', period) / 1.22)
        ocde10 = menage('ocde10', period)
        revenu_fiscal_uc = revenu_fiscal / ocde10
        bareme_cheque_energie = parameters(period).prestations.cheque_energie

        return numpy.select(
            [
                (ocde10 == 1),
                ((ocde10 > 1) * (ocde10 < 2)),
                (ocde10 >= 2),
                ],
            [
                bareme_cheque_energie.menage_avec_1_uc.calc(revenu_fiscal_uc),
                bareme_cheque_energie.menage_entre_1_et_2_uc.calc(revenu_fiscal_uc),
                bareme_cheque_energie.menage_avec_2_uc_et_plus.calc(revenu_fiscal_uc),
                ],
            default = 0.0
            )
