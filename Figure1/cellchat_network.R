library(CellChat)

in_csv <- "cellchat_network_weights.csv"
out_pdf <- "cellchat_network_3x3.pdf"

weight_df <- read.csv(in_csv, stringsAsFactors = FALSE)
pathways_show <- c("MHC-II", "SELL", "SELPLG", "VEGF", "TNF", "CXCL", "MHC-I", "NOTCH")
cell_types <- sort(unique(weight_df$source))

pdf(out_pdf, width = 10.4, height = 5.2)
par(mfrow = c(3, 3), xpd = TRUE, mar = c(0.5, 0.5, 1.5, 0.5))
for (pw in pathways_show) {
  sub <- weight_df[weight_df$pathway == pw, ]
  mat <- matrix(0, nrow = length(cell_types), ncol = length(cell_types),
                dimnames = list(cell_types, cell_types))
  for (i in seq_len(nrow(sub))) {
    mat[sub$source[i], sub$target[i]] <- sub$weight[i]
  }
  netVisual_circle(mat, weight.scale = TRUE, title.name = paste0(pw, " signaling pathway network"))
}
dev.off()

cat("done\n")
