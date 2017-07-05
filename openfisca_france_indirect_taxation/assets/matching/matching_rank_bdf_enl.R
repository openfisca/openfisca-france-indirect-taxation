# Import data
data_enl <- read.csv(file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/data_matching_enl.csv", header = -1, sep=",")
data_bdf <- read.csv(file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/data_matching_bdf.csv", header = -1, sep=",")

# Compute ranked matching
out.nnd <- rankNND.hotdeck(
  data.rec = data_bdf, data.don = data_enl,
  var.rec = c("part_energies_revtot"),
  don.class = c("decile_revtot"),
  weight.rec = "pondmen",
  weight.don = "pondmen"
)

# Create fused file
fused.nnd.m <- create.fused(
  data.rec = data_bdf, data.don = data_enl,
  mtc.ids = out.nnd$mtc.ids,
  z.vars = c("gchauf_n", "gchauf_1", "gchauf_2", "gchauf_3", "gchauf_4",
             "gchauf_5", "gchauf_6", "gchauf_7", "gchaufs_1",
             "gchaufs_2", "gchaufs_3", "gchaufs_4", "gchaufs_5",
             "gmur", "gtoit2")
)

# Save it as csv
write.csv(fused.nnd.m,
          file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/data_matched_rank.csv"
)
