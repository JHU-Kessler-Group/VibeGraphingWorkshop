# VibeGraphing Workshop

This repository was created for a workshop about **VibeGraphing in October 2026**, exploring how to create and refine data visualizations through conversation with an AI coding assistant.

## Data and plots

The examples use the penguin measurements in `penguins.csv`.

- [Bill depth vs. bill length](bill_depth_vs_bill_length.svg): scatter plot with species-specific regression lines, 95% confidence bands, equations, and R² values.
- [Body mass by species and sex](body_mass_vs_species.svg): box-and-whisker plot with individual measurements, excluding penguins with missing sex or body mass.

## Regenerate the plots

Use [uv](https://docs.astral.sh/uv/) to run the scripts and manage their dependencies:

```sh
uv run plot_bill_dimensions.py
uv run plot_body_mass.py
```

Each script saves its plot as an SVG in this directory. Dependencies are declared in the scripts and installed automatically by `uv`.
