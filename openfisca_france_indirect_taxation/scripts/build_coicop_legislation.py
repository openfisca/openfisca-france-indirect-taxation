# -*- coding: utf-8 -*-


import numpy as np
import os
import pandas as pd


from openfisca_france_indirect_taxation.scripts import build_coicop_nomenclature
from openfisca_france_indirect_taxation.utils import assets_directory


legislation_directory = os.path.join(assets_directory, 'legislation')

sub_levels = ['divisions', 'groupes', 'classes', 'sous_classes', 'postes']

divisions = ['0{}'.format(i) for i in range(1, 10)] + ['11', '12']

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
        for _, g in grouped:
            print((
                g.posteCOICOP.unique()[0], g.description.unique()[0], g.annee.min(), g.annee.max(),
                taxe_by_categorie_fiscale_number[int(g.categoriefiscale.unique())]
                ))

    def get_dominant_and_exceptions(division):
        assert division in divisions
        parametres_fiscalite_file_path = os.path.join(legislation_directory, 'coicop_to_categorie_fiscale.csv')
        parametres_fiscalite_data_frame = pd.read_csv(
            parametres_fiscalite_file_path,
            converters = {'posteCOICOP': str}
            )
        parametres_fiscalite_data_frame['division'] = parametres_fiscalite_data_frame['posteCOICOP'].str[:2].copy()
        division_dataframe = parametres_fiscalite_data_frame.query('division == @division')
        dominant_fiscal_category = division_dataframe.categoriefiscale.value_counts().argmax()
        exceptions = division_dataframe.query('categoriefiscale != @dominant_fiscal_category')
        return dominant_fiscal_category, exceptions

    for coicop_division in divisions:
        dominant, exceptions = get_dominant_and_exceptions(coicop_division)
        print(('\nDivision: {}.\nCatégorie fiscale dominante: {}.\nExceptions:'.format(
            coicop_division,
            taxe_by_categorie_fiscale_number[dominant]
            )))
        format_exceptions(exceptions)


def extract_infra_labels_from_coicop_code(coicop_nomenclature = None, coicop_code = None, label = None):
    assert coicop_nomenclature is not None
    assert coicop_code is not None
    assert label is not None
    known_levels = sub_levels[:len(coicop_code.split('.')) - 1]
    coicop_sub_code = coicop_code[:len(coicop_code) - 2]
    assert known_levels, 'No know levels for COICOP {}'.format(coicop_code)
    labels_by_sub_level = coicop_nomenclature.loc[
        coicop_nomenclature.code_coicop.str[:len(coicop_sub_code)] == coicop_sub_code,
        ['label_{}'.format(level[:-1]) for level in known_levels]
        ].drop_duplicates().dropna().to_dict(orient = 'records')[0]
    for key, value in list(labels_by_sub_level.items()):
        labels_by_sub_level[key] = value
    modified_level = sub_levels[len(coicop_code.split('.')) - 1][:-1]
    labels_by_sub_level['label_{}'.format(modified_level)] = label
    return labels_by_sub_level


def apply_modification(coicop_nomenclature = None, value = None, categorie_fiscale = None,
        origin = None, start = 1994, stop = 2024, label = ''):
    assert coicop_nomenclature is not None
    assert categorie_fiscale in list(taxe_by_categorie_fiscale_number.values())
    assert 1994 <= start < stop <= 2024, "Invalid start={} and/or stop={}".format(start, stop)

    if isinstance(value, int):
        value_str = '0' + str(value) if value < 10 else str(value)
        selection = coicop_nomenclature.code_coicop.str[:2] == value_str
    elif isinstance(value, str):
        selection = coicop_nomenclature.code_coicop.str[:len(value)] == value
    elif isinstance(value, list):
        selection = coicop_nomenclature.code_coicop.isin(value)

    if selection.any():  # la coicop existe
        filled_start_stop = (
            (coicop_nomenclature.loc[selection, 'start'].unique() != 0).any()
            or (coicop_nomenclature.loc[selection, 'stop'].unique() != 0).any()
            )
        if not filled_start_stop:
            coicop_nomenclature.loc[selection, 'start'] = 1994
            coicop_nomenclature.loc[selection, 'stop'] = 2024
            coicop_nomenclature.loc[selection, 'categorie_fiscale'] = categorie_fiscale

        else:
            equal_start = coicop_nomenclature.start == start
            equal_stop = coicop_nomenclature.stop == stop

            selection_bis = selection & (coicop_nomenclature.start <= start) & (coicop_nomenclature.stop >= stop)

            if (selection_bis & equal_start & equal_stop).any():  # meme intervalle
                coicop_nomenclature.loc[
                    selection_bis & equal_start & equal_stop, 'categorie_fiscale'
                    ] = categorie_fiscale

            elif (selection_bis & equal_start).any():  # recouvrement au debut
                coicop_nomenclature.loc[selection_bis & equal_start, 'start'] = stop + 1
                coicop_copy = coicop_nomenclature.loc[selection_bis & equal_start].copy()
                coicop_copy['categorie_fiscale'] = categorie_fiscale
                coicop_copy['start'] = start
                coicop_copy['stop'] = stop
                coicop_nomenclature = coicop_nomenclature.append(coicop_copy)
                coicop_nomenclature.reset_index(inplace = True, drop = True)
                coicop_nomenclature.sort_values(by = 'code_coicop', inplace = True)

            elif (selection_bis & equal_stop).any():  # recouvrement a la fin
                coicop_nomenclature.loc[selection_bis & equal_stop, 'stop'] = start - 1
                coicop_copy = coicop_nomenclature.loc[selection_bis & equal_stop].copy()
                coicop_copy['categorie_fiscale'] = categorie_fiscale
                coicop_copy['start'] = start
                coicop_copy['stop'] = stop
                coicop_nomenclature = coicop_nomenclature.append(coicop_copy)
                coicop_nomenclature.reset_index(inplace = True, drop = True)
                coicop_nomenclature.sort_values(by = 'code_coicop', inplace = True)

            else:  # recouvrement au milieu sans affecter les extermités
                coicop_copy_inf = coicop_nomenclature.loc[selection_bis].copy()
                coicop_copy_inf['stop'] = start - 1
                coicop_copy_sup = coicop_nomenclature.loc[selection_bis].copy()
                coicop_copy_sup['start'] = stop + 1

                coicop_nomenclature.loc[selection_bis, 'categorie_fiscale'] = categorie_fiscale
                coicop_nomenclature.loc[selection_bis, 'start'] = start
                coicop_nomenclature.loc[selection_bis, 'stop'] = stop
                coicop_nomenclature = coicop_nomenclature.append(coicop_copy_inf)
                coicop_nomenclature = coicop_nomenclature.append(coicop_copy_sup)
                coicop_nomenclature.reset_index(inplace = True, drop = True)
                coicop_nomenclature.sort_values(by = 'code_coicop', inplace = True)

    else:
        #assert origin is not None
        #assert label is not None
        #infra_labels = extract_infra_labels_from_coicop_code(coicop_nomenclature, str(value), label)
        additional_row = pd.DataFrame(columns = coicop_nomenclature.columns)
        additional_dict = {
            'code_coicop': str(value),
            'categorie_fiscale': categorie_fiscale,
            'start': start,
            'stop': stop,
            'origin': origin
            }
        #additional_dict.update(infra_labels)
        for item, val in list(additional_dict.items()):
            additional_row[item] = [val]

        coicop_nomenclature = coicop_nomenclature.append(additional_row)
        coicop_nomenclature.reset_index(inplace = True, drop = True)
        coicop_nomenclature.sort_values(by = 'code_coicop', inplace = True)

    return coicop_nomenclature


def add_fiscal_categories_to_coicop_nomenclature(coicop_nomenclature, to_csv = False):
    # On  ajoute des colonnes
    # période d'effet de la législation
    coicop_nomenclature['start'] = 0
    coicop_nomenclature['stop'] = 0
    # origine de du poste
    coicop_nomenclature['origin'] = 'COICOP INSEE'
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
    saindoux = dict(
        value = '01.1.5.2.3',
        categorie_fiscale = 'tva_taux_reduit',
        label = "Saindoux autres graisses d'origine animale",
        origin = 'TAXIPP',
        )
    # et les confiseries
    confiserie = dict(
        value ='01.1.8.1.3',
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
    # tabac
    cigares = dict(
        value = '02.2.2',
        categorie_fiscale = 'cigares',
        label = 'Cigares et cigarillos',
        origin = 'TAXIPP',
        )
    cigarettes = dict(
        value = '02.2.1',
        categorie_fiscale = 'cigarettes',
        label = 'Cigarettes',
        origin = 'TAXIPP',
        )
    tabac_a_rouler = dict(
        value = '02.2.3',
        categorie_fiscale = 'tabac_a_rouler',
        label = 'Tabac a rouler',  # TODO je n'arrive aps à mettre des accents
        origin = 'TAXIPP',
        )
    stupefiants = dict(
        value = '02.3',
        categorie_fiscale = '',
        label = 'Stupefiants',
        origin = 'COICOP UN',
        )
    alcools_tabac_stupefiants_offerts = dict(
        value = '02.4',
        categorie_fiscale = '',
        label = 'Alcools, tabcs et stupefiants offerts à un autre',
        origin = 'TAXIPP',
        )
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
    # Combustible solide de résidence principale (Ref : Code général des impôts article 278 bis 3bis a b c)
    bois_chauffage_98 = dict(
        value = '04.5.4.1.1',
        categorie_fiscale = 'tva_taux_reduit',
        start = 1998,
        stop = 2011
    )

    bois_chauffage_reforme_2012 = dict(
        value = '04.5.4.1.1',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
    )
    # Distribution d'eau, enlèvement des ordures ménagères, assainissement, autres services liés au logement n.d.a.
    # qui sont au taux réduit de 1994 à 2011
    eau_ordures_assainissement = dict(
        value = ['04.4.1.1.1', '04.4.1.2.1', '04.4.1.3.1'],
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011,
        )
    # avant de passer au taux intermédiaire
    ordures_assainissement_reforme_2012 = dict(
        value = ['04.4.1.2.1', '04.4.1.3.1'],
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    #sauf l'eau qui reste à taux réduit
    eau_post_2012 = dict(
        value = '04.4.1.1.1',
        categorie_fiscale = 'tva_taux_reduit' ,
        start = 2012,
    )

    # et pas de taxation des loyers
    loyers = dict(
        value = ['04.1.1.1.1', '04.1.1.2.1'],
        categorie_fiscale = '',
        )
    # TODO ajouter loyers fictifs
    # Services d'entretien et petites réparation dans le logement
    services_entretien = dict(
        value = '04.3.2.2.1',
        categorie_fiscale = 'tva_taux_intermediaire',
    )

    # 05 Ameublement, équipement ménager et entretien courant de la maison
    ameublement = dict(
        value = 5,
        categorie_fiscale = 'tva_taux_plein',
        )
    # sauf Services domestiques (ménage, garde enfant, jardinage)
    services_domestiques = dict(
        value = '05.6.2.1',
        categorie_fiscale = 'tva_taux_intermediaire',
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
    # Transport maritime et fluvial de passagers change en 2011  Attention 07.3.4 dans enquête BDF
    transport_maritime = dict(
        value = '07.3.6.1.2',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011,
        )
    transport_maritime_reforme_2012 = dict(
        value = '07.3.6.1.2',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )

    # Autres services de transports (yc déménagements)
    autres_services_transports = dict(
        value = '07.3.6.1.1',
        categorie_fiscale = 'tva_taux_plein'
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
    # Transport aérien de passagers change en 2012
    transport_aerien = dict(
        value = '07.3.3',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2024,
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
    # Carburants et lubrifiants pour véhicules de tourisme 1994 2024
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
        value = '08.1.1.1',
        categorie_fiscale = '',
        )
    # 09 Loisirs et cutures
    loisirs_culture = dict(
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
        stop = 2024,
        )
    #livre_reforme_2012 = dict(
        #value = '09.5.1',
        #categorie_fiscale = 'tva_taux_intermediaire',
        #start = 2012,
        #stop = 2013,
        #)
    #-> le livre est passé au taux intermediaire (7%) en 2012 avant de repasser au taux réduit à 5,5% en 2013,
    # comme on ne peut pas le passer au taux intermédiaire seulement pour une année on le laisse au taux réduit

    # Horticulture, floriculture
    plantes_fleurs = dict(
        value = '09.3.2.1',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2016,
    )
    # Jeux de hasard
    jeux_hasard = dict(
        value = '09.4.3',
        categorie_fiscale = '',
        label = 'Jeux de hasard',
        origin = 'COICOP UN'
        )
    # equipement sportif
    equipement_sportif = dict(
        value = '09.3.1.2',
        categorie_fiscale = 'tva_taux_plein',
        start = 1994
    )
    # Cinemas, théâtres, concerts
    cinema_theatre_concert = dict(
        value = '09.4.2.1',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011
        )
    # Cinemas, théâtres, concerts
    cinema_theatre_concert_reforme_2012 = dict(
        value = '09.4.2.1',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        stop = 2013
        )
    cinema_theatre_concert_reforme_2014 = dict(
        value = '09.4.2.1',
        categorie_fiscale = 'tva_taux_reduit',
        start = 2014
        )
    # Musées et zoo
    musee_zoo = dict(
        value = '09.4.2.2',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011
        )
    # Musée et zoo
    musee_zoo_reforme_2012 = dict(
        value = '09.4.2.2',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012
        )

    musee_zoo_reforme_2018 = dict(
        value = '09.4.2.2',
        categorie_fiscale = 'tva_taux_reduit',
        start = 2018
    )
    # Services de télévision et radiodiffusion
    tv_radio = dict(
        value = '09.4.2.3',
        categorie_fiscale = 'tva_taux_reduit',
        stop = 2011
        )
    # Services de télévision et radiodiffusion
    tv_radio_reforme_2012 = dict(
        value = '09.4.2.3',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012
        )
    # Autres services culturels
    autres_services_culturels = dict(
        value = '09.4.2.4',
        categorie_fiscale = 'tva_taux_plein',
        start = 1994
        )

    # Services récréatifs et sportifs
    services_recreatifs_sportifs = dict(
        value = '09.4.1',
        categorie_fiscale = 'tva_taux_reduit',
        start = 1994,
        )
    services_recreatifs_sportifs_reforme_2015 = dict(
        value = '09.4.1',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2015,
        )

    # Voyage à forfait
    voyage_forfait = dict(
        value = '09.6.1.1',
        categorie_fiscale = '',
        start = 2019
    )
    # 10 Education
    education = dict(
        value = 10,
        categorie_fiscale = '',
        )
    # 11 Hotellerie restauration
    hotellerie_restauration = dict(
        value = 11,
        categorie_fiscale = 'tva_taux_reduit',
        )
    # Consommation de boissons alcoolisées
    consommation_boissons_alcoolisees = dict(
        value = ['11.1.1.2.2', '11.1.1.2.3', '11.1.1.2.4'],
        categorie_fiscale = 'tva_taux_plein',  # TODO sauf en corse à 10%
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
    # Restauration sur place 2012 2024
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
    # Restauration à emporter 2012 2024
    restauration_a_emporter_reforme_2012 = dict(
        value = '11.1.1.1.2',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Cantines
    cantines = dict(
        value = '11.1.2',
        categorie_fiscale = 'tva_taux_reduit',
        )
    # Services d'hébergement 2012 2024
    service_hebergement = dict(
        value = '11.2.1',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # 12 Autres biens et services
    autres_biens_et_services = dict(
        value = 12,
        categorie_fiscale = 'tva_taux_plein',
        )
    # Prostitution
    prostitution = dict(
        value = '12.2',
        categorie_fiscale = '',
        label = 'Prostitution',
        origin = 'COICOP UN',
        )
    # Protection sociale TODO: check tva_taux_plein avant 2000
    protection_sociale_reforme_2000 = dict(
        value = '12.4',
        categorie_fiscale = 'tva_taux_reduit',
        start = 2000,
        stop = 2024,
        )
    # Protection sociale
    protection_sociale_reforme_2012 = dict(
        value = '12.4',
        categorie_fiscale = 'tva_taux_intermediaire',
        start = 2012,
        )
    # Autres assurances
    autres_assurances = dict(
        value = '12.5.5',
        categorie_fiscale = 'autres_assurances',
        label = 'Autres assurances',
        origin = 'COICOP UN',
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
    # Assurance vie
    assurance_vie = dict(
        value = '12.5.1',
        categorie_fiscale = 'autres_assurances',
        label = 'Assurance vie',
        origin = 'COICOP UN',
        )
    # Couts des services d'intermédiation financière indirectement mesurés
    intermediation_financiere = dict(
        value = '12.6',
        categorie_fiscale = '',
        )

    for member in [
            # 01
            alimentation,
            margarine, saindoux, confiserie,
            # 02
            alcools, vin, biere,
            cigares, cigarettes, tabac_a_rouler, stupefiants, alcools_tabac_stupefiants_offerts,
            # 03
            habillement,
            # 04
            logement, bois_chauffage_98 , bois_chauffage_reforme_2012,
            eau_ordures_assainissement, ordures_assainissement_reforme_2012,
            eau_post_2012,
            loyers, services_entretien,
            # 05
            ameublement, services_domestiques,
            # 06
            sante, pharmacie, parapharmacie, materiel_therapeutique,
            # 07
            transports,
            transport_combine_passagers, transport_combine_passagers_reforme_2012,
            transport_maritime, transport_maritime_reforme_2012,
            transport_aerien,
            transport_routier, transport_routier_reforme_2012,
            transport_ferroviaire, transport_ferroviaire_reforme_2012,
            autres_services_transports,
            carburants_lubrifiants,
            # 08
            communications, services_postaux,
            # 09
            loisirs_culture, journaux_periodiques, livre,
            plantes_fleurs , jeux_hasard,  equipement_sportif,
            cinema_theatre_concert, cinema_theatre_concert_reforme_2012, cinema_theatre_concert_reforme_2014,
            musee_zoo, musee_zoo_reforme_2012, musee_zoo_reforme_2018,
            tv_radio, tv_radio_reforme_2012 ,
            autres_services_culturels,
            services_recreatifs_sportifs, services_recreatifs_sportifs_reforme_2015,
            voyage_forfait,
            # 10 Education
            education,
            # 11 Hotellerie restauration
            hotellerie_restauration, cantines, service_hebergement,
            consommation_boissons_alcoolisees,
            restauration_sur_place, restauration_sur_place_reforme_2010, restauration_sur_place_reforme_2012,
            restauration_a_emporter, restauration_a_emporter_reforme_2010, restauration_a_emporter_reforme_2012,
            # 12
            autres_biens_et_services,
            protection_sociale_reforme_2000,
            prostitution,
            intermediation_financiere,
            autres_assurances, assurance_transports, assurance_vie, assurance_maladie, assurance_habitation,
            ]:

        coicop_nomenclature = apply_modification(coicop_nomenclature, **member)

    coicop_legislation = coicop_nomenclature.copy()
    if to_csv:
        coicop_legislation.to_csv(
            os.path.join(legislation_directory, 'coicop_legislation.csv'),
            )
    return coicop_legislation.copy()


def get_categorie_fiscale(value, year = None, assertion_error = True):
    coicop_nomenclature = pd.read_csv(
        os.path.join(legislation_directory, 'coicop_legislation.csv'),
        )
    if isinstance(value, int):
        value_str = '0' + str(value) if value < 10 else str(value)
        selection = coicop_nomenclature.code_coicop.str[:2] == value_str
    elif isinstance(value, str):
        selection = coicop_nomenclature.code_coicop.str[:len(value)] == value
    elif isinstance(value, list):
        selection = coicop_nomenclature.code_coicop.isin(value)

    if year is not None:
        selection = selection & (coicop_nomenclature.start <= year) & (year <= coicop_nomenclature.stop)

    categorie_fiscale = coicop_nomenclature.loc[selection, 'categorie_fiscale'].unique()
    if assertion_error:
        assert len(categorie_fiscale) == 1, 'Ther categorie fiscale is not unique. Candidates are: {}'.format(
            categorie_fiscale)
        return categorie_fiscale[0]
    else:
        return categorie_fiscale


def test_coicop_legislation():
    coicop_nomenclature = build_coicop_nomenclature.build_complete_coicop_nomenclature()
    coicop_nomenclature = add_fiscal_categories_to_coicop_nomenclature(coicop_nomenclature, to_csv = True)
    if coicop_nomenclature.categorie_fiscale.isnull().any():
        return coicop_nomenclature.loc[coicop_nomenclature.categorie_fiscale.isnull()]


if __name__ == '__main__':
    # extract_informations_from_coicop_to_categorie_fiscale()
    coicop_nomenclature = build_coicop_nomenclature.build_complete_coicop_nomenclature()
    coicop_nomenclature = add_fiscal_categories_to_coicop_nomenclature(coicop_nomenclature, to_csv = True)
    test_coicop_legislation()

    from openfisca_france_indirect_taxation.scripts.build_coicop_bdf import bdf
    bdf_coicop_nomenclature = bdf(year = 2011)
    bdf_coicop_nomenclature = add_fiscal_categories_to_coicop_nomenclature(bdf_coicop_nomenclature, to_csv = True)

    print((get_categorie_fiscale('11.1.1.1.1', year = 2010)))
