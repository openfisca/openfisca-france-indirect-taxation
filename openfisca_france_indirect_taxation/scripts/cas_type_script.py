from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france_indirect_taxation import CountryTaxBenefitSystem


TEST_CASE = {
    'individus': {
        'Arthur': {},
        'Brittany': {},
    },
    'menages': {
        'menage1': {
            'personne_de_reference': ["Arthur"],
            'region': {'2021': 'franche_comte'},
            'code_region' : {'2021': 27},
            'nombre_litres_gazole_b7': {'2021': 600},
            'nombre_litres_gazole_b10': {'2021': 600},
            'nombre_litres_essence_sp95_e10': {'2021': 600},
            'nombre_litres_essence_sp95': {'2021': 600},
            'nombre_litres_essence_sp98': {'2021': 600},
            'nombre_litres_essence_super_plombe': {'2021': 600},
            'nombre_litres_essence_e85': {'2021': 600},
            'nombre_litres_gpl_carburant': {'2021': 600},
        },
        'menage2': {
            'personne_de_reference': ["Brittany"],
            'region': {'2021': 'corse'},
            'code_region' : {'2021': 94},
            'nombre_litres_gazole_b7': {'2021': 600},
            'nombre_litres_gazole_b10': {'2021': 600},
            'nombre_litres_essence_sp95_e10': {'2021': 600},
            'nombre_litres_essence_sp95': {'2021': 600},
            'nombre_litres_essence_sp98': {'2021': 600},
            'nombre_litres_essence_super_plombe': {'2021': 600},
            'nombre_litres_essence_e85': {'2021': 600},
            'nombre_litres_gpl_carburant': {'2021': 600},
        },
    },
}

tax_benefit_system = CountryTaxBenefitSystem()
simulation_builder = SimulationBuilder()
simulation = simulation_builder.build_from_entities(tax_benefit_system, TEST_CASE)

cout_gazole_b7_ttc  = simulation.calculate('cout_gazole_b7_ttc','2021')
print(cout_gazole_b7_ttc)

# gazole_b7_ticpe  = simulation.calculate('gazole_b7_ticpe','2021')
# print(gazole_b7_ticpe)



'''
# TEST_CASE = {
#     'individus': {
#         'Arthur': {},
#     },
#     'menages': {
#         'menage1': {
#             'personne_de_reference': ["Arthur"],
#             'nombre_litres_diesel': {'2022': 600},
#             'nombre_litres_sp_e10': {'2022': 600},
#             'nombre_litres_sp_95': {'2005': 600,'2007':600,'2022': 600},
#             'nombre_litres_sp_98': {'2005': 600,'2007':600,'2022': 600},
#             'nombre_litres_super_plombe': {'2005': 600,'2022': 600},
#             'nombre_litres_combustibles_liquides': {'2022': 600},
#             'region': {'2022': 'franche_comte','2016': 'franche_comte'},
#         },
#     },
# }

# TEST_CASE = {
#     'individus': {
#         'Arthur': {},
#         'Brittany': {},
#     },
#     'menages': {
#         'menage1': {
#             'personne_de_reference': ["Arthur"],
#             'region': {'2022': 'franche_comte','2016': 'franche_comte'},
#             'nombre_litres_diesel': {'2022': 600},
#             'nombre_litres_sp_e10': {'2022': 600},
#             'nombre_litres_sp_95': {'2005': 600,'2007':600,'2022': 600},
#             'nombre_litres_sp_98': {'2005': 600,'2007':600,'2022': 600},
#             'nombre_litres_super_plombe': {'2005': 600,'2022': 600},
#             'nombre_litres_combustibles_liquides': {'2022': 600},
#         },
#         'menage2': {
#             'personne_de_reference': ["Brittany"],
#             'region': {'2022': 'corse','2016': 'corse'},
#             'nombre_litres_diesel': {'2022': 600},
#             'nombre_litres_sp_e10': {'2022': 600},
#             'nombre_litres_sp_95': {'2005': 600,'2007':600,'2022': 600},
#             'nombre_litres_sp_98': {'2005': 600,'2007':600,'2022': 600},
#             'nombre_litres_super_plombe': {'2005': 600,'2022': 600},
#             'nombre_litres_combustibles_liquides': {'2022': 600},
#         },
#     },
# }

TEST_CASE = {
    'individus': {
        'Arthur': {},
        'Brittany': {},
        'Dwayne': {},
    },
    'menages': {
        'menage1': {
            'personne_de_reference': ["Arthur"],
            'region': {'2005': 'franche_comte','2006': 'franche_comte','2009': 'franche_comte','2016': 'franche_comte'},
            'nombre_litres_diesel': {'2009':600,'2016':600,'2022': 600},
            'nombre_litres_sp_e10': {'2016':600,'2022': 600},
            'nombre_litres_sp_95': {'2005': 600,'2007':600,'2022': 600},
            'nombre_litres_sp_98': {'2005': 600,'2007':600,'2022': 600},
            'nombre_litres_super_plombe': {'2005': 600,'2022': 600},
            'nombre_litres_combustibles_liquides': {'2022': 600},
        },
        'menage2': {
            'personne_de_reference': ["Brittany"],
            'region': {'2005': 'corse','2006': 'corse','2009': 'corse','2016': 'corse'},
            'nombre_litres_diesel': {'2009':600,'2016':600,'2022': 600},
            'nombre_litres_sp_e10': {'2016':600,'2022': 600},
            'nombre_litres_sp_95': {'2005': 600,'2007':600,'2022': 600},
            'nombre_litres_sp_98': {'2005': 600,'2007':600,'2022': 600},
            'nombre_litres_super_plombe': {'2009': 600,'2016':600,'2022': 600},
            'nombre_litres_combustibles_liquides': {'2022': 600},
        },
        'menage3': {
            'personne_de_reference': ["Dwayne"],
            'nombre_litres_diesel': {'2009':600,'2016':600,'2022': 600},
            'nombre_litres_sp_e10': {'2016':600,'2022': 600},
            'nombre_litres_sp_95': {'2005': 600,'2007':600,'2022': 600},
            'nombre_litres_sp_98': {'2005': 600,'2007':600,'2022': 600},
            'nombre_litres_super_plombe': {'2005': 600,'2022': 600},
            'nombre_litres_combustibles_liquides': {'2022': 600},
            'region': {'2005': 'autre','2006': 'autre','2009': 'autre','2016': 'autre'},
        },
    },
}

tax_benefit_system = CountryTaxBenefitSystem()
simulation_builder = SimulationBuilder()
simulation = simulation_builder.build_from_entities(tax_benefit_system, TEST_CASE)


## test ttc to ht

diesel_ht  = simulation.calculate('prix_litre_diesel_ht','2009')
print(diesel_ht)

super_95_e10_ht =  simulation.calculate('prix_litre_super_95_e10_ht','2016')
print(super_95_e10_ht)

super_95_ht =  simulation.calculate('prix_litre_super_95_ht','2016')
print(super_95_ht)

super_98_ht =  simulation.calculate('prix_litre_super_98_ht','2016')
print(super_98_ht)

super_plombe_ht = simulation.calculate('prix_litre_super_plombe_ht','2006')
print(super_plombe_ht)

gplc_ht = simulation.calculate('prix_litre_gplc_ht','2016')
print(gplc_ht)


## ticpe diesel total

nombre_litres_diesel = simulation.calculate('nombre_litres_diesel','2022')
print(nombre_litres_diesel)

diesel_ticpe_cas_type = simulation.calculate('diesel_ticpe_cas_type','2009')
print(diesel_ticpe_cas_type)


## ticpe essence intermediaire

sp_e10_ticpe_cas_type = simulation.calculate('sp_e10_ticpe_cas_type','2022')
print(sp_e10_ticpe_cas_type)

sp95_ticpe_cas_type = simulation.calculate('sp95_ticpe_cas_type','2022')
print(sp95_ticpe_cas_type)

sp95_ticpe_cas_type = simulation.calculate('sp95_ticpe_cas_type','2007')
print(sp95_ticpe_cas_type)

sp95_ticpe_cas_type = simulation.calculate('sp95_ticpe_cas_type','2005')
print(sp95_ticpe_cas_type)

sp98_ticpe_cas_type = simulation.calculate('sp98_ticpe_cas_type','2022')
print(sp98_ticpe_cas_type)

sp98_ticpe_cas_type = simulation.calculate('sp98_ticpe_cas_type','2007')
print(sp98_ticpe_cas_type)

sp98_ticpe_cas_type = simulation.calculate('sp98_ticpe_cas_type','2005')
print(sp98_ticpe_cas_type)

super_plombe_ticpe_cas_type = simulation.calculate('super_plombe_ticpe_cas_type','2005')
print(super_plombe_ticpe_cas_type)

## ticpe essence total

#après 2009
essence_ticpe_cas_type = simulation.calculate('essence_ticpe_cas_type','2022')
print(essence_ticpe_cas_type)

#après 2007
essence_ticpe_cas_type = simulation.calculate('essence_ticpe_cas_type','2007')
print(essence_ticpe_cas_type)

#après 1990
essence_ticpe_cas_type = simulation.calculate('essence_ticpe_cas_type','2005')
print(essence_ticpe_cas_type)

## carburant liquide ticpe

combustibles_liquides_ticpe_cas_type = simulation.calculate('combustibles_liquides_ticpe_cas_type','2022')
print(combustibles_liquides_ticpe_cas_type)

## total taxe energie

total_taxes_energies_cas_type = simulation.calculate('total_taxes_energies_cas_type','2022')
print(total_taxes_energies_cas_type)

## tva sur ticpe carburant

tva_ticpe_cas_type = simulation.calculate('tva_ticpe_cas_type','2022')
print(tva_ticpe_cas_type)



## cout total hors taxe

cout_total_ht_cas_type = simulation.calculate('cout_total_ht_cas_type','2022')
print(cout_total_ht_cas_type)

## tva sur cout ht carburant

tva_cout_ht_cas_type = simulation.calculate('tva_cout_ht_cas_type','2022')
print(tva_cout_ht_cas_type)

## cout total ttc

cout_total_ttc_cas_type = simulation.calculate('cout_total_ttc_cas_type','2022')
print(cout_total_ttc_cas_type)
'''