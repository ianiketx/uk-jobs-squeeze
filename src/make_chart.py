"""UK jobs squeeze: unemployed people per vacancy, 2001 to 2026.

Reads data/unemployed_per_vacancy_jpc5.csv (ONS series JPC5) and saves
charts/unemployed_per_vacancy.png.

Run from the repo root:  python src/make_chart.py
"""
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "unemployed_per_vacancy_jpc5.csv")
df["date"] = pd.to_datetime(df["period_mid_month"] + "-15")
ratio = df["unemployed_per_vacancy"]

low = df.loc[df["date"].dt.year >= 2021].nsmallest(1, "unemployed_per_vacancy").iloc[0]
latest = df.iloc[-1]
peak = df.loc[ratio.idxmax()]
print(f"Post-pandemic low: {low['unemployed_per_vacancy']} ({low['three_month_period']} {low['date'].year})")
print(f"Latest: {latest['unemployed_per_vacancy']} ({latest['three_month_period']} {latest['date'].year})")
print(f"Series peak: {peak['unemployed_per_vacancy']} ({peak['three_month_period']} {peak['date'].year})")

BG, INK, MUTED, GREY, RED = "#FBFAF7", "#1F2328", "#6B7178", "#B9BEC4", "#C8452B"
plt.rcParams["font.family"] = ["Inter", "DejaVu Sans"]

fig, ax = plt.subplots(figsize=(10.8, 10.8), dpi=100)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
fig.subplots_adjust(left=0.08, right=0.95, top=0.73, bottom=0.17)

recent = df["date"] >= low["date"]
ax.fill_between(df["date"], ratio, color=GREY, alpha=0.18, lw=0)
ax.plot(df["date"], ratio, color=GREY, lw=2.6)
ax.plot(df.loc[recent, "date"], ratio[recent], color=RED, lw=3.6, solid_capstyle="round")

ax.scatter([low["date"], latest["date"]], [low["unemployed_per_vacancy"], latest["unemployed_per_vacancy"]],
           color=RED, s=70, zorder=3)
ax.annotate(f"{low['unemployed_per_vacancy']:.1f}\n{low['date'].year}", xy=(low["date"], low["unemployed_per_vacancy"]),
            xytext=(0, -46), textcoords="offset points", ha="center", fontsize=17, fontweight="bold", color=RED)
ax.annotate(f"{latest['unemployed_per_vacancy']:.1f}\nnow", xy=(latest["date"], latest["unemployed_per_vacancy"]),
            xytext=(0, 16), textcoords="offset points", ha="center", fontsize=17, fontweight="bold", color=RED)
ax.annotate("After the 2008\nfinancial crisis", xy=(peak["date"], peak["unemployed_per_vacancy"]),
            xytext=(8, 4), textcoords="offset points", fontsize=13, color=MUTED, va="bottom")
covid = df.loc[df["period_mid_month"] == "2020-05"].iloc[0]
ax.annotate("Pandemic", xy=(covid["date"], covid["unemployed_per_vacancy"]),
            xytext=(-10, 8), textcoords="offset points", fontsize=13, color=MUTED, ha="right")

ax.set_ylim(0, 6.6)
ax.set_xlim(df["date"].min() - pd.Timedelta(days=60), df["date"].max() + pd.Timedelta(days=200))
ax.xaxis.set_major_locator(mdates.YearLocator(5, month=1, day=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
ax.tick_params(colors=MUTED, labelsize=14, length=0, pad=6)
ax.grid(axis="y", color="#E6E3DC", lw=1)
ax.set_axisbelow(True)
for side in ["top", "right", "left"]:
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(GREY)
ax.set_ylabel("Unemployed people per job vacancy", fontsize=14, color=MUTED, labelpad=10)

fig.text(0.07, 0.93, "Finding a job in the UK has got much harder", fontsize=27, fontweight="bold", color=INK)
fig.text(0.07, 0.875, f"In {low['date'].year}, there was about one vacancy for every unemployed person.", fontsize=18, color=INK)
fig.text(0.07, 0.837, f"Now there are {latest['unemployed_per_vacancy']:.1f} people for every job.", fontsize=18, color=INK)
fig.text(0.07, 0.775, "Vacancies have fallen to their lowest since 2014, outside the pandemic.",
         fontsize=16, color=RED, fontweight="bold")

fig.text(0.07, 0.085, "Data: Office for National Statistics, series JPC5 and Vacancies and jobs in the UK (October 2026)",
         fontsize=12.5, color=MUTED)
fig.text(0.07, 0.055, f"Rolling 3-month figures, latest {latest['three_month_period']} {latest['date'].year}. Made in Python by Aniket Bansal",
         fontsize=12.5, color=MUTED)

out = ROOT / "charts" / "unemployed_per_vacancy.png"
fig.savefig(out, dpi=100, facecolor=BG)
print(f"Saved {out.relative_to(ROOT)}")
