suppressPackageStartupMessages(library("configr"))
suppressPackageStartupMessages(library("StatMatch"))

config <- read.config(file = "C:/Users/veve1/.config/openfisca-survey-manager/config.ini")
assets_directory = config$openfisca_france_indirect_taxation$assets

data_entd <- read.csv(file = file.path(assets_directory, "/matching/matching_entd/data_matching_entd.csv"), header = -1, sep=",")
data_bdf <- read.csv(file = file.path(assets_directory, "/matching/matching_entd/data_matching_bdf.csv"), header = -1, sep=",")

# Set a seed for reproducibility (When two or more donor records have the exact same distance to a recipient, the algorithm must randomly select one)
set.seed(1234)

# Compute ranked matching
out.nnd <- rankNND.hotdeck(
  data.rec = data_bdf, 
  data.don = data_entd,
  var.rec = c("poste_07_2_2_1"),
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
  file = file.path(assets_directory, "/matching/matching_entd/data_matched_rank.csv")
  )
