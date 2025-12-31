import pandas as pd
import os

from openfisca_france_indirect_taxation.utils import assets_directory

from openfisca_france_indirect_taxation.scripts.new_build_coicop_legislation import new_apply_modification
from openfisca_france_indirect_taxation.scripts import build_bdf_nomenclature


legislation_directory = os.path.join(assets_directory, 'legislation')
bdf_nomenclature = pd.read_csv(
    os.path.join(legislation_directory, 'bdf_2017_nomenclature.csv')
    )


def add_fiscal_categories_to_bdf_nomenclature(bdf_nomenclature, to_csv=False):
    """
    Ajoute des catégories fiscales au DataFrame bdf_nomenclature en fonction de règles spécifiques
    pour chaque code coicop. Les règles incluent des périodes de validité (start, stop) et des origines.

    Args:
        bdf_nomenclature (pd.DataFrame): DataFrame contenant les codes coicop.
        to_csv (bool): Si True, sauvegarde le résultat dans un fichier CSV.

    Returns:
        pd.DataFrame: DataFrame mis à jour avec les catégories fiscales.
    """
    # Ajoute les colonnes nécessaires si elles n'existent pas
    for col in ['start', 'stop', 'origin']:
        if col not in bdf_nomenclature.columns:
            bdf_nomenclature[col] = 0
    bdf_nomenclature['origin'] = 'BDF'

    # Définition des règles fiscales pour chaque code BDF
    fiscal_rules = [
        # 01 Produits alimentaires et boissons non alcoolisées
        {'value': '01', 'categorie_fiscale': 'tva_taux_reduit'},
        {'value': '01.1.5.2', 'categorie_fiscale': 'tva_taux_plein'},                         # Margarine
        {'value': '01.1.5.5', 'categorie_fiscale': 'tva_taux_reduit', 'origin': 'TAXIPP'},    # Saindoux autres graisses d'origine animale    
        {'value': '01.1.8.4', 'categorie_fiscale': 'tva_taux_plein'},                         # Confiserie (hors cocolats)

        # 02 Boissons alcoolisées et tabac
        {'value': '02.1.1', 'categorie_fiscale': 'alcools_forts'},
        {'value': '02.1.2', 'categorie_fiscale': 'vin'},                                        # Vins
        {'value': '02.1.3', 'categorie_fiscale': 'biere'},                                      # Bières
        {'value': '02.2.1.1', 'categorie_fiscale': 'cigarettes', 'origin': 'TAXIPP'},           # Cigarettes
        {'value': '02.2.1.2', 'categorie_fiscale': 'cigares', 'origin': 'TAXIPP'},              # Cigares et cigarillos
        {'value': '02.2.1.3', 'categorie_fiscale': 'tabac_a_rouler', 'origin': 'TAXIPP'},       # Tabac à rouler
        {'value': '02.3', 'categorie_fiscale': '', 'origin': 'COICOP UN'},                      # Stupéfiants
        {'value': '02.4', 'categorie_fiscale': '', 'origin': 'TAXIPP'},                         # Alcools, tabacs et stupéfiants offerts à un autre

        # 03 Habillement et chaussures
        {'value': '03', 'categorie_fiscale': 'tva_taux_plein'},

        # 04 Logement, eau, gaz, électricité et autres combustibles
        {'value': '04', 'categorie_fiscale': 'tva_taux_plein'},
        {'value': '04.5.4.1', 'categorie_fiscale': 'tva_taux_reduit', 'start': 1998, 'stop': 2011},                     # Combustible solide de résidence principale
        {'value': '04.5.4.1', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': ['04.4.1.1', '04.4.2.1', '04.4.3.1'], 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},          # Enlèvement des ordures ménagères, assainissement et distribution d'eau,
        # qui sont au taux réduit de 1994 à 2011
        {'value': ['04.4.1.1', '04.4.2.1'], 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},              # avant de passer au taux intermédiaire
        {'value': '04.4.3.1', 'categorie_fiscale': 'tva_taux_reduit', 'start': 2012},                                   # sauf l'eau qui reste à taux réduit                             
        {'value': ['04.1.1.1', '04.1.2.1'], 'categorie_fiscale': ''},                                                   # Loyers et charges locatives
        {'value': '04.3.2.1', 'categorie_fiscale': 'tva_taux_intermediaire'},                                           # Services d'entretien et réparation de logements

        # 05 Ameublement, équipement ménager et entretien courant de la maison
        {'value': '05', 'categorie_fiscale': 'tva_taux_plein'},
        {'value': '05.6.2.1', 'categorie_fiscale': 'tva_taux_intermediaire'},                                           # Services domestiques (ménage, garde enfant, jardinage)

        # 06 Santé
        {'value': '06', 'categorie_fiscale': ''},
        {'value': '06.1.1.1', 'categorie_fiscale': 'tva_taux_super_reduit'},                                            # Pharmacie
        {'value': '06.1.1.2', 'categorie_fiscale': 'tva_taux_plein'},                                                   # Parapharmacie                
        {'value': '06.1.1.3', 'categorie_fiscale': 'tva_taux_reduit'},                                                  # Matériel thérapeutique

        # 07 Transports
        {'value': '07', 'categorie_fiscale': 'tva_taux_plein'},
        {'value': '07.2.2', 'categorie_fiscale': 'ticpe'},                                                              # Carburants et lubrifiants pour véhicules de tourisme
        {'value': '07.3.1', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},                                      # Transport ferroviaire de passagers  
        {'value': '07.3.1', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '07.3.2', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},                                      # Transport routier de passagers
        {'value': '07.3.2', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '07.3.3', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2024},                                      # Transport aérien de passagers
        {'value': '07.3.3', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '07.3.4', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},                                      # Transport maritime et fluvial de passagers
        {'value': '07.3.4', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '07.3.5', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},                                      # Transport combine de passagers
        {'value': '07.3.5', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '07.3.6', 'categorie_fiscale': 'tva_taux_plein'},                                                 # Autres services de transports (yc déménagements)
        # 08 Communications
        {'value': '08', 'categorie_fiscale': 'tva_taux_plein'},
        {'value': '08.1.1.1', 'categorie_fiscale': ''},                                                                # Services postaux

        # 09 Loisirs et culture
        {'value': '09', 'categorie_fiscale': 'tva_taux_plein'},
        {'value': '09.3.1.2', 'categorie_fiscale': 'tva_taux_plein', 'start': 1994},                                   # equipement sportif
        {'value': '09.3.2.1', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2016},                           # Horticulture, floriculture
        {'value': '09.4.1', 'categorie_fiscale': 'tva_taux_reduit', 'start': 1994},                                    # Services récréatifs et sportifs
        {'value': '09.4.1', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2015},
        {'value': '09.4.2.1', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},                                   # Cinemas, théâtres, concerts
        {'value': '09.4.2.1', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012, 'stop': 2013},
        {'value': '09.4.2.1', 'categorie_fiscale': 'tva_taux_reduit', 'start': 2014},
        {'value': '09.4.2.2', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},                                   # Musées, zoos
        {'value': '09.4.2.2', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '09.4.2.2', 'categorie_fiscale': 'tva_taux_reduit', 'start': 2018},
        {'value': '09.4.2.3', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},                                   # Services de télévision et radiodiffusion
        {'value': '09.4.2.3', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '09.4.2.4', 'categorie_fiscale': 'tva_taux_plein', 'start': 1994},                                   # Autres services culturels.
        {'value': '09.4.3', 'categorie_fiscale': '', 'origin': 'COICOP UN'},                                           # Jeux de hasard
        {'value': '09.5.1', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2024},                                     # Livre
        {'value': '09.5.2', 'categorie_fiscale': 'tva_taux_super_reduit'},                                             # Journaux et publications périodiques
        {'value': '09.6.1.1', 'categorie_fiscale': '', 'start': 2019},                                                 # Voyage à forfait

        # 10 Éducation
        {'value': '10', 'categorie_fiscale': ''},

        # 11 Hôtellerie restauration
        {'value': '11', 'categorie_fiscale': 'tva_taux_reduit'},
        {'value': '11.1.1.1', 'categorie_fiscale': 'tva_taux_plein', 'stop': 2009},                                   # Restauration  (hors boissons alcoolisées)
        {'value': '11.1.1.1', 'categorie_fiscale': 'tva_taux_reduit', 'start': 2010, 'stop': 2011},
        {'value': '11.1.1.1', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '11.1.1.2', 'categorie_fiscale': 'tva_taux_plein'},                                                 # Boissons alcoolisées (cafés, bars et assimilés)
        {'value': '11.1.2', 'categorie_fiscale': 'tva_taux_reduit'},                                                  # Restauration collective
        {'value': '11.2.1', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},                            # Hébergement touristique   

        # 12 Autres biens et services
        {'value': '12', 'categorie_fiscale': 'tva_taux_plein'},
        {'value': '12.1.3.1', 'categorie_fiscale': '', 'origin': 'COICOP UN'},                                              # Prostitution
        {'value': '12.4', 'categorie_fiscale': 'tva_taux_reduit', 'start': 2000, 'stop': 2024},                         # Protection sociale
        {'value': '12.4', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '12.5.1', 'categorie_fiscale': 'autres_assurances', 'origin': 'COICOP UN'},                           # Assurance vie
        {'value': '12.5.2', 'categorie_fiscale': 'autres_assurances'},                                                  # Autres assurances
        {'value': '12.5.3', 'categorie_fiscale': 'assurance_sante'},                                                    # Assurance santé
        {'value': '12.5.4', 'categorie_fiscale': 'assurance_transport'},                                                # Assurance transport
        {'value': '12.5.5', 'categorie_fiscale': 'autres_assurances', 'origin': 'COICOP UN'},                           # Autres assurances
        {'value': '12.6', 'categorie_fiscale': ''},                                                                     # Services financiers  
        
        # 13 Impôts et taxes, gros travaux, remboursement pret, cadeaux, prelevement employeur, epargne
        {'value': '13', 'categorie_fiscale': ''},
        # 14 Allocations logement recues par le menage
        {'value': '14', 'categorie_fiscale': ''}]

    # Applique chaque règle fiscale
    for rule in fiscal_rules:
        value = rule.get('value')
        if isinstance(value, list):
            # Si 'value' est une liste, applique la règle à chaque code individuellement
            for single_value in value:
                single_rule = rule.copy()
                single_rule['value'] = single_value
                bdf_nomenclature = new_apply_modification(bdf_nomenclature, **single_rule)
        else:
            # Sinon, applique la règle normalement
            bdf_nomenclature = new_apply_modification(bdf_nomenclature, **rule)

    # Sauvegarde le résultat dans un fichier CSV si demandé
    if to_csv:
        output_path = os.path.join(legislation_directory, 'bdf_2017_legislation.csv')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)        # Crée le répertoire s'il n'existe pas
        bdf_nomenclature.to_csv(output_path, index=False)

    return bdf_nomenclature


def test_bdf_legislation():
    bdf_nomenclature = build_bdf_nomenclature.build_complete_bdf_nomenclature()
    bdf_legislation = add_fiscal_categories_to_bdf_nomenclature(bdf_nomenclature, to_csv = True)
    if bdf_legislation.categorie_fiscale.isnull().any():
        return bdf_legislation.loc[bdf_legislation.categorie_fiscale.isnull()]


if __name__ == '__main__':
    bdf_nomenclature = build_bdf_nomenclature.build_complete_bdf_nomenclature()
    bdf_legislation = add_fiscal_categories_to_bdf_nomenclature(bdf_nomenclature, to_csv = True)
    test_bdf_legislation()
