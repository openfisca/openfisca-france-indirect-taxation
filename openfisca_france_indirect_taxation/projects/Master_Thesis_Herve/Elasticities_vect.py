import pandas as pd


# To create a dataframe with elasticities from Douenne (2020)
table_data = {
    'niveau_vie_decile': ['Rural', 'Small cities', 'Medium cities', 'Large cities', 'Paris'],
    1.0: [(-0.54,-0.43), (-0.55,-0.39), (-0.58,-0.37), (-0.55,-0.21), (-0.49,-0.01)],
    2.0: [(-0.54,-0.43), (-0.54,-0.37), (-0.56,-0.34), (-0.54,-0.21), (-0.45,-0.01)],
    3.0: [(-0.52,-0.39), (-0.53,-0.35), (-0.56,-0.32), (-0.51,-0.16), (-0.47,0.07)],
    4.0: [(-0.52,-0.37), (-0.51,-0.34), (-0.53,-0.29), (-0.50,-0.13), (-0.44,0.04)],
    5.0: [(-0.51,-0.35), (-0.50,-0.33), (-0.54,-0.28), (-0.47,-0.10), (-0.42,0.06)],
    6.0: [(-0.49,-0.32), (-0.50,-0.29), (-0.51,-0.26), (-0.47,-0.08), (-0.36,0.14)],
    7.0: [(-0.48,-0.29), (-0.46,-0.25), (-0.48,-0.23), (-0.44,-0.04), (-0.41,0.14)],
    8.0: [(-0.45,-0.27), (-0.44,-0.22), (-0.46,-0.23), (-0.42,-0.02), (-0.34,0.22)],
    9.0: [(-0.45,-0.26), (-0.42,-0.20), (-0.44,-0.19), (-0.36,0.05), (-0.29,0.32)],
    10.0: [(-0.38,-0.28), (-0.37,-0.20), (-0.37,-0.19), (-0.30,0.08), (-0.17,0.38)]
}

df_elas = pd.DataFrame(table_data)
# reshape it a bit
df_elas = df_elas.T
df_elas.reset_index(inplace= True)
df_elas.rename(columns = df_elas.iloc[0],inplace = True)
df_elas.drop(index = 0, axis = 0, inplace = True)
df_elas['ref_elasticity'] = 'Douenne (2020) vector'
# Write the DataFrame to a CSV file
df_elas.to_csv(os.path.join(data_path,'Elasticities_Douenne_20.csv'))