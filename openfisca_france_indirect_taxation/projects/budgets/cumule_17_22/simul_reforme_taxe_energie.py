import logging
import numpy

from openfisca_survey_manager.utils import asof

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.examples.utils_example import (
    dataframe_by_group,
    graph_builder_bar,
    )
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.projects.budgets.reforme_energie_budgets_2018_2019 import officielle_2019_in_2017
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy
import pandas as pd
from matplotlib import pyplot as plt

log = logging.getLogger(__name__)


ident_men = pd.DataFrame(pd.HDFStore("C:/Users/c.lallemand/data_taxation_indirecte/data_collections/output/openfisca_indirect_taxation_data_2017.h5")['input']['ident_men'])
ident_men['ident_men'] = ident_men.ident_men.astype(numpy.int64)

path = "Q:/Evaluation du budget/PLF2022/donnees_relance_note_mars_2022/fiscalite_indirecte"
elasticite = True
replique_gouv = True


def simulate_reformes_energie(graph = True, replique_gouv = replique_gouv, elasticite = elasticite):

    data_year = 2017
    # on veut faire les simulations sur les quantités avant réforme
    # idéalement on voudrait l'évolution des quantités pour les années jusque 2022 s'il n'y avait pas eu de réforme
    # mais en l'absence d'information on considère que la consommation reste constante dans le contrefactuel.
    inflators_by_year = get_inflators_by_year_energy(rebuild = True, year_range = range(2011, 2020), data_year = data_year)
    inflators_by_year[2018] = inflators_by_year[2017]
    inflators_by_year[2019] = inflators_by_year[2017]
    inflators_by_year[2020] = inflators_by_year[2017]
    inflators_by_year[2021] = inflators_by_year[2017]
    inflators_by_year[2022] = inflators_by_year[2017]
    year = 2019
    # elasticités : le programme de T. Douenne n'a pas été bien adapté (pas le temps) et du coup on a pas d'élasticité pour tout le monde
    # on prend des élasticités agrégées par type de bien

    ident_men['elas_price_1_1'] = -0.45
    ident_men['elas_price_2_2'] = -0.45
    ident_men['elas_price_3_3'] = -0.2

    elasticities = ident_men
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    simulated_variables = [
        'total_taxes_energies',
        'essence_ticpe',
        'diesel_ticpe',
        'combustibles_liquides_ticpe',
        'total_taxes_energies_officielle_2019_in_2017',
        'essence_ticpe_officielle_2019_in_2017',
        'diesel_ticpe_officielle_2019_in_2017',
        'combustibles_liquides_ticpe_officielle_2019_in_2017',
        # 'revenu_reforme_officielle_2019_in_2017',
        'ticgn_officielle_2019_in_2017',
        'ticgn',
        # 'taxe_gaz_ville_officielle_2019_in_2017',
        'gains_tva_total_energies_officielle_2019_in_2017',
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

    # Résultats agrégés par déciles de niveau de vie
    df = dataframe_by_group(survey_scenario, category = 'niveau_vie_decile', variables = simulated_variables)
    df_sum = dataframe_by_group(survey_scenario, category = 'niveau_vie_decile', variables = simulated_variables, aggfunc = 'sum')

    # Simulation des effets de différentes réformes

    if replique_gouv:
        # chiffres du calage issus des fichiers envoyés par la DGTrésor en février 2022 concernant les simulations du RESF 2022
        df_sum['diesel_ticpe'] = df_sum['diesel_ticpe'] * ((survey_scenario.compute_aggregate('quantite_diesel', period = year) - 16019100000) / 16019100000)
        df_sum['diesel_ticpe_officielle_2019_in_2017'] = df_sum['diesel_ticpe_officielle_2019_in_2017'] * ((survey_scenario.compute_aggregate('quantite_diesel', period = year) - 16019100000) / 16019100000)
        df_sum['essence_ticpe'] = df_sum['essence_ticpe'] * ((survey_scenario.compute_aggregate('quantite_essence', period = year) - (6066500000 + 3938900000)) / (6066500000 + 3938900000))
        df_sum['essence_ticpe_officielle_2019_in_2017'] = df_sum['essence_ticpe_officielle_2019_in_2017'] * ((survey_scenario.compute_aggregate('quantite_essence', period = year) - (6066500000 + 3938900000)) / (6066500000 + 3938900000))
        df_sum['ticgn'] = df_sum['essence_ticpe'] * ((survey_scenario.compute_aggregate('quantites_gaz_final_cale', period = year) - 121500000000) / 121500000000)
        df_sum['ticgn_officielle_2019_in_2017'] = df_sum['essence_ticpe_officielle_2019_in_2017'] * ((survey_scenario.compute_aggregate('quantites_gaz_final_cale', period = year) - 121500000000) / 121500000000)
        df_sum['total_taxe'] = df_sum['ticgn'] + df_sum['diesel_ticpe'] + df_sum['essence_ticpe']
        df_sum['total_taxe_officielle_2019_in_2017'] = df_sum['ticgn_officielle_2019_in_2017'] + df_sum['diesel_ticpe_officielle_2019_in_2017'] + df_sum['essence_ticpe_officielle_2019_in_2017']
        df_sum['gains_tva_total_energies_officielle_2019_in_2017'] = df_sum['gains_tva_total_energies_officielle_2019_in_2017'] * ((455896033 - 391000000) / 391000000)  # 455896033 = chiffrage des gains de tva sans elasticite

    df['total_taxe'] = df['ticgn'] + df['total_taxes_energies']
    df['total_taxe_reform'] = df['ticgn_officielle_2019_in_2017'] + df['total_taxes_energies_officielle_2019_in_2017'] + df['gains_tva_total_energies_officielle_2019_in_2017']
    df['part_niveau_vie_baseline'] = df['total_taxe'] / df['rev_disponible']
    df['part_niveau_vie_reform'] = df['total_taxe_reform'] / df['rev_disponible']
    df['somme_total_taxe'] = (survey_scenario.compute_aggregate('total_taxes_energies', period = year)
                              + survey_scenario.compute_aggregate('ticgn', period = year)
                              )
    df['somme_total_taxe_reform'] = (survey_scenario.compute_aggregate('total_taxes_energies_officielle_2019_in_2017', period = year)
                                     + survey_scenario.compute_aggregate('ticgn_officielle_2019_in_2017', period = year)
                                     + survey_scenario.compute_aggregate('gains_tva_total_energies_officielle_2019_in_2017', period = year)
                                     )
    df['cout_reforme'] = df['total_taxe_reform'] - df['total_taxe']

    df.to_csv('{}/donnees_reforme_energie_19_17_replique_gouv_{}_elasticite_{}.csv'.format(path, replique_gouv, elasticite))
    df_sum.to_csv('{}/totaux_reforme_energie_19_17_replique_gouv_{}_elasticite_{}.csv'.format(path, replique_gouv, elasticite))

    if graph:
        graph_builder_bar(df['cout_total_reforme'], False)
        plt.bar(df.index, df['cout_total_reforme'])
        plt.savefig('{}/variation_reforme_energie_19_17_replique_gouv_{}_elasticite_douenne_{}'.format(path, replique_gouv, elasticite))
        plt.close()
        plt.bar(df.index, df['revenu_reforme_officielle_2019_in_2017'])
        plt.savefig('{}/revenu_reforme_enerige_19_17_replique_gouv_{}_elasticite_douenne_{}'.format(path, replique_gouv, elasticite))
        plt.close()

    log.info("Coût total de la réforme : {} milliards d'euros".format(
        (survey_scenario.compute_aggregate('revenu_reforme_officielle_2019_in_2017', period = 2019))

        ))
    return df


if __name__ == "__main__":
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    df = simulate_reformes_energie(replique_gouv = replique_gouv, elasticite = elasticite, graph = False)
