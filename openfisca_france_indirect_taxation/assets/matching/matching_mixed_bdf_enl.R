# Import data
data_enl <- read.csv(file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/data_matching_enl.csv", header = -1, sep=",")
data_bdf <- read.csv(file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/data_matching_bdf.csv", header = -1, sep=",")

mtc.1 <- mixed.mtc(
  data.rec = data_bdf, data.don = data_enl,
  match.vars = c("surfhab_d", "part_energies_revtot", "agepr"),
  y.rec = "ident_men", z.don = "idlog",
  micro = TRUE
  )
