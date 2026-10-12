library(ggplot2)
library(ggalluvial)

in_csv <- "alluvial_plot_data.csv"
out_pdf <- "alluvial.pdf"

PROJECT_ROOT <- getwd()
df <- read.csv(file.path(PROJECT_ROOT, in_csv))

species_order <- unique(df$species[df$species != "Others"])
species_order <- c(species_order, "Others")
df$species <- factor(df$species, levels = c(rev(species_order[species_order != "Others"]), "Others"))
df$group <- factor(df$group, levels = c("rest", "mature"))

species_colors <- c(
  "#ed766c", "#f19168", "#f5ac64", "#e0c88e", "#c8aec9", "#b37db4",
  "#b0b6d4", "#94b5d2", "#78b4d0", "#a8d0b8", "#8e6e95", "#d4a5a5",
  "#9fb8ad", "#c9b8d8", "#e8c4c4"
)
names(species_colors) <- species_order[species_order != "Others"]
species_colors["Others"] <- "#dcdedd"

p <- ggplot(df, aes(x = group, y = percent, fill = species,
                     stratum = species, alluvium = species)) +
  geom_flow(width = 0.55, alpha = 0.35, knot.pos = 0, color = "white") +
  geom_col(width = 0.55, color = "white", linewidth = 0.4) +
  scale_fill_manual(values = species_colors, breaks = species_order) +
  labs(x = NULL, y = "Mean relative abundance (species, %)") +
  theme(
    panel.background = element_blank(),
    panel.border = element_blank(),
    axis.line = element_line(linewidth = 0.6, color = "black"),
    axis.ticks = element_blank(),
    axis.title.y = element_text(size = 13, color = "black"),
    axis.text = element_text(size = 13, color = "black"),
    legend.title = element_blank(),
    legend.text = element_text(size = 10)
  )

out_pdf <- file.path(PROJECT_ROOT, out_pdf)
ggsave(out_pdf, p, width = 6.5, height = 6, device = cairo_pdf)
cat("done\n")
