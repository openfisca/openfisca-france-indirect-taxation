from openfisca_core.simulation_builder import SimulationBuilder
from openfisca_france_indirect_taxation import CountryTaxBenefitSystem

TEST_CASE = {
    'individus': {
        'Arthur': {},
    },
    'menages': {
        'menage1': {
            'personne_de_reference': ["Arthur"],
            'nombre_litres_diesel': {'2022': 600},
            'nombre_litres_sp_e10': {'2022': 600},
            'nombre_litres_sp_95': {'2005': 600,'2007':600,'2022': 600},
            'nombre_litres_sp_98': {'2005': 600,'2007':600,'2022': 600},
            'nombre_litres_super_plombe': {'2005': 600,'2022': 600},
            'nombre_litres_combustibles_liquides': {'2022': 600},
            'region': {'2005': 'franche_comte','2007': 'franche_comte','2022': 'franche_comte'},
        },
    },
}

tax_benefit_system = CountryTaxBenefitSystem()
simulation_builder = SimulationBuilder()
simulation = simulation_builder.build_from_entities(tax_benefit_system, TEST_CASE)

## ticpe diesel total

nombre_litres_diesel = simulation.calculate('nombre_litres_diesel','2022')
print(nombre_litres_diesel)

diesel_ticpe_cas_type = simulation.calculate('diesel_ticpe_cas_type','2022')
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
