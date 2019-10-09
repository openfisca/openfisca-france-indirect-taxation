# Import data
data_erfs <- read.csv(file = file.path(assets_directory, "/matching/matching_erfs/data_matching_erfs.csv"), header = -1, sep=",")
data_bdf <- read.csv(file = file.path(assets_directory, "/matching/matching_erfs/data_matching_bdf.csv"), header = -1, sep=",")

# Compute ranked matching
out.nnd <- rankNND.hotdeck(
  data.rec = data_bdf, data.don = data_erfs,
  var.rec = c("rev_disponible"),
  don.class = c("donation_class_1"),
  weight.rec = "pondmen",
  weight.don = "pondmen"
)

# Create fused file
fused.nnd.m <- create.fused(
  data.rec = data_bdf, data.don = data_erfs,
  mtc.ids = out.nnd$mtc.ids,
  z.vars = c("revdecm")
)

# Save it as csv
write.csv(fused.nnd.m,
  file = file.path(assets_directory, "/matching/matching_erfs/data_matched_rank.csv")
  )
