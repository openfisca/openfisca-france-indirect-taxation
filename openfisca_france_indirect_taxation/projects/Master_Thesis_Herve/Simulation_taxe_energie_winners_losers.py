import numpy
import pandas as pd
import os
import ast
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt

from wquantiles import quantile
from openfisca_survey_manager.utils import asof

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.examples.utils_example import (
    wavg,
    collapse,
    dataframe_by_group,
    graph_builder_bar,
    df_weighted_average_grouped)
from openfisca_france_indirect_taxation.almost_ideal_demand_system.utils import add_niveau_vie_decile
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.projects.Master_Thesis_Herve.Reform_carbon_tax import carbon_tax_rv
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy

data_path = "C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Data"
output_path = "C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Output"
                           
df_elasticities = pd.read_csv(os.path.join(data_path,'Reform_parameters/Elasticities_literature.csv'), sep = ";")
df_elasticities[['elas_price_1_1','elas_price_2_2','elas_price_3_3']].astype(float)

df_elas_vect = pd.read_csv(os.path.join(data_path,'Reform_parameters/Elasticities_Douenne_20.csv'), index_col = [0])
df_elas_vect = pd.melt(frame = df_elas_vect , id_vars = ["niveau_vie_decile", 'ref_elasticity'], var_name = 'strate_2', value_name = 'elas_price_1_1')
    
def simulate_reformes_energie(elas_vect, elasticites, year, reform, bonus_cheques_uc):

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
        'bonus_cheques_energie_uc',
        'bonus_cheques_energie_menage',
        'contributions_reforme',       
        'ticpe_totale',
        'ticpe_totale_'+ reform.key[0],
        #'rev_disp_loyerimput', plutot rev_disponible pour être cohérent
        'rev_disponible',
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
    menages_reform = indiv_df_reform['menage']

    rev_disponible_2_perc = menages_reform['rev_disponible'].quantile(0.02)
    perc_2 = menages_reform[menages_reform['rev_disponible'] <= rev_disponible_2_perc]

    list_var = simulated_variables
    list_var.remove('pondmen')
    average_perc_2 = df_weighted_average_grouped(perc_2,'niveau_vie_decile',list_var)
    average_perc_2['pondmen'] = perc_2['pondmen'].sum()
    
    menages_reform = menages_reform[menages_reform['rev_disponible'] > rev_disponible_2_perc] # on retire les ménages avant le 2e percentile
    menages_reform = pd.concat([menages_reform,average_perc_2])

    if bonus_cheques_uc == True :
        menages_reform['Net_transfers_reform'] = menages_reform['bonus_cheques_energie_uc'] - menages_reform['contributions_reforme']
    else :  
        menages_reform['Net_transfers_reform'] = menages_reform['bonus_cheques_energie_menage'] - menages_reform['contributions_reforme']
         
    menages_reform['Effort_rate'] = menages_reform['contributions_reforme'] / menages_reform['rev_disponible'] * 100
    menages_reform['Is_losers'] = menages_reform['Net_transfers_reform'] < 0 
    
    ref_elasticity = elasticites['ref_elasticity'].reset_index()['ref_elasticity'][0]
    menages_reform['ref_elasticity'] = ref_elasticity
    menages_reform['niveau_vie_decile'] = menages_reform['niveau_vie_decile'].astype(int)
    var_to_graph = ['Is_losers','Effort_rate','Net_transfers_reform']
    by_decile = df_weighted_average_grouped(menages_reform,'niveau_vie_decile',var_to_graph).reset_index()
    total = df_weighted_average_grouped(menages_reform,'ref_elasticity',var_to_graph).reset_index().drop('ref_elasticity',axis = 1)
    total['niveau_vie_decile'] = 'Total'
    #by_decile['niveau_vie_decile'] = by_decile['niveau_vie_decile'].astype(int)
    to_graph = pd.concat([by_decile, total])
    to_graph['ref_elasticity'] = ref_elasticity
    
    return (to_graph,menages_reform)

def run_all_elasticities(data_elasticities = df_elasticities, year = 2019, reform = carbon_tax_rv,bonus_cheques_uc = True):
    to_graph = pd.DataFrame(columns = {'ref_elasticity','niveau_vie_decile','Is_losers','Effort_rate','Net_transfers_reform'})
    menages_reform = pd.DataFrame(columns = {'ref_elasticity', 
        'bonus_cheques_energie_uc',
        'bonus_cheques_energie_menage',
        'contributions_reforme',       
        'ticpe_totale',
        'ticpe_totale_'+ reform.key[0],
        #'rev_disp_loyerimput',
        'rev_disponible',
        'pondmen',
        'ocde10',
        'niveau_vie_decile'
        })
    for elas in data_elasticities['ref_elasticity']:
        elasticities = data_elasticities[data_elasticities['ref_elasticity'] == elas]
        to_concat = simulate_reformes_energie(elas_vect = False, elasticites = elasticities, year = year, reform = reform, bonus_cheques_uc = bonus_cheques_uc)
        to_graph = pd.concat([to_graph,to_concat[0]])
        menages_reform = pd.concat([menages_reform, to_concat[1]])
    return (to_graph,menages_reform)
    
def graph_winners_losers(data,reform,elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    fig, ax = plt.subplots(figsize=(10, 7.5)) 
    if elas_vect == False :
        sns.barplot(x="niveau_vie_decile", y = 'Is_losers', data = data, hue = 'ref_elasticity', hue_order = hue_order , palette = sns.color_palette("Paired"), width = .9)
    else :
        sns.barplot(x="niveau_vie_decile", y = 'Is_losers', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector'], palette = sns.color_palette("Paired"), width = .9) 
    plt.xlabel('Revenue decile', fontdict = {'fontsize' : 14})
    plt.ylabel('Share of net losers from the reform', fontdict = {'fontsize' : 14})
    plt.legend()

    y_max = 0.6
    ax.set_ylim(ymin = 0, ymax = y_max)
    plt.savefig(os.path.join(output_path,'Figures/Winners_losers_reform_{}_elas_vect_{}_bonus_cheques_uc_{}.png').format(reform.key[0],elas_vect,bonus_cheques_uc))    
    return

def graph_net_transfers(data,reform,elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    data = data[data['niveau_vie_decile'] != 'Total']
    fig, ax = plt.subplots(figsize=(10, 7.5)) 
    if elas_vect == False :
        sns.barplot(x="niveau_vie_decile", y = 'Net_transfers_reform', data = data, hue = 'ref_elasticity', hue_order = hue_order, palette = sns.color_palette("Paired"), width = .9)
    else :
        sns.barplot(x="niveau_vie_decile", y = 'Net_transfers_reform', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = sns.color_palette("Paired"), width = .9)
    
    plt.xlabel('Revenue decile', fontdict = {'fontsize' : 14})
    plt.ylabel('Net transfers in euros', fontdict = {'fontsize' : 14})
    plt.legend()

    y_min, y_max = -12 , 17
    ax.set_ylim(ymin = y_min , ymax = y_max)
    plt.savefig(os.path.join(output_path,'Figures/Net_transfers_reform_{}_elas_vect_{}_bonus_cheques_uc_{}.png').format(reform.key[0],elas_vect,bonus_cheques_uc))
    return

def graph_effort_rate(data,reform,elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    fig, ax = plt.subplots(figsize=(10, 7.5)) 
    if elas_vect == False :
        sns.barplot(x="niveau_vie_decile", y = 'Effort_rate', data = data, hue = 'ref_elasticity', hue_order = hue_order, palette = sns.color_palette("Paired"), width = .9)
    else : 
        sns.barplot(x="niveau_vie_decile", y = 'Effort_rate', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = sns.color_palette("Paired"), width = .9)
    
    plt.xlabel('Revenue decile', fontdict = {'fontsize' : 14})
    plt.ylabel('Additional taxes over disposable income', fontdict = {'fontsize' : 14})
    plt.legend()
    
    y_max = 0.2
    ax.set_ylim(ymin = 0 , ymax = y_max)
    plt.savefig(os.path.join(output_path,'Figures/Effort_rate_reform_{}_elas_vect_{}_bonus_cheques_uc_{}.png').format(reform.key[0],elas_vect,bonus_cheques_uc))
    return

def quantiles_for_boxplot(data,y):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    out = pd.DataFrame(data = {'niveau_vie_decile' : [] , 'ref_elasticity': [] , y : []})
    i_ref = 0
    data = data[data['ref_elasticity'].isin(hue_order)]
    for ref in hue_order:
        data_ref = data[data['ref_elasticity'] == ref]
        for decile in set(data_ref['niveau_vie_decile']):
            data_decile = data_ref[data_ref['niveau_vie_decile'] == decile]
            decile = decile + 0.7 + 0.1*i_ref  - 1
            for q in [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]:
                quantil = quantile(data_decile[y],data_decile['pondmen'],q)
                out = pd.concat([out,pd.DataFrame(data = {'niveau_vie_decile' : [decile] , 'ref_elasticity' : ref, y : [quantil], 'quantile' : [q]}),])
        i_ref +=1
    return out

def subtitle_legend_boxplots(ax, legend_format,markers):
    new_handles = []
    
    handles, labels = ax.get_legend_handles_labels()
    label_dict = dict(zip(labels, handles))
    
    #Means 2 labels were the same
    if len(label_dict) != len(labels):
        raise ValueError("Can not have repeated levels in labels!")
    
    for subtitle, level_order in legend_format.items():
        #Roll a blank handle to add in the subtitle
        blank_handle = matplotlib.patches.Patch(visible=False, label=subtitle)
        new_handles.append(blank_handle)
        
        for level in level_order:
            # If level is in the label_dict, it's a label-based level
            if level in label_dict:
                handle = label_dict[level]
                new_handles.append(handle)
            else:
                # If level is not a label, create a dummy handle with markers for percentiles
                percentile_index = legend_format['Percentiles'].index(level)
                marker = markers[percentile_index]
                percentile_handle = plt.Line2D([], [], linestyle='None', marker=marker, markersize=6, label=str(level),color = 'black')
                new_handles.append(percentile_handle)

    #Labels are populated from handle.get_label() when we only supply handles as an arg
    legend = ax.legend(handles=new_handles)

    #Turn off DrawingArea visibility to left justify the text if it contains a subtitle
    for draw_area in legend.findobj(matplotlib.offsetbox.DrawingArea):
        for handle in draw_area.get_children():
            if handle.get_label() in legend_format:
                draw_area.set_visible(False)

    return legend

def boxplot_net_transfers(data,reform,elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    legend_format = {'Elasticity reference' : hue_order,
                    'Percentiles' : [0.01, 0.10, 0.25, 0.5, 0.75, 0.90, 0.99]}
    markers = ['v', 'd', 'o', 'o', 'o' , 'd', '^']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    quantiles_to_plot = quantiles_for_boxplot(data,'Net_transfers_reform')
    sns.scatterplot(data = quantiles_to_plot , x='niveau_vie_decile', y='Net_transfers_reform', hue = 'ref_elasticity',  
                    style = 'quantile',
                    hue_order = hue_order, 
                    palette = sns.color_palette("Paired"), 
                    markers = markers,
                    s = 60,
                    legend = True)
    
    plt.xlabel('Revenue decile', fontdict = {'fontsize' : 14})
    plt.ylabel('Net transfers in euros', fontdict = {'fontsize' : 14})
    subtitle_legend_boxplots(ax, legend_format,markers)
    legend = ax.get_legend()
    legend.set_bbox_to_anchor((1, 0.53))
    ax.xaxis.set_ticks(range(1,11))
    y_min, y_max = -200 , 100
    ax.yaxis.set_ticks(range(y_min,y_max,50))
    
    plt.savefig(os.path.join(output_path,'Figures/Boxplot_net_transfers_reform_{}_elas_vect_{}_bonus_cheques_uc_{}.png').format(reform.key[0],elas_vect,bonus_cheques_uc))
    return

def boxplot_effort_rate(data,reform,elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    legend_format = {'Elasticity reference' : hue_order,
                    'Percentiles' : [0.01, 0.10, 0.25, 0.5, 0.75, 0.90, 0.99]}
    markers = ['v', 'd', 'o', 'o', 'o' , 'd', '^']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    quantiles_to_plot = quantiles_for_boxplot(data,'Effort_rate')
    sns.scatterplot(data = quantiles_to_plot, x='niveau_vie_decile', y='Effort_rate', hue = 'ref_elasticity',  
                    style = 'quantile',
                    hue_order = hue_order, 
                    palette = sns.color_palette("Paired"), 
                    markers = markers,
                    s = 60,
                    legend = True)
    
    plt.xlabel('Revenue decile', fontdict = {'fontsize' : 14})
    plt.ylabel('Additional taxes over disposable income', fontdict = {'fontsize' : 14})
    subtitle_legend_boxplots(ax, legend_format,markers)
    legend = ax.get_legend()
    legend.set_bbox_to_anchor((1, 0.53))
    y_min, y_max = 0 , 1
    ax.set_ylim(y_min,y_max)
    
    plt.savefig(os.path.join(output_path,'Figures/Boxplot_effort_rate_reform_{}_elas_vect_{}_bonus_cheques_uc_{}.png').format(reform.key[0],elas_vect,bonus_cheques_uc))
    return