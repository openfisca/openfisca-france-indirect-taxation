clear
*2000:
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_2000.csv", delimiter(",")
quaids w1-w4, anot(5) prices(p1-p4) expenditure(depenses_par_uc) noquadratic
estat expenditure mu*
estat uncompensated ce*
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_quaids_2000.csv", delimiter(",") replace

*2005:
clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_2005.csv", delimiter(",")
quaids w1-w4, anot(5) prices(p1-p4) expenditure(depenses_par_uc) noquadratic
estat expenditure mu*
estat uncompensated ce*
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\data_quaids_2005.csv", delimiter(",") replace

*2011:
clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_2011.csv", delimiter(",")
quaids w1-w4, anot(5) prices(p1-p4) expenditure(depenses_par_uc) noquadratic
estat expenditure mu*
estat uncompensated ce*
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_quaids_2011.csv", delimiter(",") replace

*If we introduce some selection, i.e. if we focus on those with w1>0:

clear
*2000:
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_2000.csv", delimiter(",")
replace w1 = . if w1 == 0
quaids w1-w4, anot(5) prices(p1-p4) expenditure(depenses_par_uc) noquadratic
*estat uncompensated, atmeans
*matrix list r(uncompelas)
*estat expenditure, atmeans
*matrix list r(expelas)
estat expenditure mu*
estat uncompensated ce*
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_quaids_2000.csv", delimiter(",") replace

*2005:
clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_2005.csv", delimiter(",")
replace w1 = . if w1 == 0
quaids w1-w4, anot(5) prices(p1-p4) expenditure(depenses_par_uc) noquadratic
*estat uncompensated, atmeans
*matrix list r(uncompelas)
*estat expenditure, atmeans
*matrix list r(expelas)
estat expenditure mu*
estat uncompensated ce*
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\data_quaids_2005.csv", delimiter(",") replace

*2011:
clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_2011.csv", delimiter(",")
replace w1 = . if w1 == 0
quaids w1-w4, anot(5) prices(p1-p4) expenditure(depenses_par_uc) noquadratic
*estat uncompensated, atmeans
*matrix list r(uncompelas)
*estat expenditure, atmeans
*matrix list r(expelas)
estat expenditure mu*
estat uncompensated ce*
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_quaids_2011.csv", delimiter(",") replace

*Still with selection, if we use demographics and the quadratic specification: we control for age, the number of persons in the household, the type of area, whether they own their house, and time fixed effects

clear
*2000:
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_2000.csv", delimiter(",")
replace w1 = . if w1 == 0
quaids w1-w4, anot(5) prices(p1-p4) expenditure(depenses_par_uc) demographics(agepr nactifs nenfants vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 villes_petites villes_grandes agglo_paris proprietaire elect_only)
estat uncompensated, atmeans
matrix list r(uncompelas)
estat expenditure, atmeans
matrix list r(expelas)

*2005:
clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_2005.csv", delimiter(",")
replace w1 = . if w1 == 0
quaids w1-w4, anot(5) prices(p1-p4) expenditure(depenses_par_uc) demographics(agepr nactifs nenfants vag_18 vag_19 vag_20 vag_21 vag_22 villes_petites villes_grandes agglo_paris proprietaire elect_only)
estat uncompensated, atmeans
matrix list r(uncompelas)
estat expenditure, atmeans
matrix list r(expelas)

*2011:
clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_2011.csv", delimiter(",")
replace w1 = . if w1 == 0
quaids w1-w4, anot(5) prices(p1-p4) expenditure(depenses_par_uc) demographics(agepr nactifs nenfants vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris proprietaire elect_only)
estat uncompensated, atmeans
matrix list r(uncompelas)
estat expenditure, atmeans
matrix list r(expelas)

*To compute bootstrap standard errors, add vce(bootstrap) at the end of the quaids line
