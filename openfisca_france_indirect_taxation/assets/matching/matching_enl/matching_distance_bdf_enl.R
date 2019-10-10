suppressPackageStartupMessages(library("configr"))
suppressPackageStartupMessages(library("StatMatch"))

config <- read.config(file = "~/.config/openfisca-survey-manager/config.ini")
assets_directory = config$openfisca_france_indirect_taxation$assets

# Import data
data_matching_enl_path <- file.path(assets_directory, "/matching/data_matching_enl.csv")
data_matching_bdf_path <- file.path(assets_directory, "/matching/data_matching_bdf.csv")

data_enl <- read.csv(file = data_matching_enl_path, header = -1, sep=",")
data_bdf <- read.csv(file = data_matching_bdf_path, header = -1, sep=",")

# Compute matching
out.nnd <- NND.hotdeck(
  data.rec = data_bdf, data.don = data_enl,
  match.vars = c(
    "aides_logement",
    "bat_av_49",
    "dip14pr",
    "electricite",
    "log_indiv",
    "nactifs",
    "nenfants",
    "ouest_sud",
    "part_energies_revtot",
    "petite_ville",
    "revtot",
    "rural",
    "surfhab_d"
    ),
  don.class = c("donation_class_3"),
  dist.fun = "Gower"
  )

# Create fused file
fused.nnd.m <- create.fused(
  data.rec = data_bdf, data.don = data_enl,
  mtc.ids = out.nnd$mtc.ids,
  z.vars = c(
    "froid_cout",
    "froid_impaye",
    "froid_installation",
    "froid_isolation",
    "froid",
    "gchauf_2",
    "gchauf_6",
    "gchauf_7",
    "gchaufs_1",
    "gchaufs_2",
    "gchaufs_3",
    "gchaufs_4",
    "gchaufs_5",
    "isolation_fenetres",
    "isolation_murs",
    "isolation_toit",
    "majorite_double_vitrage"
    )
)

data_matched_distance_path <- file.path(assets_directory, "/matching/data_matched_distance.csv")
write.csv(fused.nnd.m, file = data_matched_distance_path)
