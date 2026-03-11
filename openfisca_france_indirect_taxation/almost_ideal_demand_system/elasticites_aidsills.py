import os
import pandas as pd


from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.reforms.officielle_2018_in_2016 import reforme_officielle_2018_in_2016
from openfisca_france_indirect_taxation.utils import assets_directory


###########
#   WIP   #
###########

##############
#   TO DO :  #
# Pull the modif from the desk computer
# Check the sorting does not create anything odd
# Adapt all the other scripts used in the paper to these new elasticities
# Do some tests to verify they work correctly
# Check they match households correctly
##############


year = 2016
data_year = 2011

survey_scenario = SurveyScenario.create(reform=reforme_officielle_2018_in_2016, year=year, data_year=data_year)

simulated_variables = [
    "strate",
    "niveau_vie_decile",
]

df = survey_scenario.create_data_frame_by_entity(simulated_variables, period=year)["menage"]

elasticities = {
    "elas_0_1": [-0.544, -0.428],
    "elas_0_2": [-0.543, -0.426],
    "elas_0_3": [-0.522, -0.393],
    "elas_0_4": [-0.515, -0.366],
    "elas_0_5": [-0.509, -0.353],
    "elas_0_6": [-0.487, -0.315],
    "elas_0_7": [-0.481, -0.291],
    "elas_0_8": [-0.453, -0.272],
    "elas_0_9": [-0.451, -0.264],
    "elas_0_10": [-0.377, -0.278],
    "elas_1_1": [-0.551, -0.394],
    "elas_1_2": [-0.541, -0.369],
    "elas_1_3": [-0.532, -0.353],
    "elas_1_4": [-0.507, -0.337],
    "elas_1_5": [-0.499, -0.326],
    "elas_1_6": [-0.501, -0.285],
    "elas_1_7": [-0.460, -0.246],
    "elas_1_8": [-0.439, -0.219],
    "elas_1_9": [-0.424, -0.196],
    "elas_1_10": [-0.368, -0.201],
    "elas_2_1": [-0.580, -0.368],
    "elas_2_2": [-0.560, -0.340],
    "elas_2_3": [-0.556, -0.320],
    "elas_2_4": [-0.526, -0.286],
    "elas_2_5": [-0.535, -0.275],
    "elas_2_6": [-0.508, -0.258],
    "elas_2_7": [-0.482, -0.227],
    "elas_2_8": [-0.462, -0.230],
    "elas_2_9": [-0.437, -0.188],
    "elas_2_10": [-0.370, -0.186],
    "elas_3_1": [-0.549, -0.209],
    "elas_3_2": [-0.537, -0.206],
    "elas_3_3": [-0.511, -0.162],
    "elas_3_4": [-0.502, -0.127],
    "elas_3_5": [-0.471, -0.102],
    "elas_3_6": [-0.474, -0.084],
    "elas_3_7": [-0.439, -0.036],
    "elas_3_8": [-0.421, -0.022],
    "elas_3_9": [-0.362, 0.048],
    "elas_3_10": [-0.300, 0.083],
    "elas_4_1": [-0.490, -0.013],
    "elas_4_2": [-0.445, -0.008],
    "elas_4_3": [-0.466, 0.068],
    "elas_4_4": [-0.440, 0.041],
    "elas_4_5": [-0.417, 0.060],
    "elas_4_6": [-0.356, 0.137],
    "elas_4_7": [-0.409, 0.144],
    "elas_4_8": [-0.344, 0.221],
    "elas_4_9": [-0.293, 0.320],
    "elas_4_10": [-0.167, 0.376],
}

aidsills_elas = pd.DataFrame(elasticities).transpose()
aidsills_elas.rename(columns={0: "elas_price_1_1", 1: "elas_price_2_2"}, inplace=True)

# Construction d'un index commun pour le merge :
df = df.astype(str)
df["index_nvd_area"] = df["strate"] + "_" + df["niveau_vie_decile"]
aidsills_elas = aidsills_elas.reset_index()
aidsills_elas.rename(columns={"index": "index_nvd_area"}, inplace=True)
aidsills_elas["index_nvd_area"] = aidsills_elas["index_nvd_area"].str[5:]

elasticites_new = pd.merge(df, aidsills_elas, how="left", on="index_nvd_area")
elasticites_new = elasticites_new.reset_index()
elasticites_new.rename(columns={"index": "ident_men"}, inplace=True)


def create_data_elasticities_aidsills():
    data_quaids = pd.read_csv(os.path.join(assets_directory, "quaids", "data_quaids_energy_no_alime_all.csv"), sep=",")

    data_quaids.drop(["elas_price_1_1", "elas_price_2_2"], axis=1, inplace=True)
    data_quaids.strate = data_quaids.strate.astype(str)
    data_quaids.niveau_vie_decile = data_quaids.niveau_vie_decile.astype(str)
    data_quaids["index_nvd_area"] = data_quaids["strate"] + "_" + data_quaids["niveau_vie_decile"]
    data_quaids = data_quaids.merge(aidsills_elas, on="index_nvd_area")

    liste_elasticities = [column for column in data_quaids.columns if column[:4] == "elas"]
    data_quaids[liste_elasticities] = data_quaids[liste_elasticities].astype("float32")
    dataframe = data_quaids[liste_elasticities + ["ident_men", "year"]].copy()

    dataframe = dataframe.fillna(0)
    # dataframe = dataframe.query('year == 2011')

    assert not dataframe.ident_men.duplicated().any(), "Some housholds are duplicated"

    return dataframe.to_csv(
        os.path.join(assets_directory, "quaids", "data_elasticities_energy_no_alime_all.csv"), sep=","
    )


def get_elasticities_aidsills(data_year, non_positive):
    data_elasticities = pd.read_csv(
        os.path.join(assets_directory, "quaids", "data_elasticities_energy_no_alime_all.csv"), sep=","
    )
    liste_elasticities = [column for column in data_elasticities.columns if column[:4] == "elas"]
    dataframe = data_elasticities[liste_elasticities + ["ident_men", "year"]].copy()
    data_year = data_year

    dataframe = dataframe.query("year == @data_year").copy()

    if non_positive:
        dataframe.elas_price_1_1 = 0 + dataframe.elas_price_1_1 * (dataframe.elas_price_1_1 < 0)
        dataframe.elas_price_2_2 = 0 + dataframe.elas_price_2_2 * (dataframe.elas_price_2_2 < 0)

    return dataframe


if __name__ == "__main__":
    year = 2011
    create_data_elasticities_aidsills()
    df = get_elasticities_aidsills(year, True)
    df_false = get_elasticities_aidsills(year, False)
