*AIDS model, no quadratic term, no demographics, no selection

*all years:
clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_all_years.csv", delimiter(",")
tostring ident_men, replace format(%17.0g)
replace w1 = . if w1 == 0
quaids w1-w4, anot(5) prices(p1-p4) expenditure(depenses_par_uc) noquadratic
*estat uncompensated, atmeans
*matrix list r(uncompelas)
*estat expenditure, atmeans
*matrix list r(expelas)
estat expenditure elas_exp*
estat uncompensated elas_price*
*tostring ident_men, replace
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_aids_all.csv", delimiter(",") replace



*AIDS model, if we introduce some selection, i.e. if we focus on those with w1>0:

clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_all_years.csv", delimiter(",")
replace w1 = . if w1 == 0
quaids w1-w4, anot(5) prices(p1-p4) expenditure(depenses_par_uc) noquadratic
*estat uncompensated, atmeans
*matrix list r(uncompelas)
*estat expenditure, atmeans
*matrix list r(expelas)
estat expenditure mu*
estat uncompensated ce*
tostring ident_men, replace
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_aids_all.csv", delimiter(",") replace
