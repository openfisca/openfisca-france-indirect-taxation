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
                                {'start': u'2000-01-01', 'stop': u'2013-12-31', 'value': .196},
                                {'start': u'2014-01-01', 'stop': u'2015-12-31', 'value': .2},
                                ],
                            },
                        "taux_intermediaire": {
                            "@type": "Parameter",
                            "description": "Taux intermédiaire",
                            "format": "float",
                            "values": [{'start': u'2012-01-01', 'stop': u'2014-12-31', 'value': .07}],
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
                "alcool": {
                    "@type": "Node",
                    "description": "alcools",
                    "children": {
                        "vin": {
                            "@type": "Node",
                            "description": "Pour calculer le taux de taxation implicite sur la bière",
                            "children": {
                                "droit_cn_vin": {
                                    "@type": "Parameter",
                                    "description": "Masse droit vin selon comptabilité nationale",
                                    "format": "float",
                                    "values": [
#                                        {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 127},
#                                        {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 127},
#                                        {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 127},
#                                        {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 127},
#                                        {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 125},
#                                        {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 117},
#                                        {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 119},
#                                        {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 117},
#                                        {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 114},
#                                        {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 117},
#                                        {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 119},
#                                        {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 118},
#                                        {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 120},
# Pour 2013 les données proviennent de la commission européenne "Excise Duty Table"
#                                        {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 118 },
#TO DO trouver les droits 2014           {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value':  },
#                                        
                                        ],
                                    },
                                },
                            },
                        "biere": {
                            "@type": "Node",
                            "description": "Masse droit bière selon comptabilité nationale",
                            "children": {
                                "droit_cn_biere": {
                                    "@type": "Parameter",
                                    "description": "Masse droit bière selon comptabilité nationale",
                                    "format": "float",
                                    "values": [
#                                        {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 359}
#                                        {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 364},
#                                        {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 361},
#                                        {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 370},
#                                        {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 378},
#                                        {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 364},
#                                        {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 396},
#                                        {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 382},
#                                        {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 375},
#                                        {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 376},
#                                        {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 375},
#                                        {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 375},
#                                        {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 375},
# Pour 2013 les données proviennent de la commission européenne "Excise Duty Table"
#                                        {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 670 },
# TO DO trouver les droits 2014          {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value':  },
                                        ],
                                    },
                                "conso_cn_biere": {
                                    "@type": "Parameter",
                                    "description": "Masse droit alcools selon comptabilité nationale",
                                    "format": "float",
                                    "values": [
                                        {'start': u'2005-01-01', 'stop': u'2009-12-31', 'value': .021},
                                        {'start': u'2009-01-01', 'stop': u'2010-12-31', 'value': .021},
                                        {'start': u'2010-01-01', 'stop': u'2011-12-31', 'value': .021},
                                        {'start': u'2011-01-01', 'stop': u'2012-12-31', 'value': .021},
                                        {'start': u'2012-01-01', 'stop': u'2013-12-31', 'value': .021},
                                        {'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': .021},
                                        {'start': u'2014-01-01', 'stop': u'2015-12-31', 'value': .021}
                                        ],
                                    },
                                },
                            },
                        }
                    },
                "tabac": {
                    "@type": "Node",
                    "description": "Pour calculer le taux de taxation implicite sur la bière",
                    "children": {
                        "cigarettes": {
                            "@type": "Parameter",
                            "description": "Taux de taxation cigarettes",
                            "format": "float",
                            "values": [
                                {'start': u'2004-05-01', 'stop': u'2010-12-31', 'value': .64},
                                {'start': u'2010-01-01', 'stop': u'2013-01-06', 'value': .6425},
                                {'start': u'2013-01-07', 'stop': u'2015-12-31', 'value': .647}
                                ],
                            },
                        "cigares": {
                            "@type": "Parameter",
                            "description": "Masse droit bière selon comptabilité nationale",
                            "format": "float",
                            "values": [
                                #TODO:
                                {'start': u'2004-05-01', 'stop': u'2010-12-31', 'value': .64},
                                {'start': u'2010-01-01', 'stop': u'2013-01-06', 'value': .6425},
                                {'start': u'2013-01-07', 'stop': u'2015-12-31', 'value': .647},
                                ],
                            },
                        },
                    },
                },
            },
        }
    }