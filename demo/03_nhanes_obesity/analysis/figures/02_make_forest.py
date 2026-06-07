"""
Forest plot of adjusted odds ratios from the survey-weighted logistic model.
Date: 2026-06-07
Random seed: 42
Reads analysis/tables/regression_or.csv (estimate, ci_lower, ci_upper, p).
No values are hand-typed; all come from the CSV emitted by 01_survey_analysis.R.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(HERE))
TBL = os.path.join(BASE, "analysis", "tables", "regression_or.csv")

style_path = os.path.join(
    os.environ.get("MEDSCI_SKILLS_ROOT", ""),
    "skills/analyze-stats/references/style/figure_style.mplstyle",
)
if os.path.exists(style_path):
    plt.style.use(style_path)

df = pd.read_csv(TBL)
# Drop intercept; keep adjusted predictors
df = df[df["term"] != "(Intercept)"].reset_index(drop=True)

# Order: obesity first (primary), then age, sex, race terms
order_key = []
for t in df["term"]:
    if t.startswith("Obesity"):
        order_key.append(0)
    elif t.startswith("Age"):
        order_key.append(1)
    elif t.startswith("Female"):
        order_key.append(2)
    else:
        order_key.append(3)
df["__o"] = order_key
df = df.sort_values(["__o"], kind="stable").reset_index(drop=True)

labels = df["term"].tolist()
est = df["estimate"].values
lo = df["ci_lower"].values
hi = df["ci_upper"].values
pv = df["p"].values

n = len(df)
y = np.arange(n)[::-1]  # top-to-bottom

fig, ax = plt.subplots(figsize=(7.0, 0.55 * n + 1.4))

# CI lines + point estimates
for yi, e, l, h in zip(y, est, lo, hi):
    ax.plot([l, h], [yi, yi], color="#333333", lw=1.4, zorder=2)
    ax.plot([l, l], [yi - 0.12, yi + 0.12], color="#333333", lw=1.4)
    ax.plot([h, h], [yi - 0.12, yi + 0.12], color="#333333", lw=1.4)
# Marker: highlight primary (obesity) in a distinct fill
for yi, e, lab in zip(y, est, labels):
    primary = lab.startswith("Obesity")
    ax.scatter([e], [yi], s=70 if primary else 45,
               color="#B83E3A" if primary else "#1B2A4E",
               zorder=3, edgecolor="white", linewidth=0.6)

ax.axvline(1.0, color="#999999", ls="--", lw=1.0, zorder=1)
ax.set_xscale("log")
ax.set_xticks([0.5, 1, 2, 3, 4])
ax.get_xaxis().set_major_formatter(plt.matplotlib.ticker.ScalarFormatter())
ax.set_xlabel("Adjusted odds ratio (95% CI), log scale")
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_ylim(-0.7, n - 0.3)

# Annotate OR (CI) and p on the right
xmax = ax.get_xlim()[1]
for yi, e, l, h, p in zip(y, est, lo, hi, pv):
    ptxt = "<0.001" if p < 0.001 else f"{p:.3f}"
    ax.text(xmax * 1.05, yi, f"{e:.2f} ({l:.2f}-{h:.2f}), p={ptxt}",
            va="center", ha="left", fontsize=8)

ax.set_title("Adjusted associations with self-reported diabetes\n"
             "NHANES 2017-2018, survey-weighted logistic regression (n = 5,010)",
             fontsize=10)
ax.spines[["top", "right"]].set_visible(False)
fig.subplots_adjust(left=0.30, right=0.62, top=0.86, bottom=0.16)

out_pdf = os.path.join(HERE, "forest_or.pdf")
out_png = os.path.join(HERE, "forest_or.png")
fig.savefig(out_pdf, bbox_inches="tight")
fig.savefig(out_png, dpi=300, bbox_inches="tight")
print(f"Wrote {out_pdf}")
print(f"Wrote {out_png}")
plt.close(fig)
