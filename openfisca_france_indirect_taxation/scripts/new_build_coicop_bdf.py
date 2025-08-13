import pandas as pd
import os
import importlib

from openfisca_france_indirect_taxation.utils import assets_directory

def new_guess_coicop_from_bdf(year):
    file_path = os.path.join(
        assets_directory,
        'legislation',
        'Table_bdf.xls',
        )

    table_bdf = pd.read_excel(file_path, skiprows=3)

    table_bdf.drop('Code sur\n2, 3, 4 positions', axis = 1,  inplace = True)
    table_bdf.rename(columns= {"Code sur 5 positions" : 'code_bdf' , 'Rubriques' : 'Label'}, inplace = True)
    table_bdf.dropna(axis = 0, inplace = True)
    table_bdf.loc[:,'code_bdf'] = table_bdf.loc[:,'code_bdf'].astype(int).astype(str).str.zfill(5)
    table_bdf.loc[:,'formatted_code_bdf'] = table_bdf.loc[:,'code_bdf'].apply(lambda x : ".".join([x[:2], x[2:3], x[3:4], x[4:]]))
    table_bdf.loc[:,'code_bdf'] = table_bdf.loc[:,'code_bdf'].apply(lambda x : 'c' + x)
    return(table_bdf)

adjust_to_cn_nomenclature = {
    '01.2.2.3' : '01.2.1.1' , #Jus de fruits, sirops, boissons aromatisées
    '01.2.2.4' : '01.2.1.2' , #Jus de légumes
    '01.2.1.1' : '01.2.2.1' , #Café
    '01.2.1.2' : '01.2.3.1' , #Thé et plantes à infusion
    '01.2.2.1' : '01.2.5.1' , #Eaux minérales
    '01.2.2.2' : '01.2.6.1' , #Boissons gazeuses
    '01.2.1.3' : '01.2.9.1' , #Cacao et chocolat en poudre
    '02.1.2.2' : '02.1.9.1' , #Autres apéritifs à base de vin, champagne et autres mousseux
    '02.2.1.1' : '02.3.1.1' , #Cigarettes
    '02.2.1.2' : '02.3.1.2' , #Cigares et cigarillos
    '02.2.1.3' : '02.3.1.3' , #Tabac sous d’autres formes et produits connexes
    '02.3.1.1' : '02.4.1.1' , #Stupéfiants
    '02.4.1.1' : '02.5.1.1' , #Dépenses de boissons alcoolisées, tabac et stupéfiants : cadeau offert à un autre ménage
    '04.4.3.1' : '04.4.1.1' , #Factures d’eau résidence principale, autre logement, dépendance, terrain
    '04.4.1.1' : '04.4.2.1' , #Enlèvement des ordures : Redevance ordures ménagères
    '04.4.2.1' : '04.4.3.1' , #Assainissement
    '04.4.4.1' : '04.4.4.1' , #Charges collectives relatives au logement (payées isolément du loyer ou crédits
    '05.5.1.3' : '05.5.3.1' , #Réparation du gros outillage
    '05.5.2.3' : '05.5.3.2' , #Réparation des petits outillages
    '08.1.1.1' : '07.4.1.1' , #Services postaux
    '07.3.6.1' : '07.4.9.1' , #Autres services de transports
    '07.4.1.1' : '07.5.1.1' , #Autres dépenses de transport : cérémonie, séjours hors domicile, personnes vivant hors du domicile au moins un jour par semaine
    '07.4.1.2' : '07.5.1.2' , #Autres dépenses de transport : cadeau offert (à destination d’un autre ménage)
    '08.1.3.1' : '08.3.1.1' , #Services de téléphone, internet, recharges téléphoniques
    '08.1.4.1' : '08.4.1.1' , #Autres dépenses de communications : cadeau offert (à destination d'un autre ménage)
    '09.1.1.1' : '09.1.2.1' , #Appareils de réception, d’enregistrement et de reproduction du son
    '09.1.1.2' : '09.1.2.2' , #Téléviseurs, home cinéma, lecteur DVD de salon et portables
    '09.1.2.1' : '09.1.1.1' , #Equipement photographique et cinématographique
    '09.1.2.2' : '09.1.1.2' , #Instruments d'optique
    '09.1.3.1' : '08.1.1.1' , #Micro-ordinateurs, matériels et accessoires informatiques, consommables
    '09.1.4.1' : '09.5.2.1' , #Supports vierges ou enregistrés pour l’image et le son
    '09.1.5.1' : '09.4.1.1' , #Réparation des équipements et accessoires audiovisuels, photographiques et informatiques
    '09.2.1.1' : '09.2.2.1' , #Gros équipements pour les loisirs de plein air et les sports
    '09.2.2.1' : '09.5.1.1' , #Instruments de musique et accessoires
    '09.2.2.2' : '09.1.2.3' , #Gros équipements pour les loisirs d’intérieur
    '09.2.3.1' : '09.4.2.1' , #Réparation et entretien de biens durables pour les loisirs, les sports et la culture
    '09.3.1.1' : '09.2.1.1' , #Jeux, jouets et passe temps
    '09.3.1.2' : '09.2.2.2' , #Equipements de sport, de camping et de loisirs en plein air (pêche, chasse, ustensiles et vêtements spéciaux, matériel de camping)
    '09.3.2.1' : '09.3.1.1' , #Horticulture, accessoires et frais de livraison
    '09.3.3.1' : '09.3.2.1' , #Animaux d’agrément
    '09.3.4.1' : '09.3.2.2' , #Aliments autres animaux
    '09.4.1.1' : '09.4.2.2' , #Services sportifs et récréatifs (spectacles sportifs, participation loisirs, location matériel, cours et cotisations de loisirs, abonnement jeu vidéo... )
    '09.4.2.1' : '09.6.1.1' , #Cinémas, théâtres, salles de concert
    '09.4.2.2' : '09.6.1.2' , #Musées, jardins zoologiques et similaires
    '09.4.2.3' : '09.6.9.1' , #Services de télévision et de radiodiffusion (location, redevance, abonnement)
    '09.4.2.4' : '09.6.3.1' , #Smartbox et autres services de loisirs (animateurs, photographes, services pour animaux)
    '09.4.3.1' : '09.4.7.1' , #Jeux de hasard (loto, tiercé ...)
    '09.5.1.1' : '09.7.1.1' , #Livres
    '09.5.2.1' : '09.7.2.1' , #Journaux et périodiques
    '09.5.3.1' : '09.7.3.1' , #Imprimés divers
    '09.5.4.1' : '09.7.4.1' , #Articles de papéterie et de dessin
    '09.6.1.1' : '09.8.1.1' , #Voyages à forfait, week-end, excursions... yc voyage scolaire
    '09.7.1.1' : '09.9.1.1' , #Autres dépenses des loisirs : séjours hors domicile, personnes vivant hors du domicile au moins un jour par semaine
    '09.7.1.2' : '09.9.1.2' , #Autres dépenses de loisirs et culture : cadeau offert (à destination d’un autre ménage)
    '10.1.2.1' : '10.2.1.1' , #Enseignement secondaire
    '10.1.3.1' : '10.4.1.1' , #Enseignement supérieur
    '10.1.4.1' : '10.5.1.1' , #Enseignement ne correspondant à aucun niveau particulier
    '10.1.5.1' : '10.6.1.1' , #Autres dépenses d’enseignement : personnes vivant hors du domicile au moins un jour par semaine
    '10.1.5.2' : '10.6.1.2' , #Autres dépenses d’enseignement : cadeau offert (à destination d’un autre ménage)
    '12.1.1.1' : '13.1.3.1' , #Salons de coiffure et esthétique corporelle (yc cures thermales, tatouages, piercings)
    '12.1.3.1' : '13.1.3.2' , #Services des soins personnels (services des prostituées)
    '12.1.2.1' : '13.1.1.1' , #Appareils électriques pour les soins personnels
    '12.1.2.2' : '13.1.2.1' , #Autres articles et produits pour les soins personnels
    '12.3.1.1' : '13.2.1.1' , #Articles de bijouterie, de joaillerie et d’horlogerie
    '12.3.2.1' : '13.2.9.1' , #Articles de voyage et autres contenants d'effets personnels
    '12.3.2.2' : '13.2.9.2' , #Autres effets personnels
    '12.5.1.1' : '12.1.1.1' , #Assurances vie, décès
    '12.5.2.1' : '12.1.3.1' , #Assurances liées au logement
    '12.5.3.1' : '12.1.2.1' , #Assurances liées à la santé
    '12.5.4.1' : '12.1.4.1' , #Assurances liées aux transports
    '12.5.5.1' : '12.1.9.1' , #Autres assurances
    '12.6.1.1' : '12.2.1.1' , #Services financiers
    '12.4.1.1' : '13.3.1.1' , #Services de protection sociale (assistante maternelle, crèche, maison de retraite)
    '12.7.1.1' : '13.9.1.1' , #Autres servies
    '12.7.1.2' : '13.9.1.2' , #Caution pour la location d'un logement
    '13.1.1.1' : '17.1.1.1' , #Impôts et taxes de la résidence principale
    '13.1.2.1' : '17.1.2.1' , #Impôts et taxes pour une résidence secondaire ou un autre logement
    '13.1.4.1' : '17.1.3.1' , #Impôts sur le revenu
    '13.1.5.1' : '17.1.5.1' , #Taxes automobiles
    '13.1.6.1' : '17.1.6.1' , #Autres impôts et taxes
    '13.2.1.1' : '17.2.1.1' , #Remboursements de prêts pour la résidence principale
    '13.2.2.1' : '17.2.2.1' , #Remboursements des autres prêts immobiliers
    '13.3.1.1' : '17.3.1.1' , #Aides et dons en argent offerts par le ménage et pensions
    '13.4.1.1' : '17.4.1.1' , #Gros travaux pour la résidence principale
    '13.4.2.1' : '17.4.2.1' , #Gros travaux pour une résidence secondaire ou un autre logement
    '13.5.1.1' : '17.5.1.1' , #Remboursements de crédits à la consommation
    '13.6.1.1' : '17.6.1.1' , #Prélèvements de l'employeur
    '13.7.1.1' : '17.7.1.1' , #Achats de logements, garages, parkings, box et terrains
    '13.7.2.2' : '17.7.2.2' , #Epargne salariale
    '14.1.1.1' : '18.1.1.1' , #Allocations logement reçues par le ménage
}

def new_bdf(year = 2017):
    coicop_table_bdf = new_guess_coicop_from_bdf(year)
    bdf_to_cn_dataframe = pd.DataFrame(list(adjust_to_cn_nomenclature.items()), columns = ['formatted_code_bdf' , 'code_coicop'])
    coicop_table_bdf = coicop_table_bdf.merge(bdf_to_cn_dataframe, on = 'formatted_code_bdf', how ='outer')
    coicop_table_bdf['code_coicop'].fillna(coicop_table_bdf['formatted_code_bdf'], inplace = True)

    return(coicop_table_bdf)