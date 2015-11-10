clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\almost_ideal_demand_system\data_frame_energy_2005.csv", delimiter(",")
quaids w1-w3, anot(5) prices(p1-p3) expenditure(depenses_par_uc) noquadratic
*quaids w1-w3, anot(5) prices(p1-p3) expenditure(depenses_par_uc) demographics(typmen fumeur)

estat expenditure mu*
estat compensated ce*

estat expenditure, atmeans
matrix list r(expelas)
estat compensated, atmeans
matrix list r(compelas)

outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\almost_ideal_demand_system\data_quaids_2005.csv", delimiter(",") replace
