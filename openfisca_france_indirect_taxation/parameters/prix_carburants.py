import csv
import os

from openfisca_france_indirect_taxation.location import openfisca_france_indirect_taxation_location

prix_carburant_par_annee_par_carburant_par_region_en_litre = None
prix_carburant_par_annee_par_carburant_par_region_en_hectolitre = None
prix_carburant_par_annee_par_carburant_en_hectolitre = None


def get_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre():
    if prix_carburant_par_annee_par_carburant_par_region_en_hectolitre is None:
        preload_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre()
    return prix_carburant_par_annee_par_carburant_par_region_en_hectolitre


def get_prix_carburant_par_annee_par_carburant_par_region_en_litre():
    if prix_carburant_par_annee_par_carburant_par_region_en_litre is None:
        preload_prix_carburant_par_annee_par_carburant_par_region_en_litre()
    return prix_carburant_par_annee_par_carburant_par_region_en_litre


def get_prix_carburant_par_annee_par_carburant_en_hectolitre():
    if prix_carburant_par_annee_par_carburant_en_hectolitre is None:
        preload_prix_carburant_par_annee_par_carburant_en_hectolitre()
    return prix_carburant_par_annee_par_carburant_en_hectolitre


def preload_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre():
    global prix_carburant_par_annee_par_carburant_par_region_en_hectolitre
    csv_file_path = os.path.join(
        openfisca_france_indirect_taxation_location,
        'openfisca_france_indirect_taxation',
        'assets',
        'prix',
        'prix_annuel_carburants_par_regions_hectolitre.csv'
        )
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        prix_carburant_par_annee_par_carburant_par_region_en_hectolitre = {}
        for row in csv_reader:
            carburant = prix_carburant_par_annee_par_carburant_par_region_en_hectolitre.setdefault(row['region'], {})
            annee = carburant.setdefault(row['carburant'], {})
            annee[row['annee']] = row['prix_moyen_par_hectolitre']


def preload_prix_carburant_par_annee_par_carburant_par_region_en_litre():  # On ne l'utilise par car choix arbitraire d'utiliser les prix par hectolitre
    global prix_carburant_par_annee_par_carburant_par_region_en_litre
    csv_file_path = os.path.join(
        openfisca_france_indirect_taxation_location,
        'openfisca_france_indirect_taxation',
        'assets',
        'prix',
        'prix_annuel_carburants_par_regions_litre.csv'
        )
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        prix_carburant_par_annee_par_carburant_par_region_en_litre = {}
        for row in csv_reader:
            carburant = prix_carburant_par_annee_par_carburant_par_region_en_litre.setdefault(row['region'], {})
            annee = carburant.setdefault(row['carburant'], {})
            annee[row['annee']] = row['prix_moyen_par_litre']


def preload_prix_carburant_par_annee_par_carburant_en_hectolitre():
    global prix_carburant_par_annee_par_carburant_en_hectolitre
    csv_file_path = os.path.join(
        openfisca_france_indirect_taxation_location,
        'openfisca_france_indirect_taxation',
        'assets',
        'prix',
        'prix_par_carburant_annee_hectolitre.csv'
        )
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        prix_carburant_par_annee_par_carburant_en_hectolitre = {}
        for row in csv_reader:
            annee = prix_carburant_par_annee_par_carburant_en_hectolitre.setdefault(row['carburant'], {})
            annee[row['annee']] = row['prix_moyen_par_hectolitre']
