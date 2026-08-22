library(pheatmap)
library(sciRcolor)

raw <- read.csv("TCGA_signature_heatmap_plot_data.csv", header = TRUE, check.names = FALSE)
sorted_matrix <- as.matrix(raw[, -1])
rn <- raw[[1]]
rn[is.na(rn)] <- "NA"
rownames(sorted_matrix) <- rn
rownames(sorted_matrix)[nrow(sorted_matrix)] <- ""

cluster <- read.csv("group_3.csv", header = TRUE, row.names = 1)
cluster <- cluster[, "group", drop = FALSE]
cluster$group <- factor(cluster$group, levels = c("Cluster2", "Cluster3", "Cluster4", "Cluster1"))
cluster_new <- cluster[colnames(sorted_matrix), , drop = FALSE]

colors33 <- colorRampPalette(c("white", "#ff9517", "#b83835", "#6d4490", "#000000"))(500)
breaks <- seq(0, 5, length.out = length(colors33) + 1)

plot.scale <- pheatmap(sorted_matrix, scale = "row", cluster_rows = FALSE, cluster_cols = FALSE,
                        border_color = NA, color = colors33, breaks = breaks,
                        annotation_col = cluster_new, show_colnames = FALSE)
pdf("cluster.pdf")
print(plot.scale)
dev.off()

color_lin <- sciRcolor::pal_scircolor(86)[c(6, 10)]
color_interp <- colorRampPalette(color_lin)
expanded_colors <- color_interp(20)
breaks <- seq(0, 4, length.out = length(expanded_colors) + 1)

plot.TLS.imprint <- pheatmap(sorted_matrix, scale = "row", cluster_rows = FALSE, cluster_cols = FALSE,
                              border_color = NA, color = expanded_colors, breaks = breaks,
                              annotation_col = cluster_new, show_colnames = FALSE)
pdf("TLS_imprint.pdf")
print(plot.TLS.imprint)
dev.off()
