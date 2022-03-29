import logging


from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.projects.base import nombre_paquets_cigarettes_by_year
from openfisca_france_indirect_taxation.projects.calage_depenses_cigarettes import create_reforme_calage_depenses_cigarettes


log = logging.getLogger(__name__)


def test_masses(year):

    data_year = 2017
    inflators_by_year = get_inflators_by_year_energy(rebuild = True, year_range = range(2011, 2020), data_year = data_year)
    inflators_by_year[2020] = inflators_by_year[2019]

    baseline_tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()

    # Recalage des dépenses de cigarettes BDF sur consommations agrégées officielles
    reforme_calage = create_reforme_calage_depenses_cigarettes(
        agregat_depenses = nombre_paquets_cigarettes_by_year[int(year)],
        niveau_calage = 'decile',
        year_calage = year,
        )
    baseline_tax_benefit_system = reforme_calage(baseline_tax_benefit_system)

    survey_scenario = SurveyScenario.create(
        inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year]),
        tax_benefit_system = baseline_tax_benefit_system,
        year = year,
        data_year = data_year
        )

    log.info("Masse de taxes indirectes en {} : {} milliards d'euros".format(
        year,
        survey_scenario.compute_aggregate(variable = 'taxes_indirectes_total', period = year) / 1e9
        ))
    log.info("Masse de TICPE en {} : {} milliards d'euros".format(
        year,
        survey_scenario.compute_aggregate(variable = 'ticpe_totale', period = year) / 1e9
        ))
    log.info("Masse de chèque énergie en {} : {} milliards d'euros".format(
        year,
        survey_scenario.compute_aggregate(variable = 'cheques_energie', period = year) / 1e9
        ))
    log.info("Masse de TVA en {} : {} milliards d'euros".format(
        year,
        survey_scenario.compute_aggregate(variable = 'tva_total', period = year) / 1e9
        ))
    log.info("Masse de droits accises tabacs en {} : {} milliards d'euros".format(
        year,
        survey_scenario.compute_aggregate(variable = 'total_tabac_droit_d_accise', period = year) / 1e9
        ))


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    for year in [2017, 2018, 2019, 2020]:
        test_masses(year)
