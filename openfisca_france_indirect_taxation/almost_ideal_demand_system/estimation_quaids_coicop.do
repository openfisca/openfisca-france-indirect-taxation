clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\data_frame_r_2005_by_coicop.csv", delimiter(",")
quaids w1-w9, anot(5) prices(p1-p9) expenditure(depenses_reelles)
*quaids w1-w12, anot(5) prices(p1-p12) expenditure(depenses_reelles) demographics(typmen fumeur temps)
estat expenditure, atmeans
matrix list r(expelas)
estat compensated, atmeans
matrix list r(compelas)
