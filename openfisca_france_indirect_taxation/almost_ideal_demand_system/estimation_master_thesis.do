*w1: Transport fuels / w2: Housing energy / w3: Other non-durable goods

* Global estimates
clear
insheet using "C:\Users\Thomas\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_no_alime_all_years.csv", delimiter(",")
tostring ident_men, replace format(%17.0g)
replace w1 = . if w1 == 0

aidsills w1-w3, prices(p1-p3) expenditure(depenses_par_uc) intercept(agepr nactifs nenfants diesel vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 vag_17 vag_18 vag_19 vag_20 vag_21 vag_22 vag_23 vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris proprietaire elect_only froid) quadratic alpha_0(5)

aidsills_elas

* Global estimates for 2011
clear
insheet using "C:\Users\Thomas\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_no_alime_2011.csv", delimiter(",")
tostring ident_men, replace format(%17.0g)
replace w1 = . if w1 == 0

aidsills w1-w3, prices(p1-p3) expenditure(depenses_par_uc) intercept(agepr nactifs nenfants vag_24 vag_25 vag_26 vag_27 vag_28 agglo_paris proprietaire elect_only) quadratic alpha_0(5)

aidsills_elas


* Estimates on rural households
clear
insheet using "C:\Users\Thomas\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_no_alime_all_years.csv", delimiter(",")
tostring ident_men, replace format(%17.0g)
replace w1 = . if w1 == 0

aidsills w1-w3, prices(p1-p3) expenditure(depenses_par_uc) intercept(agepr nactifs nenfants vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 vag_17 vag_18 vag_19 vag_20 vag_21 vag_22 vag_23 vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris proprietaire elect_only) quadratic alpha_0(5)

aidsills_elas if rural == 1


* Estimates on low income group
clear
insheet using "C:\Users\Thomas\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_no_alime_all_years.csv", delimiter(",")
tostring ident_men, replace format(%17.0g)
replace w1 = . if w1 == 0
egen median_expenditures = median(depenses_par_uc)

aidsills w1-w3, prices(p1-p3) expenditure(depenses_par_uc) intercept(agepr nactifs nenfants vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 vag_17 vag_18 vag_19 vag_20 vag_21 vag_22 vag_23 vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris proprietaire elect_only) quadratic alpha_0(5)

aidsills_elas if depenses_par_uc < median_expenditures


* Estimates on high income group
clear
insheet using "C:\Users\Thomas\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_no_alime_all_years.csv", delimiter(",")
tostring ident_men, replace format(%17.0g)
replace w1 = . if w1 == 0
egen median_expenditures = median(depenses_par_uc)

aidsills w1-w3, prices(p1-p3) expenditure(depenses_par_uc) intercept(agepr nactifs nenfants vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 vag_17 vag_18 vag_19 vag_20 vag_21 vag_22 vag_23 vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris proprietaire elect_only) quadratic alpha_0(5)

aidsills_elas if depenses_par_uc > median_expenditures


* Estimates on those who felt cold in winter
clear
insheet using "C:\Users\Thomas\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_no_alime_all_years.csv", delimiter(",")
tostring ident_men, replace format(%17.0g)
replace w1 = . if w1 == 0
egen median_expenditures = median(depenses_par_uc)

aidsills w1-w3, prices(p1-p3) expenditure(depenses_par_uc) intercept(agepr nactifs nenfants vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 vag_17 vag_18 vag_19 vag_20 vag_21 vag_22 vag_23 vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris proprietaire elect_only) quadratic alpha_0(5)

aidsills_elas if froid == 1


* Estimates on electricity only
clear
insheet using "C:\Users\Thomas\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_no_alime_all_years.csv", delimiter(",")
tostring ident_men, replace format(%17.0g)
replace w1 = . if w1 == 0
egen median_expenditures = median(depenses_par_uc)

aidsills w1-w3, prices(p1-p3) expenditure(depenses_par_uc) intercept(agepr nactifs nenfants vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 vag_17 vag_18 vag_19 vag_20 vag_21 vag_22 vag_23 vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris proprietaire elect_only) quadratic alpha_0(5)

aidsills_elas if elect_only == 1


* Estimates on gas and domestic fuel consumers
clear
insheet using "C:\Users\Thomas\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_no_alime_all_years.csv", delimiter(",")
tostring ident_men, replace format(%17.0g)
replace w1 = . if w1 == 0
egen median_expenditures = median(depenses_par_uc)

aidsills w1-w3, prices(p1-p3) expenditure(depenses_par_uc) intercept(agepr nactifs nenfants vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 vag_17 vag_18 vag_19 vag_20 vag_21 vag_22 vag_23 vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris proprietaire elect_only) quadratic alpha_0(5)

aidsills_elas if elect_only == 0


*Global estimates using quaids command
clear
insheet using "C:\Users\Thomas\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_frame_energy_no_alime_all_years.csv", delimiter(",")
tostring ident_men, replace format(%17.0g)
replace w1 = . if w1 == 0
quaids w1-w3, anot(5) prices(p1-p3) expenditure(depenses_par_uc) demographics(agepr nactifs nenfants vag_10 vag_11 vag_12 vag_13 vag_14 vag_15 vag_16 vag_17 vag_18 vag_19 vag_20 vag_21 vag_22 vag_23 vag_24 vag_25 vag_26 vag_27 vag_28 villes_petites villes_grandes agglo_paris proprietaire diesel froid elect_only)
estat expenditure elas_exp*
estat uncompensated elas_price*
estat compensated comp_price*
tostring ident_men, replace
outsheet using "C:\Users\Thomas\Documents\GitHub\openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\quaids\data_quaids_energy_no_alime_all.csv", delimiter(",") replace
