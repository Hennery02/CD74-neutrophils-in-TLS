library(ggplot2)
library(patchwork)
library(ggrastr)

set2_8 <- c('#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3')
lineage_b_states <- c("Lineage_B_Subtype_4", "Lineage_B_Subtype_8", "Lineage_B_Subtype_9",
                 "Lineage_B_Subtype_1", "Lineage_B_Subtype_2", "Lineage_B_Subtype_3",
                 "Lineage_B_Subtype_5", "Lineage_B_Subtype_6", "Lineage_B_Subtype_7")
lineage_b_colors <- setNames(set2_8[((seq_along(lineage_b_states) - 1) %% length(set2_8)) + 1], lineage_b_states)

theme_tcr <- function(base_size = 11) {
  theme_classic(base_size = base_size) +
    theme(
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      axis.line = element_line(color = "#52514e", linewidth = 0.4),
      axis.ticks = element_line(color = "#52514e", linewidth = 0.3),
      legend.position = "right",
      legend.title = element_text(size = rel(0.85))
    )
}

tbl <- read.csv("clone_type_UMAP_plot_data.csv", header = TRUE)
color <- setNames(unname(lineage_b_colors), names(lineage_b_colors))

size_max <- max(tbl$clone_id_size, na.rm = TRUE)
brks <- unique(round(c(1, size_max / 2, size_max)))

plot_group <- function(df) {
  ggplot(df, aes(x = X, y = Y, size = clone_id_size, fill = cluster_short)) +
    geom_point_rast(shape = 21, colour = "white", stroke = 0.15, alpha = 0.85, raster.dpi = 300) +
    scale_fill_manual(values = color, name = "Subtype") +
    scale_size_continuous(range = c(1, 9), limits = c(0, size_max), breaks = brks, labels = brks, name = "clone size") +
    labs(x = "UMAP 1", y = "UMAP 2") +
    theme_tcr() +
    theme(panel.grid.major = element_blank(),
          axis.text = element_blank(), axis.ticks = element_blank())
}

group_order <- c(none = "nTLS", immature = "imTLS", mature = "mTLS")
single_plots <- list()
for (g in names(group_order)) {
  df_g <- tbl[tbl$group == g, ]
  if (nrow(df_g) == 0) next
  single_plots[[g]] <- plot_group(df_g)
}

combined <- (single_plots[["none"]] + theme(legend.position = "none")) +
  (single_plots[["immature"]] + theme(legend.position = "none") + labs(y = NULL)) +
  (single_plots[["mature"]] + labs(y = NULL)) +
  plot_layout(nrow = 1, widths = c(1, 1, 1.5))
ggsave("clone_type_all_groups.pdf", plot = combined, width = 15, height = 5.2)
