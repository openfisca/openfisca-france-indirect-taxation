# Import data
data_entd <- read.csv(file = "C:/Users/t.douenne/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/matching_entd/data_matching_entd.csv", header = -1, sep=",")
data_bdf <- read.csv(file = "C:/Users/t.douenne/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/matching_entd/data_matching_bdf.csv", header = -1, sep=",")

# Compute ranked matching
out.nnd <- rankNND.hotdeck(
  data.rec = data_bdf, data.don = data_entd,
  var.rec = c("poste_coicop_722"),
  var.don = c("distance"),
  don.class = c("niveau_vie_decile", "rural"),
  weight.rec = "pondmen",
  weight.don = "pondmen"
)

# Create fused file
fused.nnd.m <- create.fused(
  data.rec = data_bdf, data.don = data_entd,
  mtc.ids = out.nnd$mtc.ids,
  z.vars = c("distance", "distance_autre_carbu", "distance_diesel", "distance_essence")
)

# Save it as csv
write.csv(fused.nnd.m,
          file = "C:/Users/t.douenne/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/matching_entd/data_matched_rank.csv"
)
