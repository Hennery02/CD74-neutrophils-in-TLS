#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(ggplot2)
  library(ggrastr)
  library(ggnewscale)
  library(grid)
})

source("palette.R")

tls_groups <- c("nTLS", "imTLS", "mTLS")

pt_facets <- read.csv("panelD_tls_plot_data.csv")
pt_facets$TLS_group <- factor(pt_facets$TLS_group, levels = tls_groups)
edges <- read.csv("panelD_tls_edges.csv")
edges$TLS_group <- factor(edges$TLS_group, levels = tls_groups)
shared_cells <- read.csv("panelD_tls_shared_cells.csv")
arrow_df <- read.csv("panelD_tls_arrows.csv")
arrow_df$TLS_group <- factor(arrow_df$TLS_group, levels = tls_groups)

n_shared_by_group <- read.csv("panelD_tls_n_shared_by_group.csv")
facet_labeller <- as_labeller(function(g) sprintf("%s  (n = %d shared clones)", g,
                                                    n_shared_by_group$n_shared_clones[match(g, n_shared_by_group$TLS_group)]))

p <- ggplot() +
  geom_point_rast(data = pt_facets, aes(x = UMAP1, y = UMAP2, color = dpt_pseudotime),
                   size = 0.25, alpha = 0.45, raster.dpi = 300) +
  scale_color_gradientn(colors = c("#2a3d8f", "#2f9bd6", "#61c96f", "#e8d34a", "#e8792a", "#b3202c"),
                        name = "pseudotime", breaks = c(0, 1), labels = c("0", "1")) +
  new_scale_color() +
  geom_segment(data = edges, aes(x = x, y = y, xend = xend, yend = yend, color = pt_dist),
               linewidth = 0.3, alpha = 0.45) +
  scale_color_gradientn(colors = c("#d8d6cd", "#8a6ccf", "#5a2a86"), name = "|delta pseudotime|\nwithin clone") +
  geom_point_rast(data = shared_cells, aes(x = UMAP1, y = UMAP2),
                   shape = 21, fill = "#f2c14e", color = "#3a3a37", stroke = 0.3, size = 1.9,
                   raster.dpi = 300) +
  new_scale_color() +
  geom_segment(data = arrow_df, aes(x = x, y = y, xend = xend, yend = yend),
               color = "#111111", linewidth = 1.0, arrow = arrow(length = unit(0.2, "cm"), type = "closed")) +
  geom_text(data = arrow_df, aes(x = label_x, y = label_y, label = label, color = branch),
            fontface = "bold", size = 3.6, hjust = 0.5, show.legend = FALSE) +
  scale_color_manual(values = setNames(arrow_df$color, arrow_df$branch), guide = "none") +
  facet_wrap(~TLS_group, nrow = 1, labeller = facet_labeller) +
  scale_x_continuous(expand = expansion(mult = c(0.05, 0.2))) +
  coord_equal(clip = "off") +
  labs(x = "UMAP-1", y = "UMAP-2") +
  theme_tcr() +
  theme(legend.position = "right",
        panel.grid.major = element_blank(),
        axis.text = element_blank(), axis.ticks = element_blank(),
        plot.margin = margin(5.5, 20, 5.5, 5.5))

ggsave("pseudotime_trajectory_clone_share_UMAP_by_TLS.pdf", plot = p, width = 15, height = 5.6)
