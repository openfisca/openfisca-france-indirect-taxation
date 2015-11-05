clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\almost_ideal_demand_system\data_frame_energy.csv", delimiter(",")
quaids w1-w3, anot(5) prices(p1-p3) expenditure(depenses_par_uc) noquadratic
*quaids w1-w3, anot(5) prices(p1-p3) expenditure(depenses_par_uc) demographics(typmen fumeur)
estat expenditure, atmeans
matrix list r(expelas)
estat compensated, atmeans
matrix list r(compelas)
