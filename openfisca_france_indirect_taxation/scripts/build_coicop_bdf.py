# -*- coding: utf-8 -*-


import pandas


from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_survey_manager.survey_collections import SurveyCollection

from openfisca_france_indirect_taxation.scripts.build_coicop_nomenclature import build_coicop_nomenclature
from openfisca_france_indirect_taxation.scripts.build_coicop_legislation import get_categorie_fiscale


def coicop_from_aliss(year = 2011):
    assert year == 2011
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


def guess_coicop_from_bdf(year = 2011):
    assert year == 2011
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
        entries.append(dict(
            code_coicop = code_coicop,
            label = matrice_passage_data_frame.loc[selection, 'label'].unique()[0],
            code_bdf = dirty_produit_str,
            ))

    result = pandas.DataFrame(entries)
    assert not result.code_coicop.duplicated().any()
    return result


def merge_with_coicop_nomenclature(data_frame):
    coicop_nomenclature = build_coicop_nomenclature()
    # First pass on coicop level 5
    coicop_nomenclature['poste_coicop'] = coicop_nomenclature['code_coicop'].copy()
    df1 = coicop_nomenclature.merge(data_frame, on = 'code_coicop', how = 'left')

    level = data_frame['code_coicop'].loc[0].count('.') + 1
    coicop_nomenclature['code_coicop'] = coicop_nomenclature['code_coicop'].str[:2 * level]

    remaining_data_frame = data_frame.loc[
        ~(data_frame.code_coicop.isin(coicop_nomenclature['poste_coicop'].unique()))
        ].copy()
    df2 = coicop_nomenclature.merge(remaining_data_frame, on = 'code_coicop', how = 'outer')

    result = df1.append(df2, ignore_index = True)

    df3 = result.copy()
    result = result.loc[~(result.poste_coicop.duplicated(keep = False) & result.label.isnull())].copy()

    result = result.append(coicop_nomenclature.loc[
        ~coicop_nomenclature.poste_coicop.isin(result.poste_coicop.unique())])

    result = result[[
        'label_division', 'label_groupe', 'label_classe', 'label_sous_classe', 'label_poste',
        'poste_coicop', 'code_coicop', 'label', 'code_bdf',
        ]].sort_values(by = ['code_coicop'])

    return result


def test_coicop_to_legislation(data_frame, adjust_coicop, year):
    errors = list()
    for code_coicop in data_frame.code_coicop.unique():
        selection = data_frame.loc[data_frame.code_coicop == code_coicop].copy()
        products = selection.label.unique()
        try:
            print code_coicop, products
            print get_categorie_fiscale(
                adjust_coicop.get(code_coicop, code_coicop), year = year)
        except AssertionError:
            print 'error'
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
    '01.1.1.5': '01.1.1.4.1',  # Autres céréales et produits à base de céréales]
    '01.1.2.7': '01.1.2.6.1',  # Autres viandes comestibles fraîches ou surge...
    '01.1.3.0': '01.1.3.1.1',  # Poissons frais
    '01.1.3.3': '01.1.3.2.1',  # Poissons et fruits de mer salés, fumés, séchés]
    '01.1.3.4': '01.1.3.2.2',  # Conserves et plats préparés à base de produi...
    '01.1.4.5': '01.1.4.3.1',  # Fromage et lait caillé]
    '01.1.4.6': '01.1.4.2.2',  # Autres produits laitiers (dessert à base de ...
    '01.1.4.7': '01.1.4.4.1',  # Oeufs
    '01.1.5.2': '01.1.5.2.2',  # Margarine
    '01.1.5.3': '01.1.5.2.1',  # Huiles alimentaires d'olive]
    '01.1.5.4': '01.1.5.2.1',  # Huiles alimentaires d'arachide, de tournesol...
    # On a rassemblé les deux les huiles alimentaires # TODO: peut-être faut-il séparer les huiles végétales
    # '01.1.5.5'  [ saindoux et autres graisses d'origine animale]
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
    '01.1.9.4': '01.1.8.1.1',  # autres produits alimentaires (aliments enfants, produits diététiques)
    '01.2.1.1': '01.2.1.2',    # café
    '01.2.1.2': '01.2.1.3.1',  # thé et plantes à infusion
    '01.2.1.3': '01.2.1.1.1',  # cacao et chocolat en poudre
    '01.2.2.1': '01.2.2.1.1',  # eaux minérales
    '01.2.2.2': '01.2.2.2.2',  # boissons gazeuses
    '01.2.2.3': '01.2.2.2',    # jus de fruits et de légumes, sirops, boisson...
    '01.2.2.4': '01.2.2.2.1',  # jus de légumes
    '11.1.1.2': '11.1.1.1.2',  # Repas dans cafés, bar
    }

adjust_bdf_coicop = {
    # '01.1.9.5':	'Panier alimentaire
    # '01.3.1.1':	"autres dépenses d'alimentation : cérémonies, séjours hors domicile, personne viv"
    # '01.3.1.2':	"autres dépenses d'alimentation : cadeau offert (à destination d'un autre ménage"
    '02.2.1.1': '02.2.1',  # Cigarettes
    '02.2.1.2': '02.2.2',  # cigares et cigarillos
    '02.2.1.3': '02.2.3',  # tabac sous d'autres formes et produits connexes
    '02.3.1.1': '02.3',    # Stupéfiants
    # '02.4.1.1':	'Dépenses de boissons alcoolisées, tabac et stupéfiants : cadeau offert à un autre'
    # '03.2.1.3':	'Chaussures pour enfant (3 à 13 ans)'
    # '03.2.2.1':	'Réparation et location de chaussures'
    # '03.3.1.1':	"Autres dépenses d'habillement : cérémonie, séjours hors domicile, personnes viva"
    # '03.3.1.2':	"Autres dépenses d'habillement : cadeau offert (à destination d'un autre  ménage)"
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
    # '05.3.1.6':	'Machine à coudre et à tricoter'
    # '05.3.1.7':	'Autres gros appareils ménagers'
    # '05.4.1.4':	'Réparation et entretien verrerie, vaisselle et autres ustensiles de cuisine'
    # '05.5.1.2':	'Gros outillage de jardinage'
    # '05.5.1.3':	'Réparation du gros outillage'
    # '05.5.2.1':	'Petit outillage et accessoires divers de bricolage yc petit matériel électrique'
    # '05.5.2.2':	"Petit outillage et accessoires divers de jardinage, matériaux d'aménagement exté"
    # '05.5.2.3':	'Réparation des petits outillages'
    # '05.7.1.1':	'Autres dépenses en équipement : personnes vivant hors du domicile au moins un jo'
    # '05.7.1.2':	"Autres dépenses en équipement : cadeau offert (à destination d'un autre ménage)"
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
    }

adjusted_coicop_by_original.update(adjust_bdf_coicop)


def adjust_coicop(data_frame):
    non_overlapping_adjust_coicop = dict()
    remaining_adjust_coicop = dict()
    for key, value in adjusted_coicop_by_original.iteritems():
        if value not in adjusted_coicop_by_original.keys():
            non_overlapping_adjust_coicop[key] = value
        else:
            remaining_adjust_coicop[key] = value
    result = data_frame.copy()
    result.replace(to_replace = {'code_coicop': non_overlapping_adjust_coicop}, inplace = True)
    result.replace(to_replace = {'code_coicop': remaining_adjust_coicop}, inplace = True)
    return result


def aliss(year = 2011):
    aliss_coicop = coicop_from_aliss(year = year)
    data_frame = merge_with_coicop_nomenclature(aliss_coicop)
    return test_coicop_to_legislation(data_frame, adjust_coicop, year = year)


def bdf(year = 2011):
    bdf_coicop = guess_coicop_from_bdf(year = year)
    bdf_coicop = adjust_coicop(bdf_coicop)
    data_frame = merge_with_coicop_nomenclature(bdf_coicop)
    errors = None  # test_coicop_to_legislation(data_frame, adjust_coicop, year = year)
    return errors, data_frame


# TODO check notamment problème avec sucre confiseries
if __name__ == '__main__':
    # result = coicop_from_bdf(year = 2011)
    # errors, data_frame = bdf()
    year = 2011
    bdf_coicop = guess_coicop_from_bdf(year = year)
    bdf_coicop2 = adjust_coicop(bdf_coicop)
    data_frame = merge_with_coicop_nomenclature(bdf_coicop2)

#   len(errors)
#    df = pandas.DataFrame.from_records(errors).sort_values(by = 'code_coicop')
#    print df[['code_coicop', 'products', 'categorie_fiscale']]
