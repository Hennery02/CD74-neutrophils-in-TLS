library(survival)
library(ggplot2)

rt <- read.csv("KM_3_plot_data.csv")
rt$group <- factor(rt$group, levels = c("high", "low"))

diff <- survdiff(Surv(days, fustat) ~ group, data = rt)
p_val <- round(1 - pchisq(diff$chisq, df = 1), 5)

fit <- survfit(Surv(days, fustat) ~ group, data = rt)

surv_df <- data.frame(
  time = fit$time,
  surv = fit$surv,
  strata = rep(names(fit$strata), fit$strata)
)
surv_df$group <- sub("group=", "", surv_df$strata)
surv_df$group <- factor(surv_df$group, levels = c("high", "low"))

n_labels <- table(rt$group)

p <- ggplot(surv_df, aes(x = time, y = surv, color = group)) +
  geom_step(linewidth = 1) +
  scale_color_manual(values = c("high" = "#FFB1A4", "low" = "#53B385"),
                      labels = c(paste0("high (n=", n_labels["high"], ")"),
                                 paste0("low (n=", n_labels["low"], ")"))) +
  labs(x = "Time (month)", y = "Survival probability", color = NULL) +
  annotate("text", x = max(surv_df$time) * 0.6, y = 0.9,
           label = paste0("p = ", p_val), size = 4) +
  theme_minimal(base_size = 14) +
  theme(panel.grid.minor = element_blank())

ggsave("KM_3.pdf", p, width = 6, height = 5.5)
