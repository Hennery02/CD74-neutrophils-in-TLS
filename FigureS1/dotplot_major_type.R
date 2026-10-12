library(tidyverse)
library(ggplot2)
library(cowplot)
library(RColorBrewer)

plot_data <- read.csv("cluster_1_dot_plot_data.csv", header = TRUE)

custom_order_cell_type <- c("MajorType_1",
                  "MajorType_2",
                  "MajorType_3",
                  "MajorType_4",
                  "MajorType_5",
                  "MajorType_6",
                  "MajorType_7",
                  "MajorType_8",
                  "MajorType_9",
                  "MajorType_10")
plot_data$cell_type <- factor(plot_data$cell_type, levels = custom_order_cell_type)

custom_order_contrast <- c("nTLS", "imTLS", "mTLS")
plot_data$contrast <- factor(plot_data$contrast, levels = custom_order_contrast)

heatmap_layers <- list(
  scale_fill_manual(values = c(scales::muted("blue"), scales::muted("red"), "grey10")),
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5),
        axis.ticks = element_blank(),
        axis.line = element_blank(),
        axis.title = element_blank(),
        plot.margin = margin(0, 0, 0, 0),
        strip.text = element_blank())
)

p_odds_ratio <- plot_data %>%
  ggplot(aes(x = cell_type, y = forcats::fct_rev(contrast), color = log2.odds.ratio, size = -log10(p.value))) +
  geom_point() +
  scale_color_gradientn(
    colors = rev(brewer.pal(9, "RdBu")),
    limits = c(-1.5, 1.5),
    labels = c("≤-1.5", 0, "≥1.5"),
    breaks = c(-1.5, 0, 1.5)
  ) +
  scale_size_continuous(
    limits = c(0, 200),
    breaks = c(0, 100, 200),
    labels = c(0, 100, 200)
  ) +
  scale_x_discrete(drop=FALSE) +
  theme(
    axis.line = element_blank(),
    axis.text.x = element_blank(),
    axis.text.y = element_blank(),
    axis.ticks = element_blank(),
    legend.title = element_text(size = 14),
    legend.direction = "vertical",
    legend.position = "top",
    legend.box = "vertical",
    legend.box.just = "left",
    panel.background = element_blank(),
    panel.border = element_blank(),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    plot.title = element_text(face = "plain", size = 14),
    strip.background = element_blank(),
    strip.text.x = element_blank()
  ) +
  guides(color = guide_colourbar(title.position="top", title.hjust = 0.5, title.vjust = 0),
         size = guide_legend(title.position="top", title.hjust = 0.5, title.vjust = 0)) +
  labs(title = NULL, x = NULL, y = NULL, color = 'log2(odds ratio)', size = "\n-log10(p value)") +
  facet_grid(contrast_variable ~ ., scales = "free_y", space = "free")

p_signature_site_anno <- plot_data %>%
  distinct(contrast, contrast_variable, .keep_all = T) %>%
  ggplot() +
  geom_tile(aes(x=0, y=forcats::fct_rev(contrast), fill = contrast)) +
  heatmap_layers +
  facet_grid(contrast_variable~., scales = "free", space = "free") +
  theme(axis.text.x = element_blank(),
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        strip.text = element_blank()) +
  guides(fill = "none")

color_palette <- brewer.pal(11, "Spectral")
color_palette <- rep(color_palette, each = ceiling(22 / 11))[1:22]

p_cluster_anno <- plot_data %>%
  mutate(facet_helper = "") %>%
  distinct(cell_type, facet_helper, .keep_all = T) %>%
  ggplot() +
  geom_tile(aes(cell_type, facet_helper, fill = cell_type)) +
  heatmap_layers +
  scale_x_discrete(drop=FALSE) +
  facet_grid(~facet_helper, scales = "free", space = "free") +
  theme(axis.text.y = element_blank(),
        strip.text = element_blank()) +
  guides(fill = "none") +
  scale_fill_manual(values = color_palette)

p_left <-
  plot_grid(
    p_signature_site_anno + theme(plot.margin = margin(t = 6, r = 0, b = 0, l = 6)),
    ggdraw(),
    nrow = 2,
    align = "hv",
    axis = "tbr",
    rel_heights = c(1, 0.7),
    rel_widths = c(0.75, 1)
  )

p_right <-
  plot_grid(
    p_odds_ratio + theme(legend.position = "none", plot.margin = margin(t = 0, r = 6, b = 0, l = 0)),
    p_cluster_anno + theme(plot.margin = margin(t = 0, r = 6, b = 6, l = 6)),
    nrow = 2,
    align = "v",
    axis = "lr",
    rel_heights = c(1, 0.7),
    rel_widths = c(0.75, 1)
  )

p_scrna_odds_ratio <- plot_grid(
  plot_grid(
    p_left,
    p_right,
    nrow = 1,
    align = "hv",
    axis = "tblr",
    rel_widths = c(0.5, 1)
  ),
  get_legend(p_odds_ratio),
  ncol = 1,
  rel_heights = c(1, 0.15)
)

ggsave("cluster_1_dot_plot.pdf", plot = p_scrna_odds_ratio, width = 5, height = 3)
