# -*- coding: utf-8 -*-

from __future__ import division

from numpy import logical_not as not_, minimum as min_
from openfisca_core import columns, reforms

from .. import entities
from ..model.base import PREF
from ..model.prelevements_obligatoires.impot_revenu import charges_deductibles


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'alimentation',
        name = u"Réforme de l'imposition indirecte des biens alimentaires",
        reference = tax_benefit_system,
        )

    class charges_deduc(Reform.Variable):
        label = u"Charge déductibles intégrant la charge pour loyer (Trannoy-Wasmer)"
        reference = charges_deductibles.charges_deduc

        def function(menage, period, parameters):
            period = period.this_year
            cd1 = menage('cd1', period)
            cd2 = menage('cd2', period)
            charge_loyer = menage('charge_loyer', period)

            return period, cd1 + cd2 + charge_loyer

    class charge_loyer(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.FoyersFiscaux
        label = u"Charge déductible pour paiement d'un loyer"

        def function(foyer_fiscal, period, parameters):
            period = period.this_year
            loyer_i = foyer_fiscal.members.menage('loyer', period)
            loyer = foyer_fiscal.sum(loyer_i, role = Menage.PERSONNE_DE_REFERENCE)
            nbptr = simulation.calculate('nbptr', period)
            charge_loyer = parameters(period).charge_loyer

            plaf = charge_loyer.plaf
            plaf_nbp = charge_loyer.plaf_nbp
            plafond = plaf * (not_(plaf_nbp) + plaf * nbptr * plaf_nbp)

            return period, 12 * min_(loyer / 12, plafond)

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "Charge de loyer",
        "children": {
            "active": {
                "@type": "Parameter",
                "description": u"Activation de la charge",
                "format": "boolean",
                "values": [{'start': u'2002-01-01', 'stop': '2013-12-31', 'value': 1}],
                },
            "plaf": {
                "@type": "Parameter",
                "description": u'Plafond mensuel',
                "format": 'integer',
                "unit": 'currency',
                "values": [{'start': '2002-01-01', 'stop': '2013-12-31', 'value': 1000}],
                },
            "plaf_nbp": {
                "@type": "Parameter",
                "description": u'Ajuster le plafond au nombre de part',
                "format": 'boolean',
                "values": [{'start': '2002-01-01', 'stop': '2013-12-31', 'value': 0}],
                },
            },
        }
    reference_legislation_json_copy['children']['charge_loyer'] = reform_legislation_subtree
    return reference_legislation_json_copy
