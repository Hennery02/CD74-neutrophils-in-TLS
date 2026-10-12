library(pheatmap)

plot_df_normalized <- read.csv("GSE195832_imprint_heatmap_plot_data.csv", row.names = 1, check.names = FALSE)
plot_df_normalized <- as.matrix(plot_df_normalized)

colors33 <- colorRampPalette(c("white", "#abd7bb", "#379ba2", "#3d3a70"))(100)
breaks <- seq(0, 1, length.out = length(colors33) + 1)

plot <- pheatmap(plot_df_normalized,
                  scale = "row",
                  cluster_rows = FALSE,
                  cluster_cols = FALSE,
                  border_color = NA,
                  color = colors33,
                  breaks = breaks,
                  show_colnames = FALSE)

pdf("GEO_imprint.pdf")
print(plot)
dev.off()
