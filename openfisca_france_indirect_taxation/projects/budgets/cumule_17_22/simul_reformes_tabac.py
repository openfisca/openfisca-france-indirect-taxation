import logging
import pandas as pd

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, dataframe_by_group
from openfisca_france_indirect_taxation.projects.base import nombre_paquets_cigarettes_by_year
from openfisca_france_indirect_taxation.projects.calage_depenses_cigarettes import create_reforme_calage_depenses_cigarettes,create_reforme_calage_depenses_tabac
from openfisca_france_indirect_taxation.reforms.reforme_tabac import create_reforme_tabac
from matplotlib import pyplot as plt


log = logging.getLogger(__name__)


# agregat_depenses = {
#     2017 : 20441000000,
#     2018 : 21722000000,
#     2019 : 22531000000,
#     2020 : 22531000000,
#     }

## on prend les dépenses avant réponse comportementale en baseline, peut improte les années
agregat_depenses = {
    2017 : 20441000000,
    2018 : 20441000000,
    2019 : 20441000000,
    2020 : 20441000000,
    }

path = "Q:/Evaluation du budget/PLF2022/donnees_relance_note_mars_2022/fiscalite_indirecte"
is_elasticite = False
replique_gouv = False

if not(is_elasticite):
    elasticite_tabac = 0
elif not(replique_gouv):
    elasticite_tabac = -0.5
elif replique_gouv:
    elasticite_tabac = -0.635

def simulate_reforme_tabac(year, baseline_year, graph = True, elasticite = None):

    
    data_year = 2017
    inflators_by_year = get_inflators_by_year_energy(rebuild = True, year_range = range(2011, 2020), data_year = data_year)
    inflators_by_year[2020] = inflators_by_year[2019]
    inflators_by_year[2021] = inflators_by_year[2020]
    inflators_by_year[2022] = inflators_by_year[2020]

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
        inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year]),
        baseline_tax_benefit_system = baseline_tax_benefit_system,
        reform = reform,
        year = year,
        data_year = data_year
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
        variables = ['rev_disponible'],
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
        / df['rev_disponible']
        )
    diff = pd.concat([diff,df],axis = 1)
    diff = pd.concat([diff,nivvie],axis = 1)
    diff['cout_agrege'] = survey_scenario.compute_aggregate(variable = 'depenses_tabac', period = year, difference = True)
    diff.to_csv('{}/donnees_reforme_tabac_17_20_elasticite_{}.csv'.format(path,elasticite_tabac))
    
    if graph:
        plt.bar(diff.index,diff['variation_relative_depenses_tabac'])
        plt.savefig('{}/variation_relative_depenses_tabac_{}_{}_elas_{}.png'.format(path,baseline_year,year,elasticite))
        plt.close()
        
        plt.bar(diff.index,diff['depenses_tabac'])
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
                                                                         elasticite = elasticite_tabac)
        couts["{}_{}".format(baseline_year, str(year))] = cout
        
