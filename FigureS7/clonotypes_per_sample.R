library(ggplot2)
library(dplyr)

tls_group_colors <- c(nTLS = "#21ba7e", imTLS = "#9a6ccf", mTLS = "#f87967")

theme_tcr <- function(base_size = 11) {
  theme_classic(base_size = base_size) +
    theme(
      panel.grid.major = element_blank(),
      panel.grid.major.y = element_blank(),
      panel.grid.minor = element_blank(),
      axis.line = element_line(color = "#52514e", linewidth = 0.4),
      axis.ticks = element_line(color = "#52514e", linewidth = 0.3),
      strip.background = element_blank(),
      strip.text = element_text(face = "bold", size = rel(0.95)),
      legend.position = "bottom",
      legend.title = element_text(size = rel(0.85))
    )
}

metrics <- read.csv("diversity_metrics_by_sample.csv", header = TRUE)
metrics$TLS_group <- factor(metrics$TLS_group, levels = c("nTLS", "imTLS", "mTLS"))

kw_p <- kruskal.test(n_clonotypes ~ TLS_group, data = metrics)$p.value
p_label <- if (kw_p < 0.001) "italic(P) < 0.001" else sprintf("italic(P) == %.3g", kw_p)
y_max <- max(metrics$n_clonotypes, na.rm = TRUE)
y_min <- min(metrics$n_clonotypes, na.rm = TRUE)
bracket_y <- y_max + 0.14 * (y_max - y_min)
text_y <- y_max + 0.22 * (y_max - y_min)

p <- ggplot(metrics, aes(x = TLS_group, y = n_clonotypes, color = TLS_group)) +
  geom_jitter(width = 0.12, size = 4.2, alpha = 0.85, stroke = 0) +
  stat_summary(fun = mean, geom = "crossbar", width = 0.35, linewidth = 0.45, color = "#2a2a28") +
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.16, linewidth = 0.45, color = "#2a2a28") +
  annotate("segment", x = 1, xend = 3, y = bracket_y, yend = bracket_y, linewidth = 0.5, color = "#2a2a28") +
  annotate("text", x = 2, y = text_y, label = p_label, parse = TRUE, size = 4.2, color = "#2a2a28") +
  scale_color_manual(values = tls_group_colors, name = "TLS maturity") +
  scale_y_continuous(expand = expansion(mult = c(0.05, 0.28))) +
  labs(x = NULL, y = "Clonotypes / sample") +
  theme_tcr()

ggsave("clonotypes_per_sample.pdf", plot = p, width = 3.6, height = 3.6, device = cairo_pdf)
