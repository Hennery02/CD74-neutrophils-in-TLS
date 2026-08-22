source("xiantao_group_compare.R")

long <- read.csv("group_compare_plot_data.csv")
long$x_group <- factor(long$x_group, levels = unique(long$x_group))

stats <- auto_stat_all(long, "1D", comparisons = NULL)

p <- plot_group_compare(
  long, "1D", stats,
  plot_type = "bar", show_points = TRUE, sig_label = "p.equals",
  title = "", xlab = "", ylab = "value",
)

ggsave("分组比较图.pdf", p, width = 10, height = 8, units = "cm", device = cairo_pdf)
