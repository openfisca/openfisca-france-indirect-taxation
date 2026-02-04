# -*- coding: utf-8 -*-
# Compare les distances de hellinger et les histogrammes (ou boxplots) des variables utilisées pour l'appariement.
import os
import matplotlib.pyplot as plt
import pandas as pd

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_2_homogenize_variables import create_niveau_vie_quantiles
from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_3_1_compute_hellinger_distance import hellinger_distance
from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_3_2_compute_histograms import histogram_cat_variable, boxplot_variable


output_path = "C:/Users/veve1/OneDrive/Documents/ENSAE PhD/Carbon tax/Output/Figures"
data_bdf, data_entd = create_niveau_vie_quantiles(2017)


matching_varlist = ["nb_diesel", "agepr", "age_vehicule", "rural", "paris", "npers", "nactifs", "veh_tot"]
hellinger_distances = {var: hellinger_distance(data_bdf, data_entd, var = var, weight_col = 'pondmen')[2] for var in matching_varlist}
df_hellinger_distance = pd.DataFrame(hellinger_distances.items(), columns=['Variable', 'Hellinger Distance'])
df_hellinger_distance.to_csv(os.path.join(output_path, "hellinger_distances.csv"), index=False)


for var in ['agepr', 'age_vehicule', 'ocde10']:
    ax = boxplot_variable(data_bdf, data_entd, var = var, savefig=True, filename = os.path.join(output_path, f'Matching_bdf_emp/boxplot_{var}.pdf'))
    plt.close()

for var in ['nactifs', 'nb_diesel', 'nb_essence', 'nenfants', 'niveau_vie_decile', 'npers', 'situapr', 'typmen', 'tuu', 'rural', 'paris', 'veh_tot']:
    ax = histogram_cat_variable(data_bdf, data_entd, var = var, savefig=True, filename = os.path.join(output_path, f'Matching_bdf_emp/histogram_{var}.pdf'))
    plt.close()