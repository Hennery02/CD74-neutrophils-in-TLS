library(pheatmap)
library(ggplot2)
library(scatterpie)

tls_group_colors <- c(none = "#21ba7e", immature = "#9a6ccf", mature = "#f87967")

theme_tcr <- function(base_size = 11) {
  theme_classic(base_size = base_size) +
    theme(
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      axis.line = element_line(color = "#52514e", linewidth = 0.4),
      axis.ticks = element_line(color = "#52514e", linewidth = 0.3),
      legend.position = "bottom",
      legend.title = element_text(size = rel(0.85))
    )
}

disp_num <- as.matrix(read.csv("clone_share_hm_data.csv", row.names = 1, check.names = FALSE))
log_hm <- log10(disp_num + 1)

colours <- colorRampPalette(c("#f0efec", "#cde2fb", "#6da7ec", "#2a78d6", "#104281"))(500)

pdf("clone_share_hm.pdf", width = 6.8, height = 6.2)
pheatmap(log_hm, color = colours, scale = "none",
         cluster_rows = FALSE, cluster_cols = FALSE, border_color = "white",
         display_numbers = disp_num, number_color = "#0b0b0b",
         fontsize = 11, fontsize_number = 9)
dev.off()

table <- read.csv("clone_share_scatter_data.csv", header = TRUE)

scatter_cd4 <- ggplot() +
  geom_scatterpie(aes(x = x, y = y, r = r), data = table, cols = c("n", "im", "m"), color = "white", linewidth = 0.3) +
  geom_scatterpie_legend(table$r, n = 3, x = 2.5, y = 4, labeller = function(x) round(x * 30)) +
  scale_y_reverse() +
  scale_fill_manual(values = unname(tls_group_colors), labels = c("nTLS", "imTLS", "mTLS")) +
  coord_equal() +
  labs(x = NULL, y = NULL, fill = "TLS maturity") +
  theme_tcr() +
  theme(axis.text = element_blank(), axis.ticks = element_blank(), axis.line = element_blank())

ggsave("clone_share_scatter.pdf", plot = scatter_cd4, width = 4.5, height = 4)
