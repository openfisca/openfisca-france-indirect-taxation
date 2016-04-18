# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import reforms


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'contribution_climat_energie_reforme',
        name = u"Réforme de la contribution climat energie anticipée simulée sur les données de 2014",
        reference = tax_benefit_system,
        )

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform

# Montants de taxe prévus par la loi Contribution climat-énergie. 7€ en 2014, 14,5€ en 2015, 22€ en 2016,
# 30,5€ en 2017, 39€ en 2018 et 47.5€ en 2019 En utilisant nos données d'équivalence entre consommation et émission,
# on met en place les montants de taxe suivants :
# Dans cette réforme on suppose qu'on impute à la législation de 2014 une augmentation équivalente à ce qui est prévu
# par la loi pour les années à venir.


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "contribution_climat_energie_reforme",
        "children": {
            "diesel_2014_2015": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du diesel (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2014-01-01', 'stop': '2014-12-31', 'value': 3.857 - 1.862}]
                },
            "diesel_2014_2016": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du diesel (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2014-01-01', 'stop': '2014-12-31', 'value': 5.852 - 1.862}]
                },
            "essence_2014_2015": {
                "@type": "Parameter",
                "description": u"Surcroît de prix de l'essence (en euros par hectolitres)",
                "format": "float",
                "unit": 'currency',
                "values": [{'start': u'2014-01-01', 'stop': '2014-12-31', 'value': 3.509 - 1.694}],
                },
            "essence_2014_2016": {
                "@type": "Parameter",
                "description": u"Surcroît de prix de l'essence (en euros par hectolitres)",
                "format": "float",
                "unit": 'currency',
                "values": [{'start': u'2014-01-01', 'stop': '2014-12-31', 'value': 5.324 - 1.694}],
                },
            "fioul_domestique_2014_2015": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du fioul domestique (en euros par litre)",
                "format": "float",
                "unit": 'currency',
                "values": [{'start': u'2014-01-01', 'stop': '2014-12-31', 'value': 0.04495 - 0.0217}],
                },
            "fioul_domestique_2014_2016": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du fioul domestique (en euros par litre)",
                "format": "float",
                "unit": 'currency',
                "values": [{'start': u'2014-01-01', 'stop': '2014-12-31', 'value': 0.0682 - 0.0217}],
                },
            "gaz_2014_2015": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du gaz (en euros par kWh)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2014-01-01', 'stop': '2014-12-31', 'value': 0.00348 - 0.00168}],
                },
            "gaz_2014_2016": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du gaz (en euros par kWh)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2014-01-01', 'stop': '2014-12-31', 'value': 0.00528 - 0.00168}],
                },
            "abaissement_tva_taux_plein_2014_2015": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.004}],
                },
            "abaissement_tva_taux_plein_2014_2016": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.008}],
                },
            "abaissement_tva_taux_plein_bis_2014_2015": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.002}],
                },
            "abaissement_tva_taux_plein_bis_2014_2016": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.005}],
                },
            "abaissement_tva_taux_reduit_2014_2015": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.004}],
                },
            "abaissement_tva_taux_reduit_2014_2016": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.006}],
                },
            "abaissement_tva_taux_super_reduit_2014_2015": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.004}],
                },
            "abaissement_tva_taux_super_reduit_2014_2016": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [{'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.006}],
                },
            },
        }

    reference_legislation_json_copy['children']['contribution_climat_energie_reforme'] = reform_legislation_subtree
    return reference_legislation_json_copy
