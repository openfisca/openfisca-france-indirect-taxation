# Import data
data_entd <- read.csv(file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/matching_entd/data_matching_entd.csv", header = -1, sep=",")
data_bdf <- read.csv(file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/matching_entd/data_matching_bdf.csv", header = -1, sep=",")

# Compute random matching
out.nnd <- RANDwNND.hotdeck(
  data.rec = data_bdf, data.don = data_entd,
  match.vars = c("nb_diesel", "agepr", "age_vehicule", "rural", "paris", "npers", "nactifs", "veh_tot"),
  don.class = c("niveau_vie_decile"),
  dist.fun = "Gower",
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
          file = "C:/Users/Thomas/Documents/GitHub/openfisca-france-indirect-taxation/openfisca_france_indirect_taxation/assets/matching/matching_entd/data_matched_random.csv"
)
