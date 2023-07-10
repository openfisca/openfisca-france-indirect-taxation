import numpy
import pandas as pd
import os
import ast
import seaborn as sns
from matplotlib import pyplot as plt

from openfisca_survey_manager.utils import asof

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.examples.utils_example import (
    wavg,
    collapse,
    dataframe_by_group,
    graph_builder_bar)
from openfisca_france_indirect_taxation.almost_ideal_demand_system.utils import add_niveau_vie_decile
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.projects.Master_Thesis_Herve.Reform_carbon_tax import carbon_tax_rv
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy

data_path = "C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Data"
output_path = "C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Output"
                           
df_elasticities = pd.read_csv(os.path.join(data_path,'Elasticities_literature.csv'), sep = ";")
df_elasticities[['elas_price_1_1','elas_price_2_2','elas_price_3_3']].astype(float)

df_elas_vect = pd.read_csv(os.path.join(data_path,'Elasticities_Douenne_20.csv'), index_col = [0])
df_elas_vect = pd.melt(frame = df_elas_vect , id_vars = ["niveau_vie_decile", 'ref_elasticity'], var_name = 'strate_2', value_name = 'elas_price_1_1')
    
def simulate_reformes_energie(elas_vect, elasticites, year, reform):

    ident_men = pd.HDFStore("C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Data/data_collections/output/openfisca_indirect_taxation_data_2017.h5")['input'][['ident_men','pondmen', 'rev_disponible','ocde10','strate']]
    ident_men['ident_men'] = ident_men.ident_men.astype(numpy.int64)
    ident_men = add_niveau_vie_decile(ident_men)

    data_year = 2017
    inflators_by_year = get_inflators_by_year_energy(rebuild = True, year_range = range(2011, 2020), data_year = data_year)
    
    if elas_vect == True :
        # elasticités vectorielles : on a une elasctitié-prix du carburant par décile de niveau de vie x type de ville 
        dict_strate = { 0 : 'Rural' , 1 : 'Small cities' , 2 : 'Medium cities' , 3 : 'Large cities' , 4 : 'Paris'}
        ident_men['strate_2'] = ident_men['strate'].apply(lambda x : dict_strate.get(x))
        ident_men = ident_men.merge(right = elasticites , how = 'inner' , on = ['niveau_vie_decile','strate_2'])
        ident_men['elas_price_1_1'] = ident_men['elas_price_1_1'].apply( lambda x : ast.literal_eval(x)[0])
        ident_men = ident_men[['ident_men','elas_price_1_1']]
    
    else:
        # elasticités scalaires : on prend des élasticités agrégées par type de bien
        ident_men['elas_price_1_1'] = elasticites['elas_price_1_1'].reset_index()['elas_price_1_1'][0] # transport fuel
        ident_men['elas_price_2_2'] = elasticites['elas_price_2_2'].reset_index()['elas_price_2_2'][0] # housing fuel
        ident_men['elas_price_3_3'] = elasticites['elas_price_3_3'].reset_index()['elas_price_3_3'][0] # other non durable goods ??
        ident_men = ident_men[['ident_men','elas_price_1_1','elas_price_2_2','elas_price_3_3']]
        
    elasticities = ident_men 
        
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    simulated_variables = [
        'bonus_cheques_energie',
        'contributions_reforme',       
        'ticpe_totale',
        'ticpe_totale_'+ reform.key[0],
        'rev_disp_loyerimput',
        'pondmen',
        'ocde10',
        'niveau_vie_decile'
        ]

    baseline_tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
    asof(baseline_tax_benefit_system, "2018-01-01")  # A modifier
    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        baseline_tax_benefit_system = baseline_tax_benefit_system,
        reform = reform,
        year = year,
        data_year = data_year
        )

    indiv_df_reform = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
    menages_reform= indiv_df_reform['menage']

    revenu_disp_loyer_imput_2_perc = menages_reform['rev_disp_loyerimput'].quantile(0.02)
    menages_reform = menages_reform[menages_reform['rev_disp_loyerimput'] >= revenu_disp_loyer_imput_2_perc] # on retire les ménages avant le 3e percentile
    
    menages_reform['Net_transfers_reform'] = menages_reform['bonus_cheques_energie'] - menages_reform['contributions_reforme']  
    menages_reform['Effort_rate'] = menages_reform['contributions_reforme'] / menages_reform['rev_disp_loyerimput'] * 100
    menages_reform['Is_losers'] = menages_reform['Net_transfers_reform'] < 0 
    
    to_graph = pd.DataFrame(data = {'niveau_vie_decile' : [1.0 , 2.0 , 3.0 , 4.0, 5.0 , 6.0 , 7.0 , 8.0 , 9.0 , 10.0, 'Total']})
    for var in ['Is_losers','Effort_rate','Net_transfers_reform']:
        by_decile = pd.DataFrame(data = collapse(menages_reform,'niveau_vie_decile',var)).reset_index().rename(columns = { 0 : var}) 
        total = pd.DataFrame(data = {'niveau_vie_decile' : 'Total', var : wavg(menages_reform, var)}, index = [0]) 
        to_merge = pd.concat([by_decile, total])
        to_graph = to_graph.merge(right = to_merge, how = 'inner', on = 'niveau_vie_decile') 
    
    ref_elasticity = elasticites['ref_elasticity'].reset_index()['ref_elasticity'][0]
    menages_reform['ref_elasticity'] = ref_elasticity
    to_graph['ref_elasticity'] = ref_elasticity
    return (to_graph,menages_reform)

def run_all_elasticities(data_elasticities = df_elasticities, year = 2019, reform = carbon_tax_rv):
    to_graph = pd.DataFrame(columns = {'ref_elasticity','niveau_vie_decile','Is_losers','Effort_rate','Net_transfers_reform'})
    menages_reform = pd.DataFrame(columns = {'ref_elasticity', 
        'bonus_cheques_energie',
        'contributions_reforme',       
        'ticpe_totale',
        'ticpe_totale_'+ reform.key[0],
        'rev_disp_loyerimput',
        'pondmen',
        'ocde10',
        'niveau_vie_decile'
        })
    for elas in data_elasticities['ref_elasticity']:
        elasticities = data_elasticities[data_elasticities['ref_elasticity'] == elas]
        to_concat = simulate_reformes_energie(elas_vect = False, elasticites = elasticities, year = year, reform = reform)
        to_graph = pd.concat([to_graph,to_concat[0]])
        menages_reform = pd.concat([menages_reform, to_concat[1]])
    return (to_graph,menages_reform)
    
def graph_winners_losers(data,reform,elas_vect):
   hue_order = ['Berry (2019)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)']
   plt.figure(figsize= (10,7.5))
   if elas_vect == False :
       sns.barplot(x="niveau_vie_decile", y = 'Is_losers', data = data, hue = 'ref_elasticity', hue_order = hue_order , palette = sns.color_palette("Paired"), width = .9)
   else :
       sns.barplot(x="niveau_vie_decile", y = 'Is_losers', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector'], palette = sns.color_palette("Paired"), width = .9) 
   
   plt.xlabel('Revenue decile', fontdict = {'fontsize' : 12})
   plt.ylabel('Share of net losers from the reform', fontdict = {'fontsize' : 12})
   plt.legend()
   plt.savefig(os.path.join(output_path,'Figures/Winners_losers_reform_{}_elas_vect_{}.png').format(reform.key[0],elas_vect))    
   return

def graph_net_transfers(data,reform,elas_vect):
    hue_order = ['Berry (2019)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)']
    plt.figure(figsize= (10,7.5)) 
    if elas_vect == False :
        sns.barplot(x="niveau_vie_decile", y = 'Net_transfers_reform', data = data, hue = 'ref_elasticity', hue_order = hue_order, palette = sns.color_palette("Paired"), width = .9)
    else :
        sns.barplot(x="niveau_vie_decile", y = 'Net_transfers_reform', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = sns.color_palette("Paired"), width = .9)
    
    plt.xlabel('Revenue decile', fontdict = {'fontsize' : 12})
    plt.ylabel('Net transfers in euros', fontdict = {'fontsize' : 12})
    plt.legend()
    plt.savefig(os.path.join(output_path,'Figures/Net_transfers_reform_{}_elas_vect_{}.png').format(reform.key[0],elas_vect))
    return

def graph_effort_rate(data,reform,elas_vect):
    hue_order = ['Berry (2019)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)']
    plt.figure(figsize= (10,7.5)) 
    if elas_vect == False :
        sns.barplot(x="niveau_vie_decile", y = 'Effort_rate', data = data, hue = 'ref_elasticity', hue_order = hue_order, palette = sns.color_palette("Paired"), width = .9)
    else : 
        sns.barplot(x="niveau_vie_decile", y = 'Effort_rate', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = sns.color_palette("Paired"), width = .9)
    
    plt.xlabel('Revenue decile', fontdict = {'fontsize' : 12})
    plt.ylabel('Additional taxes over disposable income', fontdict = {'fontsize' : 12})
    plt.legend()
    plt.savefig(os.path.join(output_path,'Figures/Effort_rate_reform_{}_elas_vect_{}.png').format(reform.key[0],elas_vect))
    return