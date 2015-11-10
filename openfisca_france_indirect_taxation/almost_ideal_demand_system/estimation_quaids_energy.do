clear
*2000:
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\almost_ideal_demand_system\data_frame_energy_2000.csv", delimiter(",")
quaids w1-w3, anot(5) prices(p1-p3) expenditure(depenses_par_uc) noquadratic
estat expenditure mu*
estat compensated ce*
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\almost_ideal_demand_system\data_quaids_2000.csv", delimiter(",") replace

*2005:
clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\almost_ideal_demand_system\data_frame_energy_2005.csv", delimiter(",")
quaids w1-w3, anot(5) prices(p1-p3) expenditure(depenses_par_uc) noquadratic
estat expenditure mu*
estat compensated ce*
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\almost_ideal_demand_system\data_quaids_2005.csv", delimiter(",") replace

*2011:
clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\almost_ideal_demand_system\data_frame_energy_2011.csv", delimiter(",")
quaids w1-w3, anot(5) prices(p1-p3) expenditure(depenses_par_uc) noquadratic
estat expenditure mu*
estat compensated ce*
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\almost_ideal_demand_system\data_quaids_2011.csv", delimiter(",") replace
