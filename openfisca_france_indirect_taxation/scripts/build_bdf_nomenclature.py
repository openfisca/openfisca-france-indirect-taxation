import pandas as pd
import os

from openfisca_france_indirect_taxation.utils import assets_directory


def build_raw_bdf_nomenclature(year = 2017):
    """Build the raw BDF nomenclature DataFrame from the Excel file of BDF 2017 nomenclature.

    Returns:
        pd.DataFrame: A DataFrame containing the complete BDF nomenclature with
                      columns for division, group, class, and subclass labels
                      and codes.
    """
    assert year == 2017  # Currently only implemented for 2017

    file_path = os.path.join(
        assets_directory,
        'legislation',
        'Table_bdf.xls',
        )

    table_bdf = pd.read_excel(file_path, skiprows=3)

    # Get divisions
    table_bdf['Division'] = table_bdf['Code sur\n2, 3, 4 positions'].str.endswith('***')
    bdf_division = table_bdf.loc[table_bdf['Division'], ['Code sur\n2, 3, 4 positions', 'Rubriques']]
    bdf_division.rename(columns={'Code sur\n2, 3, 4 positions': 'Code_division', 'Rubriques': 'Label_division'}, inplace=True)
    bdf_division['Label_division'] = bdf_division['Label_division'].str.lower()
    bdf_division['Code_division'] = bdf_division['Code_division'].str.replace(r'\*', '', regex=True)
    table_bdf.drop(table_bdf[table_bdf['Division']].index, inplace=True)

    # Get groups
    table_bdf['Groupe'] = table_bdf['Code sur\n2, 3, 4 positions'].str.endswith('**')
    bdf_groupe = table_bdf.loc[table_bdf['Groupe'], ['Code sur\n2, 3, 4 positions', 'Rubriques']]
    bdf_groupe.rename(columns={'Code sur\n2, 3, 4 positions': 'Code_groupe', 'Rubriques': 'Label_groupe'}, inplace=True)
    bdf_groupe['Label_groupe'] = bdf_groupe['Label_groupe'].str.lower()
    bdf_groupe['Code_groupe'] = bdf_groupe['Code_groupe'].str.replace(r'\*', '', regex=True)
    table_bdf.drop(table_bdf[table_bdf['Groupe']].index, inplace=True)

    # Get classes
    table_bdf.loc[:, 'Classe'] = table_bdf.loc[:, 'Code sur\n2, 3, 4 positions'].str.endswith('*')
    bdf_classe = table_bdf.loc[table_bdf['Classe'], ['Code sur\n2, 3, 4 positions', 'Rubriques']]
    bdf_classe.rename(columns={'Code sur\n2, 3, 4 positions': 'Code_classe', 'Rubriques': 'Label_classe'}, inplace=True)
    bdf_classe.loc[:, 'Label_classe'] = bdf_classe.loc[:, 'Label_classe'].str.lower()
    bdf_classe.loc[:, 'Code_classe'] = bdf_classe.loc[:, 'Code_classe'].str.replace(r'\*', '', regex=True)

    table_bdf.drop(table_bdf[table_bdf['Classe']].index, inplace=True)
    table_bdf.drop(columns=['Code sur\n2, 3, 4 positions', 'Division', 'Groupe', 'Classe'], axis= 1, inplace=True)
    table_bdf.drop(table_bdf[table_bdf['Code sur 5 positions'].isna()].index, axis = 0, inplace = True)

    table_bdf.loc[:, 'Code_sous_classe'] = table_bdf.loc[:, 'Code sur 5 positions'].astype(int).astype(str).str.zfill(5)

    # Extract first two digits for the division, the first three for the group, the first four for the class
    table_bdf.loc[:, 'Code_division'] = table_bdf.loc[:, 'Code_sous_classe'].str[:2]
    table_bdf.loc[:, 'Code_groupe'] = table_bdf.loc[:, 'Code_sous_classe'].str[:3]
    table_bdf.loc[:, 'Code_classe'] = table_bdf.loc[:, 'Code_sous_classe'].str[:4]

    table_bdf.drop(columns=['Code sur 5 positions'], axis= 1, inplace=True)

    # Merge with the tables of divisions, groups and classes extracted above
    table_bdf = table_bdf.merge(bdf_division, on='Code_division', how='left')
    table_bdf = table_bdf.merge(bdf_groupe, on='Code_groupe', how='left')
    table_bdf = table_bdf.merge(bdf_classe, on='Code_classe', how='left')

    table_bdf.rename(columns={'Rubriques': 'Label_sous_classe'}, inplace=True)
    bdf_nomenclature = table_bdf.loc[:, ['Label_division', 'Label_groupe', 'Label_classe', 'Label_sous_classe', 'Code_sous_classe']]
    bdf_nomenclature.loc[:, 'code_coicop'] = bdf_nomenclature.loc[:, 'Code_sous_classe'].apply(lambda x: ".".join([x[:2], x[2:3], x[3:4], x[4:]]))

    return bdf_nomenclature


# A dictionnary used to adjust some BDF codes to match the CN nomenclature
adjust_to_cn_nomenclature = {
    '01.2.2.3': '01.2.1.1',     # Jus de fruits, sirops, boissons aromatisées
    '01.2.2.4': '01.2.1.2',     # Jus de légumes
    '01.2.1.1': '01.2.2.1',     # Café
    '01.2.1.2': '01.2.3.1',     # Thé et plantes à infusion
    '01.2.2.1': '01.2.5.1',     # Eaux minérales
    '01.2.2.2': '01.2.6.1',     # Boissons gazeuses
    '01.2.1.3': '01.2.9.1',     # Cacao et chocolat en poudre
    '02.1.2.2': '02.1.9.1',     # Autres apéritifs à base de vin, champagne et autres mousseux
    '02.2.1.1': '02.3.1.1',     # Cigarettes
    '02.2.1.2': '02.3.1.2',     # Cigares et cigarillos
    '02.2.1.3': '02.3.1.3',     # Tabac sous d’autres formes et produits connexes
    '02.3.1.1': '02.4.1.1',     # Stupéfiants
    '02.4.1.1': '02.5.1.1',     # Dépenses de boissons alcoolisées, tabac et stupéfiants : cadeau offert à un autre ménage
    '04.4.3.1': '04.4.1.1',     # Factures d’eau résidence principale, autre logement, dépendance, terrain
    '04.4.1.1': '04.4.2.1',     # Enlèvement des ordures : Redevance ordures ménagères
    '04.4.2.1': '04.4.3.1',     # Assainissement
    '04.4.4.1': '04.4.4.1',     # Charges collectives relatives au logement (payées isolément du loyer ou crédits
    '05.5.1.3': '05.5.3.1',     # Réparation du gros outillage
    '05.5.2.3': '05.5.3.2',     # Réparation des petits outillages
    '08.1.1.1': '07.4.1.1',     # Services postaux
    '07.3.6.1': '07.4.9.1',     # Autres services de transports
    '07.4.1.1': '07.5.1.1',     # Autres dépenses de transport : cérémonie, séjours hors domicile, personnes vivant hors du domicile au moins un jour par semaine
    '07.4.1.2': '07.5.1.2',     # Autres dépenses de transport : cadeau offert (à destination d’un autre ménage)
    '08.1.3.1': '08.3.1.1',     # Services de téléphone, internet, recharges téléphoniques
    '08.1.4.1': '08.4.1.1',     # Autres dépenses de communications : cadeau offert (à destination d'un autre ménage)
    '09.1.1.1': '09.1.2.1',     # Appareils de réception, d’enregistrement et de reproduction du son
    '09.1.1.2': '09.1.2.2',     # Téléviseurs, home cinéma, lecteur DVD de salon et portables
    '09.1.2.1': '09.1.1.1',     # Equipement photographique et cinématographique
    '09.1.2.2': '09.1.1.2',     # Instruments d'optique
    '09.1.3.1': '08.1.1.1',     # Micro-ordinateurs, matériels et accessoires informatiques, consommables
    '09.1.4.1': '09.5.2.1',     # Supports vierges ou enregistrés pour l’image et le son
    '09.1.5.1': '09.4.1.1',     # Réparation des équipements et accessoires audiovisuels, photographiques et informatiques
    '09.2.1.1': '09.2.2.1',     # Gros équipements pour les loisirs de plein air et les sports
    '09.2.2.1': '09.5.1.1',     # Instruments de musique et accessoires
    '09.2.2.2': '09.1.2.3',     # Gros équipements pour les loisirs d’intérieur
    '09.2.3.1': '09.4.2.1',     # Réparation et entretien de biens durables pour les loisirs, les sports et la culture
    '09.3.1.1': '09.2.1.1',     # Jeux, jouets et passe temps
    '09.3.1.2': '09.2.2.2',     # Equipements de sport, de camping et de loisirs en plein air (pêche, chasse, ustensiles et vêtements spéciaux, matériel de camping)
    '09.3.2.1': '09.3.1.1',     # Horticulture, accessoires et frais de livraison
    '09.3.3.1': '09.3.2.1',     # Animaux d’agrément
    '09.3.4.1': '09.3.2.2',     # Aliments autres animaux
    '09.4.1.1': '09.4.2.2',     # Services sportifs et récréatifs (spectacles sportifs, participation loisirs, location matériel, cours et cotisations de loisirs, abonnement jeu vidéo... )
    '09.4.2.1': '09.6.1.1',     # Cinémas, théâtres, salles de concert
    '09.4.2.2': '09.6.1.2',     # Musées, jardins zoologiques et similaires
    '09.4.2.3': '09.6.9.1',     # Services de télévision et de radiodiffusion (location, redevance, abonnement)
    '09.4.2.4': '09.6.3.1',     # Smartbox et autres services de loisirs (animateurs, photographes, services pour animaux)
    '09.4.3.1': '09.4.7.1',     # Jeux de hasard (loto, tiercé ...)
    '09.5.1.1': '09.7.1.1',     # Livres
    '09.5.2.1': '09.7.2.1',     # Journaux et périodiques
    '09.5.3.1': '09.7.3.1',     # Imprimés divers
    '09.5.4.1': '09.7.4.1',     # Articles de papéterie et de dessin
    '09.6.1.1': '09.8.1.1',     # Voyages à forfait, week-end, excursions... yc voyage scolaire
    '09.7.1.1': '09.9.1.1',     # Autres dépenses des loisirs : séjours hors domicile, personnes vivant hors du domicile au moins un jour par semaine
    '09.7.1.2': '09.9.1.2',     # Autres dépenses de loisirs et culture : cadeau offert (à destination d’un autre ménage)
    '10.1.2.1': '10.2.1.1',     # Enseignement secondaire
    '10.1.3.1': '10.4.1.1',     # Enseignement supérieur
    '10.1.4.1': '10.5.1.1',     # Enseignement ne correspondant à aucun niveau particulier
    '10.1.5.1': '10.6.1.1',     # Autres dépenses d’enseignement : personnes vivant hors du domicile au moins un jour par semaine
    '10.1.5.2': '10.6.1.2',     # Autres dépenses d’enseignement : cadeau offert (à destination d’un autre ménage)
    '12.1.1.1': '13.1.3.1',     # Salons de coiffure et esthétique corporelle (yc cures thermales, tatouages, piercings)
    '12.1.3.1': '13.1.3.2',     # Services des soins personnels (services des prostituées)
    '12.1.2.1': '13.1.1.1',     # Appareils électriques pour les soins personnels
    '12.1.2.2': '13.1.2.1',     # Autres articles et produits pour les soins personnels
    '12.3.1.1': '13.2.1.1',     # Articles de bijouterie, de joaillerie et d’horlogerie
    '12.3.2.1': '13.2.9.1',     # Articles de voyage et autres contenants d'effets personnels
    '12.3.2.2': '13.2.9.2',     # Autres effets personnels
    '12.5.1.1': '12.1.1.1',     # Assurances vie, décès
    '12.5.2.1': '12.1.3.1',     # Assurances liées au logement
    '12.5.3.1': '12.1.2.1',     # Assurances liées à la santé
    '12.5.4.1': '12.1.4.1',     # Assurances liées aux transports
    '12.5.5.1': '12.1.9.1',     # Autres assurances
    '12.6.1.1': '12.2.1.1',     # Services financiers
    '12.4.1.1': '13.3.1.1',     # Services de protection sociale (assistante maternelle, crèche, maison de retraite)
    '12.7.1.1': '13.9.1.1',     # Autres servies
    '12.7.1.2': '13.9.1.2',     # Caution pour la location d'un logement
    '13.1.1.1': '17.1.1.1',     # Impôts et taxes de la résidence principale
    '13.1.2.1': '17.1.2.1',     # Impôts et taxes pour une résidence secondaire ou un autre logement
    '13.1.4.1': '17.1.3.1',     # Impôts sur le revenu
    '13.1.5.1': '17.1.5.1',     # Taxes automobiles
    '13.1.6.1': '17.1.6.1',     # Autres impôts et taxes
    '13.2.1.1': '17.2.1.1',     # Remboursements de prêts pour la résidence principale
    '13.2.2.1': '17.2.2.1',     # Remboursements des autres prêts immobiliers
    '13.3.1.1': '17.3.1.1',     # Aides et dons en argent offerts par le ménage et pensions
    '13.4.1.1': '17.4.1.1',     # Gros travaux pour la résidence principale
    '13.4.2.1': '17.4.2.1',     # Gros travaux pour une résidence secondaire ou un autre logement
    '13.5.1.1': '17.5.1.1',     # Remboursements de crédits à la consommation
    '13.6.1.1': '17.6.1.1',     # Prélèvements de l'employeur
    '13.7.1.1': '17.7.1.1',     # Achats de logements, garages, parkings, box et terrains
    '13.7.2.2': '17.7.2.2',     # Epargne salariale
    '14.1.1.1': '18.1.1.1',     # Allocatons logement reçues par le ménage
    }


def build_complete_bdf_nomenclature(year = 2017, to_csv=True):
    """Build the complete BDF nomenclature DataFrame from the Excel file of BDF 2017 nomenclature and the dict to adjust to the national accounts.

    Returns:
        pd.DataFrame: A DataFrame containing the complete BDF nomenclature with
                      columns for division, group, class, and subclass labels
                      intial BDF codes and adjusted ones.
    """
    bdf_nomenclature = build_raw_bdf_nomenclature(year = 2017)
    bdf_to_cn_dataframe = pd.DataFrame(list(adjust_to_cn_nomenclature.items()), columns = ['code_coicop', 'adjusted_bdf'])
    bdf_nomenclature = bdf_nomenclature.merge(bdf_to_cn_dataframe, on = 'code_coicop', how ='outer')
    bdf_nomenclature.loc[:, 'adjusted_bdf'] = bdf_nomenclature.loc[:, 'adjusted_bdf'].fillna(bdf_nomenclature.loc[:, 'code_coicop'])

    # Optionally save to CSV
    if to_csv:
        output_path = os.path.join(
            assets_directory,
            'legislation',
            f'bdf_{year}_nomenclature.csv'
            )
        bdf_nomenclature.to_csv(output_path, index=False)

    return bdf_nomenclature


if __name__ == '__main__':
    bdf_nomenclature = build_complete_bdf_nomenclature(year = 2017, to_csv = True)
    print(bdf_nomenclature.dtypes)
