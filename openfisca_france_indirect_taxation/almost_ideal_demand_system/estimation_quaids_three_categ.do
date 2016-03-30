*If we want to study (1) fuel, (2) housing energy and (3) all the rest:

clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_no_alime_all_years.csv", delimiter(",")
replace w1 = . if w1 == 0
quaids w1-w3, anot(5) prices(p1-p3) expenditure(depenses_par_uc) demographics(agepr nactifs nenfants vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 vag_17 vag_18 vag_19 vag_20 vag_21 vag_22 vag_23 vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris proprietaire elect_only)
*estat uncompensated, atmeans
*matrix list r(uncompelas)
*estat expenditure, atmeans
*matrix list r(expelas)
estat expenditure mu*
estat uncompensated ce*
tostring ident_men, replace
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_quaids_energy_no_alime_all.csv", delimiter(",") replace

*If now we want to focus on those who do not consume only electricity: 

clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_no_elect_only_no_alime_all_years.csv", delimiter(",")
tostring ident_men, replace format(%17.0g)
replace w1 = . if w1 == 0
quaids w1-w3, anot(5) prices(p1-p3) expenditure(depenses_par_uc) demographics(agepr nactifs nenfants vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 vag_17 vag_18 vag_19 vag_20 vag_21 vag_22 vag_23 vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris proprietaire)
*estat uncompensated, atmeans
*matrix list r(uncompelas)
*estat expenditure, atmeans
*matrix list r(expelas)
estat expenditure elas_exp*
estat uncompensated elas_price*
*tostring ident_men, replace
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_quaids_all_no_elect_only_no_alime.csv", delimiter(",") replace




*QAIDS model, if now we restrict our analysis to the fuel only, i.e. without including housing energy in a specific category:

*The three years taken together:
clear
insheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_carbu_all_years.csv", delimiter(",")
replace w1 = . if w1 == 0
quaids w1-w3, anot(5) prices(p1-p3) expenditure(depenses_par_uc) demographics(agepr nactifs nenfants vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 vag_17 vag_18 vag_19 vag_20 vag_21 vag_22 vag_23 vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris)
estat uncompensated, atmeans
matrix list r(uncompelas)
estat expenditure, atmeans
matrix list r(expelas)
estat expenditure mu*
estat uncompensated ce*
tostring ident_men, replace
outsheet using "C:\Users\thomas.douenne\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_quaids_carbu_all.csv", delimiter(",") replace
