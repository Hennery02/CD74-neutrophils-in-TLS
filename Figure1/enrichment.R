library(gground)
library(ggprism)
library(tidyverse)
library(dplyr)

use_pathway <- read.csv("../../data/Lineage_C_enrichment_plot_data.csv") %>%
  mutate(Description = factor(Description, levels = rev(Description)))

selected_celltype <- "Subcluster_7"
pal <- c('#eaa052')
names(pal) <- selected_celltype
width <- 0.5

use_pathway_plot <- use_pathway %>%
  mutate(
    log_p_adjust = -log10(p.adjust),
    log_p_adjust = ifelse(is.infinite(log_p_adjust),
                          max(log_p_adjust[is.finite(log_p_adjust)], na.rm = TRUE) + 5,
                          log_p_adjust)
  )

p <- use_pathway_plot %>%
  ggplot(aes(log_p_adjust, y = Description)) +
  geom_round_col(width = 0.7, alpha = 0.8, fill = pal[1]) +
  geom_text(aes(x = 0.05, label = Description), hjust = 0, size = 4.5) +
  geom_point(aes(x = -width, size = Statistic), shape = 21, fill = pal[1]) +
  geom_text(aes(x = -width, label = round(Statistic, 1)), size = 3.5) +
  scale_size_continuous(name = 'Enrichment\nStrength', range = c(4, 10)) +
  geom_segment(
    aes(x = 0, y = 0, xend = max(log_p_adjust, na.rm = TRUE) + 0.5, yend = 0),
    linewidth = 1.5
  ) +
  labs(
    y = NULL,
    x = "-log10(Adjusted P-value)"
  ) +
  scale_x_continuous(
    breaks = pretty(c(0, max(use_pathway_plot$log_p_adjust, na.rm = TRUE))),
    expand = expansion(c(0, 0.05))
  ) +
  theme_prism() +
  theme(
    axis.text.y = element_blank(),
    axis.line.y = element_blank(),
    axis.ticks.y = element_blank(),
    legend.title = element_text(size = 12),
    legend.position = "right"
  )

ggsave("../../data/enrichment.pdf", p, width = 10, height = 6)
