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


## cout total des réformes
survey_scenario.compute_aggregate('revenu_reforme_officielle_2019_in_2017',period = 2019)/1e9

## cout de la réforme sur le gaz
survey_scenario.compute_aggregate('taxe_gaz_ville_officielle_2019_in_2017',period = 2019)/1e9

survey_scenario.compute_aggregate('quantites_gaz_final_officielle_2019_in_2017',period = 2019)/1e9
survey_scenario.compute_aggregate('quantites_gaz_final',period = 2019)/1e9

survey_scenario.compute_aggregate('depenses_gaz_ville_officielle_2019_in_2017',period = 2019)/1e9

(survey_scenario.compute_aggregate('depenses_gaz_prix_unitaire',period = 2019) +
 survey_scenario.compute_aggregate('depenses_gaz_variables',period = 2019) +
 survey_scenario.compute_aggregate('tarifs_sociaux_gaz',period = 2019) +
 survey_scenario.compute_aggregate('depenses_gaz_tarif_fixe',period = 2019)
 )/1e9

depenses_gaz_tarif_fixe
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