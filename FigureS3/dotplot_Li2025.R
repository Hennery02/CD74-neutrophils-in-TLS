library(ggplot2)
library(RColorBrewer)
library(dplyr)

name <- "CellType_2"
src <- "Li2025"

df_all <- read.csv(paste0(name, "_AUCell_Li2025.csv"), header = TRUE, stringsAsFactors = FALSE)
src_var_names <- colnames(read.csv(paste0(name, "_aucell_acts_Li2025.csv"), header = TRUE, nrows = 1, row.names = 1, check.names = FALSE))
df <- df_all[df_all$source %in% src_var_names, ]

df <- df %>%
  group_by(source) %>%
  mutate(padj = p.adjust(pvalue, method = "BH")) %>%
  ungroup()

df_scaled <- df %>%
  group_by(source) %>%
  mutate(scaled_meanchange = as.numeric(scale(mean_difference))) %>%
  ungroup() %>%
  mutate(
    padj = ifelse(padj < 1e-300, 1e-300, padj),
    scaled_meanchange = ifelse(scaled_meanchange > 1, 1, scaled_meanchange),
    scaled_meanchange = ifelse(scaled_meanchange < -1, -1, scaled_meanchange)
  )

p <- ggplot(df_scaled, aes(x = source, y = factor(group, levels = rev(sort(unique(group)))),
                            color = scaled_meanchange, size = -log10(padj))) +
  geom_point() +
  scale_color_gradientn(
    colors = rev(brewer.pal(9, "RdBu")),
    limits = c(-1, 1),
    labels = c("<=-1", 0, ">=1"),
    breaks = c(-1, 0, 1)
  ) +
  scale_size_continuous(range = c(1, 8)) +
  scale_x_discrete(drop = FALSE) +
  labs(x = src, y = "CellType_2", color = "scaled\nmean diff", size = "-log10(padj)") +
  theme_classic() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))

n_group <- length(unique(df_scaled$group))
n_source <- length(unique(df_scaled$source))
w <- max(6.5, 0.45 * n_source + 2)
h <- max(4, 0.35 * n_group + 2)

ggsave("dotplot_aucell_Li2025.pdf", p, width = w, height = h)
write.csv(df_scaled, "dotplot_aucell_Li2025.csv", row.names = FALSE)
