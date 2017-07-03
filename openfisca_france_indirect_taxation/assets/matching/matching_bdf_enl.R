# Import data
data_enl <- read.csv(file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/data_matching_enl_small.csv", header = -1, sep=",")
data_bdf <- read.csv(file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/data_matching_bdf_small.csv", header = -1, sep=",")

# Compute matching
out.nnd <- NND.hotdeck(
  data.rec = data_bdf, data.don = data_enl,
  match.vars = c("surfhab_d", "nbphab", "ocde10", "revtot", "poste_coicop_451",
                 "poste_coicop_452", "poste_coicop_453", "agepr", "aba",
                 "cataeu", "tau", "tuu", "zeat")
)

# Create fused file
fused.nnd.m <- create.fused(
  data.rec = data_bdf, data.don = data_enl,
  mtc.ids = out.nnd$mtc.ids,
  z.vars = c("gchauf_1", "gchauf_2", "gchauf_3", "gchauf_4",
             "gchauf_5", "gchauf_6", "gchauf_7", "gchaufs_1",
             "gchaufs_2", "gchaufs_3", "gchaufs_4", "gchaufs_4",
             "gmur", "gtoit2",
             "part_energies_revenu")
)

# Save it as csv
write.csv(fused.nnd.m,
          file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/data_matched_small.csv")
