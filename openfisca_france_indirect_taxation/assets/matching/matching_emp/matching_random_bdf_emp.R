suppressPackageStartupMessages(library("configr"))
suppressPackageStartupMessages(library("StatMatch"))
library(diplyr)

config <- read.config(file = "C:/Users/veve1/.config/openfisca-survey-manager/config.ini")
assets_directory = config$openfisca_france_indirect_taxation$assets

# Import data
data_emp <- read.csv(file = file.path(assets_directory, "/matching/matching_emp/data_matching_emp.csv"), header = -1, sep=",")
data_bdf <- read.csv(file = file.path(assets_directory, "/matching/matching_emp/data_matching_bdf.csv"), header = -1, sep=",")

vars <- c("nb_diesel", "agepr", "age_vehicule", "rural", "paris", 
          "npers", "nactifs", "veh_tot")

# Coerce to numeric in both datasets
num_vars <- c("nb_diesel", "agepr", "age_vehicule", "npers", "nactifs", "veh_tot")
cat_vars <- c("rural", "paris")

# Recast in both datasets
data_bdf <- data_bdf %>%
  mutate(across(all_of(num_vars), as.numeric)) %>%
  mutate(across(all_of(cat_vars), as.factor))

data_emp <- data_emp %>%
  mutate(across(all_of(num_vars), as.numeric)) %>%
  mutate(across(all_of(cat_vars), as.factor))

# Set a seed for reproducibility
set.seed(1234)

# Compute random matching
out.nnd <- RANDwNND.hotdeck(
  data.rec = data_bdf, 
  data.don = data_emp,
  match.vars = c("nb_diesel", "agepr", "age_vehicule", "rural", "paris", "npers", "nactifs", "veh_tot"),
  don.class = c("niveau_vie_decile"),
  dist.fun = "Gower",
  weight.don = "pondmen"
  )

# Create fused file
fused.nnd.m <- create.fused(
  data.rec = data_bdf, 
  data.don = data_emp,
  mtc.ids = out.nnd$mtc.ids,
  z.vars = c("distance", "distance_autre_carbu", "distance_diesel", "distance_essence")
  )

write.csv(fused.nnd.m,
  file = file.path(assets_directory, "/matching/matching_emp/data_matched_random.csv"),
  row.names =  FALSE
  )
