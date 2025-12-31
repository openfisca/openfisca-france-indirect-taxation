# import numpy as np
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


def _handle_overlap_start(df, overlap_selection, start, stop, categorie_fiscale):
    """Gère le chevauchement au début de l'intervalle."""
    # Découpe l'intervalle existant
    df.loc[overlap_selection, 'start'] = stop + 1
    # Ajoute une nouvelle ligne pour le nouvel intervalle
    new_row = df.loc[overlap_selection].copy()
    new_row[['categorie_fiscale', 'start', 'stop']] = categorie_fiscale, start, stop
    df = pd.concat([df, new_row], ignore_index=True)
    df.sort_values(by=['code_coicop', 'start'], inplace=True)
    return df


def _handle_overlap_stop(df, overlap_selection, start, stop, categorie_fiscale):
    """Gère le chevauchement à la fin de l'intervalle."""
    # Découpe l'intervalle existant
    df.loc[overlap_selection, 'stop'] = start - 1
    # Ajoute une nouvelle ligne pour le nouvel intervalle
    new_row = df.loc[overlap_selection].copy()
    new_row[['categorie_fiscale', 'start', 'stop']] = categorie_fiscale, start, stop
    df = pd.concat([df, new_row], ignore_index=True)
    df.sort_values(by=['code_coicop', 'start'], inplace=True)
    return df


def _handle_overlap_middle(df, overlap_selection, start, stop, categorie_fiscale):
    """Gère le chevauchement au milieu de l'intervalle."""
    # Découpe en trois parties
    lower_part = df.loc[overlap_selection].copy()
    lower_part['stop'] = start - 1
    upper_part = df.loc[overlap_selection].copy()
    upper_part['start'] = stop + 1
    # Met à jour la partie centrale
    df.loc[overlap_selection, ['categorie_fiscale', 'start', 'stop']] = categorie_fiscale, start, stop
    # Ajoute les parties inférieure et supérieure
    df = pd.concat([df, lower_part, upper_part], ignore_index=True)
    df.sort_values(by='code_coicop', inplace=True)
    return df


def new_apply_modification(coicop_nomenclature= None,
        value= None,
        categorie_fiscale= None,
        origin= None,
        start= 1994,
        stop= 2024):
 
    """
    Modifie ou ajoute une entrée dans le DataFrame coicop_nomenclature pour un code COICOP donné,
    une catégorie fiscale, et un intervalle de temps [start, stop].

    Args:
        coicop_nomenclature (pd.DataFrame): DataFrame contenant les codes COICOP et leurs métadonnées.
        value (int, str, list): Code COICOP ou liste de codes à modifier.
        categorie_fiscale (str): Catégorie fiscale à appliquer.
        origin (str): Origine de la modification (optionnel).
        start (int): Année de début de l'intervalle.
        stop (int): Année de fin de l'intervalle.

    Returns:
        pd.DataFrame: DataFrame modifié.
    """
    assert coicop_nomenclature is not None, "coicop_nomenclature ne peut pas être None."
    assert categorie_fiscale in list(taxe_by_categorie_fiscale_number.values()), \
        f"Catégorie fiscale invalide: {categorie_fiscale}."
    assert 1994 <= start < stop <= 2024, f"Intervalle invalide: start={start}, stop={stop}."

    # Détermine la sélection en fonction du type de `value`
    if isinstance(value, int):
        prefix = f"{value}."
        selection = coicop_nomenclature['code_coicop'].str.startswith(prefix)
    # Gère les cas où 'value' est une chaîne (code raccourci ou code complet)
    elif isinstance(value, str):
        selection = coicop_nomenclature['code_coicop'].str.startswith(value)
    # Gère les cas où 'value' est une liste de codes
    elif isinstance(value, list):
        selection = coicop_nomenclature['code_coicop'].isin(value)

    else:
        raise ValueError(f"Type de 'value' non supporté : {type(value)}")

    if selection.any():
        # Vérifie si les colonnes 'start' et 'stop' sont déjà remplies
        filled_start_stop = (
            (coicop_nomenclature.loc[selection, 'start'] != 0).any() or
            (coicop_nomenclature.loc[selection, 'stop'] != 0).any()
            )
        if not filled_start_stop:
            # Cas 1: Aucune période définie, on initialise
            coicop_nomenclature.loc[selection, ['start', 'stop', 'categorie_fiscale']] = 1994, 2024, categorie_fiscale
        else:
            #  Vérifie les chevauchements
            equal_start = (coicop_nomenclature['start'] == start)
            equal_stop = (coicop_nomenclature['stop'] == stop)
            
            overlap_selection = selection & (coicop_nomenclature['start'] <= start) & (coicop_nomenclature['stop'] >= stop)

            if overlap_selection.any():
                if (overlap_selection & equal_start & equal_stop).any():
                    # Même intervalle: met à jour la catégorie fiscale
                    coicop_nomenclature.loc[overlap_selection & equal_start & equal_stop, 'categorie_fiscale'] = categorie_fiscale
                    if origin is not None:
                        coicop_nomenclature.loc[overlap_selection & equal_start & equal_stop, 'origin'] = origin
                elif (overlap_selection & equal_start).any():
                    # Chevauchement au début: découpe l'intervalle existant
                    coicop_nomenclature = _handle_overlap_start(coicop_nomenclature, overlap_selection, start, stop, categorie_fiscale)
                elif (overlap_selection & equal_stop).any():
                    # Chevauchement à la fin: découpe l'intervalle existant
                    coicop_nomenclature = _handle_overlap_stop(coicop_nomenclature, overlap_selection, start, stop, categorie_fiscale)
                else:
                    # Chevauchement au milieu: découpe en trois parties
                    coicop_nomenclature = _handle_overlap_middle(coicop_nomenclature, overlap_selection, start, stop, categorie_fiscale)
    else:
        # Pas de lignes existantes, on ajoute simplement une nouvelle entrée
        new_row = pd.DataFrame([{
            'code_coicop': value,
            'categorie_fiscale': categorie_fiscale,
            'start': start,
            'stop': stop,
            'origin': origin
            }])
        coicop_nomenclature = pd.concat([coicop_nomenclature, new_row], ignore_index=True)
        coicop_nomenclature.sort_values(by='code_coicop', inplace=True)

    return coicop_nomenclature


def new_add_fiscal_categories_to_coicop_nomenclature(coicop_nomenclature, to_csv=False):
    """
    Ajoute des catégories fiscales au DataFrame coicop_nomenclature en fonction de règles spécifiques
    pour chaque code COICOP. Les règles incluent des périodes de validité (start, stop) et des origines.

    Args:
        coicop_nomenclature (pd.DataFrame): DataFrame contenant les codes COICOP.
        to_csv (bool): Si True, sauvegarde le résultat dans un fichier CSV.

    Returns:
        pd.DataFrame: DataFrame mis à jour avec les catégories fiscales.
    """
    # Ajoute les colonnes nécessaires si elles n'existent pas
    for col in ['start', 'stop', 'origin']:
        if col not in coicop_nomenclature.columns:
            coicop_nomenclature[col] = 0
    coicop_nomenclature['origin'] = 'ECOICOP 2016'

    # Définition des règles fiscales pour chaque code COICOP
    fiscal_rules = [
        # 1 Produits alimentaires et boissons non alcoolisées
        {'value': 1, 'categorie_fiscale': 'tva_taux_reduit'},
        {'value': '1.1.5.2.1', 'categorie_fiscale': 'tva_taux_plein'},   # Margarine
        # {'value': '1.1.5.2.3', 'categorie_fiscale': 'tva_taux_reduit'}, # Saindoux autres graisses d'origine animale
        {'value': '1.1.8.4.1', 'categorie_fiscale': 'tva_taux_plein'},   # Produits de confiserie (hors chocolat)

        # 2 Boissons alcoolisées et tabac
        {'value': 2, 'categorie_fiscale': ''},
        {'value': '2.1.1', 'categorie_fiscale': 'alcools_forts'},        # Alcools forts
        {'value': '2.1.2', 'categorie_fiscale': 'vin'},                  # Vin
        {'value': '2.1.3', 'categorie_fiscale': 'biere'},                # Bière 
        {'value': '2.2.0.1.1', 'categorie_fiscale': 'cigarettes'},       # Cigarettes
        {'value': '2.2.0.2.1', 'categorie_fiscale': 'cigares'},          # Cigares
        {'value': '2.2.0.3.1', 'categorie_fiscale': 'tabac_a_rouler'},   # Tabac à rouler

        # 03 Habillement et chaussures
        {'value': 3, 'categorie_fiscale': 'tva_taux_plein'},

        # 04 Logement, eau, gaz, électricité et autres combustibles
        {'value': 4, 'categorie_fiscale': 'tva_taux_plein'},
        {'value': ['4.1.', '4.2.'], 'categorie_fiscale': ''},     # Pas de taxation des loyers
        {'value': '4.5.4.1.1', 'categorie_fiscale': 'tva_taux_reduit', 'start': 1998, 'stop': 2011},    # Combustible solide de résidence principale (Ref : Code général des impôts article 278 bis 3bis a b c)
        {'value': '4.5.4.1.1', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},           
        {'value': ['4.4.1.0.1', '4.4.2.0.1', '4.4.3.0.1'], 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},  # Distribution d'eau, enlèvement des ordures ménagères, assainissement, autres services liés au logement n.d.a.
        # qui sont au taux réduit de 1994 à 2011
        {'value': ['4.4.2.0.1', '4.4.3.0.1'], 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},    # Puis au taux intermédiaire à partir de 2012
        {'value': '4.4.1.0.1', 'categorie_fiscale': 'tva_taux_reduit', 'start': 2012},                          # sauf pour la distribution d'eau qui reste au taux réduit
        {'value': '4.3.2.2.1', 'categorie_fiscale': 'tva_taux_intermediaire'},                                  # Services d'entretien et petites réparation dans le logement

        # 05 Ameublement, équipement ménager et entretien courant de la maison
        {'value': 5, 'categorie_fiscale': 'tva_taux_plein'},
        {'value': '5.6.2.1', 'categorie_fiscale': 'tva_taux_intermediaire'},                # Services domestiques (ménage, garde enfant, jardinage)
       
        # 06 Santé
        {'value': 6, 'categorie_fiscale': ''},
        {'value': '6.1.1.0.1', 'categorie_fiscale': 'tva_taux_super_reduit'},               # Pharmacie
        {'value': '6.1.2', 'categorie_fiscale': 'tva_taux_plein'},                          # Parapharmacie
        {'value': '6.1.3', 'categorie_fiscale': 'tva_taux_reduit'},                         # Matériel thérapeutique

        # 07 Transports
        {'value': 7, 'categorie_fiscale': 'tva_taux_plein'},
        {'value': '7.2.2', 'categorie_fiscale': 'ticpe'},                                   # Carburants et lubrifiants pour véhicules de tourisme 
        {'value': '7.3.1', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},           # Transport ferroviaire de passagers
        {'value': '7.3.1', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '7.3.2', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},           # Transport routier de passagers
        {'value': '7.3.2', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '7.3.3', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2024},           # Transport aérien de passagers
        {'value': '7.3.4', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},           # Transport maritime et fluvial de passager
        {'value': '7.3.4', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},  
        {'value': '7.3.5', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},           # Transport combine de passagers
        {'value': '7.3.5', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '7.3.6', 'categorie_fiscale': 'tva_taux_plein'},                          # Autres services de transports (yc déménagements)
          
        # 08 Communications
        {'value': 8, 'categorie_fiscale': 'tva_taux_plein'},
        {'value': '8.1', 'categorie_fiscale': ''},                                          # Services postaux 

        # 09 Loisirs et culture
        {'value': 9, 'categorie_fiscale': 'tva_taux_plein'},
        {'value': '9.3.2.1', 'categorie_fiscale': 'tva_taux_plein', 'start': 1994},                                         # Equipement sportif
        {'value': '9.3.3', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2016},                                   # Horticulture, floriculture
        {'value': '9.4.1', 'categorie_fiscale': 'tva_taux_reduit', 'start': 1994},                                          # Services récréatifs et sportifs
        {'value': '9.4.1', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2015},
        {'value': '9.4.2.1', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},                                         # Cinema, theatre, concerts
        {'value': '9.4.2.1', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012, 'stop': 2013},
        {'value': '9.4.2.1', 'categorie_fiscale': 'tva_taux_reduit', 'start': 2014},
        {'value': '9.4.2.2', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},                                         # Musées et zoos
        {'value': '9.4.2.2', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '9.4.2.2', 'categorie_fiscale': 'tva_taux_reduit', 'start': 2018},
        {'value': '9.4.2.3', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2011},                                         # Services de télévision et radiodiffusion
        {'value': '9.4.2.3', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '9.4.3', 'categorie_fiscale': '', 'origin': 'COICOP UN'},                                                 # Jeux de hasard
        {'value': '9.5.1', 'categorie_fiscale': 'tva_taux_reduit', 'stop': 2024},                                           # Livre
        {'value': '9.5.2', 'categorie_fiscale': 'tva_taux_super_reduit'},                                                   # Journaux et publications périodiques  
        {'value': '9.6', 'categorie_fiscale': '', 'start': 2019},                                                           # Voyages à forfait

        # 10 Éducation
        {'value': 10, 'categorie_fiscale': ''},

        # 11 Hôtellerie restauration
        {'value': 11, 'categorie_fiscale': 'tva_taux_reduit'},
        {'value': ['11.1.1.1.4', '11.1.1.1.5', '11.1.1.1.6', '11.1.1.1.8'], 'categorie_fiscale': 'tva_taux_plein'},         # Consommation de boissons alcoolisées
        {'value': '11.1.1.1.', 'categorie_fiscale': 'tva_taux_plein', 'stop': 2009},                                        # Restauration avec service à table (hors boissons alcoolisées) 
        {'value': '11.1.1.1.', 'categorie_fiscale': 'tva_taux_reduit', 'start': 2010, 'stop': 2011},
        {'value': '11.1.1.1.', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '11.1.1.2', 'categorie_fiscale': 'tva_taux_plein', 'stop': 1997},                                         # Restauration sans service à table (rapide et à emporter)
        {'value': '11.1.1.2', 'categorie_fiscale': 'tva_taux_reduit', 'start': 1998, 'stop': 2011},
        {'value': '11.1.1.2', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '11.1.2', 'categorie_fiscale': 'tva_taux_reduit'},                                                        # Restauration collective
        {'value': '11.2', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},                                    # Hébergement touristique

        # 12 Autres biens et services
        {'value': 12, 'categorie_fiscale': 'tva_taux_plein'},
        {'value': '12.2', 'categorie_fiscale': '', 'origin': 'COICOP UN'},                                                    # Prostitution
        {'value': '12.4', 'categorie_fiscale': 'tva_taux_reduit', 'start': 2000, 'stop': 2024},                               # Protection sociale
        {'value': '12.4', 'categorie_fiscale': 'tva_taux_intermediaire', 'start': 2012},
        {'value': '12.5.1', 'categorie_fiscale': 'autres_assurances', 'origin': 'COICOP UN'},                                 # Assurance-vie
        {'value': '12.5.2', 'categorie_fiscale': 'autres_assurances'},                                                        # Assurance habitation
        {'value': '12.5.3', 'categorie_fiscale': 'assurance_sante'},                                                          # Assurance santé                                 
        {'value': '12.5.4', 'categorie_fiscale': 'assurance_transport'},                                                      # Assurance transport 
        {'value': '12.5.5', 'categorie_fiscale': 'autres_assurances', 'origin': 'COICOP UN'},                                 # Autres assurances
        {'value': '12.6', 'categorie_fiscale': ''}, ]                                                                         # Services financiers

    # Applique chaque règle fiscale
    for rule in fiscal_rules:
        value = rule.get('value')
        if isinstance(value, list):
            # Si 'value' est une liste, applique la règle à chaque code individuellement
            for single_value in value:
                single_rule = rule.copy()
                single_rule['value'] = single_value
                coicop_nomenclature = new_apply_modification(coicop_nomenclature, **single_rule)
        else:
            # Sinon, applique la règle normalement
            coicop_nomenclature = new_apply_modification(coicop_nomenclature, **rule)

    # Sauvegarde le résultat dans un fichier CSV si demandé
    if to_csv:
        output_path = os.path.join(legislation_directory, 'new_coicop_legislation.csv')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)        # Crée le répertoire s'il n'existe pas
        coicop_nomenclature.to_csv(output_path, index=False)

    return coicop_nomenclature


def new_get_categorie_fiscale(value, year=None, assertion_error=True):
    """
    Récupère la catégorie fiscale associée à un code COICOP donné, éventuellement pour une année spécifique.

    Args:
        value (str, list): Code COICOP (ex: '1', '1.1.2', ['1.1.2', '1.2.3']).
        year (int, optional): Année pour laquelle récupérer la catégorie fiscale. Defaults to None.
        assertion_error (bool, optional): Si True, lève une erreur si plusieurs catégories fiscales sont trouvées.
                                          Sinon, retourne un tableau de catégories. Defaults to True.

    Returns:
        str or list: Catégorie fiscale ou tableau de catégories fiscales.
    """
    # Vérifie que le fichier existe
    file_path = os.path.join(legislation_directory, 'new_coicop_legislation.csv')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")

    # Charge le fichier CSV
    coicop_nomenclature = pd.read_csv(file_path)

    # Sélectionne les lignes en fonction du type de 'value'
    if isinstance(value, int):
        value_str = '0' + str(value) if value < 10 else str(value)
        selection = coicop_nomenclature.code_coicop.str.startswith(value_str + '.')
    elif isinstance(value, str):
        selection = coicop_nomenclature.code_coicop.str.startswith(value)
    elif isinstance(value, list):
        selection = coicop_nomenclature.code_coicop.isin(value)
    else:
        raise ValueError(f"Type de 'value' non supporté : {type(value)}")

    # Filtre par année si nécessaire
    if year is not None:
        if 'start' not in coicop_nomenclature.columns or 'stop' not in coicop_nomenclature.columns:
            raise ValueError("Les colonnes 'start' ou 'stop' ne sont pas présentes dans le DataFrame.")
        selection = selection & (coicop_nomenclature.start <= year) & (year <= coicop_nomenclature.stop)

    # Récupère les catégories fiscales
    categorie_fiscale = coicop_nomenclature.loc[selection, 'categorie_fiscale'].unique()

    # Vérifie si des catégories fiscales ont été trouvées
    if len(categorie_fiscale) == 0:
        raise ValueError(f"Aucune catégorie fiscale trouvée pour {value}.")

    # Gestion des cas multiples
    if assertion_error:
        if len(categorie_fiscale) > 1:
            raise AssertionError(f"La catégorie fiscale n'est pas unique pour {value}. Candidates: {categorie_fiscale}")
        return categorie_fiscale[0]
    else:
        return categorie_fiscale

   
def new_test_coicop_legislation():
    coicop_nomenclature = build_coicop_nomenclature.build_complete_coicop_nomenclature()
    coicop_legislation = new_add_fiscal_categories_to_coicop_nomenclature(coicop_nomenclature, to_csv = False)
    if coicop_legislation.categorie_fiscale.isnull().any():
        return coicop_legislation.loc[coicop_legislation.categorie_fiscale.isnull()]

   
if __name__ == '__main__':
    coicop_nomenclature = build_coicop_nomenclature.build_complete_coicop_nomenclature()
    coicop_nomenclature = new_add_fiscal_categories_to_coicop_nomenclature(coicop_nomenclature, to_csv = True)
    new_test_coicop_legislation()
