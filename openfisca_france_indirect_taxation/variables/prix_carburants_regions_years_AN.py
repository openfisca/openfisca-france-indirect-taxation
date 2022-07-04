import csv

prix_carburant_par_region_litre = None
prix_carburant_par_region_hectolitre = None


def get_prix_carburant_par_region_par_carburant_par_an_litre():
    global prix_carburant_par_region_litre
    if prix_carburant_par_region_litre is None:
        with open('openfisca_france_indirect_taxation/assets/prix/prix_annuel_carburants_par_regions_litre.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            prix_carburant_par_region_litre = {}
            for row in csv_reader:
                carburant = prix_carburant_par_region_litre.setdefault(row['region'], {})
                annee = carburant.setdefault(row['carburant'], {})
                annee[row['annee']] = row['prix_moyen_par_litre']
    return prix_carburant_par_region_litre


def get_prix_carburant_par_region_par_carburant_par_an_hectolitre():
    global prix_carburant_par_region_hectolitre
    if prix_carburant_par_region_hectolitre is None:
        with open('openfisca_france_indirect_taxation/assets/prix/prix_annuel_carburants_par_regions_hectolitre.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            prix_carburant_par_region_hectolitre = {}
            for row in csv_reader:
                carburant = prix_carburant_par_region_hectolitre.setdefault(row['region'], {})
                annee = carburant.setdefault(row['carburant'], {})
                annee[row['annee']] = row['prix_moyen_par_hectolitre']
    return prix_carburant_par_region_hectolitre
