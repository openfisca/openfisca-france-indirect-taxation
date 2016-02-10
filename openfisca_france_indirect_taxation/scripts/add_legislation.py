# -*- coding: utf-8 -*-


import numpy as np
import os
import pandas as pd
import pkg_resources


import build_coicop_nomenclature

legislation_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'legislation',
    )


sub_levels = ['divisions', 'groupes', 'classes', 'sous_classes', 'postes']
divisions = ['0{}'.format(i) for i in range(1, 10)] + ['11', '12']  # TODO: fix this
taxe_by_categorie_fiscale_number = {
    0: '',
    1: 'tva_taux_super_reduit',
    2: 'tva_taux_reduit',
    3: 'tva_taux_plein',
    4: 'tva_taux_intermediaire',
    7: 'cigarettes',
    8: 'cigares',
    9: 'tabac_a_rouler',
    10: 'alcools_forts',
    11: 'tva_taux_plein',
    12: 'vin',
    13: 'biere',
    14: 'ticpe',
    15: 'assurance_transport',
    16: 'assurance_sante',
    17: 'autres_assurances'
    }


def extract_informations_from_coicop_to_categorie_fiscale():

    def format_exceptions(exceptions):
        grouped = exceptions.groupby(
            by = [exceptions.annee - np.arange(exceptions.shape[0]), 'posteCOICOP', 'categoriefiscale']
            )
        for k, g in grouped:
            print g.posteCOICOP.unique()[0], g.description.unique()[0], g.annee.min(), g.annee.max(), \
                taxe_by_categorie_fiscale_number[int(g.categoriefiscale.unique())]

    def get_dominant_and_exceptions(division):
        assert division in divisions
        parametres_fiscalite_file_path = os.path.join(legislation_directory, 'coicop_to_categorie_fiscale.csv')
        parametres_fiscalite_data_frame = pd.read_csv(
            parametres_fiscalite_file_path,
            sep = ';',
            converters = {'posteCOICOP': unicode}
            )
        parametres_fiscalite_data_frame['division'] = parametres_fiscalite_data_frame['posteCOICOP'].str[:2].copy()
        division_dataframe = parametres_fiscalite_data_frame.query('division == @division')
        dominant_fiscal_category = division_dataframe.categoriefiscale.value_counts().argmax()
        exceptions = division_dataframe.query('categoriefiscale != @dominant_fiscal_category')
        return dominant_fiscal_category, exceptions

    for coicop_division in divisions:
        dominant, exceptions = get_dominant_and_exceptions(coicop_division)
        print u'\nDivision: {}.\nCatégorie fiscale dominante: {}.\nExceptions:'.format(
            coicop_division,
            taxe_by_categorie_fiscale_number[dominant]
            )
        format_exceptions(exceptions),


def apply_modification(coicop_nomenclature = None, value = None, categorie_fiscale = None, start = 1994, stop = 2014):
    assert coicop_nomenclature is not None

    categorie_fiscale in taxe_by_categorie_fiscale_number.values()

    if isinstance(value, int):
        selection = coicop_nomenclature.divisions == value
    elif isinstance(value, str):
        selection = coicop_nomenclature.code_coicop.str[:len(value)] == value
    elif isinstance(value, list):
        selection = coicop_nomenclature.code_coicop.isin(value)

    coicop_nomenclature.loc[selection, 'categorie_fiscale'] = categorie_fiscale
    filled_start_stop = (
        (coicop_nomenclature.loc[selection, 'start'].unique() != 0).any() or
        (coicop_nomenclature.loc[selection, 'stop'].unique() != 0).any()
        )
    if filled_start_stop and (start != 1994 or stop != 2014):
        coicop_copy = coicop_nomenclature.loc[selection].copy()
        coicop_copy['start'] = start
        coicop_copy['stop'] = stop
        print coicop_copy
        coicop_nomenclature = coicop_nomenclature.append(coicop_copy, ignore_index = True)
        coicop_nomenclature.reset_index(inplace = True, drop = True)
        coicop_nomenclature.sort_values(by = 'code_coicop', inplace = True)
    else:
        coicop_nomenclature.loc[selection, 'start'] = 1994
        coicop_nomenclature.loc[selection, 'stop'] = 2014

    print coicop_nomenclature.categorie_fiscale.value_counts()
    return coicop_nomenclature


def build_coicop_nomenclature_with_fiscal_categories():
    coicop_nomenclature = build_coicop_nomenclature.build_coicop_nomenclature()

    # 01 Produits alimentaires et boissons non alcoolisées
    # ils sont tous à taux réduit
    alimentation = dict(
        value = 1,
        categorie_fiscale = 'tva_taux_reduit'
        )
    # sauf la margarine à taux plein
    margarine = dict(
        value = '01.1.5.2.2',
        categorie_fiscale = 'tva_taux_plein',
        )
    # et les confiseries et le chocolat  # TODO check
    confiserie = dict(
        value = ['01.1.8.1.3', '01.1.8.2.1', '01.1.8.2.2'],
        categorie_fiscale = 'tva_taux_plein'
        )
    # 02 Boissons alcoolisées et tabac
    # alccols forts
    alcools = dict(
        value = '02.1.1',
        categorie_fiscale = 'alcools_forts',
        )
    # vins et boissons fermentées
    vin = dict(
        value = '02.1.2',
        categorie_fiscale = 'vin',
        )
    # bière
    biere = dict(
        value = '02.1.3',
        categorie_fiscale = 'biere',
        )
    # TODO: tabac
    # u'02202'] ['Cigares et cigarillos'] 1994 2014 cigares
    # [u'02201'] ['Cigarettes'] 1994 2014 cigarettes
    # TODO: Rajouter Stupéfiants sans taxe
    #
    # 03 Habillement et chaussures
    habillement = dict(
        value = 3,
        categorie_fiscale = 'tva_taux_plein'
        )

    # 04 Logement, eau, gaz, électricité et autres combustibles
    logement = dict(
        value = 4,
        categorie_fiscale = 'tva_taux_plein',
        )
    # sauf distribution d'eau, enlèvement des ordures ménagères, assainissement, autres services liés au logement n.d.a.
    # qui sont au taux réduit de 1994 à 2011
    eau_ordures_assainissement = dict(
        value = ['04.4.1.1.1', '04.4.1.2.1', '04.4.1.3.1'],
        categorie_fiscale = 'tva_taux_reduit',
        stop = '2011',
        )
    # avant de passer au taux intermédiaire
    eau_ordures_assainissement_reforme_2012 = dict(
        value = ['04.4.1.1.1', '04.4.1.2.1', '04.4.1.3.1'],
        categorie_fiscale = 'tva_taux_intermediaire',
        start = '2012',
        )
    # et pas de taxation des loyers
    loyers = dict(
        value = ['04.1.1.1.1', '04.1.1.2.1'],
        categorie_fiscale = '',
        )
    # TODO ajouter loyers fictifs
    # 05 Ameublement, équipement ménager et entretien courant de la maison
    ameublement = dict(
        value = 5,
        categorie_fiscale = 'tva_taux_plein',
        )
    # sauf Services domestiques et autres services pour l'habitation
    services_domestiques = dict(
        value = '05.6.2',
        categorie_fiscale = 'tva_taux_reduit',
        )
    # 06 Santé pas taxée
    sante = dict(
        value = 6,
        categorie_fiscale = '',
        )
    # sauf pharmacie
    pharmacie = dict(
        value = '06.1.1.1',
        categorie_fiscale = 'tva_taux_super_reduit',
        )
    # parapharmacie
    parapharmacie = dict(
        value = '06.1.1.2',
        categorie_fiscale = 'tva_taux_plein',
        )
    # materiel therapeutique
    materiel_therapeutique = dict(
        value = '06.1.1.3',
        categorie_fiscale = 'tva_taux_reduit',
        )
    # 07 Transports
    transports = dict(
        value = 7,
        categorie_fiscale = 'tva_taux_plein',
        )
    # Transport combine de passagers change en 2012 #
    transport_combine_passagers = dict(
        value = '07.3.5',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011,
        )
    transport_combine_passagers_reforme_2012 = dict(
        value = '07.3.5',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Transport maritime et fluvial de passagers change en 2011  Attention 07.3.4 dans enquête BDF
    transport_maritime = dict(
        value = '07.3.6',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011,
        )
    transport_maritime_reforme_2012 = dict(
        value = '07.3.6',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Transport aérien de passagers change en 2012
    transport_aerien = dict(
        value = '07.3.3',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011,
        )
    transport_aerien_reforme_2012 = dict(
        value = '07.3.3',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Transport routier de passagers 1994 2011 change en 2012
    transport_routier = dict(
        value = '07.3.2',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011,
        )
    transport_routier_reforme_2012 = dict(
        value = '07.3.2',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Transport ferroviaire de passagers change en 2012
    transport_ferroviaire = dict(
        value = '07.3.1',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011,
        )
    transport_ferroviaire_reforme_2012 = dict(
        value = '07.3.1',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Carburants et lubrifiants pour véhicules de tourisme 1994 2014
    carburants_lubrifiants = dict(
        value = '07.2.2',
        categorie_fiscale = 'ticpe',
        )
    # 08 Communications
    communications = dict(
        value = 8,
        categorie_fiscale = 'tva_taux_plein',
        )
    services_postaux = dict(
        value = '08.1.1,1',
        categorie_fiscale = '',
        )
    # 09 Loisirs et cutures
    loisirs_cuture = dict(
        value = 9,
        categorie_fiscale = 'tva_taux_plein',
        )
    # Journaux et publications périodiques']
    journaux_periodiques = dict(
        value = '09.5.2',
        categorie_fiscale = 'tva_taux_super_reduit',
        )
    # Livre'
    livre = dict(
        value = '09.5.1',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011,
        )
    livre_reforme_2012 = dict(
        value = '09.5.1',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Jeux de hasard TODO: trouver les jeux de hasard
    jeux_hasard = dict(
        value = '09.4.3',
        categorie_fiscale = '',
        )
    # Services culturels
    services_culturels = dict(
        value = '09.4.2',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011,
        )
    # Services culturels
    services_culturels_reforme_2012 = dict(
        value = '09.4.2',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Services récréatifs et sportifs
    services_recreatifs_sportifs = dict(
        value = '09.4.1',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011,
        )
    services_recreatifs_sportifs_reforme_2012 = dict(
        value = '09.4.1',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # 10 Education TODO: check and introduce     categorie_fiscale = '' if needed
    # 11 Hotellerie restauration
    hotellerie_restauration = dict(
        value = 11,
        categorie_fiscale = 'tva_taux_reduit',
        )
    # Cantines'] 1994
    cantines = dict(
        value = '11.1.2',
        categorie_fiscale = '',
        )
    # Services d'hébergement 2012 2014
    service_hebergement = dict(
        value = '11.2.1',  # TODO: check
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Consommation de boissons alcoolisées
    consommation_boissons_alcoolisees = dict(
        value = ['11.1.1.2.2', '11.1.1.2.3', '11.1.1.2.4'],  # TODO check
        categorie_fiscale = 'tva_taux_plein',
        )
    # Restauration sur place 1994 2009
    restauration_sur_place = dict(
        value = '11.1.1.1.1',
        categorie_fiscale = 'tva_taux_plein',
        stop = 2009,
        )
    restauration_sur_place_reforme_2010 = dict(
        value = '11.1.1.1.1',
        categorie_fiscale = 'tva_taux_reduit',
        start = 2010,
        stop = 2011,
        )
    # Restauration sur place 2012 2014
    restauration_sur_place_reforme_2012 = dict(
        value = '11.1.1.1.1',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Restauration à emporter 1994 1997
    restauration_a_emporter = dict(
        value = '11.1.1.1.2',
        categorie_fiscale = 'tva_taux_plein',
        stop = 1997,
        )
    # Restauration à emporter 2010 2011
    restauration_a_emporter_reforme_2010 = dict(
        value = '11.1.1.1.2',
        categorie_fiscale = 'tva_taux_reduit',
        start = 1998,
        stop = 2011,
        )
    # Restauration à emporter 2012 2014
    restauration_a_emporter_reforme_2012 = dict(
        value = '11.1.1.1.2',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # 12 Autres biens et services
    autres_biens_et_services = dict(
        value = 12,
        categorie_fiscale = 'tva_taux_plein',
        )
    # Couts des services d'intermédiation financière indirectement mesurés
    intermediation_financiere = dict(
        value = '12.6.1',
        categorie_fiscale = '',
        )
    # Autres assurances  # TODO
    autres_assurances = dict(
        value = '1255',
        categorie_fiscale = 'autres_assurances',
        )
    # Assurance_transports
    assurance_transports = dict(
        value = '12.5.4',
        categorie_fiscale = 'assurance_transport',
        )
    # Assurance maladie
    assurance_maladie = dict(
        value = '12.5.3',
        categorie_fiscale = 'assurance_sante',
        )
    # Assurance habitation
    assurance_habitation = dict(
        value = '12.5.2',
        categorie_fiscale = 'autres_assurances',
        )
    # Assurance vie  # TODO où sont les coicop 12.5.1
    assurance_vie = dict(
        value = '1251',
        categorie_fiscale = 'autres_assurances',
        )
    # Protection sociale TODO: check tva_taux_plein avant 2000
    protection_sociale_reforme_2000 = dict(
        value = '12.4',
        categorie_fiscale = 'tva_taux_reduit',
        start = 2000,
        stop = 2011,
        )
    # Protection sociale
    protection_sociale_reforme_2012 = dict(
        value = '12.4',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Prostitution TODO check
    prostitution = dict(
        value = '1220',
        categorie_fiscale = '',
        )

    for member in [
        # 01
        alimentation, margarine, confiserie,
        # 02
        alcools, vin, biere,
        # 03
        habillement,
        # 04
        logement, eau_ordures_assainissement, eau_ordures_assainissement_reforme_2012, loyers,
        # 05
        ameublement, services_domestiques,
        # 06
        sante, pharmacie, parapharmacie, materiel_therapeutique,
        # 07
        transports,
        transport_combine_passagers, transport_combine_passagers_reforme_2012,
        transport_maritime, transport_maritime_reforme_2012,
        transport_aerien, transport_aerien_reforme_2012,
        transport_routier, transport_routier_reforme_2012,
        transport_ferroviaire, transport_ferroviaire_reforme_2012,
        carburants_lubrifiants,
        # 08
        communications, services_postaux,
        # 09
        loisirs_cuture, journaux_periodiques, livre, livre_reforme_2012, jeux_hasard,
        services_culturels, services_culturels_reforme_2012,
        services_recreatifs_sportifs, services_recreatifs_sportifs_reforme_2012,
        # 10 Education
        # 11 Hotellerie restauration
        hotellerie_restauration, cantines, service_hebergement,
        consommation_boissons_alcoolisees,
        restauration_sur_place, restauration_sur_place_reforme_2010, restauration_sur_place_reforme_2012,
        restauration_a_emporter, restauration_a_emporter_reforme_2010, restauration_a_emporter_reforme_2012,
        # 12
        autres_biens_et_services, intermediation_financiere,
        autres_assurances, assurance_transports, assurance_vie, assurance_maladie, assurance_habitation,
        protection_sociale_reforme_2000, protection_sociale_reforme_2012,
        prostitution]:
        coicop_nomenclature = apply_modification(coicop_nomenclature, **member)

    return coicop_nomenclature


if __name__ == "__main__":
    extract_informations_from_coicop_to_categorie_fiscale()
    coicop_nomenclature = build_coicop_nomenclature_with_fiscal_categories()