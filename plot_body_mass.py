# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib>=3.9,<4"]
# ///
"""Run with: uv run plot_body_mass.py.

Boxes show the median and interquartile range. Whiskers extend to the
most extreme observations within 1.5 IQR; points beyond are outliers.
"""

import csv
from pathlib import Path
import tempfile
from random import Random

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

ROOT = Path(__file__).resolve().parent
with (ROOT / "penguins.csv").open(newline="", encoding="utf-8") as source:
    rows = list(csv.DictReader(source))

species_styles = {
    "Adelie": ("o", "#0072B2"),
    "Chinstrap": ("^", "#D55E00"),
    "Gentoo": ("s", "#009E73"),
}
plt.rcParams.update({"font.size": 11, "svg.fonttype": "none"})
fig, ax = plt.subplots(figsize=(9.5, 5.5), layout="constrained")
plotted = 0
rng = Random(42)
tick_positions = []
tick_labels = []
for species_index, (species, (marker, color)) in enumerate(species_styles.items()):
    center = 1 + species_index * 3
    for offset, sex in enumerate(("female", "male")):
        position = center + offset - 0.5
        masses = [
            float(row["body_mass_g"])
            for row in rows
            if row["species"] == species and row["sex"] == sex
            and row["body_mass_g"] not in ("", "NA")
        ]
        if not masses:
            continue
        plotted += len(masses)
        tick_positions.append(position)
        tick_labels.append(sex.capitalize())
        ax.boxplot(
            [masses], positions=[position], widths=0.6, whis=1.5, patch_artist=True,
            showfliers=False,
            boxprops={"facecolor": to_rgba(color, 0.40), "edgecolor": color, "linewidth": 1.8},
            medianprops={"color": color, "linewidth": 2},
            whiskerprops={"color": color, "linewidth": 1.8},
            capprops={"color": color, "linewidth": 1.8},
        )
        ax.scatter(
            [position + rng.uniform(-0.22, 0.22) for _ in masses], masses,
            s=32, marker=marker, color=color, alpha=0.40, linewidths=0, zorder=3,
        )
        print(f"{species}, {sex}: n = {len(masses)}")
    ax.text(center, -0.09, species, transform=ax.get_xaxis_transform(),
            ha="center", va="top", fontsize=11)

ax.set_xticks(tick_positions, tick_labels)
ax.set(ylabel="Body mass (g)", xlim=(-0.3, 8.3))
ax.set_xlabel("Species / sex", labelpad=35)
ax.grid(False)
ax.spines[["top", "right", "bottom", "left"]].set_visible(True)
ax.tick_params(direction="in")
output = ROOT / "body_mass_vs_species.svg"
fig.savefig(output)
preview = Path(tempfile.gettempdir()) / "vibegraphing_body_mass.png"
fig.savefig(preview, dpi=150)
print(f"Saved {output}\nPreview: {preview}\nPlotted {plotted} of {len(rows)} rows")
