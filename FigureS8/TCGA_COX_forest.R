library(ggplot2)

df <- read.csv("TCGA_COX_forest_data.csv", stringsAsFactors = FALSE)
df$term <- factor(df$term, levels = rev(df$term))

p <- ggplot(df, aes(x = HR, y = term)) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "grey50") +
  geom_errorbarh(aes(xmin = lower95, xmax = upper95), height = 0.2) +
  geom_point(size = 3, shape = 15) +
  scale_x_log10() +
  labs(x = "Hazard ratio", y = NULL) +
  theme_classic(base_size = 12)

ggsave("TCGA_COX_forest.pdf", p, width = 7, height = 5)
