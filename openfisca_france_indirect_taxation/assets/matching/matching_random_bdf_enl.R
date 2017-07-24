# Import data
data_enl <- read.csv(file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/data_matching_enl.csv", header = -1, sep=",")
data_bdf <- read.csv(file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/data_matching_bdf.csv", header = -1, sep=",")

# Compute random matching
out.nnd <- RANDwNND.hotdeck(
  data.rec = data_bdf, data.don = data_enl,
  match.vars = c("part_energies_revtot", "log_indiv", "electricite", "ouest_sud",
                 "nactifs", "dip14pr", "bat_av_49", "bat_49_74", "revtot", "rural", "nenfants",
                 "petite_ville", "surfhab_d"),
  don.class = c("donation_class_1"),
  dist.fun = "Gower",
  weight.don = "pondmen"
)

# Create fused file
fused.nnd.m <- create.fused(
  data.rec = data_bdf, data.don = data_enl,
  mtc.ids = out.nnd$mtc.ids,
  z.vars = c("froid", "gchauf_1", "gchauf_2", "froid_cout", "froid_isolation",
             "gchauf_5", "gchauf_6", "gchauf_7", "gchaufs_1",
             "gchaufs_2", "gchaufs_3", "gchaufs_4", "gchaufs_5",
             "gmur", "gtoit2")
)

# Save it as csv
write.csv(fused.nnd.m,
          file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/data_matched_random.csv"
)
