import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns 
import os 
from wquantiles import quantile

data_path = "C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Data"
output_path = "C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Output"

def graph_winners_losers(data,reform,elas_ext, elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
    fig, ax = plt.subplots(figsize=(10, 7.5)) 
    if elas_ext == True:
        sns.barplot(x="niveau_vie_decile", y = 'Is_losers', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector', 'Douenne (2020) ext margin'], palette = palette_douenne, width = .9) 
    else: 
        if elas_vect == False :
            sns.barplot(x="niveau_vie_decile", y = 'Is_losers', data = data, hue = 'ref_elasticity', hue_order = hue_order , palette = sns.color_palette("Paired"), width = .9)
        else :
            sns.barplot(x="niveau_vie_decile", y = 'Is_losers', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector'], palette = palette_douenne, width = .9) 
    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Share of net losers from the reform', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)

    y_max = 0.6
    ax.set_ylim(ymin = 0, ymax = y_max)
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Distributive_effects/Winners_losers/Winners_losers_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))    
    return

def graph_net_transfers(data,reform, elas_ext, elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
    data = data[data['niveau_vie_decile'] != 'Total']
    fig, ax = plt.subplots(figsize=(10, 7.5))
    if elas_ext == True:
        sns.barplot(x="niveau_vie_decile", y = 'Net_transfers_reform', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector', 'Douenne (2020) ext margin'], palette = palette_douenne, width = .9) 
    else: 
        if elas_vect == False :
            sns.barplot(x="niveau_vie_decile", y = 'Net_transfers_reform', data = data, hue = 'ref_elasticity', hue_order = hue_order, palette = sns.color_palette("Paired"), width = .9)
        else :
            sns.barplot(x="niveau_vie_decile", y = 'Net_transfers_reform', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = palette_douenne, width = .9)
        
    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Net transfers per households(in €)', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)

    y_min, y_max = -12 , 17
    ax.set_ylim(ymin = y_min , ymax = y_max)
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Distributive_effects/Net_transfers/Net_transfers_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))
    return

def graph_net_transfers_uc(data,reform, elas_ext, elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
    data = data[data['niveau_vie_decile'] != 'Total']
    fig, ax = plt.subplots(figsize=(10, 7.5))
    if elas_ext == True:
        sns.barplot(x="niveau_vie_decile", y = 'Net_transfers_reform_uc', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector', 'Douenne (2020) ext margin'], palette = palette_douenne, width = .9) 
    
    else: 
        if elas_vect == False :
            sns.barplot(x="niveau_vie_decile", y = 'Net_transfers_reform_uc', data = data, hue = 'ref_elasticity', hue_order = hue_order, palette = sns.color_palette("Paired"), width = .9)
        else :
            sns.barplot(x="niveau_vie_decile", y = 'Net_transfers_reform_uc', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = palette_douenne, width = .9)
    
    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Net transfers per consumption unit (in €)', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)

    y_min, y_max = -12 , 17
    ax.set_ylim(ymin = y_min , ymax = y_max)
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Distributive_effects/Net_transfers/Net_transfers_uc_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))
    return

def graph_effort_rate(data,reform, elas_ext, elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
    fig, ax = plt.subplots(figsize=(10, 7.5))
    if elas_ext == True:
        sns.barplot(x="niveau_vie_decile", y = 'Effort_rate', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector', 'Douenne (2020) ext margin'], palette = palette_douenne, width = .9) 
    else: 
        if elas_vect == False :
            sns.barplot(x="niveau_vie_decile", y = 'Effort_rate', data = data, hue = 'ref_elasticity', hue_order = hue_order, palette = sns.color_palette("Paired"), width = .9)
        else : 
            sns.barplot(x="niveau_vie_decile", y = 'Effort_rate', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = palette_douenne, width = .9)
    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Additional taxes over disposable income (in %)', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)
    
    y_max = 0.2
    ax.set_ylim(ymin = 0 , ymax = y_max)
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Distributive_effects/Effort_rate/Effort_rate_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))
    return

def graph_CO2_emissions(data,reform, elas_ext, elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
    fig, ax = plt.subplots(figsize=(10, 7.5))
    if elas_ext == True:
        sns.barplot(x="niveau_vie_decile", y = 'emissions_CO2_carburants_carbon_tax_rv', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector', 'Douenne (2020) ext margin'], palette = palette_douenne, width = .9) 
    else: 
        if elas_vect == False :
            sns.barplot(x="niveau_vie_decile", y = 'emissions_CO2_carburants_carbon_tax_rv', data = data, hue = 'ref_elasticity', hue_order = hue_order , palette = sns.color_palette("Paired"), width = .9)
        else : 
            sns.barplot(x="niveau_vie_decile", y = 'emissions_CO2_carburants_carbon_tax_rv', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = palette_douenne, width = .9)

    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Emissions from transport fuel (in tCO2)', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)
    
    y_max = 3.5
    ax.set_ylim(ymin = 0 , ymax = y_max)
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Environmental_effects/CO2_emissions_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))
    return

def graph_delta_CO2(data,reform, elas_ext, elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
    fig, ax = plt.subplots(figsize=(10, 7.5)) 
    if elas_ext == True:
        sns.barplot(x="niveau_vie_decile", y = 'Reduction_CO2', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector', 'Douenne (2020) ext margin'], palette = palette_douenne, width = .9) 
    
    else:
        if elas_vect == False :
            sns.barplot(x="niveau_vie_decile", y = 'Reduction_CO2', data = data, hue = 'ref_elasticity', hue_order = hue_order , palette = sns.color_palette("Paired"), width = .9)
        else : 
            sns.barplot(x="niveau_vie_decile", y = 'Reduction_CO2', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = palette_douenne, width = .9)

    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Reduction in CO2 emissions from transport fuel (in %)', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)
    
    y_min = -9
    ax.set_ylim(ymin = y_min , ymax = 0)
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Environmental_effects/Delta_CO2_emissions_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))
    return

def graph_share_co2_emissions(data,reform, elas_ext, elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
    fig, ax = plt.subplots(figsize=(10, 7.5)) 
    if elas_ext == True:
        sns.barplot(x="niveau_vie_decile", y = 'Share_emissions_CO2', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector', 'Douenne (2020) ext margin'], palette = palette_douenne, width = .9) 
    else:
        if elas_vect == False :
            sns.barplot(x="niveau_vie_decile", y = 'Share_emissions_CO2', data = data, hue = 'ref_elasticity', hue_order = hue_order , palette = sns.color_palette("Paired"), width = .9)
        else : 
            sns.barplot(x="niveau_vie_decile", y = 'Share_emissions_CO2', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = palette_douenne, width = .9)
        
    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Share of total CO2 emissions from transport fuel (in %)', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Environmental_effects/Share_CO2_emissions_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))
    
def graph_share_emissions_reduction(data,reform, elas_ext, elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
    fig, ax = plt.subplots(figsize=(10, 7.5))
    if elas_ext == True:
        sns.barplot(x="niveau_vie_decile", y = 'Share_reduction_CO2', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector', 'Douenne (2020) ext margin'], palette = palette_douenne, width = .9) 
    else:   
        if elas_vect == False :
            sns.barplot(x="niveau_vie_decile", y = 'Share_reduction_CO2', data = data, hue = 'ref_elasticity', hue_order = hue_order , palette = sns.color_palette("Paired"), width = .9)
        else : 
            sns.barplot(x="niveau_vie_decile", y = 'Share_reduction_CO2', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = palette_douenne, width = .9)
        
    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Share of total CO2 emissions reduction from transport fuel (in %)', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Environmental_effects/Share_emissions_reduction_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))

def graph_ratio_emissions_reduction(data,reform,elas_ext,elas_vect,bonus_cheques_uc):
    hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
    palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
    data['ratio_reduction_emissions'] = data['Share_reduction_CO2']/data['Share_emissions_CO2']
    fig, ax = plt.subplots(figsize=(10, 7.5))
    if elas_ext == True:
        sns.barplot(x="niveau_vie_decile", y = 'ratio_reduction_emissions', data = data, hue = 'ref_elasticity', hue_order= ['Douenne (2020)', 'Douenne (2020) vector', 'Douenne (2020) ext margin'], palette = palette_douenne, width = .9) 
    else: 
        if elas_vect == False :
            sns.barplot(x="niveau_vie_decile", y = 'ratio_reduction_emissions', data = data, hue = 'ref_elasticity', hue_order = hue_order , palette = sns.color_palette("Paired"), width = .9)
        else : 
            sns.barplot(x="niveau_vie_decile", y = 'ratio_reduction_emissions', data = data, hue = 'ref_elasticity', hue_order = ['Douenne (2020)' , 'Douenne (2020) vector'], palette = palette_douenne, width = .9)
    
    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Share of total emissions reduction over share of total emissions', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Environmental_effects/Ratio_emissions_reduction_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))

def quantiles_for_boxplot(data,y,hue_order):
    out = pd.DataFrame(data = {'niveau_vie_decile' : [] , 'ref_elasticity': [] , y : []})
    i_ref = 0
    data = data[data['ref_elasticity'].isin(hue_order)]
    for ref in hue_order:
        data_ref = data[data['ref_elasticity'] == ref]
        for decile in set(data_ref['niveau_vie_decile']):
            data_decile = data_ref[data_ref['niveau_vie_decile'] == decile]
            plot_decile = decile + 0.7 + 0.1*i_ref  - 1
            for q in [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]:
                quantil = quantile(data_decile[y],data_decile['pondmen'],q)
                out = pd.concat([out,pd.DataFrame(data = {'niveau_vie_decile' : [decile] , 'plot_decile' : [plot_decile], 'ref_elasticity' : ref, y : [quantil], 'quantile' : [q]}),])
        i_ref +=1
    percentile_dict = { 0.01 : 'P1',
                       0.1 : 'P10 (D1)',
                       0.25 : 'P25 (Q1)',
                       0.5 : 'P50 (Median)',
                       0.75 : 'P75 (Q3)',
                       0.9 : 'P90 (D9)',
                       0.99 : 'P99',
                        }
    out['Percentile'] = out['quantile'].apply(lambda x : percentile_dict.get(x))
    return out

def subtitle_legend_boxplots(ax, legend_format, markers):
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
                percentile_index = legend_format['Percentile'].index(level)
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

def boxplot_net_transfers(data,reform,elas_ext,elas_vect,bonus_cheques_uc):
    legend_format = {'Percentile' : ['P1', 'P10 (D1)', 'P25 (Q1)', 'P50 (Median)', 'P75 (Q3)', 'P90 (D9)', 'P99']}
    markers = ['v', 'd', 'o', 'o', 'o' , 'd', '^']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    if elas_ext == True:
        hue_order = ['Douenne (2020)','Douenne (2020) vector','Douenne (2020) ext margin']
        palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
        palette = palette_douenne 
        quantiles_to_plot = quantiles_for_boxplot(data,'Net_transfers_reform',hue_order)
    else: 
        if elas_vect == False :
            hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
            palette = sns.color_palette("Paired") 
            quantiles_to_plot = quantiles_for_boxplot(data,'Net_transfers_reform',hue_order)
        else:
            hue_order = ['Douenne (2020)','Douenne (2020) vector']
            palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
            palette = palette_douenne 
            quantiles_to_plot = quantiles_for_boxplot(data,'Net_transfers_reform',hue_order)
    sns.scatterplot(data = quantiles_to_plot , x='plot_decile', y='Net_transfers_reform', hue = 'ref_elasticity',  
                    style = 'quantile',
                    hue_order = hue_order, 
                    palette = palette, 
                    markers = markers,
                    s = 60,
                    legend = True)
    
    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Net transfers per households (in €)', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)
    subtitle_legend_boxplots(ax, legend_format,markers)
    legend = ax.get_legend()
    legend.set_bbox_to_anchor((0.19, 0.3))
    ax.xaxis.set_ticks(range(1,11))
    y_min, y_max = -200 , 150
    ax.yaxis.set_ticks(range(y_min,y_max,50))
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Distributive_effects/Net_transfers/Boxplot_net_transfers_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))
    return

def boxplot_net_transfers_uc(data,reform,elas_ext,elas_vect,bonus_cheques_uc):
    legend_format = {'Percentile' : ['P1', 'P10 (D1)', 'P25 (Q1)', 'P50 (Median)', 'P75 (Q3)', 'P90 (D9)', 'P99']}
    markers = ['v', 'd', 'o', 'o', 'o' , 'd', '^']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    if elas_ext == True:
        hue_order = ['Douenne (2020)','Douenne (2020) vector','Douenne (2020) ext margin']
        legend_format = {'Elasticity reference' : hue_order,
                        'Percentile' : ['P1', 'P10 (D1)', 'P25 (Q1)', 'P50 (Median)', 'P75 (Q3)', 'P90 (D9)', 'P99']}
        palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
        palette = palette_douenne 
        quantiles_to_plot = quantiles_for_boxplot(data,'Net_transfers_reform_uc',hue_order)
    else:
        if elas_vect == False :
            hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
            palette = sns.color_palette("Paired") 
            quantiles_to_plot = quantiles_for_boxplot(data,'Net_transfers_reform_uc',hue_order)
        else:
            hue_order = ['Douenne (2020)','Douenne (2020) vector']
            palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
            palette = palette_douenne
            quantiles_to_plot = quantiles_for_boxplot(data,'Net_transfers_reform_uc',hue_order)
    sns.scatterplot(data = quantiles_to_plot , x='plot_decile', y='Net_transfers_reform_uc', hue = 'ref_elasticity',  
                    style = 'quantile',
                    hue_order = hue_order, 
                    palette = palette, 
                    markers = markers,
                    s = 60,
                    legend = True)
    
    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Net transfers per consumption unit (in €)', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)
    subtitle_legend_boxplots(ax, legend_format,markers)
    legend = ax.get_legend()
    legend.set_bbox_to_anchor((0.19, 0.3))
    ax.xaxis.set_ticks(range(1,11))
    y_min, y_max = -200 , 150
    ax.yaxis.set_ticks(range(y_min,y_max,50))
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Distributive_effects/Net_transfers/Boxplot_net_transfers_uc_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))
    return

def boxplot_effort_rate(data,reform,elas_ext,elas_vect,bonus_cheques_uc):
    markers = ['v', 'd', 'o', 'o', 'o' , 'd', '^']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    if elas_ext == True:
        hue_order = ['Douenne (2020)','Douenne (2020) vector','Douenne (2020) ext margin']
        legend_format = {'Elasticity reference' : hue_order,
                        'Percentile' : ['P1', 'P10 (D1)', 'P25 (Q1)', 'P50 (Median)', 'P75 (Q3)', 'P90 (D9)', 'P99']}
        palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
        palette = palette_douenne 
        quantiles_to_plot = quantiles_for_boxplot(data,'Effort_rate',hue_order)
    else:
        if elas_vect == False : 
            hue_order = ['Berry (2019)', 'Adam et al (2023)', 'Douenne (2020)', 'Combet et al (2009)', 'Ruiz & Trannoy (2008)','Rivers & Schaufele (2015)']
            legend_format = {'Elasticity reference' : hue_order,
                        'Percentile' : ['P1', 'P10 (D1)', 'P25 (Q1)', 'P50 (Median)', 'P75 (Q3)', 'P90 (D9)', 'P99']}
            palette = sns.color_palette("Paired") 
            quantiles_to_plot = quantiles_for_boxplot(data,'Effort_rate',hue_order)
        else:
            hue_order = ['Douenne (2020)','Douenne (2020) vector']
            legend_format = {'Elasticity reference' : hue_order,
                        'Percentile' : ['P1', 'P10 (D1)', 'P25 (Q1)', 'P50 (Median)', 'P75 (Q3)', 'P90 (D9)', 'P99']}
            palette_douenne = sns.color_palette([(0.6980392156862745, 0.8745098039215686, 0.5411764705882353), (1.0, 0.4980392156862745, 0.0), (0.9921568627450981, 0.7490196078431373, 0.43529411764705883)])
            palette = palette_douenne 
            quantiles_to_plot = quantiles_for_boxplot(data,'Effort_rate',hue_order)
    sns.scatterplot(data = quantiles_to_plot, x='plot_decile', y='Effort_rate', hue = 'ref_elasticity',  
                    style = 'quantile',
                    hue_order = hue_order, 
                    palette = palette, 
                    markers = markers,
                    s = 60,
                    legend = True)
    
    plt.xlabel('Income decile', fontdict= {'fontsize' : 15})
    plt.ylabel('Additional taxes over disposable income (in %)', fontdict= {'fontsize' : 15})
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.legend(fontsize = 12)
    subtitle_legend_boxplots(ax, legend_format,markers)
    legend = ax.get_legend()
    ax.xaxis.set_ticks(range(1,11))
    legend.set_bbox_to_anchor((0.71, 0.46))
    y_min, y_max = 0 , 1
    ax.set_ylim(y_min,y_max)
    plt.subplots_adjust(left=0.09, right=0.98, bottom=0.07, top=0.98)
    plt.savefig(os.path.join(output_path,'Figures/Distributive_effects/Effort_rate/Boxplot_effort_rate_reform_{}_elas_ext_{}_elas_vect_{}_bonus_cheques_uc_{}.pdf').format(reform.key[0],elas_ext,elas_vect,bonus_cheques_uc))
    return