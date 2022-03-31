import logging


from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, dataframe_by_group
from openfisca_france_indirect_taxation.projects.base import nombre_paquets_cigarettes_by_year
from openfisca_france_indirect_taxation.projects.calage_depenses_cigarettes import create_reforme_calage_depenses_cigarettes
from openfisca_france_indirect_taxation.reforms.reforme_tabac import create_reforme_tabac


log = logging.getLogger(__name__)


def simulate_reforme_tabac(year, baseline_year, graph = True):

    data_year = 2011
    inflators_by_year = get_inflators_by_year_energy(rebuild = True, year_range = range(2011, 2020), data_year = data_year)
    inflators_by_year[2020] = inflators_by_year[2019]

    baseline_tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()

    # Recalage des dépenses de cigarettes BDF sur consommations agrégées officielles
    reforme_calage = create_reforme_calage_depenses_cigarettes(
        agregat_depenses = nombre_paquets_cigarettes_by_year[int(baseline_year)],
        niveau_calage = 'decile',
        year_calage = baseline_year,
        )
    baseline_tax_benefit_system = reforme_calage(baseline_tax_benefit_system)

    # Applicatin des réformes de la fiscalité tabac
    reform = create_reforme_tabac(baseline_year = baseline_year)

    survey_scenario = SurveyScenario.create(
        inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year]),
        baseline_tax_benefit_system = baseline_tax_benefit_system,
        reform = reform,
        year = year,
        data_year = data_year
        )

    df = dataframe_by_group(
        survey_scenario,
        category = 'niveau_vie_decile',
        variables = ['rev_disp_loyerimput'],
        use_baseline = True,
        )
    diff = dataframe_by_group(
        survey_scenario,
        category = 'niveau_vie_decile',
        variables = ['depenses_tabac'],
        difference = True
        )
    diff['variation_relative_depenses_tabac'] = (
        diff['depenses_tabac']
        / df['rev_disp_loyerimput']
        )
    if graph:
        graph_builder_bar(diff['variation_relative_depenses_tabac'], False)
    log.info("Coût total de la réforme (baseline : {}): {} milliards d'euros".format(
        baseline_year,
        survey_scenario.compute_aggregate(variable = 'depenses_tabac', period = year, difference = True) / 1e9
        ))

    return diff['variation_relative_depenses_tabac'].values


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    for baseline_year in ['2017', '2018']:
        from openfisca_france_indirect_taxation.tests.budgets.budget_2019 import test_plf_2019_reforme_tabac
        test_plf_2019_reforme_tabac(baseline_year)
        variation_relative_depenses_tabac = simulate_reforme_tabac(year = 2019, baseline_year = baseline_year)
