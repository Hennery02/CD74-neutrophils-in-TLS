library(dplyr)
library(ggplot2)
library(RColorBrewer)

odds_result <- read.csv("odds_ratio_1_plot_data.csv")
odds_result$contrast_name <- ordered(odds_result$contrast_name)

p_odds <- odds_result %>%
  ggplot(aes(x = cell_type, y = forcats::fct_rev(contrast_name), color = log2_odds, size = -log10(p_val))) +
  geom_point() +
  scale_color_gradientn(colors = rev(brewer.pal(9, "RdBu")), limits = c(-0.5, 0.5), labels = c("<=-0.5", 0, ">=0.5"), breaks = c(-0.5, 0, 0.5)) +
  scale_size_continuous(limits = c(0, 50), breaks = c(0, 25, 50), labels = c(0, 25, 50)) +
  scale_x_discrete(drop = FALSE) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1), legend.position = "top",
        panel.grid = element_blank(), strip.text = element_blank()) +
  guides(color = guide_colourbar(title.position = "top", title.hjust = 0.5, title.vjust = 0),
         size = guide_legend(title.position = "top", title.hjust = 0.5, title.vjust = 0)) +
  labs(title = NULL, x = NULL, y = NULL, color = 'log2(odds ratio)', size = "\n-log10(p value)") +
  facet_grid(contrast_var ~ ., scales = "free_y", space = "free")

ggsave("odds_ratio_dotplot.pdf", plot = p_odds, width = 10, height = 6)
