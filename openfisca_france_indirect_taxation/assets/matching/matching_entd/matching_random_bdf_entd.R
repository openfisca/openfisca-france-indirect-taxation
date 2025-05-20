suppressPackageStartupMessages(library("configr"))
suppressPackageStartupMessages(library("StatMatch"))

config <- read.config(file = "C:/Users/veve1/.config/openfisca-survey-manager/config.ini")
assets_directory = config$openfisca_france_indirect_taxation$assets

# Import data
data_entd <- read.csv(file = file.path(assets_directory, "/matching/matching_entd/data_matching_entd.csv"), header = -1, sep=",")
data_bdf <- read.csv(file = file.path(assets_directory, "/matching/matching_entd/data_matching_bdf.csv"), header = -1, sep=",")

data_bdf$agepr = round(as.numeric(data_bdf$agepr), digits = 2)
data_bdf$npers = round(as.numeric(data_bdf$npers), digits = 2)
data_bdf$nactifs = round(as.numeric(data_bdf$nactifs), digits = 2)

# Compute random matching
out.nnd <- RANDwNND.hotdeck(
  data.rec = data_bdf, 
  data.don = data_entd,
  match.vars = c("nb_diesel", "agepr", "age_vehicule", "rural", "paris", "npers", "nactifs", "veh_tot"),
  don.class = c("niveau_vie_decile"),
  dist.fun = "Gower",
  weight.don = "pondmen"
  )

# Create fused file
fused.nnd.m <- create.fused(
  data.rec = data_bdf, 
  data.don = data_entd,
  mtc.ids = out.nnd$mtc.ids,
  z.vars = c("distance", "distance_autre_carbu", "distance_diesel", "distance_essence")
  )

write.csv(fused.nnd.m,
  file = file.path(assets_directory, "/matching/matching_entd/data_matched_random.csv")
  )
