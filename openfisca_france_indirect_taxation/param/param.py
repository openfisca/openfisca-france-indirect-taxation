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
                            "values": [
                                {'start': u'200-01-01', 'stop': u'2012-12-31', 'value': 0},
                                {'start': u'2012-01-01', 'stop': u'2014-12-31', 'value': .07},
                                {'start': u'2014-01-01', 'stop': u'2015-12-31', 'value': .1}
                                ],
                            },
                        "taux_reduit": {
                            "@type": "Parameter",
                            "description": "Taux réduit",
                            "format": "float",
                            "values": [
                                {'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .055}
                                ],
                            },
                        "taux_super_reduit": {
                            "@type": "Parameter",
                            "description": "Taux super réduit",
                            "format": "float",
                            "values": [
                                {'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .021}
                                ],
                            },
                        },
                    },
                "taux_assurances": {
                    "@type": "Node",
                    "description": "Différentes taxes sur les assurances",
                    "children": {
                        "taux_assur_transport": {
                            "@type": "Parameter",
                            "description": "Le taux d'assurance sur les transports",
                            "format": "float",
                            "values": [
                                {'start': u'2000-01-01', 'stop': u'2001-12-31', 'value': 0.18},
                                {'start': u'2002-01-01', 'stop': u'2004-12-31', 'value': 0.33},
                                {'start': u'2005-01-01', 'stop': u'2007-12-31', 'value': 0.331},
                                {'start': u'2008-01-01', 'stop': u'2009-12-31', 'value': 0.336},
                                {'start': u'2010-01-01', 'stop': u'2014-12-31', 'value': 0.342},
                                ],
                            },
                        "taux_assurances_sante": {
                            "@type": "Parameter",
                            "description": "Le taux d'assurance sante",
                            "format": "float",
                            "values": [
                                {'start': u'2000-01-01', 'stop': u'2002-12-31', 'value': 0.0875},
                                {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 0.0775},
                                {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 0.0675},
                                {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 0.0575},
                                {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 0.055},
                                {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 0.045},
                                {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 0.035},
                                {'start': u'2009-01-01', 'stop': u'2010-12-31', 'value': 0.059},
                                {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 0.094},
                                {'start': u'2012-01-01', 'stop': u'2014-12-31', 'value': 0.1327},
                                ],
                            },
                        "taux_assurances_autres": {
                            "@type": "Parameter",
                            "description": "Le taux d'assurance sur autres",
                            "format": "float",
                            "values": [
                                {'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 0.09},
                                ],
                            },
                        },
                    },
                "prix_carburants": {
                    "@type": "Node",
                    "description": "prix des carburants",
                    "children": {
                        "prix_ttc_gazole": {
                            "@type": "Parameter",
                            "description": "prix ttc gazole",
                            "format": "float",
                            "values": [
                                # Deplacer les prix dans un autre arbre ?s
                                {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 84.68271802},
                                {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 79.60183423},
                                {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 77.24235269},
                                {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 79.34711538},
                                {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 88.4709434},
                                {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 102.6803846},
                                {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 107.7509615},
                                {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 109.4932692},
                                {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 126.7092308},
                                {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 100.235},
                                {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 114.6749057},
                                {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 133.42},
                                {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 139.58},
                                {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 135.02},
                                {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 128.56},
                                ],
                            },
                        "prix_ttc_super95": {
                            "@type": "Parameter",
                            "description": "Prix ttc super95 ",
                            "format": "float",
                            "values": [
                                {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 109.1731165},
                                {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 103.2881858},
                                {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 101.4594819},
                                {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 101.6317308},
                                {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 106.0273585},
                                {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 116.5913462},
                                {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 123.6817308},
                                {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 127.6451923},
                                {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 135.3755769},
                                {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 120.9205769},
                                {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 134.6401887},
                                {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 149.94},
                                {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 156.58},
                                {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 153.67},
                                {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 148.46},
                                ],
                            },
                        "prix_ttc_super98": {
                            "@type": "Parameter",
                            "description": "prix ttc super98",
                            "format": "float",
                            "values": [
                                {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 110.9293672},
                                {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 105.7028769},
                                {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 103.6501704},
                                {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 103.655},
                                {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 108.2684906},
                                {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 120.5273077},
                                {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 127.4303846},
                                {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 130.8551923},
                                {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 139.2867308},
                                {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 124.3081974},
                                {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 138.214717},
                                {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 153.75},
                                {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 161.82},
                                {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 159.43},
                                {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 154.48},
                                ],
                            },
                        },
                    },
                "tipp": {
                    "@type": "Node",
                    "description": "tipp sur les différents carburants",
                    "children": {
                        "tipp_super9598": {
                            "@type": "Parameter",
                            "description": "tipp sur super95 super98",
                            "format": "float",
                            "values": [
                                {'start': u'2000-01-01', 'stop': u'2002-12-31', 'value': 58.63},
                                {'start': u'2003-01-01', 'stop': u'2006-12-31', 'value': 58.92},
                                {'start': u'2007-01-01', 'stop': u'2010-12-31', 'value': 60.69},
                                {'start': u'2011-01-01', 'stop': u'2014-12-31', 'value': 61.42},
                                ],
                            },
                        "tipp_gazole": {
                            "@type": "Parameter",
                            "description": "tipp sur gazole ",
                            "format": "float",
                            "values": [
                                {'start': u'2000-01-01', 'stop': u'2002-12-31', 'value': 38.9},
                                {'start': u'2003-01-01', 'stop': u'2006-12-31', 'value': 39.19},
                                {'start': u'2007-01-01', 'stop': u'2010-12-31', 'value': 42.84},
                                {'start': u'2011-01-01', 'stop': u'2014-12-31', 'value': 44.19},
                                ],
                            },
                        },
                    },
                "alcool_conso_et_vin": {
                    "@type": "Node",
                    "description": "alcools",
                    "children": {
                        "vin": {
                            "@type": "Node",
                            "description": "Pour calculer le taux de taxation implicite sur le vin",
                            "children": {
                                "droit_cn_vin": {
                                    "@type": "Parameter",
                                    "description": "Masse droit vin, vin mousseux, cidres et poirés selon comptabilité nationale",
                                    "format": "float",
                                    "values": [
                                        {'start': u'2000-01-01', 'stop': u'2003-12-31', 'value': 127},
                                        {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 125},
                                        {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 117},
                                        {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 119},
                                        {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 117},
                                        {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 114},
                                        {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 117},
                                        {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 119},
                                        {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 118},
                                        {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 120},
                                        {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 122},
#                                       {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                                        ],
                                    },
                                "masse_conso_cn_vin": {
                                    "@type": "Parameter",
                                    "description": "Masse consommation vin, vin mousseux, cidres et poirés selon comptabilité nationale",
                                    "format": "float",
                                    "values": [
                                        {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 8854},
                                        {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 9168},
                                        {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 9476},
                                        {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 9695},
                                        {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 9985},
                                        {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 9933},
                                        {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 10002},
                                        {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 10345},
                                        {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 10461},
                                        {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 10728},
                                        {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 11002},
                                        {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 11387},
                                        {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 11407},
                                        {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 11515},
#                                       {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                                        ],
                                    },
                                },
                            },
                        "biere": {
                            "@type": "Node",
                            "description": "Pour calculer le taux de taxation implicite sur la bière",
                            "children": {
                                "droit_cn_biere": {
                                    "@type": "Parameter",
                                    "description": "Masse droit biere selon comptabilité nationale",
                                    "format": "float",
                                    "values": [
                                        {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 359},
                                        {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 364},
                                        {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 361},
                                        {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 370},
                                        {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 378},
                                        {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 364},
                                        {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 396},
                                        {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 382},
                                        {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 375},
                                        {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 376},
                                        {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 375},
                                        {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 393},
                                        {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 783},
                                        {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 897},
#                                       {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                                        ],
                                    },
                                "masse_conso_cn_biere": {
                                    "@type": "Parameter",
                                    "description": "Masse consommation biere selon comptabilité nationale",
                                    "format": "float",
                                    "values": [
                                        {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 2290},
                                        {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 2327},
                                        {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 2405},
                                        {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 2554 },
                                        {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 2484 },
                                        {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 2466 },
                                        {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 2486 },
                                        {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 2458 },
                                        {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 2287 },
                                        {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 2375 },
                                        {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 2461 },
                                        {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 2769 },
                                        {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 2868 },
                                        {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 3321 },
#                                       {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                                        ],
                                    },
                                },
                            },
                        "alcools_forts": {
                            "@type": "Node",
                            "description": "Pour calculer le taux de taxation implicite sur alcools forts",
                            "children": {
                                "droit_cn_alcools": {
                                    "@type": "Parameter",
                                    "description": "Masse droit alcool selon comptabilité nationale",
                                    "format": "float",
                                    "values": [
                                        {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 1872},
                                        {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 1957},
                                        {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 1932},
                                        {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 1891},
                                        {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 1908},
                                        {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 1842},
                                        {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 1954},
                                        {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 1990},
                                        {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 2005},
                                        {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 2031},
                                        {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 2111},
                                        {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 2150},
                                        {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 2225},
                                        #TODO: trouver les droits apres 2012
                                        ],
                                    },
                                "masse_conso_cn_alcools": {
                                    "@type": "Parameter",
                                    "description": "Masse droit alcool selon comptabilité nationale",
                                    "format": "float",
                                    "values": [
#                                        {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 1872},
                                        ],
                                    },
                                },
                            },
                        },
                    },
                "tabac": {
                    "@type": "Node",
                    "description": "Pour calculer le taux de taxation implicite sur le tabac",
                    "children": {
                        "cigarettes": {
                            "@type": "Parameter",
                            "description": "Taux de taxation cigarettes",
                            "format": "float",
                            "values": [
                                {'start': u'2000-01-01', 'stop': u'2000-03-31', 'value': 0.5830},
                                {'start': u'2000-04-01', 'stop': u'2003-08-31', 'value': 0.5899},
                                {'start': u'2003-09-01', 'stop': u'2004-04-30', 'value': 0.62},
                                {'start': u'2004-04-30', 'stop': u'2010-12-31', 'value': 0.64}
                                {'start': u'2011-01-01', 'stop': u'2013-06-30', 'value': 0.6425}
#                               {'start': u'2013-07-01', 'stop': u'', 'value':}
                                ],
                            },
#                            Continuer sur le tabac
                        "cigares": {
                            "@type": "Parameter",
                            "description": "Masse droit bière selon comptabilité nationale",
                            "format": "float",
                            "values": [
                                #TODO:
                                {'start': u'2004-05-01', 'stop': u'2010-12-31', 'value': },
                                {'start': u'2010-01-01', 'stop': u'2013-01-06', 'value': },
                                {'start': u'2013-01-07', 'stop': u'2015-12-31', 'value': },
                                ],
                            },
                        },
                    },
                },
            },
        },
    }
