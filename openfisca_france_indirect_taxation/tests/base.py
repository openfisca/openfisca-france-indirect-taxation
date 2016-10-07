# -*- coding: utf-8 -*-


from openfisca_core.reforms import Reform, compose_reforms
from openfisca_core.tools import assert_near

from .. import FranceIndirectTaxationTaxBenefitSystem
from ..reforms import (
    alimentation,
    aliss,
    contribution_climat_energie,
    taxes_carburants,
    taxe_carbone,
    )


__all__ = [
    'assert_near',
    'get_cached_composed_reform',
    'get_cached_reform',
    'tax_benefit_system',
    ]

# Initialize a tax_benefit_system
tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()


# Reforms cache, used by long scripts like test_yaml.py
# The reforms commented haven't been adapted to the new core API yet.
reform_list = {
    'aliss_ajustable': aliss.aliss_ajustable,
    'aliss_environnement': aliss.aliss_environnement,
    'aliss_mixte': aliss.aliss_mixte,
    'aliss_sante': aliss.aliss_sante,
    'aliss_tva_sociale': aliss.aliss_tva_sociale,
    # 'contribution_climat_energie': contribution_climat_energie.build_reform,
    # 'test_reforme_alimentation': alimentation.build_reform,
    # 'taxes_carburants': taxes_carburants.build_reform,
    # 'taxe_carbone': taxe_carbone.build_reform,
    }

reform_by_full_key = {}
