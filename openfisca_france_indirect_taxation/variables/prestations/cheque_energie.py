
from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class cheques_energie_officielle_2019_in_2017(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des chèques énergie tels que prévus par la loi"

    def formula(menage, period):
        revenu_fiscal = menage('revdecm', period) / 1.22
        ocde10 = menage('ocde10', period)
        revenu_fiscal_uc = revenu_fiscal / ocde10

        cheque = (
            0
            + 144 * (revenu_fiscal_uc < 5600) * (ocde10 == 1)
            + 190 * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2)
            + 227 * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2))
            + 96 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 == 1)
            + 126 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 > 1) * (ocde10 < 2)
            + 152 * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * ((ocde10 == 2) + (ocde10 > 2))
            + 48 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 == 1)
            + 63 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 > 1) * (ocde10 < 2)
            + 76 * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * ((ocde10 == 2) + (ocde10 > 2))
            )

        return cheque


class cheques_energie_majore_officielle_2019_in_2017(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des chèques énergie tels que prévus par la loi"

    def formula(menage, period):
        revenu_fiscal = menage('revdecm', period) / 1.22
        ocde10 = menage('ocde10', period)
        revenu_fiscal_uc = revenu_fiscal / ocde10

        cheque = (
            0
            + (144 + 50) * (revenu_fiscal_uc < 5600) * (ocde10 == 1)
            + (190 + 50) * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2)
            + (227 + 50) * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2))
            + (96 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 == 1)
            + (126 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 > 1) * (ocde10 < 2)
            + (152 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * ((ocde10 == 2) + (ocde10 > 2))
            + (48 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 == 1)
            + (63 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 > 1) * (ocde10 < 2)
            + (76 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * ((ocde10 == 2) + (ocde10 > 2))
            )

        return cheque

class cheques_energie_philippe_officielle_2019_in_2017(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Montant des chèques énergie tels que prévus par la loi"

    def formula(menage, period):
        revenu_fiscal = menage('revdecm', period) / 1.22
        ocde10 = menage('ocde10', period)
        revenu_fiscal_uc = revenu_fiscal / ocde10

        cheque = (
            0
            + (144 + 50) * (revenu_fiscal_uc < 5600) * (ocde10 == 1)
            + (190 + 50) * (revenu_fiscal_uc < 5600) * (ocde10 > 1) * (ocde10 < 2)
            + (227 + 50) * (revenu_fiscal_uc < 5600) * ((ocde10 == 2) + (ocde10 > 2))
            + (96 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 == 1)
            + (126 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * (ocde10 > 1) * (ocde10 < 2)
            + (152 + 50) * (revenu_fiscal_uc > 5600) * (revenu_fiscal_uc < 6700) * ((ocde10 == 2) + (ocde10 > 2))
            + (48 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 == 1)
            + (63 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * (ocde10 > 1) * (ocde10 < 2)
            + (76 + 50) * (revenu_fiscal_uc > 6700) * (revenu_fiscal_uc < 7700) * ((ocde10 == 2) + (ocde10 > 2))
            + (48) * (revenu_fiscal_uc > 7700) * (revenu_fiscal_uc < 9700) * (ocde10 == 1)
            + (63) * (revenu_fiscal_uc > 7700) * (revenu_fiscal_uc < 9700) * (ocde10 > 1) * (ocde10 < 2)
            + (76) * (revenu_fiscal_uc > 7700) * (revenu_fiscal_uc < 9700) * ((ocde10 == 2) + (ocde10 > 2))
            )

        return cheque