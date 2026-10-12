library(dplyr)
library(rstatix)
library(ggplot2)
library(ggpubr)

IN_LONG <- "group_compare_plot_data.csv"
IN_PAIRWISE <- "pairwise_comparison.csv"
OUT_PDF <- "group_compare.pdf"

PALETTE <- c("#7C9CB4", "#8FA888", "#C97B8A", "#C9A27B", "#B3BB81", "#81BB99", "#8A81BB", "#BB81BB")

plot_group_compare <- function(long, pw) {
  groups <- levels(long$x_group)
  summ <- long %>%
    group_by(x_group) %>%
    summarise(mean = mean(value), sd = sd(value), .groups = "drop")
  p <- ggplot(summ, aes(x = x_group, y = mean, fill = x_group)) +
    geom_col(width = 0.7, color = "black", linewidth = 0.3) +
    geom_errorbar(aes(ymin = mean - sd, ymax = mean + sd), width = 0.2) +
    geom_jitter(data = long, aes(x = x_group, y = value, fill = x_group), height = 0, width = 0.15,
                shape = 21, color = "black", alpha = 0.7, inherit.aes = FALSE) +
    scale_fill_manual(values = rep(PALETTE, length.out = length(groups)))

  pw <- pw[pw$p.adj.signif != "ns", , drop = FALSE]
  if (length(groups) > 2 && nrow(pw) > 0) {
    pw <- pw[pw$group1 == groups[1] | pw$group2 == groups[1], , drop = FALSE]
  }
  if (nrow(pw) > 0) {
    pw$label <- paste0("P = ", signif(pw$p.adj, 3))
    pw <- add_xy_position(pw, x = "x_group", step.increase = 0.14, data = long, formula = value ~ x_group)
    y_lo <- min(long$value)
    y_hi <- max(long$value)
    pad_top <- max(max(pw$y.position) - y_hi, 0) + (y_hi - y_lo) * 0.1
    p <- p + stat_pvalue_manual(pw, label = "label", tip.length = 0, label.size = 3.6,
                                bracket.size = 0.4, fontface = "italic") +
      scale_y_continuous(expand = expansion(mult = c(0.02, 0)),
                         limits = c(min(0, y_lo), y_hi + pad_top + (y_hi - y_lo) * 0.06))
  }

  x_angle <- if (length(groups) > 5 || max(nchar(groups)) > 6) 45 else 0
  x_text <- if (x_angle > 0) element_text(color = "black", angle = x_angle, hjust = 1, vjust = 1) else element_text(color = "black")
  p +
    labs(x = "", y = "value", fill = NULL) +
    theme_classic(base_size = 12) +
    theme(axis.text.x = x_text, axis.text.y = element_text(color = "black"))
}

set.seed(1)
long <- read.csv(IN_LONG, stringsAsFactors = FALSE)
long$x_group <- factor(long$x_group, levels = unique(long$x_group))
pw <- read.csv(IN_PAIRWISE, stringsAsFactors = FALSE)

p <- plot_group_compare(long, pw)
ggsave(OUT_PDF, p, width = 10, height = 8, units = "cm", device = cairo_pdf)
cat("done\n")
