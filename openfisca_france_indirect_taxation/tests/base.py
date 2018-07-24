# -*- coding: utf-8 -*-


from openfisca_core.reforms import Reform, compose_reforms
from openfisca_core.tools import assert_near

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.reforms import (
    alimentation,
    aliss,
    cce_2015_in_2014,
    cce_2016_in_2014,
    contribution_climat_energie_reforme,
    officielle_2018_in_2016,
    rattrapage_diesel,
    taxe_carbone,
    reforme_tva_2019,
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
    'rattrapage_diesel': rattrapage_diesel.rattrapage_diesel,
    'taxe_carbone': taxe_carbone.taxe_carbone,
    'cce_2015_in_2014': cce_2015_in_2014.cce_2015_in_2014,
    'cce_2016_in_2014': cce_2016_in_2014.cce_2016_in_2014,
    'officielle_2018_in_2016': officielle_2018_in_2016.officielle_2018_in_2016,
    'reforme_tva_2019': reforme_tva_2019.reforme_tva_2019,
    # 'contribution_climat_energie': contribution_climat_energie.build_reform,
    # 'test_reforme_alimentation': alimentation.build_reform,
    # 'taxes_carburants': taxes_carburants.build_reform,
    # 'taxe_carbone': taxe_carbone.build_reform,
    }

reform_by_full_key = {}


def get_cached_composed_reform(reform_keys, tax_benefit_system):
    full_key = '.'.join(
        [tax_benefit_system.full_key] + reform_keys
        if isinstance(tax_benefit_system, Reform)
        else reform_keys
        )
    composed_reform = reform_by_full_key.get(full_key)

    if composed_reform is None:
        reforms = []
        for reform_key in reform_keys:
            assert reform_key in reform_list, \
                'Error loading cached reform "{}" in build_reform_functions'.format(reform_key)
            reform = reform_list[reform_key]
            reforms.append(reform)
        composed_reform = compose_reforms(
            reforms = reforms,
            tax_benefit_system = tax_benefit_system,
            )
        assert full_key == composed_reform.full_key, (full_key, composed_reform.full_key)
        reform_by_full_key[full_key] = composed_reform
    return composed_reform


def get_cached_reform(reform_key, tax_benefit_system):
    return get_cached_composed_reform([reform_key], tax_benefit_system)
