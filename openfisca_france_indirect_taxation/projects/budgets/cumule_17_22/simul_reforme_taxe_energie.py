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

path = "Q:/Evaluation du budget/PLF2022/donnees_relance_note_mars_2022/fiscalite_indirecte"
elasticite = False
replique_gouv = False

def simulate_reformes_energie(graph = True, replique_gouv = replique_gouv, elasticite = elasticite):
    
       
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
    if elasticite:
        survey_scenario = SurveyScenario.create(
            elasticities = elasticities,
            inflation_kwargs = inflation_kwargs,
            baseline_tax_benefit_system = baseline_tax_benefit_system,
            reform = officielle_2019_in_2017,
            year = year,
            data_year = data_year
            )
    else:
        survey_scenario = SurveyScenario.create(
            inflation_kwargs = inflation_kwargs,
            baseline_tax_benefit_system = baseline_tax_benefit_system,
            reform = officielle_2019_in_2017,
            year = year,
            data_year = data_year
            )
        
    df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

    # Résultats agrégés par déciles de niveau de vie
    df = dataframe_by_group(survey_scenario, category = 'niveau_vie_decile', variables = simulated_variables)

    # Simulation des effets de différentes réformes
    
    if replique_gouv:
        df['revenu_reforme_officielle_2019_in_2017'] = 2/3 * df['revenu_reforme_officielle_2019_in_2017']
        df['cout_reforme_pures_taxes'] = \
            df['revenu_reforme_officielle_2019_in_2017']/ df['rev_disponible']
        df['cout_total_reforme'] = (
            - df['cout_reforme_pures_taxes']
            )
        df['cout_agrege'] = 2/3 * survey_scenario.compute_aggregate('revenu_reforme_officielle_2019_in_2017',period = year)
    else:        
        df['cout_reforme_pures_taxes'] = \
            df['revenu_reforme_officielle_2019_in_2017']/ df['rev_disponible']
        df['cout_total_reforme'] = (
            - df['cout_reforme_pures_taxes']
            )
        df['cout_agrege'] = survey_scenario.compute_aggregate('revenu_reforme_officielle_2019_in_2017',period = year)
    
    df.to_csv('{}/donnees_reforme_energie_19_17_replique_gouv_{}_elasticite_{}.csv'.format(path,replique_gouv,elasticite))
        
    if graph:
        graph_builder_bar(df['cout_total_reforme'], False)
        plt.bar(df.index,df['cout_total_reforme'])
        plt.savefig('{}/variation_reforme_energie_19_17_replique_gouv_{}_elasticite_douenne_{}'.format(path,replique_gouv,elasticite))
        plt.close()
        plt.bar(df.index,df['revenu_reforme_officielle_2019_in_2017'])
        plt.savefig('{}/revenu_reforme_enerige_19_17_replique_gouv_{}_elasticite_douenne_{}'.format(path,replique_gouv,elasticite))
        plt.close()

    log.info("Coût total de la réforme : {} milliards d'euros".format(
        (survey_scenario.compute_aggregate('revenu_reforme_officielle_2019_in_2017',period = 2019))

        ))
    return df


if __name__ == "__main__":
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    df = simulate_reformes_energie(replique_gouv = replique_gouv, elasticite = elasticite)
