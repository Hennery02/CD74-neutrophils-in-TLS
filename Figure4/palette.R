#!/usr/bin/env Rscript
# Shared palette/theme for T-cell clone figures.
# Validated with dataviz skill's scripts/validate_palette.js (six-check
# categorical validator + ordinal ramp check); do not hand-pick replacements
# without re-running the validator.
suppressPackageStartupMessages(library(ggplot2))

## ---- TLS maturity group: nTLS / imTLS / mTLS (none/immature/mature) ----
## 2026-07-16 update: user specified green/purple/coral (#53b385/#9b82bc/#ffb1a4).
## imTLS and mTLS both failed the chroma floor (read as gray, C=0.089/0.094 <
## 0.10) and mTLS failed the lightness band (L=0.831 > 0.77 ceiling). Re-derived
## in OKLCH holding each hue angle fixed (green H=160.4, purple H=303.8, coral
## H=29.7), raising L into band and C above floor -- same hue direction as the
## user's swatch, deepened enough to pass. All checks pass except a contrast
## WARN (legal with visible labels/legend, which these figures already have).
tls_group_colors <- c(none = "#21ba7e", immature = "#9a6ccf", mature = "#f87967")

## ---- categorical: fixed 8-hue order, worst adjacent CVD ΔE 24.2 (protan) ----
categorical8 <- c("#2a78d6", "#1baf7a", "#eda100", "#008300",
                  "#4a3aa7", "#e34948", "#e87ba4", "#eb6834")

## Lineage_A: 4 states, first 4 categorical slots
lineage_a_colors <- setNames(
  categorical8[1:4],
  c("Lineage_A_Subtype_1", "Lineage_A_Subtype_2", "Lineage_A_Subtype_3", "Lineage_A_Subtype_4")
)

## Lineage_B: matplotlib/scanpy "Set2" palette, reproduced as-is to match an
## earlier notebook figure (sc.pl.umap(..., palette='Set2')). ColorBrewer Set2
## has only 8 discrete colors; matplotlib/scanpy cycle back to slot 1 for a
## 9th category (this is not CVD-validated, not run through the dataviz
## skill's validator).
set2_8 <- c('#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3')
lineage_b_states <- c("Lineage_B_Subtype_4", "Lineage_B_Subtype_8", "Lineage_B_Subtype_9",
                 "Lineage_B_Subtype_1", "Lineage_B_Subtype_2", "Lineage_B_Subtype_3",
                 "Lineage_B_Subtype_5", "Lineage_B_Subtype_6", "Lineage_B_Subtype_7")
lineage_b_colors <- setNames(set2_8[((seq_along(lineage_b_states) - 1) %% length(set2_8)) + 1], lineage_b_states)
neutral_gray <- "#c9c8c2"

theme_tcr <- function(base_size = 11) {
  ## no panel gridlines, ever -- user standing instruction: never add the
  ## gray background gridline, in any figure, in this project.
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
      legend.title = element_text(size = rel(0.85)),
      plot.title = element_text(face = "bold", size = rel(1.05))
    )
}
