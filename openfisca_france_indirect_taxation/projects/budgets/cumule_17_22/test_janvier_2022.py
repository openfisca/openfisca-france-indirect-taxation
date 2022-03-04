import logging
import numpy

from openfisca_survey_manager.utils import asof

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.examples.utils_example import (
    dataframe_by_group,
    graph_builder_bar,
    )
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.projects.budgets.reforme_energie_budgets_2018_2019 import officielle_2019_in_2017
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy
import pandas as pd
from matplotlib import pyplot as plt

log = logging.getLogger(__name__)


ident_men = pd.DataFrame(pd.HDFStore("C:/Users/c.lallemand/data_taxation_indirecte/data_collections/output/openfisca_indirect_taxation_data_2017.h5")['input']['ident_men'])
ident_men['ident_men'] = ident_men.ident_men.astype(numpy.int64)

data_year = 2017
## on veut faire les simulations sur les quantités avant réforme
## idéalement on voudrait l'évolution des quantités pour les années jusque 2022 s'il n'y avait pas eu de réforme
## mais en l'absence d'information on considère que la consommation reste constante dans le contrefactuel.
inflators_by_year = get_inflators_by_year_energy(rebuild = True, year_range = range(2011, 2020),data_year = data_year)
inflators_by_year[2018] = inflators_by_year[2017]
inflators_by_year[2019] = inflators_by_year[2017]
inflators_by_year[2020] = inflators_by_year[2017]
inflators_by_year[2021] = inflators_by_year[2017]
inflators_by_year[2022] = inflators_by_year[2017]
year = 2019
## elasticités : le programme de T. Douenne n'a pas été bien adapté (pas le temps) et du coup on a pas d'élasticité pour tout le monde
## on prend des élasticités agrégées par type de bien

ident_men['elas_price_1_1'] = -0.45
ident_men['elas_price_2_2'] = -0.45
ident_men['elas_price_3_3'] = -0.2

elasticities = ident_men
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'revenu_reforme_officielle_2019_in_2017',
    'rev_disponible',
    'niveau_de_vie',
    ]

baseline_tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
asof(baseline_tax_benefit_system, "2017-12-31")

survey_scenario = SurveyScenario.create(
    #elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    baseline_tax_benefit_system = baseline_tax_benefit_system,
    reform = officielle_2019_in_2017,
    year = year,
    data_year = data_year
    )

survey_scenario.compute_aggregate('depenses_gaz_ville_officielle_2019_in_2017',period = 2019)/1e9
survey_scenario.compute_aggregate('quantite_gaz_ville_officielle_2019_in_2017',period = 2019)/1e9

survey_scenario.compute_aggregate('gains_tva_total_energies_officielle_2019_in_2017',period = 2019)
(survey_scenario.compute_aggregate('combustibles_liquides_ticpe_officielle_2019_in_2017',period = 2019)/1e9 -
survey_scenario.compute_aggregate('combustibles_liquides_ticpe',period = 2019)/1e9)

## cout total des réformes
survey_scenario.compute_aggregate('revenu_reforme_officielle_2019_in_2017',period = 2019)/1e9

## Check 1 : est ce que les quantités sont bien les memes en baseline et en réforme en l'absence de réaction comportementale ?
## Cela signifie que la variation de dépenses est bien égale à la variation de prix engendrée par la réforme
survey_scenario.compute_aggregate('depenses_essence',period = 2019)/survey_scenario.tax_benefit_system.parameters('2017-01-01').prix_carburants.super_95_ttc/100
(survey_scenario.compute_aggregate('depenses_essence_corrigees_officielle_2019_in_2017',period = 2019)
 /(survey_scenario.tax_benefit_system.parameters('2017-01-01').prix_carburants.super_95_ttc + survey_scenario.tax_benefit_system.parameters('2017-01-01').officielle_2019_in_2017.essence_2019_in_2017))/100

survey_scenario.compute_aggregate('depenses_diesel',period = 2019)/survey_scenario.tax_benefit_system.parameters('2017-01-01').prix_carburants.diesel_ttc/100
(survey_scenario.compute_aggregate('depenses_diesel_corrigees_officielle_2019_in_2017',period = 2019)
 /(survey_scenario.tax_benefit_system.parameters('2017-01-01').prix_carburants.diesel_ttc + survey_scenario.tax_benefit_system.parameters('2017-01-01').officielle_2019_in_2017.diesel_2019_in_2017))/100

survey_scenario.compute_aggregate('depenses_combustibles_liquides',period = 2019)/survey_scenario.tax_benefit_system.parameters('2017-01-01').tarifs_energie.prix_fioul_domestique.prix_annuel_moyen_fioul_domestique_ttc_livraisons_2000_4999_litres_en_euro_par_litre/100
(survey_scenario.compute_aggregate('depenses_combustibles_liquides_officielle_2019_in_2017',period = 2019)
 /(survey_scenario.tax_benefit_system.parameters('2017-01-01').tarifs_energie.prix_fioul_domestique.prix_annuel_moyen_fioul_domestique_ttc_livraisons_2000_4999_litres_en_euro_par_litre + survey_scenario.tax_benefit_system.parameters('2017-01-01').officielle_2019_in_2017.combustibles_liquides_2019_in_2017))/100

survey_scenario.compute_aggregate('depenses_gaz_de_ville',period = 2019)/survey_scenario.tax_benefit_system.parameters('2017-01-01').tarifs_energie.prix_fioul_domestique.prix_annuel_moyen_fioul_domestique_ttc_livraisons_2000_4999_litres_en_euro_par_litre/100
(survey_scenario.compute_aggregate('depenses_gaz_de_ville_officielle_2019_in_2017',period = 2019)
 /(survey_scenario.tax_benefit_system.parameters('2017-01-01').tarifs_energie.prix_fioul_domestique.prix_annuel_moyen_fioul_domestique_ttc_livraisons_2000_4999_litres_en_euro_par_litre + survey_scenario.tax_benefit_system.parameters('2017-01-01').officielle_2019_in_2017.combustibles_liquides_2019_in_2017))/100


survey_scenario.compute_aggregate('revenu_reforme_officielle_2019_in_2017',period = 2019)/1e9
survey_scenario.compute_aggregate('revenu_reforme_officielle_2019_in_2017',period = 2019)/1e9
survey_scenario.compute_aggregate('revenu_reforme_officielle_2019_in_2017',period = 2019)/1e9
survey_scenario.compute_aggregate('revenu_reforme_officielle_2019_in_2017',period = 2019)/1e9


## Check 2: est ce que le ticpe est calculé de la même manière en baseline et en réforme
(survey_scenario.compute_aggregate('combustibles_liquides_ticpe_officielle_2019_in_2017',period = 2019)/1e9 - 
#compute_aggregate('combustibles_liquides_ticpe_test',period = 2019)/1e9
 survey_scenario.compute_aggregate('combustibles_liquides_ticpe',period = 2019)/1e9)

(survey_scenario.compute_aggregate('diesel_ticpe_officielle_2019_in_2017',period = 2019)/1e9 -
#survey_scenario.compute_aggregate('diesel_ticpe_test',period = 2019)/1e9
survey_scenario.compute_aggregate('diesel_ticpe',period = 2019)/1e9)

(survey_scenario.compute_aggregate('sp95_ticpe_officielle_2019_in_2017',period = 2019)/1e9 -
#survey_scenario.compute_aggregate('sp95_ticpe_test',period = 2019)/1e9
survey_scenario.compute_aggregate('sp95_ticpe',period = 2019)/1e9)

(survey_scenario.compute_aggregate('sp98_ticpe_officielle_2019_in_2017',period = 2019)/1e9 -
#survey_scenario.compute_aggregate('sp98_ticpe_test',period = 2019)/1e9
survey_scenario.compute_aggregate('sp98_ticpe',period = 2019)/1e9)

(survey_scenario.compute_aggregate('sp_e10_ticpe_officielle_2019_in_2017',period = 2019)/1e9 -
#survey_scenario.compute_aggregate('sp_e10_ticpe_test',period = 2019)/1e9
survey_scenario.compute_aggregate('sp_e10_ticpe',period = 2019)/1e9)

(survey_scenario.compute_aggregate('sp_e10_ticpe_officielle_2019_in_2017',period = 2019)/1e9 -
#survey_scenario.compute_aggregate('sp_e10_ticpe_test',period = 2019)/1e9
survey_scenario.compute_aggregate('sp_e10_ticpe',period = 2019)/1e9)

survey_scenario.compute_aggregate('ticpe_total_officielle_2019_in_2017',period = 2019)/1e9
survey_scenario.compute_aggregate('ticpe_total_test',period = 2019)/1e9
survey_scenario.compute_aggregate('ticpe_total',period = 2019)/1e9

## cout de la réforme sur le gaz
survey_scenario.compute_aggregate('taxe_gaz_ville_officielle_2019_in_2017',period = 2019)/1e9

survey_scenario.compute_aggregate('quantites_gaz_final_officielle_2019_in_2017',period = 2019)/1e9
survey_scenario.compute_aggregate('quantites_gaz_final',period = 2019)/1e9
survey_scenario.compute_aggregate('quantites_diesel',period = 2019)/1e9

survey_scenario.compute_aggregate('depenses_gaz_ville_officielle_2019_in_2017',period = 2019)/1e9

(survey_scenario.compute_aggregate('depenses_gaz_prix_unitaire',period = 2019) +
 survey_scenario.compute_aggregate('depenses_gaz_variables',period = 2019) +
 survey_scenario.compute_aggregate('tarifs_sociaux_gaz',period = 2019) +
 survey_scenario.compute_aggregate('depenses_gaz_tarif_fixe',period = 2019)
 )/1e9

## gain de tva du fait de la réforme
survey_scenario.compute_aggregate('gains_tva_total_energies_officielle_2019_in_2017',period = 2019)/1e9

## ticpe en reforme
ticpe_reforme = survey_scenario.compute_aggregate('total_taxes_energies_officielle_2019_in_2017',period = 2019)/1e9 - survey_scenario.compute_aggregate('taxe_gaz_ville_officielle_2019_in_2017',period = 2019)/1e9
ticpe_reforme

## ticpe en baseline
ticpe_baseline = survey_scenario.compute_aggregate('total_taxes_energies',period = 2019)/1e9
ticpe_baseline

## cout de la reforme ticpe 

ticpe_reforme - ticpe_baseline 

test = survey_scenario.create_data_frame_by_entity(['depenses_gaz_ville_officielle_2019_in_2017'],period = 2019,merge = True) 
test = survey_scenario.create_data_frame_by_entity(['pondmen'],period = 2019,merge = True) 