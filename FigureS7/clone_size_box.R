library(ggplot2)
library(dplyr)
library(ggpubr)
library(ggrastr)

tls_group_colors <- c(none = "#21ba7e", immature = "#9a6ccf", mature = "#f87967")

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

data <- read.csv("clone_size_data.csv", header = TRUE, check.names = FALSE)
data$group <- factor(data$group, levels = c("none", "immature", "mature"))
stat_df <- read.csv("clone_size_statistics.csv", header = TRUE)
sig_df <- stat_df %>% filter(p_BH < 0.05)

state_cols <- c("Lineage_B_Subtype_4", "Lineage_B_Subtype_8", "Lineage_B_Subtype_9",
                 "Lineage_B_Subtype_1", "Lineage_B_Subtype_2", "Lineage_B_Subtype_3",
                 "Lineage_B_Subtype_5", "Lineage_B_Subtype_6", "Lineage_B_Subtype_7")
state_cols <- intersect(state_cols, colnames(data))

fmt_p <- function(p) if (p < 0.001) "p < 0.001" else sprintf("p = %.3g", p)

box_one <- function(df, col) {
  data_max <- max(df[[col]], na.rm = TRUE)
  sig_here <- sig_df %>% filter(metric == col)
  n_sig <- nrow(sig_here)
  top_mult <- 1.15 + 0.18 * max(n_sig - 1, 0)

  p <- ggplot(df, aes(x = group, y = .data[[col]], fill = group)) +
    geom_boxplot(width = 0.55, outlier.shape = NA, alpha = 0.55, linewidth = 0.4, color = "#3a3a37") +
    geom_jitter_rast(aes(color = group), width = 0.16, size = 1.1, alpha = 0.75, stroke = 0,
                      raster.dpi = 300) +
    scale_fill_manual(values = tls_group_colors, guide = "none") +
    scale_color_manual(values = tls_group_colors, name = "TLS maturity",
                        labels = c(none = "nTLS", immature = "imTLS", mature = "mTLS")) +
    labs(x = NULL, y = "clone size (cells)") +
    theme_tcr() +
    theme(panel.grid.major.y = element_blank())

  if (n_sig > 0) {
    sig_here$y.position <- data_max * (top_mult + 0.12 * (seq_len(n_sig) - 1))
    sig_here$p_label <- vapply(sig_here$p_BH, fmt_p, character(1))
    p <- p +
      stat_pvalue_manual(
        sig_here, label = "p_label",
        xmin = "group1", xmax = "group2", y.position = "y.position",
        tip.length = 0.02, size = 3.1
      ) +
      scale_y_continuous(expand = expansion(mult = c(0.05, 0.08 + 0.15 * n_sig)))
  }
  p
}

plots <- list(box_one(data, "total_num"))
for (cn in state_cols) {
  df_f <- data %>% filter(.data[[cn]] != 0)
  plots[[length(plots) + 1]] <- box_one(df_f, cn)
}

p_all <- ggarrange(plotlist = plots, nrow = 1, common.legend = TRUE, legend = "bottom")
ggsave("clone_size.pdf", plot = p_all, width = 2.3 * length(plots), height = 2.3, limitsize = FALSE)
