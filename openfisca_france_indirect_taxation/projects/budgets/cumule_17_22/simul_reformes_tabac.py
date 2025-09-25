import logging
import pandas as pd

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.Calage_consommation_bdf import new_get_inflators
from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group
from openfisca_france_indirect_taxation.projects.budgets.base import nombre_paquets_cigarettes_by_year
from openfisca_france_indirect_taxation.projects.budgets.calage_depenses_cigarettes import create_reforme_calage_depenses_cigarettes, create_reforme_calage_depenses_tabac
from openfisca_france_indirect_taxation.reforms.reforme_tabac import create_reforme_tabac
from matplotlib import pyplot as plt


log = logging.getLogger(__name__)


# agregat_depenses = {
#     2017 : 20441000000,
#     2018 : 21722000000,
#     2019 : 22531000000,
#     2020 : 22531000000,
#     }

# on prend les dépenses avant réponse comportementale en baseline, peut improte les années
agregat_depenses = {
    2017: 20441000000,
    2018: 20441000000,
    2019: 20441000000,
    2020: 20441000000,
    }

path = 'Q:/Evaluation du budget/PLF2022/donnees_relance_note_mars_2022/fiscalite_indirecte'
is_elasticite = True
replique_gouv = True

if not (is_elasticite):
    elas = 0
elif not (replique_gouv):
    elas = -0.5
elif replique_gouv:
    elas = -0.635


def simulate_reforme_tabac(year, baseline_year, graph = True, elasticite = None):

    data_year = 2017
    inflators_by_year = new_get_inflators(2011, 2020)
    inflators_by_year[2018] = inflators_by_year[2017]
    inflators_by_year[2019] = inflators_by_year[2017]
    inflators_by_year[2020] = inflators_by_year[2017]
    inflators_by_year[2021] = inflators_by_year[2017]
    inflators_by_year[2022] = inflators_by_year[2017]
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    baseline_tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()

    # Recalage des dépenses de cigarettes BDF sur consommations agrégées officielles
    reforme_calage = create_reforme_calage_depenses_cigarettes(
        agregat_depenses = nombre_paquets_cigarettes_by_year[int(baseline_year)],
        niveau_calage = 'decile',
        year_calage = baseline_year,
        )
    reforme_calage = create_reforme_calage_depenses_tabac(
        agregat_depenses = agregat_depenses[int(baseline_year)],
        year_calage = baseline_year,
        )

    baseline_tax_benefit_system = reforme_calage(baseline_tax_benefit_system)

    # Applicatin des réformes de la fiscalité tabac
    reform = create_reforme_tabac(baseline_year = baseline_year, elasticite = elasticite)

    survey_scenario = SurveyScenario.create(
        baseline_tax_benefit_system = baseline_tax_benefit_system,
        reform = reform,
        year = year,
        data_year = data_year,
        inflation_kwargs = inflation_kwargs
        )

    nivvie = dataframe_by_group(
        survey_scenario,
        category = 'niveau_vie_decile',
        variables = ['niveau_de_vie'],
        use_baseline = True,
        )

    df = dataframe_by_group(
        survey_scenario,
        category = 'niveau_vie_decile',
        variables = ['rev_disponible', 'depenses_tabac'],
        use_baseline = True,
        )

    df = df.rename(columns = {'depenses_tabac': 'depenses_tabac_baseline'})

    df_sum = dataframe_by_group(
        survey_scenario,
        category = 'niveau_vie_decile',
        variables = ['rev_disponible', 'depenses_tabac'],
        use_baseline = True,
        aggfunc = 'sum',
        )

    df_sum = df_sum.rename(columns = {'depenses_tabac': 'depenses_tabac_baseline'})

    dfr = dataframe_by_group(
        survey_scenario,
        category = 'niveau_vie_decile',
        variables = ['depenses_tabac'],
        use_baseline = False,
        )

    dfr = dfr.rename(columns = {'depenses_tabac': 'depenses_tabac_reforme'})

    dfr_sum = dataframe_by_group(
        survey_scenario,
        category = 'niveau_vie_decile',
        variables = ['depenses_tabac'],
        use_baseline = False,
        aggfunc = 'sum',
        )

    dfr_sum = dfr_sum.rename(columns = {'depenses_tabac': 'depenses_tabac_reforme'})

    diff = dataframe_by_group(
        survey_scenario,
        category = 'niveau_vie_decile',
        variables = ['depenses_tabac'],
        difference = True
        )
    diff = diff.rename(columns = {'depenses_tabac': 'depenses_tabac_difference'})

    diff['variation_relative_depenses_tabac'] = (
        diff['depenses_tabac_difference']
        / df['rev_disponible']
        )
    diff = pd.concat([diff, df], axis = 1)
    diff = pd.concat([diff, dfr], axis = 1)
    diff = pd.concat([diff, nivvie], axis = 1)
    diff['cout_agrege'] = survey_scenario.compute_aggregate(variable = 'depenses_tabac', period = year, difference = True)
    diff['part_niveau_vie_baseline'] = diff['depenses_tabac_baseline'] / diff['rev_disponible']
    diff['part_niveau_vie_reforme'] = diff['depenses_tabac_reforme'] / diff['rev_disponible']
    diff.to_csv('{}/donnees_reforme_tabac_17_20_elasticite_{}.csv'.format(path, elasticite))

    df_sum = pd.concat([df_sum, dfr_sum], axis = 1)
    df_sum.to_csv('{}/totaux_reforme_tabac_17_20_elasticite_{}.csv'.format(path, elasticite))

    if graph:
        plt.bar(diff.index, diff['variation_relative_depenses_tabac'])
        plt.savefig('{}/variation_relative_depenses_tabac_{}_{}_elas_{}.png'.format(path, baseline_year, year, elasticite))
        plt.close()

        plt.bar(diff.index, diff['depenses_tabac_difference'])
        plt.close()
    cout = survey_scenario.compute_aggregate(variable = 'depenses_tabac', period = year, difference = True) / 1e9
    log.info("Coût total de la réforme (baseline : {}): {} milliards d'euros".format(
        baseline_year, cout

        ))

    return diff['variation_relative_depenses_tabac'].values, cout


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    couts = {}
    for baseline_year in ['2017']:
        year = 2020
        variation_relative_depenses_tabac, cout = simulate_reforme_tabac(year = year,
                                                                         baseline_year = baseline_year,
                                                                         elasticite = elas)
        couts['{}_{}'.format(baseline_year, str(year))] = cout
