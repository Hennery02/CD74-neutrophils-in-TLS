library(ggplot2)
library(RColorBrewer)

in_csv <- "LTB_LTBR_bubble_plot_data.csv"

df <- read.csv(in_csv, stringsAsFactors = FALSE)
pal <- colorRampPalette(rev(brewer.pal(n = 10, name = "Spectral")))(99)

for (sl in unique(df$source_group)) {
  sub <- df[df$source_group == sl, ]
  sub$label <- paste0(sub$source, " -> ", sub$target)
  sub$color_value <- -1 / log(sub$prob)
  sub$label <- factor(sub$label, levels = sub$label)
  p <- ggplot(sub, aes(x = label, y = interaction_name, color = color_value)) +
    geom_point(size = 5) +
    scale_color_gradientn(colors = pal, name = "Commun. Prob.",
                          breaks = range(sub$color_value), labels = c("min", "max")) +
    labs(x = NULL, y = NULL) +
    theme_bw(base_size = 9) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          panel.grid.minor = element_blank())
  w <- max(8, 0.45 * nrow(sub) + 3)
  ggsave(paste0("LTB_LTBR_bubble_", sl, ".pdf"), p, width = w, height = 4)
}
cat("done\n")
