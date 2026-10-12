suppressPackageStartupMessages({ library(ggplot2) })

in_summary <- "growth_curve_2_plot_data.csv"
in_points <- "growth_curve_2_points.csv"
out_pdf <- "growth_curve_2.pdf"

df_summary <- read.csv(in_summary, stringsAsFactors = FALSE, check.names = FALSE)
df_long <- read.csv(in_points, stringsAsFactors = FALSE, check.names = FALSE)

group_order <- c("group1", "group2", "group3", "group4",
                 "group5", "group6", "group7", "group8")
group_colors <- c("group1" = "#7C9CB4", "group2" = "#C97B8A", "group3" = "#B3BB81", "group4" = "#8A81BB",
                  "group5" = "#8FA888", "group6" = "#C9A27B", "group7" = "#81BB99", "group8" = "#BB81BB")
grp <- intersect(group_order, unique(df_summary$group))
df_summary$group <- factor(df_summary$group, levels = grp)
df_long$group <- factor(df_long$group, levels = grp)

p <- ggplot(df_summary, aes(x = time, y = mean_vol, color = group, group = group)) +
  geom_point(data = df_long, aes(x = time, y = volume, color = group),
             position = position_jitter(width = 0.3, seed = 42),
             size = 1.2, alpha = 0.35, shape = 16, inherit.aes = FALSE) +
  geom_errorbar(aes(ymin = mean_vol - sem_vol, ymax = mean_vol + sem_vol), width = 0.3, linewidth = 0.4) +
  geom_line(linewidth = 0.8) +
  geom_point(size = 3.5, shape = 16) +
  scale_color_manual(values = group_colors[grp]) +
  scale_x_continuous(breaks = sort(unique(df_summary$time))) +
  labs(x = "Days after tumor injection", y = expression("Tumor volume (mm"^3*")"), color = "Group") +
  theme_classic(base_size = 13)
ggsave(out_pdf, p, width = 8, height = 5)
cat("done\n")
