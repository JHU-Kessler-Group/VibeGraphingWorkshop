"""Run with: uv run plot_bill_dimensions.py."""

import csv
from pathlib import Path
import tempfile
from statistics import linear_regression
from math import sqrt

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import t

ROOT = Path(__file__).resolve().parent
with (ROOT / "penguins.csv").open(newline="", encoding="utf-8") as source:
    rows = list(csv.DictReader(source))
points = [
    (float(row["bill_length_mm"]), float(row["bill_depth_mm"]), row["species"])
    for row in rows
    if row["bill_length_mm"] not in ("", "NA")
    and row["bill_depth_mm"] not in ("", "NA")
]

plt.rcParams.update({"font.size": 11, "svg.fonttype": "none"})
fig, ax = plt.subplots(figsize=(9.5, 5.5), layout="constrained")
species_styles = {
    "Adelie": ("o", "#0072B2"),
    "Chinstrap": ("^", "#D55E00"),
    "Gentoo": ("s", "#009E73"),
}
for index, (species, (marker, color)) in enumerate(species_styles.items()):
    species_points = [(length, depth) for length, depth, name in points if name == species]
    ax.scatter(
        *zip(*species_points), s=128, marker=marker, color=color,
        alpha=0.40, linewidths=0, label=species,
    )
    lengths, depths = zip(*species_points)
    slope, intercept = linear_regression(lengths, depths)
    line_x = [min(lengths) + (max(lengths) - min(lengths)) * i / 199 for i in range(200)]
    fitted = [intercept + slope * length for length in line_x]
    n = len(lengths)
    mean_length = sum(lengths) / n
    sxx = sum((length - mean_length) ** 2 for length in lengths)
    residual_sd = sqrt(
        sum((depth - intercept - slope * length) ** 2 for length, depth in species_points)
        / (n - 2)
    )
    mean_depth = sum(depths) / n
    total_ss = sum((depth - mean_depth) ** 2 for depth in depths)
    residual_ss = sum(
        (depth - intercept - slope * length) ** 2 for length, depth in species_points
    )
    r_squared = 1 - residual_ss / total_ss
    equation = f"y = {slope:.3f}x {intercept:+.3f}"
    ax.text(
        1.02, 0.66 - index * 0.18,
        f"{species}\n{equation}\n$R^2$ = {r_squared:.3f}",
        transform=ax.transAxes, va="top", color=color, fontsize=10,
    )
    print(f"{species}: {equation}; R² = {r_squared:.3f}; n = {n}")
    critical_t = t.ppf(0.975, df=n - 2)
    margins = [
        critical_t * residual_sd * sqrt(1 / n + (length - mean_length) ** 2 / sxx)
        for length in line_x
    ]
    ax.fill_between(
        line_x,
        [value - margin for value, margin in zip(fitted, margins)],
        [value + margin for value, margin in zip(fitted, margins)],
        color=color, alpha=0.18, linewidth=0,
    )
    ax.plot(
        line_x, fitted, color=color, linewidth=1.8, linestyle="-",
    )
ax.legend(
    loc="upper left", bbox_to_anchor=(1.02, 1), frameon=False,
    title="Bands: 95% confidence", fontsize=9, title_fontsize=9,
)
ax.set(xlabel="Bill length (mm)", ylabel="Bill depth (mm)")
ax.grid(False)
ax.spines[["top", "right", "bottom", "left"]].set_visible(True)
ax.tick_params(direction="in")
output = ROOT / "bill_depth_vs_bill_length.svg"
fig.savefig(output)
preview = Path(tempfile.gettempdir()) / "vibegraphing_bill_dimensions.png"
fig.savefig(preview, dpi=150)
print(f"Saved {output}\nPreview: {preview}\nPlotted {len(points)} of {len(rows)} rows")
