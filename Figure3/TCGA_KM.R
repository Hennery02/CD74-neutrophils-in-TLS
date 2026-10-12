library(survival)
library(ggplot2)

GROUP_LABEL <- c("2" = "nTLS", "1" = "mTLS")
COLORS <- c("nTLS" = "#53B385", "mTLS" = "#FFB1A4")

rt_mn <- read.csv("TCGA_KM_plot_data.csv")
rt_mn$cluster_type <- factor(rt_mn$cluster_type, levels = c(2, 1))

fit <- survfit(Surv(OS.time, OS) ~ cluster_type, data = rt_mn)
diff <- survdiff(Surv(OS.time, OS) ~ cluster_type, data = rt_mn)
p_val <- 1 - pchisq(diff$chisq, length(diff$n) - 1)

surv_df <- data.frame(
  time = fit$time,
  surv = fit$surv,
  strata = rep(names(fit$strata), fit$strata)
)
surv_df$cluster_type <- sub("cluster_type=", "", surv_df$strata)
surv_df$group <- GROUP_LABEL[surv_df$cluster_type]
surv_df$group <- factor(surv_df$group, levels = c("nTLS", "mTLS"))

n_labels <- sapply(levels(surv_df$group), function(g) {
  cl <- names(GROUP_LABEL)[GROUP_LABEL == g]
  sum(rt_mn$cluster_type == cl)
})

p <- ggplot(surv_df, aes(x = time, y = surv, color = group)) +
  geom_step(linewidth = 1) +
  scale_color_manual(values = COLORS,
                      labels = paste0(levels(surv_df$group), " (n=", n_labels, ")")) +
  labs(x = "Time (months)", y = "Survival probability", color = NULL) +
  annotate("text", x = max(surv_df$time) * 0.6, y = 0.9,
           label = paste0("P = ", sprintf("%.3f", p_val)), size = 4) +
  theme_minimal(base_size = 14) +
  theme(panel.grid.minor = element_blank())

ggsave("TCGA_KM.pdf", p, width = 6, height = 5.5)
