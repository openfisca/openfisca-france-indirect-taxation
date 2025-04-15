# -*- coding: utf-8 -*-

import os
import pandas as pd

from openfisca_france_indirect_taxation.variables.base import ParameterNode
from openfisca_france_indirect_taxation.utils import assets_directory
from openfisca_france_indirect_taxation.parameters.series_rv import alcool_conso_et_vin

def preprocess_legislation(parameters):
    '''
    Preprocess the legislation parameters to add prices and amounts from national accounts
    '''

    prix_annuel_carburants = pd.read_csv(
        os.path.join(
            assets_directory,
            'prix',
            'prix_annuel_carburants.csv'
            ), sep =','
        )
    prix_annuel_carburants['Date'] = prix_annuel_carburants['Date'].astype(int)
    prix_annuel_carburants = prix_annuel_carburants.set_index('Date')
    prix_carburants = dict()

    # For super_95_e10, we need to use the price of super_95 between 2009 and 2012 included,
    # because we don't have the data. We use super_95 because it is very close and won't affect the results too much
    prix_annuel = prix_annuel_carburants['super_95_e10_ttc']
    years = list(range(2013, 2017))
    years = sorted(years, key=int, reverse=True)
    values = dict()
    for year in years:
        values['{}-01-01'.format(year)] = dict(value = prix_annuel[year] * 100)

    prix_annuel = prix_annuel_carburants['super_95_ttc']
    years = list(range(2009, 2013))
    years = sorted(years, key=int, reverse=True)
    for year in years:
        values['{}-01-01'.format(year)] = dict(value = prix_annuel[year] * 100)

    prix_annuel = prix_annuel_carburants['super_95_e10_ttc']
    years = list(range(1990, 2009))
    years = sorted(years, key=int, reverse=True)
    for year in years:
        values['{}-01-01'.format(year)] = dict(value = prix_annuel[year] * 100)

    prix_carburants['super_95_e10_ttc'] = {
        "description": 'super_95_e10_ttc'.replace('_', ' '),
        "unit": "currency",
        "values": values
        }
    autres_carburants = [
        'diesel_ht',
        'diesel_ttc',
        'gplc_ht',
        'gplc_ttc',
        'super_95_e10_ht',
        'super_95_ht',
        'super_95_ttc',
        'super_98_ht',
        'super_98_ttc',
        'super_plombe_ht',
        'super_plombe_ttc',
        ]
    for element in autres_carburants:
        assert element in prix_annuel_carburants.columns
        prix_annuel = prix_annuel_carburants[element]
        years = list(range(1990, 2022))
        years = sorted(years, key=int, reverse=True)
        values = dict()
        for year in years:
            values['{}-01-01'.format(year)] = prix_annuel[year] * 100

        prix_carburants[element] = {
            "description": element.replace('_', ' '),
            "unit": "currency",
            "values": values
            }
    prix_carburants['description'] = "Prix des carburants"
    node_prix_carburants = ParameterNode(
        'prix_carburants',
        data = prix_carburants,
        )
    parameters.add_child('prix_carburants', node_prix_carburants)

    # Add the number of vehicle in circulation to the tree
    parc_annuel_moyen_vp = pd.read_csv(
        os.path.join(
            assets_directory,
            'quantites',
            'parc_annuel_moyen_vp.csv'
            ), sep =','
        )

    parc_annuel_moyen_vp = parc_annuel_moyen_vp.set_index('Unnamed: 0')
    parc_vp = {
        "description": "taille moyenne du parc automobile en France métropolitaine en milliers de véhicules",
        }
    for element in ['diesel', 'essence']:
        taille_parc = parc_annuel_moyen_vp[element]
        years = list(range(1990, 2017))
        years = sorted(years, key=int, reverse=True)
        values = dict()
        for year in years:
            values['{}-01-01'.format(year)] = taille_parc[year]

        parc_vp[element] = {
            "description": "nombre de véhicules particuliers immatriculés en France à motorisation " + element,
            "unit": 1000,
            "values": values,
            }

    node_parc_vp = ParameterNode(
        'parc_vp',
        data = parc_vp,
        )
    parameters.add_child('parc_vp', node_parc_vp)

    # Add the total quantity of fuel consumed per year to the tree
    quantite_carbu_vp_france = pd.read_csv(
        os.path.join(
            assets_directory,
            'quantites',
            'quantite_carbu_vp_france.csv'
            ), sep =','
        )

    quantite_carbu_vp_france = quantite_carbu_vp_france.set_index('Unnamed: 0')
    quantite_carbu_vp = {
        "description": "quantite de carburants consommés en France métropolitaine",
        }
    for element in ['diesel', 'essence']:
        quantite_carburants = quantite_carbu_vp_france[element]
        years = list(range(1990, 2017))
        years = sorted(years, key=int, reverse=True)
        values = dict()
        for year in years:
            values['{}-01-01'.format(year)] = quantite_carburants[year]

        quantite_carbu_vp[element] = {
            "description": "consommation totale de " + element + " en France",
            "values": values
            }

    node_quantite_carbu_vp = ParameterNode(
        'quantite_carbu_vp',
        data = quantite_carbu_vp,
        )
    parameters.add_child('quantite_carbu_vp', node_quantite_carbu_vp)

    # Add the shares of each type of supercabrurant (SP95, SP98, E10, etc.) among supercarburants
    part_des_types_de_supercarburants = pd.read_csv(
        os.path.join(
            assets_directory,
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
            part_des_types_de_supercarburants[element]
            / (part_des_types_de_supercarburants['somme'] - part_des_types_de_supercarburants['sp_e85'])
            )
    del part_des_types_de_supercarburants['sp_e85']
    del part_des_types_de_supercarburants['somme']
    cols = part_des_types_de_supercarburants.columns
    part_des_types_de_supercarburants['somme'] = 0
    for element in cols:
        part_des_types_de_supercarburants['somme'] += part_des_types_de_supercarburants[element]
    assert (part_des_types_de_supercarburants['somme'] == 1).any(), "The weighting of the shares did not work"

    part_type_supercaburants = {
        "description": "part de la consommation totale d'essence de chaque type supercarburant",
        }
    for element in ['super_plombe', 'sp_95', 'sp_98', 'sp_e10']:
        part_par_carburant = part_des_types_de_supercarburants[element]
        years = list(range(2000, 2017))
        years = sorted(years, key=int, reverse=True)
        values = dict()
        for year in years:
            values['{}-01-01'.format(year)] = part_par_carburant[year]

        part_type_supercaburants[element] = {
            "description": "part de " + element + " dans la consommation totale d'essences",
            "unit": "/1",
            "values": values
            }

    node_part_type_supercaburants = ParameterNode(
        'part_type_supercaburants',
        data = part_type_supercaburants,
        )
    parameters.children['imposition_indirecte'].add_child('part_type_supercarburants', node_part_type_supercaburants)

    # Add CO2 emissions from energy (Source : Ademe)
    emissions_CO2 = {
        "description": "émissions de CO2 des énergies",
        }
    emissions_CO2['carburants'] = {
        "description": "émissions de CO2 des carburants",
        "CO2_diesel": {
            "description": "émissions de CO2 du diesel (en kg par litre)",
            # "unit": "kg/l",
            "values": {'1990-01-01': 2.66}
            },
        "CO2_essence": {
            "description": "émissions de CO2 du diesel en kg par litre",
            # "unit": "kg/l",
            "values": {'1990-01-01': 2.42},
            },
        }

    emissions_CO2['energie_logement'] = {
        "description": "émissions de CO2 de l'énergie dans le logement",
        "CO2_electricite": {
            "description": "émissions de CO2 de l'électricité (kg par kWh)",
            # "unit": "kg/kWh",
            "values": {'1990-01-01': 0.09},
            },
        "CO2_gaz_ville": {
            "description": "émissions de CO2 du gaz (kg par kWh)",
            # "unit": "kg/kWh",
            "values": {'1990-01-01': 0.241},
            },
        "CO2_gaz_liquefie": {
            "description": "émissions de CO2 du gaz (kg par kWh)",
            # "unit": "kg/kWh",
            "values": {'1990-01-01': 0.253},
            },
        "CO2_combustibles_liquides": {
            "description": "émissions de CO2 des combustibles liquides, (kg par litre)",
            # "unit": "kg/l",
            "values": {'1990-01-01': 3.24},
            },
        }
    node_emissions_CO2 = ParameterNode(
        'emissions_CO2',
        data = emissions_CO2,
        )
    parameters.children['imposition_indirecte'].add_child('emissions_CO2', node_emissions_CO2)

    # Add data from comptabilite national about alcohol (stored the old one)
    alcool_conso_et_vin_old = {
        "description": "alcools",
        }
    alcool_conso_et_vin_old['vin'] = {
        "description": "Pour calculer le taux de taxation implicite sur le vin",
        "droit_cn_vin": {
            "description": "Masse droit vin, vin mousseux, cidres et poirés selon comptabilité nationale",
            # TODO "unit": "currency" ?
            "values": {
                '2013-01-01': 122,
                '2012-01-01': 120,
                '2011-01-01': 118,
                '2010-01-01': 119,
                '2009-01-01': 117,
                '2008-01-01': 114,
                '2007-01-01': 117,
                '2006-01-01': 119,
                '2005-01-01': 117,
                '2004-01-01': 125,
                '2003-01-01': 127,
                '2002-01-01': 127,
                '2001-01-01': 127,
                '2000-01-01': 127,
                '1999-01-01': 133,
                '1998-01-01': 132,
                '1997-01-01': 129,
                '1996-01-01': 130,
                '1995-01-01': 129,
                },
            },
        "masse_conso_cn_vin": {
            "description": "Masse consommation vin, vin mousseux, cidres et poirés selon comptabilité nationale",
            # TODO "unit": "currency" ?
            "values": {
                '2013-01-01': 11515,
                '2012-01-01': 11407,
                '2011-01-01': 11387,
                '2010-01-01': 11002,
                '2009-01-01': 10728,
                '2008-01-01': 10461,
                '2007-01-01': 10345,
                '2006-01-01': 10002,
                '2005-01-01': 9933,
                '2004-01-01': 9985,
                '2003-01-01': 9695,
                '2002-01-01': 9476,
                '2001-01-01': 9168,
                '2000-01-01': 8854,
                '1999-01-01': 8451,
                '1998-01-01': 8025,
                '1997-01-01': 7636,
                '1996-01-01': 7419,
                '1995-01-01': 7191,
                # {u'2014-01-01': },
                },
            },
        }

    alcool_conso_et_vin_old['biere'] = {
        "description": "Pour calculer le taux de taxation implicite sur la bière",
        "droit_cn_biere": {
            "description": "Masse droit biere selon comptabilité nationale",
            # TODO "unit": "float",
            "values": {
                '2013-01-01': 897,
                '2012-01-01': 783,
                '2011-01-01': 393,
                '2010-01-01': 375,
                '2008-01-01': 375,
                '2009-01-01': 376,
                '2007-01-01': 382,
                '2006-01-01': 396,
                '2005-01-01': 364,
                '2004-01-01': 378,
                '2003-01-01': 370,
                '2002-01-01': 361,
                '2001-01-01': 364,
                '2000-01-01': 359,
                '1999-01-01': 380,
                '1998-01-01': 365,
                '1997-01-01': 364,
                '1996-01-01': 366,
                '1995-01-01': 361,
                }
            },
        "masse_conso_cn_biere": {
            "description": "Masse consommation biere selon comptabilité nationale",
            # TODO "unit": "float",
            "values": {
                '2013-01-01': 3321,
                '2012-01-01': 2868,
                '2011-01-01': 2769,
                '2010-01-01': 2461,
                '2009-01-01': 2375,
                '2008-01-01': 2287,
                '2007-01-01': 2458,
                '2006-01-01': 2486,
                '2005-01-01': 2466,
                '2004-01-01': 2484,
                '2003-01-01': 2554,
                '2002-01-01': 2405,
                '2001-01-01': 2327,
                '2000-01-01': 2290,
                '1999-01-01': 2334,
                '1998-01-01': 2291,
                '1997-01-01': 2186,
                '1996-01-01': 2144,
                '1995-01-01': 2111,
                },
            },
        }

    alcool_conso_et_vin_old['alcools_forts'] = {
        "description": "Pour calculer le taux de taxation implicite sur alcools forts",
        "droit_cn_alcools": {
            "description": "Masse droit alcool selon comptabilité nationale sans droits sur les produits intermediaires et cotisation spéciale alcool fort",
            # TODO "unit": "float",
            "values": {
                '2012-01-01': 2225,
                '2011-01-01': 2150,
                '2010-01-01': 2111,
                '2009-01-01': 2031,
                '2008-01-01': 2005,
                '2007-01-01': 1990,
                '2006-01-01': 1954,
                '2005-01-01': 1842,
                '2004-01-01': 1908,
                '2003-01-01': 1891,
                '2002-01-01': 1932,
                '2001-01-01': 1957,
                '2000-01-01': 1872,
                # TODO: Problème pour les alcools forts chiffres différents entre les deux bases excel !
                },
            },
        "droit_cn_alcools_total": {
            "description": "Masse droit alcool selon comptabilité nationale avec les differents droits",
            # TODO "unit": "float",
            "values": {
                '2013-01-01': 3022,
                '2012-01-01': 2718,
                '2011-01-01': 3078,
                '2010-01-01': 2734,
                '2009-01-01': 2629,
                '2008-01-01': 2528,
                '2007-01-01': 2516,
                '2006-01-01': 2477,
                '2005-01-01': 2352,
                '2004-01-01': 2409,
                '2003-01-01': 2453,
                '2002-01-01': 2503,
                '2000-01-01': 2416,
                '2001-01-01': 2514,
                '1999-01-01': 2385,
                '1998-01-01': 2369,
                '1997-01-01': 2366,
                '1996-01-01': 2350,
                '1995-01-01': 2337,
                },
            },
        "masse_conso_cn_alcools": {
            "description": "Masse consommation alcool selon comptabilité nationale",
            # TODO "unit": "float",
            "values": {
                '2013-01-01': 7022,
                '2012-01-01': 6996,
                '2011-01-01': 6680,
                '2010-01-01': 6618,
                '2009-01-01': 6342,
                '2008-01-01': 6147,
                '2007-01-01': 6142,
                '2006-01-01': 6106,
                '2005-01-01': 5960,
                '2004-01-01': 5967,
                '2003-01-01': 5895,
                '2002-01-01': 5932,
                '2001-01-01': 5721,
                '2000-01-01': 5558,
                '1999-01-01': 5234,
                '1998-01-01': 5123,
                '1997-01-01': 5065,
                '1996-01-01': 5075,
                '1995-01-01': 4893,
                },
            },
        }

        # the new one has been imported from series_rv.py 
    node_alcool_conso_et_vin = ParameterNode(
        'alcool_conso_et_vin',
        data = alcool_conso_et_vin,
        )
    parameters.children['imposition_indirecte'].add_child('alcool_conso_et_vin', node_alcool_conso_et_vin)
    # Make the change from francs to euros for excise taxes in ticpe
    keys_ticpe = list(parameters.imposition_indirecte.produits_energetiques.ticpe.children.keys())
    for element in keys_ticpe:
        values_list = \
            parameters.imposition_indirecte.produits_energetiques.ticpe.children[element].values_list
        for dated_value in values_list:
            year = int(dated_value.instant_str[:4])
            if year < 2002:
                if dated_value.value:
                    dated_value.value = dated_value.value / 6.55957

    return parameters
