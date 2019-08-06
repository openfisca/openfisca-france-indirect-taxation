# -*- coding: utf-8 -*-


import pandas

try:
    from openfisca_survey_manager import default_config_files_directory as config_files_directory
    from openfisca_survey_manager.survey_collections import SurveyCollection
except ImportError:
    SurveyCollection, config_files_directory = None, None


from openfisca_france_indirect_taxation.scripts.build_coicop_nomenclature import build_complete_coicop_nomenclature
from openfisca_france_indirect_taxation.scripts.build_coicop_legislation import get_categorie_fiscale


def coicop_from_aliss(year):
    aliss_survey_collection = SurveyCollection.load(
        collection = 'aliss', config_files_directory = config_files_directory
        )
    survey = aliss_survey_collection.get_survey('aliss_{}'.format(year))

    aliss = survey.get_values(table = 'Base_ALISS_2011')
    dirty_produits = aliss.souscode.unique()
    entries = list()

    for dirty_produit in dirty_produits:
        entries.append(dict(
            code_coicop = '0' + '.'.join(dirty_produit[:4]),
            label = dirty_produit[6:],
            code_aliss = dirty_produit[:6],
            ))

    result = pandas.DataFrame(entries)

    assert not result.code_coicop.duplicated().any()

    return result


def guess_coicop_from_bdf(year):
    from openfisca_france_indirect_taxation.utils import get_transfert_data_frames
    matrice_passage_data_frame, _ = get_transfert_data_frames(year)
    matrice_passage_data_frame.rename(
        columns = {
            'poste{}'.format(year): 'poste_bdf',
            'label{}'.format(year): 'label',
            },
        inplace = True
        )
    dirty_produits = matrice_passage_data_frame['poste_bdf'].unique()
    entries = list()

    for dirty_produit in dirty_produits:
        dirty_produit_str = str(dirty_produit)
        selection = matrice_passage_data_frame.poste_bdf == dirty_produit
        code_coicop = '0' + '.'.join(dirty_produit_str) \
            if len(dirty_produit_str) <= 4 \
            else dirty_produit_str[:2] + '.' + '.'.join(dirty_produit_str[2:])

        code_bdf = 'c0' + dirty_produit_str if len(dirty_produit_str) <= 4 else 'c' + dirty_produit_str
        entries.append(dict(
            code_coicop = code_coicop,
            label = matrice_passage_data_frame.loc[selection, 'label'].unique()[0],
            code_bdf = code_bdf,
            ))

    result = pandas.DataFrame(entries)
    assert not result.code_coicop.duplicated().any()
    return result


def merge_with_coicop_nomenclature(data_frame):
    coicop_nomenclature = build_complete_coicop_nomenclature()
    # First pass on coicop level 5
    coicop_nomenclature['poste_coicop'] = coicop_nomenclature['code_coicop'].copy()
    df1 = coicop_nomenclature.merge(data_frame, on = 'code_coicop', how = 'left', sort = True)

    level = data_frame['code_coicop'].loc[0].count('.') + 1
    coicop_nomenclature['code_coicop'] = coicop_nomenclature['code_coicop'].str[:2 * level]

    remaining_data_frame = data_frame.loc[
        ~(data_frame.code_coicop.isin(coicop_nomenclature['poste_coicop'].unique()))
        ].copy()

    df2 = coicop_nomenclature.merge(remaining_data_frame, on = 'code_coicop', how = 'outer', sort = True)

    result = df1.append(df2, ignore_index = True)

    result = result.loc[~(result.poste_coicop.duplicated(keep = False) & result.label.isnull())].copy()
    result = result.append(
        coicop_nomenclature.loc[
            ~coicop_nomenclature.poste_coicop.isin(result.poste_coicop.unique())],
        sort = True,
        )
    result = result[[
        'label_division', 'label_groupe', 'label_classe', 'label_sous_classe', 'label_poste',
        'poste_coicop', 'code_coicop', 'label', 'code_bdf',
        ]].sort_values(by = ['code_coicop', 'code_bdf'])
    return result


def test_coicop_to_legislation(data_frame, adjust_coicop, year):
    errors = list()
    for code_coicop in data_frame.code_coicop.unique():
        selection = data_frame.loc[data_frame.code_coicop == code_coicop].copy()
        products = selection.label.unique()
        try:
            print((code_coicop, products))
            print((
                get_categorie_fiscale(adjust_coicop.get(code_coicop, code_coicop), year = year)
                ))
        except AssertionError:
            print('error')
            error = dict(
                code_coicop = code_coicop,
                products = products,
                categorie_fiscale = get_categorie_fiscale(
                    adjust_coicop.get(code_coicop, code_coicop),
                    year = year,
                    assertion_error = False)
                )
            errors.append(error)
    return errors


adjusted_coicop_by_original = {
    '01.1.1.1': '01.1.1.4.3',  # Riz sous toutes ses formes et produits Ã  base de riz
    '01.1.1.2': '01.1.1.1.1',  # Pain et autres produits de boulangerie et de viennoiserie yc biscuits et gÃ¢teaux
    '01.1.1.3': '01.1.1.4.2',  # Pâtes alimentaires sous toutes leurs formes et plats à  base de pâtes
    '01.1.1.4': '01.1.1.3.3',  # Préparations telles que pâte à pâtisser, gâteau industriel, tarte, tourte, quich
    '01.1.1.5': '01.1.1.4.1',  # Autres céréales et produits à base de céréales]
    '01.1.2.1': '01.1.2.1.1',  # Viande bovine fraîche ou surgelée
    '01.1.2.2': '01.1.2.4.1',  # Viande porcine fraîche ou surgelée
    '01.1.2.3': '01.1.2.3.1',  # Viande ovine ou caprine fraîche ou surgelée
    '01.1.2.4': '01.1.2.5.1',  # Viande de volaille fraîche ou surgelée
    '01.1.2.5': '01.1.2.4.2',  # Viande séchée salée ou fumée, charcuterie et abats, frais ou surgelé (jambon, sa
    '01.1.2.6': '01.1.2.6.3',  # Conserve de viande, produit de transformation des viandes, plat préparé de viand
    '01.1.2.7': '01.1.2.6.1',  # Autres viandes comestibles fraîches ou surge...
    '01.1.3.0': '01.1.3.1.1',  # Poissons frais
    '01.1.3.1': '01.1.3.2.1',  # Poissons surgelés ou congelés (hors poissons panés ou cuisinés)
    '01.1.3.2': '01.1.3.1.2',  # Fruits de mer frais ou surgelés (yc cuits, nc cuisinés ) TODO: frais et surg. meme TVA
    '01.1.3.3': '01.1.3.2.1',  # Poissons et fruits de mer salés, fumés, séchés]
    '01.1.3.4': '01.1.3.2.2',  # Conserves et plats préparés à base de produi...
    '01.3.1.1': '01.10.1',     # autres dépenses d'alimentation : cérémonies, séjours hors domicile, personne viv
    '01.3.1.2': '01.10.2',     # autres dépenses d'alimentation : cadeau offert (à destination d'un autre ménage
    '01.1.4.1': '01.1.4.1.1',  # Lait entier
    '01.1.4.2': '01.1.4.1.1',  # Lait demi-écrémé, écrémé
    '01.1.4.3': '01.1.4.1.1',  # lait de conserve
    '01.1.4.4': '01.1.4.2.1',  # Yaourts, fromage blanc et petits suisses yc de soja
    '01.1.4.5': '01.1.4.3.1',  # Fromage et lait caillé]
    '01.1.4.6': '01.1.4.2.2',  # Autres produits laitiers (dessert à base de ...
    '01.1.4.7': '01.1.4.4.1',  # Oeufs
    '01.1.5.1': '01.1.5.1.1',  # Beurre
    '01.1.5.2': '01.1.5.2.2',  # Margarine
    '01.1.5.3': '01.1.5.2.1',  # Huiles alimentaires d'olive]
    '01.1.5.4': '01.1.5.2.1',  # Huiles alimentaires d'arachide, de tournesol...
    # On a rassemblé les deux les huiles alimentaires # TODO: peut-être faut-il séparer les huiles végétales
    '01.1.5.5': '01.1.5.2.2',  # saindoux et autres graisses d'origine animale
    '01.1.6.1': '01.1.6.1.1',  # agrumes frais et surgelés
    '01.1.6.2': '01.1.6.1.1',  # bananes fraiches
    '01.1.6.3': '01.1.6.1.1',  # pommes
    '01.1.6.4': '01.1.6.1.1',  # poires
    # TODO: affiner 01.1.6.1.1 ou pas ?
    '01.1.6.5': '01.1.6.2.1',  # fruits à noyaux (frais ou congelés)]
    '01.1.6.6': '01.1.6.2.1',  # baies (fraîches ou congelées)]
    '01.1.6.7': '01.1.6.2.1',  # autres fruits, fruits tropicaux (frais ou co...
    '01.1.6.8': '01.1.6.2.1',  # fruits séchés]
    '01.1.6.9': '01.1.6.2.1',  # fruits au sirop et fruits surgelés]
    # TODO: affiner 01.1.6.2.1 ou pas ?
    '01.1.7.1': '01.1.7.1.1',  # légumes frais Ã  feuilles et à tiges, herbes aromatiques (frais)
    '01.1.7.2': '01.1.7.1.1',  # choux (frais)
    '01.1.7.3': '01.1.7.1.1',  # légumes frais cultivés pour leurs fruits]
    '01.1.7.4': '01.1.7.1.1',  # racines alimentaires fraiches et champignons...
    '01.1.7.5': '01.1.7.2.1',  # légumes secs]
    '01.1.7.6': '01.1.7.2.1',  # légumes surgelés (non cuisinés)]
    '01.1.7.7': '01.1.7.2.1',  # légumes et plats à base de légume, en conser...
    '01.1.7.9': '01.1.7.2.2',  # pomme de terre, autres tubercules, produits ...
    '01.1.7.8': '01.1.7.2.3',  # légumes préparés et plats à base de légumes,...
    '01.1.8.1': '01.1.8.1.1',  # sucre
    '01.1.8.2': '01.1.8.1.2',  # confitures, marmelade, compote, gelées, purées et pâtes de fruits, miel
    '01.1.8.3': '01.1.8.2.1',  # chocolat
    '01.1.8.4': '01.1.8.1.3',  # sucreries, bonbons et autres confiseries
    '01.1.8.5': '01.1.8.3.1',  # crèmes glacées, sorbets, entremets glacés]
    '01.1.8.6': '01.1.8.1.1',  # autres produits à base de sucre (fruits confits, pâtes à tartiner)
    # TODO: créer une nouvelle section ? pour 01.1.8.6
    '01.1.9.1': '01.1.9.1.1',  # sauces et condiments
    '01.1.9.2': '01.1.9.1.1',  # sel et épices sèches
    '01.1.9.3': '01.1.9.3.2',  # levure , préparations pour desserts, soupes TODO verif soupe à remettre ailleurs
    '01.1.9.4': '01.1.8.1.1',  # autres produits alimentaires (aliments enfants, produits diététiques)
    # TODO panier alimentaire
    '01.2.1.1': '01.2.1.2.1',  # café
    '01.2.1.2': '01.2.1.3.1',  # thé et plantes à infusion
    '01.2.1.3': '01.2.1.1.1',  # cacao et chocolat en poudre
    '01.2.2.1': '01.2.2.1.1',  # eaux minérales
    '01.2.2.2': '01.2.2.2.2',  # boissons gazeuses
    '01.2.2.3': '01.2.2.2.3',  # jus de fruits et de légumes, sirops, boisson... TODO verif
    '01.2.2.4': '01.2.2.2.1',  # jus de légumes
    '02.1.1.1': '02.1.1.1.1',  # spiritueux et liqueurs
    '02.1.2.1': '02.1.2.1.1',  # vins et cidres
    '11.1.1.2': '11.1.1.1.2',  # Repas dans cafés, bar
    '02.1.2.2': '02.1.2.2.1',  # autres apéritifs à base de vin, champagne et autres mousseux, saké et autres
    '02.1.3.1': '02.1.3.1.1',  # bière et boissons à base de bière
    '02.2.1.1': '02.2.1',      # Cigarettes
    '02.2.1.2': '02.2.2',      # cigares et cigarillos
    '02.2.1.3': '02.2.3',      # tabac sous d'autres formes et produits connexes
    '02.3.1.1': '02.3',        # Stupéfiants
    '02.4.1.1': '02.4',        # Dépenses de boissons alcoolisées, tabac et stupéfiants : cadeau offert à un autre
    '03.1.1.1': '03.1.1.1.1',  # Tissus d'habillement
    '03.1.2.1': '03.1.2.1.1',  # vêtements pour homme
    '03.1.2.2': '03.1.2.2.1',  # vêtements pour femme
    '03.1.2.3': '03.1.2.3.1',  # vêtements pour enfants
    '03.1.3.1': '03.1.3.1.1',  # mercerie et  accessoire sont groupés dans bdf et pas dans coicop
    '03.1.4.1': '03.1.4.1.1',  # Nettoyage, réparation et location de vêtements
    '03.2.1.1': '03.2.1.1.1',  # Chaussures pour homme
    '03.2.1.2': '03.2.1.1.2',  # chaussures pour femmes
    '03.2.1.3': '03.2.1.1.3',  # chaussures pour enfants
    '03.2.2.1': '03.2.1.2.3',  # Réparation de chaussures
    '03.3.1.1': '03.3.1',      # Autres dépenses d'habillement : cérémonie, séjours hors domicile, personnes viva"
    '03.3.1.2': '03.3.2',	  # "Autres dépenses d'habillement : cadeau offert (à destination d'un autre  ménage)"
    '04.1.1.1': '04.1.1.1.1',  # loyer en résidence principale
    '04.1.2.1': '04.1.1.2.1',  # loyer autres résidence
    '04.3.1.1': '04.3.1.1.1',  # Produits destinés aux travaux courants d’entretien et de réparation du logement
    '04.3.2.1': '04.3.2.2.1',  # Services d'entretien et petites réparation dans le logement (plombier, entretien)
    '04.4.1.1': '04.4.1.2.1',  # Redevance d’enlèvement des ordures
    '04.4.2.1': '04.4.1.3.1',  # Services d’assainissement
    '04.4.3.1': '04.4.1.1.1',  # Factures d’eau résidence principale, autre logement, dépendance, terrain
    '04.4.4.1': '04.4.1.4.1',  # Charges collectives relatives au logement (payées isolément du loyer ou crédit)
    '04.5.1.1': '04.5.1.1.1',  # Facture d'électricité résidence principale, autre logement, garage, dépendance
    '04.5.0.0': '04.5.1.1.1',  # Facture électricité + gaz (non dissociables)
    '04.5.2.1': '04.5.2.1.1',  # Facture de gaz résidence principale, autre logement
    '04.5.2.2': '04.5.2.2.1',  # Achats de butane, propane résidence principale, autre logement
    '04.5.3.1': '04.5.3.1.1',  # Combustibles liquides pour la résidence principale : fuel, mazout, pétrole
    '04.5.4.1': '04.5.4.1.1',  # Combustible solide résidence principale
    '04.5.5.1': '04.5.5.1.1',  # Chauffage urbain (par vapeur)
    '04.6.1.1': '04.6',        # autres dépenses d'habitation
    '05.1.1.2': '05.1.1.2.2',  # Mobilier de séjour (buffet, bahut, bibliothèque, etc.)
    '05.1.1.4': '05.1.1.2.3',  # Tables, sièges, chaises hors cuisine et salle de bain
    '05.1.1.1': '05.1.1.1.2',  # Mobilier de chambre (lit, armoire, commode, chevet, bureau enfant, sommier) yc m
    '05.1.1.3': '05.1.1.3.1',  # Mobilier de cuisine et de salle de bain yc éléments intégrés ou non, tabourets,
    '05.1.1.5': '05.1.1.5.3',  # Mobilier de jardin (balancelle, table, fauteuil, abri de jardin, portique, etc.)
    '05.1.1.6': '05.1.1.5.1',  # Autres meubles, accessoires du mobilier (yc luminaires, décoration, équipement e
    '05.1.2.1': '05.1.2.1.1',  # Tapis et autres revêtements de sol (lino, moquette, etc.), pose et réparation de
    '05.1.3.1': '05.1.1.5.4',  # Réparation de meubles
    '05.2.1.1': '05.2.1.1.3',  # Articles de literie (futons, oreillers, couettes, couvertures, draps, alèses, et
    '05.2.1.2': '05.2.1.2.1',  # Autres articles de ménage en textile (tissu d'ameublement, voilages, linge de ma
    '05.3.1.1': '05.3.1.3.1',  # Réfrigérateurs, congélateurs et caves à vin
    '05.3.1.2': '05.3.1.1.1',  # Lave linge, sèche linge et lave vaisselle
    '05.3.1.3': '05.3.1.2.1',  # Gros appareils de cuisson
    '05.3.1.4': '05.3.1.4.2',  # Appareils de chauffage et de climatisation et autres gros appareils électroménag
    '05.3.1.5': '05.3.1.4.1',  # Appareils de nettoyage (aspirateur, nettoyeur vapeur etc.)
    '05.3.1.6': '05.3.1.4.1',  # 'Machine à coudre et à tricoter'
    '05.3.1.7': '05.3.1.4.1',  # Autres gros appareils ménagers
    '05.3.2.1': '05.3.2.1.1',  # petit électroménager
    '05.3.3.1': '05.3.3.1.1',  # Réparation et entretien des appareils électroménagers
    '05.4.1.1': '05.4.1.1.2',  # Verrerie et cristallerie, vaisselle, articles de ménage ou de toilette en faïenc
    '05.4.1.2': '05.4.1.2.1',  # Coutellerie et argenterie
    '05.4.1.3': '05.4.1.3.1',  # Ustensiles de cuisine et autres articles de ménage
    '05.4.1.4': '05.3.3.1.1',  # Réparation et entretien verrerie, vaisselle et autres ustensiles de cuisine
    '05.5.1.1': '05.5.1.1.1',  # Gros outillage de bricolage
    '05.5.1.2': '05.5.1.1.1',  # 'Gros outillage de jardinage'
    '05.5.2.2': '05.5.1.1.4',  # Petit outillage et accessoires divers de jardinage, matériaux d'aménagement exté
    '05.5.2.1': '05.5.1.1.5',  # Petit outillage et accessoires divers de bricolage yc petit matériel électrique
    '05.6.1.1': '05.6.1.2.1',  # Produits de nettoyage et d’entretien (yc pour piscine)
    '05.6.2.1': '05.6.2.1.1',  # Services domestiques (ménage, garde enfant, jardinage, etc.)
    '05.6.2.2': '05.6.2.2.1',  # Autres services d’entretien pour le logement (blanchisserie, location appareils,
    '05.7.1.1': '05.7.1',      # Autres dépenses en équipement : personnes vivant hors du domicile au moins un jo
    '05.7.1.2': '05.7.2',      # Autres dépenses en équipement : cadeau offert (à destination d'un autre ménage)
    # '05.6.1.2': ,            # Autres produits ménagers (articles papier et plastique, brosserie, produits dive TODO
    '06.1.1.1': '06.1.1.1.1',  # Produits pharmaceutiques à ingurgiter et traitants, compléments alimentaires, vi
    '06.1.1.2': '06.1.1.2.1',  # Autres produits pharmaceutiques (parapharmacie, pansements, préservatifs, etc. )
    '06.1.1.3': '06.1.1.3.1',  # Appareils et matériels thérapeutiques (lunettes, prothèses, etc.) yc leur répara
    '06.2.1.1': '06.2.1.1.1',  # Consultations des médecins généralistes ou spécialistes hors hospitalisation
    '06.2.2.1': '06.2.2.1.1',  # Dentiste, orthodontie
    '06.2.3.1': '06.2.3.1.1',  # Services des laboratoires d’analyse médicale et des cabinets de radiologie
    '06.2.3.2': '06.2.3.1.2',  # Services des auxiliaires médicaux (infirmier, kiné, laboratoire, etc.)
    '06.2.3.3': '06.2.3.1.3',  # Services extra hospitaliers (ambulance, location matériel)
    '06.3.1.1': '06.3',	  # Services et soins hospitaliers'
    '06.4.1.1': '06.4.1',      # Autres dépenses de santé : personnes vivant hors du domicile au moins un jour pa
    '06.4.1.2': '06.4.2',      # Autres dépenses de santé : cadeau offert (à destination d’un autre ménage)
    '07.1.1.1': '07.1.1.1.1',  # Achats d'automobiles neuves
    '07.1.1.2': '07.1.1.2.1',  # Achats d'automobiles d'occasion
    '07.1.2.1': '07.1.2.1.1',  # Motocycles
    '07.1.3.1': '07.1.2.1.2',  # Achats de cycles neufs et occasion
    '07.2.1.1': '07.2.1.1.1',  # Pièces détachées, pneus et accessoires pour les véhicules personnels (hors ceux
    '07.2.2.1': '07.2.2.1.1',  # Carburants, électricité, huiles, lubrifiants, etc. TODO: séparer les postes?
    '07.2.3.1': '07.2.3.2.1',  # Réparations, dépannages, révisions, lavage, entretien et contrôle technique
    '07.2.4.1': '07.2.4.1.2',  # Services de location d’un local, frais de parking
    '07.2.4.2': '07.2.4.2.1',  # Autres services liés à l’utilisation de véhicules personnels (péages, auto école
    '07.3.1.1': '07.3.1.1.1',  # Services de transports de voyageurs locaux (métro, tram) et SNCF longue distance
    '07.3.2.1': '07.3.2.1.1',  # Services de transports de voyageurs par route yc car scolaire
    '07.3.3.1': '07.3.3.1.1',  # Services de transports de voyageurs par air (yc transport de bagages et de véhic
    '07.3.5.1': '07.3.5.1.1',  # Services combinés de transport de voyageurs carte navigo, tickets train + bus, e
    '07.3.4.1': '07.3.6.1.2',  # Services de transport par mer et voies navigables intérieures (yc transport de b
    '07.3.6.1': '07.3.6.1.1',  # Autres services de transport (yc déménagement)
    '07.1.4.1': '07.1.3',      # Achats d'autres véhicules neufs et occasion
    '07.4.1.1': '07.4.1',      # Autres dépenses de transport : cérémonie, séjours hors domicile, personnes vivan
    '07.4.1.2': '07.4.2',      # Autres dépenses de transport : cadeau offert (à destination d’un autre ménage)
    '08.1.1.1': '08.1.1.1.1',  # Services postaux (yc timbres, enveloppes)
    '08.1.2.1': '08.1.2.1.1',  # Achats et réparation téléphones fixes ou portables, télécopieurs et accessoires
    '08.1.3.1': '08.1.2.2.1',  # Services de téléphone et fax, internet, recharges téléphoniques
    # La nomenclature coicop chargée sur le site de l'INSEE ne suit pas celle de l'ONU
    '08.1.4.1': '08.2',        # Autres dépenses de communications  : cadeau offert (à destination d’un autre mén
    '09.1.1.1': '09.1.1.1.3',  # Appareils de réception, d’enregistrement et de reproduction du son
    '09.1.1.2': '09.1.1.1.2',  # Téléviseurs, home cinéma, magnétoscopes, antennes, adapteur et lecteur DVD de sa
    '09.1.2.1': '09.1.2.1.1',  # Equipement photographique et cinématographique (yc accessoires)
    '09.1.2.2': '09.1.2.1.1',  # Instruments d'optique non médicale et divers électroacoustique (microscope, jume
    '09.1.3.1': '09.1.3.1.1',  # Micro-ordinateurs, tablettes, matériels et accessoires informatiques (yc pièces
    '09.1.4.1': '09.1.4.1.1',  # Supports vierges ou enregistrés pour l’image et le son (yc téléchargement)
    '09.1.5.1': '09.1.5.1.1',  # Réparation des équipements et accessoires audiovisuels photographiques et inform
    '09.2.1.1': '09.2.1.1.1',  # Gros équipements pour les loisirs de plein air et les sports (caravanes, camping
    '09.2.2.1': '09.2.1.1.3',  # Instruments de musique et accessoires
    '09.3.1.1': '09.3.1.1.1',  # Jeux, jouets et passe temps yc jeux vidéos
    '09.3.1.2': '09.3.2.1.1',  # Equipements de sport, de camping et de loisirs en plein air (pêche, chasse, uste
    '09.3.3.1': '09.3.4.1.2',  # Animaux d’agrément, nourriture, produits et accessoires pour les animaux d’agrém
    '09.3.4.1': '09.3.4.1.1',  # Aliments autres animaux (chèvre, volaille, cabri, cochon, etc.)
    '09.4.1.1': '09.4.1.1.2',  # Services sportifs et récréatifs (spectacles sportifs, participation loisirs, loc
    '09.4.2.1': '09.4.2.1.1',  # Cinémas, théâtres, salles de concert, cirques, foire
    '09.4.2.2': '09.4.2.2.2',  # Musées, jardins zoologiques et similaires
    '09.4.2.3': '09.4.2.3.1',  # Services de télévision et de radiodiffusion (location, redevance, abonnement)
    '09.4.2.4': '09.4.2.4.1',  # Smartbox et autres services de loisirs (animateurs, photographes, services pour
    '09.4.3.1': '09.4.3',      # Jeux de hasard
    '09.5.1.1': '09.5.1.1.2',  # Livres yc e-books
    '09.5.2.1': '09.5.2.1.1',  # Journaux et périodiques yc par abonnement
    '09.5.3.1': '09.5.3.1.1',  # Imprimés divers (carte postale, de visite, poster, calendrier, carte routière, a
    '09.5.4.1': '09.5.3.1.2',  # Articles de papeterie et de dessin (yc toner pour imprimante)
    '09.6.1.1': '09.6.1.1.1',  # Voyages à forfait, week-end, excursions yc voyage scolaire
    '09.7.1.1': '09.7.1',      # Autres dépenses des loisirs : séjours hors domicile, personnes vivant hors du do
    '09.7.1.2': '09.7.2',      # Autres dépenses de loisirs et culture : cadeau offert (à destination d’un autre
    '10.1.1.1': '10.1',        # Enseignement maternel et primaire (scolarité et cours d’alphabétisation)
    '10.1.2.1': '10.2',        # Enseignement secondaire (scolarité et inscription aux concours de niveau seconda
    '10.1.3.1': '10.3',        # Enseignement supérieur et frais d’inscription aux concours des grandes écoles
    '10.1.4.1': '10.4',        # Enseignement ne correspondant à aucun niveau particulier (cours particuliers, en
    '10.1.5.1': '10.5.1',      # Autres dépenses d’enseignement : personnes vivant hors du domicile au moins un j
    '10.1.5.2': '10.5.2',      # Autres dépenses d’enseignement : cadeau offert (à destination d’un autre ménage)
    '11.1.1.1': '11.1.1.1.1',  # Repas pris dans un restaurant
    '11.1.2.1': '11.1.2.1.1',  # Cantines scolaire et professionnelle
    '11.2.1.1': '11.2.1.1.1',  # Services d’hébergement (hôtels, gîtes, campings, CROUS, internats)
    # '11.1.3.1': '11.1.3.1',    # Autres dépenses de restauration : séjours hors domicile, personnes vivant hors d
    # '11.1.3.2': '11.1.3.2',    # Autres dépenses de restauration : cadeau offert (à destination d’un autre ménage
    '12.1.1.1': '12.1.1.1.1',  # Salons de coiffure et esthétique corporelle (yc cures thermales, tatouages, pier
    '12.1.2.1': '12.1.3.3.3',  # Appareils électriques pour les soins personnels
    '12.1.2.2': '12.1.3.2.1',  # Autres articles et produits pour les soins personnels (savon, produits de toilet
    '12.3.1.1': '12.3.1.1.1',  # Articles de bijouterie, de joaillerie et d’horlogerie (yc leur réparation)
    '12.3.2.1': '12.3.2.1.1',  # Articles de voyage et autres contenants d'effets personnels (maroquinerie, valis
    '12.3.2.2': '12.3.2.2.2',  # Autres effets personnels (briquets, parapluies, lunettes de soleil, articles pou
    '12.3.3.1': '12.3.3.1.1',  # Autres biens et services offerts (à des personnes extérieures au ménage)
    '12.4.1.1': '12.4.1.1.1',  # Services de protection sociale (assistante maternelle, crèche, maison de retrait
    '12.5.1.1': '12.5.1.1.1',  # Assurance vie décès
    '12.5.2.1': '12.5.2.1.1',  # Assurances liées au logement
    '12.5.3.1': '12.5.3.1.1',  # Assurances liées à la santé
    '12.5.4.1': '12.5.4.1.1',  # Assurances liées aux transports (yc assurance voyage)
    '12.5.5.1': '12.5.5.1.1',  # Autres assurances (pack assurance, scolaire, dépendance, prévoyance, animaux, ob
    '12.6.1.1': '12.6.1.1.1',  # Services financiers
    '12.7.1.1': '12.7.1.1.1',  # Autres services (pompes funèbres, services juridiques, vestiaires, consignes, gr
    '12.7.1.2': '12.7.1.2.1',  # Caution pour la location d'un logement
    '12.8.1.1': '12.8.1',      # Autres dépenses occasionnées par une cérémonie
    }


# '01.3.1.1':	"autres dépenses d'alimentation : cérémonies, séjours hors domicile, personne viv"
# '01.3.1.2':	"autres dépenses d'alimentation : cadeau offert (à destination d'un autre ménage"
# '03.2.1.3':	'Chaussures pour enfant (3 à 13 ans)'
# '03.2.2.1':	'Réparation et location de chaussures'
# '04.1.2.1':	'Loyers (hors charges ou avec charges non isolables) des locataires autres réside'
# '04.4.2.1':	"Services d'assainissement"
# '04.4.3.1':	"Factures d'eau résidence principale, autre logement, dépendance, terrain"
# '04.4.4.1':	'Charges collectives relatives au logement (payées isolément du loyer ou crédit)'
# '04.5.0.0':	'Facture électricité + gaz (non dissociables)'
# '04.5.5.2':	'Glace'
# '04.6.1.1':	"Autres dépenses d'habitation : cadeau offert (à destination d'un autre ménage)""
# '05.1.1.0':	"Meubles informatiques"
# '05.1.1.6':	'Autres meubles, accessoires du mobilier (yc luminaires, décoration, équipement e'
# '05.1.3.1':	'Réparation de meubles'
# '05.3.1.5':	'Appareils de nettoyage (aspirateur, nettoyeur vapeur etc.)'
# '05.3.1.7':	'Autres gros appareils ménagers'
# '05.4.1.4':	'Réparation et entretien verrerie, vaisselle et autres ustensiles de cuisine'
# '05.5.1.2':	'Gros outillage de jardinage'
# '05.5.1.3':	'Réparation du gros outillage'
# '05.5.2.1':	'Petit outillage et accessoires divers de bricolage yc petit matériel électrique'
# '05.5.2.2':	"Petit outillage et accessoires divers de jardinage, matériaux d'aménagement exté"
# '05.5.2.3':	'Réparation des petits outillages'
# '06.2.3.2':	'Services des auxiliaires médicaux (infirmier, kiné, laboratoire, etc.)'
# '06.2.3.3':	'Services extra hospitaliers (ambulance, location matériel)'
# '06.3.1.1':	'Services et soins hospitaliers'
# '06.4.1.1':	"Autres dépenses de santé : personnes vivant hors du domicile au moins un jour pa"
# '06.4.1.2':	"Autres dépenses de santé : cadeau offert (à destination d'un autre ménage)"
# '07.1.3.1':	"Achats de cycles neufs et occasion"
# '07.1.4.1':	"Achats d'autres véhicules neufs et occasion
# '07.3.4.1':	"Services de transport par mer et voies navigables intérieures (yc transport de b"
# '07.4.1.1':	"Autres dépenses de transport : cérémonie, séjours hors domicile, personnes vivan"
# '07.4.1.2':	"Autres dépenses de transport : cadeau offert (à destination d'un autre ménage)"
# '08.1.3.1':	"Services de téléphone et fax, internet, recharges téléphoniques"
# '08.1.4.1':	"Autres dépenses de communications  : cadeau offert (à destination d'un autre mén"
# '09.1.1.2':	"Téléviseurs, home cinéma, magnétoscopes, antennes, adapteur et lecteur DVD de sa"
# '09.1.2.2':	"Instruments d'optique non médicale et divers électroacoustique (microscope, jume"
# '09.2.2.1':	'Instruments de musique et accessoires'
# '09.2.2.2':	"Gros équipements pour les loisirs d'intérieur (table de billard, de ping-pong, f"
# '09.2.3.1':	"Réparation et entretien de biens durables pour les loisirs, les sports et la cul"
# '09.3.1.2':	"Equipements de sport, de camping et de loisirs en plein air (pêche, chasse, uste"
# '09.4.3.1':	"Jeux de hasard (loto, tiercé, etc.)"
# '09.5.4.1':	"Articles de papeterie et de dessin (yc toner pour imprimante)"
# '09.7.1.1':	"Autres dépenses des loisirs : séjours hors domicile, personnes vivant hors du do"
# '09.7.1.2':	"Autres dépenses de loisirs et culture : cadeau offert (à destination d'un autre"
# '10.1.2.1':	"Enseignement secondaire (scolarité et inscription aux concours de niveau seconda"
# '10.1.3.1':	"Enseignement supérieur et frais d'inscription aux concours des grandes écoles"
# '10.1.4.1':	"Enseignement ne correspondant à aucun niveau particulier (cours particuliers, en"
# '10.1.5.1':	"Autres dépenses d'enseignement : personnes vivant hors du domicile au moins un j"
# '10.1.5.2':	"Autres dépenses d'enseignement : cadeau offert (à destination d'un autre ménage)"
# '11.1.3.1':	"Autres dépenses de restauration : séjours hors domicile, personnes vivant hors d"
# '11.1.3.2':	"Autres dépenses de restauration : cadeau offert (à destination d'un autre ménage"
# '12.1.2.1':	"Appareils électriques pour les soins personnels"
# '12.1.2.2':	"Autres articles et produits pour les soins personnels (savon, produits de toilet"
# '12.3.3.1':	"Autres biens et services offerts (à des personnes extérieures au ménage)"
# '12.5.1.1':	"Assurances vie, décès"
# '12.5.5.1':	"Autres assurances (pack assurance, scolaire, dépendance, prévoyance, animaux, ob"
# '12.8.1.1':	"Autres dépenses occasionnées par une cérémonie"
# '12.9.1.1':	"Dépenses SAI des personnes vivant hors du domicile au moins un jour par semaine"
# '13.1.1.1':	"Impôts et taxes de la résidence principale"
# '13.1.2.1':	"Impôts et taxes pour une résidence secondaire ou un autre logement"
# '13.1.4.1':	"Impôts sur le revenu"
# '13.1.5.1':	"Taxes automobiles (cartes grises, contraventions)"
# '13.1.6.1':	"Autres impôts et taxes (taxe foncière pour jardin ou autre, amendes, passeport),"
# '13.2.1.1':	"Remboursements de prêts pour la résidence principale (yc garage et dépendance)"
# '13.2.2.1':	"Remboursements des autres prêts immobiliers"
# '13.3.1.1':	"Aides et dons (occasionnels ou réguliers) en argent offerts par le ménage et pen"
# '13.4.1.1':	"Gros travaux pour la résidence principale yc matériaux de construction de gros oeuvre"
# '13.4.2.1':	"Gros travaux pour une résidence secondaire ou un autre logement yc matériaux de"
# '13.5.1.1':	"lRemboursements de crédits à a consommation (yc voiture, gros travaux, biens dur"
# '13.6.1.1':	"Prélèvements de l'employeur"
# '13.7.1.1':	"Achats de logements, garages, parkings, box et terrains"
# '13.7.2.2':	"Epargne salariale : achat d'actions de l'entreprise"
# '14.1.1.1':	"Allocations logement reçu par le ménage"


def adjust_coicop(data_frame):
    non_overlapping_adjust_coicop = dict()
    remaining_adjust_coicop = dict()
    for key, value in list(adjusted_coicop_by_original.items()):
        if value not in list(adjusted_coicop_by_original.keys()):
            non_overlapping_adjust_coicop[key] = value
        else:
            remaining_adjust_coicop[key] = value
    result = data_frame.copy()
    result.replace(to_replace = {'code_coicop': non_overlapping_adjust_coicop}, inplace = True)
    if remaining_adjust_coicop:
        result.replace(to_replace = {'code_coicop': remaining_adjust_coicop}, inplace = True)
    return result


def aliss(year):
    aliss_coicop = coicop_from_aliss(year = year)
    data_frame = merge_with_coicop_nomenclature(aliss_coicop)
    return test_coicop_to_legislation(data_frame, adjust_coicop, year = year)


def bdf(year):
    bdf_coicop = guess_coicop_from_bdf(year = year)
    bdf_coicop = adjust_coicop(bdf_coicop)
    data_frame = merge_with_coicop_nomenclature(bdf_coicop)
    duplicated_coicop = data_frame.loc[data_frame.code_coicop.dropna().duplicated()]
    for code_coicop in duplicated_coicop.code_coicop.unique():
        n = sum(data_frame.code_coicop == code_coicop)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        enhanced_code_coicops = [code_coicop + '.' + alphabet[i] for i in range(n)]
        data_frame.loc[data_frame.code_coicop == code_coicop, 'code_coicop'] = enhanced_code_coicops

    # errors = None  # test_coicop_to_legislation(data_frame, adjust_coicop, year = year)
    return data_frame  # errors


# TODO check notamment problème avec sucre confiseries
if __name__ == '__main__':
    year = 2011
    bdf_coicop = guess_coicop_from_bdf(year = year)
    adjusted_bdf_coicop = adjust_coicop(bdf_coicop)
    data_frame = merge_with_coicop_nomenclature(adjusted_bdf_coicop)

    #   len(errors)
    #   df = pandas.DataFrame.from_records(errors).sort_values(by = 'code_coicop')
    #   print df[['code_coicop', 'products', 'categorie_fiscale']]
