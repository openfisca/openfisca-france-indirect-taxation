# -*- coding: utf-8 -*-

# Avant le 1e janvier 2014

# tva :
P_tva_taux_plein = 0.196
P_tva_taux_intermediaire = 0.07
P_tva_taux_reduit = 0.055
P_tva_taux_super_reduit = 0.021

# Pour l'année 2010

P_alcool_0211 = 1.734
P_alcool_0212 = 0.015
P_alcool_0213 = 0.411


legislation_json = {
    "start": u'2000-01-01',
    "stop": u'2014-12-31',
    "@type": "Node",
    "children": {
        "imposition_indirecte": {
            "@type": "Node",
            "description": "Impôts et taxes indirectes",
            "children": {
                "tva": {
                    "@type": "Node",
                    "description": "Taxe sur la valeur ajoutée",
                    "children": {
                        "taux_plein": {
                            "@type": "Parameter",
                            "description": "Taux plein",
                            "format": "float",
                            "values": [
                                {'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .196}
                                ],
                            },
                        "taux_intermediaire": {
                            "@type": "Parameter",
                            "description": "Taux intermédiaire",
                            "format": "float",
                            "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .07}],
                            },
                        "taux_reduit": {
                            "@type": "Parameter",
                            "description": "Taux réduit",
                            "format": "float",
                            "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .055}],
                            },
                        "taux_super_reduit": {
                            "@type": "Parameter",
                            "description": "Taux super réduit",
                            "format": "float",
                            "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .021}],
                            },
                        },
                    },
                },
            },
        }
    }
