import logging


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


log = logging.getLogger(__name__)


def simulate_reformes_energie(graph = True):
    inflators_by_year = get_inflators_by_year_energy(rebuild = True, year_range = range(2011, 2020))
    year = 2019
    data_year = 2011
    elasticities = get_elasticities_aidsills(data_year, True)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    simulated_variables = [
        'revenu_reforme_officielle_2019_in_2017',
        'cheques_energie',
        'rev_disp_loyerimput',
        'rev_disponible',
        'niveau_de_vie',
        'tarifs_sociaux_electricite',
        'tarifs_sociaux_gaz',
        'pondmen'
        ]

    baseline_tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
    asof(baseline_tax_benefit_system, "2017-12-31")
    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
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

    df['cout_reforme_pures_taxes'] = (
        df['revenu_reforme_officielle_2019_in_2017']
        - df['tarifs_sociaux_electricite'] - df['tarifs_sociaux_gaz']
        ) / df['rev_disponible']
    df['cout_passage_tarifs_sociaux_cheque_energie_majore_et_etendu'] = (
        df['cheques_energie']
        - df['tarifs_sociaux_electricite'] - df['tarifs_sociaux_gaz']
        ) / df['rev_disponible']
    df['cout_total_reforme'] = (
        - df['cout_reforme_pures_taxes']
        + df['cout_passage_tarifs_sociaux_cheque_energie_majore_et_etendu']
        )

    if graph:
        graph_builder_bar(df['cout_total_reforme'], False)

    log.info("Coût total de la réforme : {} milliards d'euros".format(
        df['cout_total_reforme'].mean() * df_reforme['pondmen'].sum() / 1e9)
        )
    return df


if __name__ == "__main__":
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    from openfisca_france_indirect_taxation.tests.budgets.budget_2019 import test_plf_2019_reformes_energie
    test_plf_2019_reformes_energie()
    df = simulate_reformes_energie()
