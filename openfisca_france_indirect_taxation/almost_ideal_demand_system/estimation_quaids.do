clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\almost_ideal_demand_system\data_frame_for_stata.csv", delimiter(",")
*quaids w1-w9, anot(10) prices(p1-p9) expenditure(depenses_reelles) noquadratic
quaids w1-w9, anot(5) prices(p1-p9) expenditure(depenses_reelles) demographics(typmen fumeur d1 d2 d3 d4 d5 d6 d7 d8 d9)
estat expenditure, atmeans
matrix list r(expelas)
estat compensated, atmeans
matrix list r(compelas)
