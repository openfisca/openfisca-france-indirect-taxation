# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from openfisca_core import reforms


def preprocess_legislation(legislation_json):
    '''
    Preprocess the legislation parameters to add prices and amounts from national accounts
    '''
    import os
    import pkg_resources
    import pandas as pd

    # Add fuel prices to the tree

    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    prix_annuel_carburants = pd.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'prix_annuel_carburants.csv'
            ), sep =';'
        )
    prix_annuel_carburants['Date'] = prix_annuel_carburants['Date'].astype(int)
    prix_annuel_carburants = prix_annuel_carburants.set_index('Date')
    all_values = {}
    prix_carburants = {
        "@type": "Node",
        "description": "prix des carburants en euros par hectolitre",
        "children": {},
        }
    for element in ['diesel_ht', 'diesel_ttc', 'super_95_ht', 'super_95_ttc', 'super_98_ht', 'super_98_ttc',
            'super_95_e10_ht', 'super_95_e10_ttc', 'gplc_ht', 'gplc_ttc', 'super_plombe_ht', 'super_plombe_ttc']:
        assert element in prix_annuel_carburants.columns
        prix_annuel = prix_annuel_carburants[element]
        all_values[element] = []
        for year in range(1990, 2015):
            values = dict()
            values['start'] = u'{}-01-01'.format(year)
            values['stop'] = u'{}-12-31'.format(year)
            values['value'] = prix_annuel.loc[year] * 100
            all_values[element].append(values)

        prix_carburants['children'][element] = {
            "@type": "Parameter",
            "description": element.replace('_', ' '),
            "format": "float",
            "values": all_values[element]
            }
    legislation_json['children']['imposition_indirecte']['children']['prix_carburants'] = prix_carburants

    # Add the number of vehicle in circulation to the tree

    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    parc_annuel_moyen_vp = pd.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'parc_annuel_moyen_vp.csv'
            ), sep =';'
        )

    parc_annuel_moyen_vp = parc_annuel_moyen_vp.set_index('Unnamed: 0')
    values_parc = {}
    parc_vp = {
        "@type": "Node",
        "description": "taille moyenne du parc automobile en France métropolitaine en milliers de véhicules",
        "children": {},
    }
    for element in ['diesel', 'essence']:
        taille_parc = parc_annuel_moyen_vp[element]
        values_parc[element] = []
        for year in range(1990, 2014):
            values = dict()
            values['start'] = u'{}-01-01'.format(year)
            values['stop'] = u'{}-12-31'.format(year)
            values['value'] = taille_parc.loc[year]
            values_parc[element].append(values)

        parc_vp['children'][element] = {
            "@type": "Parameter",
            "description": "nombre de véhicules particuliers immatriculés en France à motorisation " + element,
            "format": "float",
            "values": values_parc[element]
        }

        legislation_json['children']['imposition_indirecte']['children']['parc_vp'] = parc_vp

    # Add the total quantity of fuel consumed per year to the tree

    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    quantite_carbu_vp_france = pd.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'quantite_carbu_vp_france.csv'
            ), sep =';'
        )

    quantite_carbu_vp_france = quantite_carbu_vp_france.set_index('Unnamed: 0')
    values_quantite = {}
    quantite_carbu_vp = {
        "@type": "Node",
        "description": "quantite de carburants consommés en France métropolitaine",
        "children": {},
    }
    for element in ['diesel', 'essence']:
        quantite_carburants = quantite_carbu_vp_france[element]
        values_quantite[element] = []
        for year in range(1990, 2014):
            values = dict()
            values['start'] = u'{}-01-01'.format(year)
            values['stop'] = u'{}-12-31'.format(year)
            values['value'] = quantite_carburants.loc[year]
            values_quantite[element].append(values)

        quantite_carbu_vp['children'][element] = {
            "@type": "Parameter",
            "description": "consommation totale de " + element + " en France",
            "format": "float",
            "values": values_quantite[element]
        }

        legislation_json['children']['imposition_indirecte']['children']['quantite_carbu_vp'] = quantite_carbu_vp

    # Add the shares of each type of supercabrurant (SP95, SP98, E10, etc.) among supercarburants

    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    part_des_types_de_supercarburants = pd.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'part_des_types_de_supercarburants.csv'
            ), sep =';'
        )

    del part_des_types_de_supercarburants['Source']
    part_des_types_de_supercarburants = \
        part_des_types_de_supercarburants[part_des_types_de_supercarburants['annee'] > 0].copy()
    part_des_types_de_supercarburants['annee'] = part_des_types_de_supercarburants['annee'].astype(int)
    part_des_types_de_supercarburants = part_des_types_de_supercarburants.set_index('annee')

    # delete share of e_85 because we have no data for its price
    # When the sum of all shares is not one, need to multiply each share by the same coefficient
    cols = part_des_types_de_supercarburants.columns
    for element in cols:
        part_des_types_de_supercarburants[element] = (
            part_des_types_de_supercarburants[element] /
            (part_des_types_de_supercarburants['somme'] - part_des_types_de_supercarburants['sp_e85'])
            )
    del part_des_types_de_supercarburants['sp_e85']
    del part_des_types_de_supercarburants['somme']
    cols = part_des_types_de_supercarburants.columns
    part_des_types_de_supercarburants['somme'] = 0
    for element in cols:
        part_des_types_de_supercarburants['somme'] += part_des_types_de_supercarburants[element]
    assert (part_des_types_de_supercarburants['somme'] == 1).any(), "The weighting of the shares did not work"


    values_part_supercarburants = {}
    part_type_supercaburant = {
        "@type": "Node",
        "description": "part de la consommation totale d'essence de chaque type supercarburant",
        "children": {},
    }
    for element in ['super_plombe', 'sp_95', 'sp_98', 'sp_e10']:
        part_par_carburant = part_des_types_de_supercarburants[element]
        values_part_supercarburants[element] = []
        for year in range(2000, 2015):
            values = dict()
            values['start'] = u'{}-01-01'.format(year)
            values['stop'] = u'{}-12-31'.format(year)
            values['value'] = part_par_carburant.loc[year]
            values_part_supercarburants[element].append(values)

        part_type_supercaburant['children'][element] = {
            "@type": "Parameter",
            "description": "part de " + element + " dans la consommation totale d'essences",
            "format": "float",
            "values": values_part_supercarburants[element]
        }

        legislation_json['children']['imposition_indirecte']['children']['part_type_supercarburants'] = \
            part_type_supercaburant

    # Add data from comptabilite national about alcohol

    alcool_conso_et_vin = {
        "@type": "Node",
        "description": "alcools",
        "children": {},
        }
    alcool_conso_et_vin['children']['vin'] = {
        "@type": "Node",
        "description": "Pour calculer le taux de taxation implicite sur le vin",
        "children": {
            "droit_cn_vin": {
                "@type": "Parameter",
                "description": u"Masse droit vin, vin mousseux, cidres et poirés selon comptabilité nationale",
                "format": "float",
                "values": [
                    {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 129},
                    {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 130},
                    {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 129},
                    {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 132},
                    {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 133},
                    {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 127},
                    {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 127},
                    {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 127},
                    {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 127},
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
                    # {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                    ],
                },
            "masse_conso_cn_vin": {
                "@type": "Parameter",
                "description": u"Masse consommation vin, vin mousseux, cidres et poirés selon comptabilité nationale",
                "format": "float",
                "values": [
                    {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 7191},
                    {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 7419},
                    {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 7636},
                    {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 8025},
                    {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 8451},
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
                    # {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                    ],
                },
            },
        }

    alcool_conso_et_vin['children']['biere'] = {
        "@type": "Node",
        "description": "Pour calculer le taux de taxation implicite sur la bière",
        "children": {
            "droit_cn_biere": {
                "@type": "Parameter",
                "description": "Masse droit biere selon comptabilité nationale",
                "format": "float",
                "values": [
                    {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 361},
                    {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 366},
                    {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 364},
                    {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 365},
                    {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 380},
                    {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 359},
                    {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 364},
                    {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 361},
                    {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 370},
                    {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 378},
                    {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 364},
                    {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 396},
                    {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 382},
                    {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 375},                                            {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 376},
                    {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 375},
                    {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 393},
                    {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 783},
                    {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 897},
                    # {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                    ],
                },
            "masse_conso_cn_biere": {
                "@type": "Parameter",
                "description": u"Masse consommation biere selon comptabilité nationale",
                "format": "float",
                "values": [
                    {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 2111},
                    {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 2144},
                    {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 2186},
                    {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 2291},
                    {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 2334},
                    {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 2290},
                    {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 2327},
                    {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 2405},
                    {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 2554},
                    {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 2484},
                    {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 2466},
                    {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 2486},
                    {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 2458},
                    {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 2287},
                    {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 2375},
                    {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 2461},
                    {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 2769},
                    {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 2868},
                    {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 3321},
                    # {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                    ],
                },
            },
        }

    alcool_conso_et_vin['children']['alcools_forts'] = {
        "@type": "Node",
        "description": "Pour calculer le taux de taxation implicite sur alcools forts",
        "children": {
            "droit_cn_alcools": {
                "@type": "Parameter",
                "description": "Masse droit alcool selon comptabilité nationale sans droits sur les produits intermediaires et cotisation spéciale alcool fort",
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
                    # TODO: Problème pour les alcools forts chiffres différents entre les deux bases excel !
                    ],
                },
            "droit_cn_alcools_total": {
                "@type": "Parameter",
                "description": u"Masse droit alcool selon comptabilité nationale avec les differents droits",
                "format": "float",
                "values": [
                    {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 2337},
                    {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 2350},
                    {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 2366},
                    {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 2369},
                    {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 2385},
                    {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 2416},                                            {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 2514},
                    {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 2503},
                    {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 2453},
                    {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 2409},
                    {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 2352},
                    {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 2477},
                    {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 2516},
                    {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 2528},
                    {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 2629},
                    {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 2734},
                    {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 3078},
                    {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 2718},
                    {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 3022},
                    # {'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': },
                    ],
                },
            "masse_conso_cn_alcools": {
                "@type": "Parameter",
                "description": u"Masse consommation alcool selon comptabilité nationale",
                "format": "float",
                "values": [
                    {'start': u'1995-01-01', 'stop': u'1995-12-31', 'value': 4893},
                    {'start': u'1996-01-01', 'stop': u'1996-12-31', 'value': 5075},
                    {'start': u'1997-01-01', 'stop': u'1997-12-31', 'value': 5065},
                    {'start': u'1998-01-01', 'stop': u'1998-12-31', 'value': 5123},
                    {'start': u'1999-01-01', 'stop': u'1999-12-31', 'value': 5234},
                    {'start': u'2000-01-01', 'stop': u'2000-12-31', 'value': 5558},
                    {'start': u'2001-01-01', 'stop': u'2001-12-31', 'value': 5721},
                    {'start': u'2002-01-01', 'stop': u'2002-12-31', 'value': 5932},
                    {'start': u'2003-01-01', 'stop': u'2003-12-31', 'value': 5895},
                    {'start': u'2004-01-01', 'stop': u'2004-12-31', 'value': 5967},
                    {'start': u'2005-01-01', 'stop': u'2005-12-31', 'value': 5960},
                    {'start': u'2006-01-01', 'stop': u'2006-12-31', 'value': 6106},
                    {'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 6142},
                    {'start': u'2008-01-01', 'stop': u'2008-12-31', 'value': 6147},
                    {'start': u'2009-01-01', 'stop': u'2009-12-31', 'value': 6342},
                    {'start': u'2010-01-01', 'stop': u'2010-12-31', 'value': 6618},
                    {'start': u'2011-01-01', 'stop': u'2011-12-31', 'value': 6680},
                    {'start': u'2012-01-01', 'stop': u'2012-12-31', 'value': 6996},
                    {'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 7022},
                    ],
                },
            },
        }

    legislation_json['children']['imposition_indirecte']['children']['alcool_conso_et_vin'] = alcool_conso_et_vin

    return legislation_json
