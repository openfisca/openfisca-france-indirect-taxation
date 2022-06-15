import openfisca_france_indirect_taxation

import csv
import codecs
import pkg_resources
import sys


prix_carburant_par_region_par_an = None

def preload_prix_carburant_par_region_par_an():
    global prix_carburant_par_region_par_an
    if prix_carburant_par_region_par_an is None:
        with open( 'openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/prix/prix_annuel_carburant_par_region_annee_litre.csv' , 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader
            print(dict(row))

prix_carburant_par_region_par_an()

# class zone_apl(Variable):
#     value_type = Enum
#     possible_values = TypesZoneApl
#     default_value = TypesZoneApl.zone_2
#     entity = Menage
#     label = 'Zone APL'
#     definition_period = MONTH
#     set_input = set_input_dispatch_by_period

#     def formula(menage, period):
#         '''
#         Retrouve la zone APL (aide personnalisée au logement) de la commune
#         en fonction du depcom (code INSEE)
#         '''
#         depcom = menage('depcom', period)

#         preload_zone_apl()
#         default_value = 2
#         zone = fromiter(
#             (
#                 zone_apl_by_depcom.get(depcom_cell if isinstance(depcom_cell, str) else depcom_cell.decode('utf-8'), default_value)
#                 for depcom_cell in depcom
#                 ),
#             dtype = int16,
#             )
#         return select(
#             (zone == 1, zone == 2, zone == 3),
#             # The .index is not striclty necessary, but it improves perfomances by avoiding a later encoding
#             (TypesZoneApl.zone_1.index, TypesZoneApl.zone_2.index, TypesZoneApl.zone_3.index)
#             )