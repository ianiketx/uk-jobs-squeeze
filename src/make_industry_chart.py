"""Which sectors have lost the most job vacancies since before the pandemic?

Compares vacancies in April to June 2026 with the 2019 average for each industry
(ONS vacancies by industry, seasonally adjusted, thousands).
Reads data/vacancies_by_industry.csv and saves charts/vacancies_by_industry.png.

Run from the repo root:  python src/make_industry_chart.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "vacancies_by_industry.csv")
df["avg_2019"] = df[["q1_2019", "q2_2019", "q3_2019", "q4_2019"]].mean(axis=1)
df["change_vs_2019_pct"] = (df["apr_jun_2026"] / df["avg_2019"] - 1) * 100
df["change_vs_2022_pct"] = (df["apr_jun_2026"] / df["apr_jun_2022"] - 1) * 100

total = df[df["ons_series"] == "AP2Y"].iloc[0]
sectors = df[df["ons_series"] != "AP2Y"].sort_values("change_vs_2019_pct", ascending=False)
print(sectors[["industry", "avg_2019", "apr_jun_2026", "change_vs_2019_pct", "change_vs_2022_pct"]]
      .round(1).to_string(index=False))
print(f"All industries: {total['change_vs_2019_pct']:.1f}% vs 2019, {total['change_vs_2022_pct']:.1f}% vs 2022")

BG, INK, MUTED, GREY, RED, TEAL = "#FBFAF7", "#1F2328", "#6B7178", "#C3C8CE", "#C8452B", "#2F7F79"
plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]
fig, ax = plt.subplots(figsize=(10.8, 10.8), dpi=100)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
fig.subplots_adjust(left=0.33, right=0.92, top=0.72, bottom=0.16)

worst = sectors["change_vs_2019_pct"].idxmin()
colours = [TEAL if v >= 0 else (RED if i == worst else GREY)
           for i, v in zip(sectors.index, sectors["change_vs_2019_pct"])]
y = range(len(sectors))
ax.barh(list(y), sectors["change_vs_2019_pct"], color=colours, height=0.66)
for yi, v in zip(y, sectors["change_vs_2019_pct"]):
    ax.text(v + (1.2 if v >= 0 else -1.2), yi, (f"{v:+.0f}%" if round(v) else "0%"), va="center",
            ha="left" if v >= 0 else "right", fontsize=15, fontweight="bold",
            color=TEAL if v >= 0 else (RED if v == sectors.loc[worst, "change_vs_2019_pct"] else INK))
ax.set_yticks(list(y))
ax.set_yticklabels(sectors["industry"], fontsize=15, color=INK)
ax.axvline(0, color=INK, lw=1.2)
ax.axvline(total["change_vs_2019_pct"], color=MUTED, lw=1.2, ls=(0, (3, 3)))
ax.text(total["change_vs_2019_pct"], -0.62, f"All industries {total['change_vs_2019_pct']:+.0f}%",
        ha="center", va="bottom", fontsize=13, color=MUTED, clip_on=False)
ax.set_xlim(-48, 40)
ax.set_ylim(len(sectors) - 0.5, -0.75)
ax.tick_params(axis="x", colors=MUTED, labelsize=13, length=0)
ax.tick_params(axis="y", length=0, pad=10)
ax.xaxis.set_major_formatter(lambda v, _: f"{v:+.0f}%" if v else "0")
ax.grid(axis="x", color="#E6E3DC", lw=1)
ax.set_axisbelow(True)
for side in ["top", "right", "left", "bottom"]:
    ax.spines[side].set_visible(False)

fig.text(0.07, 0.935, "Where have the jobs gone?", fontsize=28, fontweight="bold", color=INK)
fig.text(0.07, 0.88, "Change in UK job vacancies, April to June 2026 vs 2019 average", fontsize=18, color=INK)
fig.text(0.07, 0.83, f"Retail has lost about a third of its openings. Construction is still above", fontsize=16, color=MUTED)
fig.text(0.07, 0.80, "its 2019 level, though it fell sharply in July to September.", fontsize=16, color=MUTED)

fig.text(0.07, 0.08, "Data: ONS vacancies by industry (seasonally adjusted), series JP9I to JP9W and AP2Y",
         fontsize=12.5, color=MUTED)
fig.text(0.07, 0.05, "Nine sectors shown; hospitality, education and public sector not included.",
         fontsize=12.5, color=MUTED)

out = ROOT / "charts" / "vacancies_by_industry.png"
fig.savefig(out, dpi=100, facecolor=BG)
print(f"Saved {out.relative_to(ROOT)}")
