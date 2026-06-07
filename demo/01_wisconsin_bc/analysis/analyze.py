"""
Analysis: Wisconsin Breast Cancer Diagnostic Accuracy Study (clean-room, v3.7.0 demo 1)
Date: 2026-06-07
Random seed: 42
Python: 3.x
Key packages: scikit-learn, scipy, numpy, pandas, matplotlib
Reference standard: histopathology diagnosis (malignant vs benign).
Index tests: logistic regression, random forest, SVM (RBF) probability of malignancy.
"""
import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import roc_curve, confusion_matrix, brier_score_loss

SEED = 42
np.random.seed(SEED)

HERE = Path(__file__).resolve()
WORK = HERE.parents[1]
DATA = WORK / "data" / "wisconsin_breast_cancer.csv"
TBL = WORK / "analysis" / "tables"
FIG = WORK / "analysis" / "figures"
TBL.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

# Figure style (skill style file if available; portable resolution, no hardcoded paths).
_style_candidates = [Path.home() / ".claude/skills/analyze-stats/references/style/figure_style.mplstyle"]
_root = os.environ.get("MEDSCI_SKILLS_ROOT")
if _root:
    _style_candidates.append(Path(_root) / "skills/analyze-stats/references/style/figure_style.mplstyle")
for _style in _style_candidates:
    if _style.exists():
        plt.style.use(str(_style))
        break


# ── DeLong AUC variance (fast algorithm, Sun & Xu 2014) ──────────────────────
def _compute_midrank(x):
    J = np.argsort(x)
    Z = x[J]
    N = len(x)
    T = np.zeros(N, dtype=float)
    i = 0
    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        T[i:j] = 0.5 * (i + j - 1) + 1
        i = j
    T2 = np.empty(N, dtype=float)
    T2[J] = T
    return T2


def _fast_delong(preds_sorted, m):
    """preds_sorted: rows = predictors, columns = samples (positives first)."""
    n = preds_sorted.shape[1] - m
    k = preds_sorted.shape[0]
    tx = np.empty([k, m], dtype=float)
    ty = np.empty([k, n], dtype=float)
    tz = np.empty([k, m + n], dtype=float)
    for r in range(k):
        tx[r, :] = _compute_midrank(preds_sorted[r, :m])
        ty[r, :] = _compute_midrank(preds_sorted[r, m:])
        tz[r, :] = _compute_midrank(preds_sorted[r, :])
    aucs = tz[:, :m].sum(axis=1) / m / n - (m + 1.0) / 2.0 / n
    v01 = (tz[:, :m] - tx[:, :]) / n
    v10 = 1.0 - (tz[:, m:] - ty[:, :]) / m
    sx = np.cov(v01)
    sy = np.cov(v10)
    delongcov = sx / m + sy / n
    return aucs, np.atleast_2d(delongcov)


def delong_auc_var(y_true, y_score):
    order = (-y_true).argsort(kind="mergesort")
    label_1_count = int(y_true.sum())
    preds_sorted = y_score[order].reshape(1, -1)
    aucs, cov = _fast_delong(preds_sorted, label_1_count)
    return float(aucs[0]), float(cov[0, 0])


def delong_ci(y_true, y_score, alpha=0.05):
    auc, var = delong_auc_var(np.asarray(y_true, float), np.asarray(y_score, float))
    se = np.sqrt(var)
    z = stats.norm.ppf(1 - alpha / 2)
    lo, hi = auc - z * se, auc + z * se
    return auc, max(0.0, lo), min(1.0, hi), se


def delong_test(y_true, score_a, score_b):
    """Two-sided p-value for AUC_a == AUC_b (paired, same samples)."""
    y_true = np.asarray(y_true, float)
    order = (-y_true).argsort(kind="mergesort")
    m = int(y_true.sum())
    preds = np.vstack([np.asarray(score_a, float)[order], np.asarray(score_b, float)[order]])
    aucs, cov = _fast_delong(preds, m)
    var = cov[0, 0] + cov[1, 1] - 2 * cov[0, 1]
    if var <= 0:
        return float(aucs[0]), float(aucs[1]), 1.0
    z = (aucs[0] - aucs[1]) / np.sqrt(var)
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return float(aucs[0]), float(aucs[1]), float(p)


def wilson_ci(k, n, alpha=0.05):
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    z = stats.norm.ppf(1 - alpha / 2)
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return p, max(0.0, center - half), min(1.0, center + half)


# ── Load ─────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA)
y = (df["diagnosis"] == "malignant").astype(int).to_numpy()
feature_cols = [c for c in df.columns if c not in ("target", "diagnosis")]
X = df[feature_cols].to_numpy()
N = len(df)
n_mal = int(y.sum())
print(f"N={N}, malignant={n_mal} ({n_mal/N*100:.1f}%), benign={N-n_mal}, features={len(feature_cols)}")

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=SEED
)
scaler = StandardScaler().fit(X_tr)
X_tr_s, X_te_s = scaler.transform(X_tr), scaler.transform(X_te)
print(f"train n={len(y_tr)} (mal={int(y_tr.sum())}), test n={len(y_te)} (mal={int(y_te.sum())})")

models = {
    "Logistic Regression": LogisticRegression(max_iter=5000, random_state=SEED),
    "Random Forest": RandomForestClassifier(n_estimators=400, random_state=SEED),
    "SVM (RBF)": SVC(kernel="rbf", probability=True, random_state=SEED),
}

# ── Table 1: key features by reference-standard class (10 "mean ___" features) ──
mean_feats = [c for c in feature_cols if c.startswith("mean ")]
rows = []
for c in mean_feats:
    a = df.loc[y == 1, c]  # malignant
    b = df.loc[y == 0, c]  # benign
    # Welch t-test (large n; report SMD)
    t, p = stats.ttest_ind(a, b, equal_var=False)
    pooled_sd = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    smd = (a.mean() - b.mean()) / pooled_sd if pooled_sd > 0 else np.nan
    rows.append({
        "Feature": c,
        "Malignant_mean_SD": f"{a.mean():.2f} ({a.std(ddof=1):.2f})",
        "Benign_mean_SD": f"{b.mean():.2f} ({b.std(ddof=1):.2f})",
        "SMD": round(smd, 2),
        "P_value": f"{p:.2e}" if p < 0.001 else f"{p:.3f}",
    })
table1 = pd.DataFrame(rows)
table1.to_csv(TBL / "table1_features_by_class.csv", index=False)
print("\nTable 1 (features by reference-standard class):")
print(table1.to_string(index=False))

# ── Diagnostic accuracy ────────────────────────────────────────────────────────
def metrics_at_threshold(y_true, proba, thr):
    pred = (proba >= thr).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, pred, labels=[0, 1]).ravel()
    sens, sl, sh = wilson_ci(tp, tp + fn)
    spec, pl, ph = wilson_ci(tn, tn + fp)
    ppv, ppl, pph = wilson_ci(tp, tp + fp) if (tp + fp) else (np.nan, np.nan, np.nan)
    npv, nl, nh = wilson_ci(tn, tn + fn) if (tn + fn) else (np.nan, np.nan, np.nan)
    acc, al, ah = wilson_ci(tp + tn, tp + tn + fp + fn)
    return dict(tp=tp, fp=fp, fn=fn, tn=tn,
                sens=sens, sens_lo=sl, sens_hi=sh,
                spec=spec, spec_lo=pl, spec_hi=ph,
                ppv=ppv, ppv_lo=ppl, ppv_hi=pph,
                npv=npv, npv_lo=nl, npv_hi=nh,
                acc=acc, acc_lo=al, acc_hi=ah)


proba_te = {}
acc_rows = []
for name, mdl in models.items():
    mdl.fit(X_tr_s, y_tr)
    p = mdl.predict_proba(X_te_s)[:, 1]
    proba_te[name] = p
    auc, lo, hi, se = delong_ci(y_te, p)
    brier = brier_score_loss(y_te, p)
    # Youden-optimal threshold
    fpr, tpr, thr = roc_curve(y_te, p)
    youden = tpr - fpr
    j_thr = float(thr[np.argmax(youden)])
    m05 = metrics_at_threshold(y_te, p, 0.5)
    mYou = metrics_at_threshold(y_te, p, j_thr)
    acc_rows.append({
        "Model": name,
        "AUC": round(auc, 3), "AUC_lo": round(lo, 3), "AUC_hi": round(hi, 3),
        "Brier": round(brier, 3),
        "Thr0.5_Sens": round(m05["sens"], 3), "Thr0.5_Sens_lo": round(m05["sens_lo"], 3), "Thr0.5_Sens_hi": round(m05["sens_hi"], 3),
        "Thr0.5_Spec": round(m05["spec"], 3), "Thr0.5_Spec_lo": round(m05["spec_lo"], 3), "Thr0.5_Spec_hi": round(m05["spec_hi"], 3),
        "Thr0.5_PPV": round(m05["ppv"], 3), "Thr0.5_NPV": round(m05["npv"], 3),
        "Thr0.5_Acc": round(m05["acc"], 3),
        "Youden_thr": round(j_thr, 3),
        "Youden_Sens": round(mYou["sens"], 3), "Youden_Spec": round(mYou["spec"], 3),
        "TP": m05["tp"], "FP": m05["fp"], "FN": m05["fn"], "TN": m05["tn"],
    })

acc_df = pd.DataFrame(acc_rows)
acc_df.to_csv(TBL / "diagnostic_accuracy.csv", index=False)
print("\nDiagnostic accuracy (test set, threshold 0.5; Wilson CIs for proportions, DeLong CIs for AUC):")
print(acc_df.to_string(index=False))

# Pairwise DeLong AUC comparisons
names = list(models.keys())
cmp_rows = []
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a_auc, b_auc, p = delong_test(y_te, proba_te[names[i]], proba_te[names[j]])
        cmp_rows.append({"Model_A": names[i], "Model_B": names[j],
                         "AUC_A": round(a_auc, 3), "AUC_B": round(b_auc, 3),
                         "DeLong_p": f"{p:.3f}" if p >= 0.001 else f"{p:.2e}"})
cmp_df = pd.DataFrame(cmp_rows)
cmp_df.to_csv(TBL / "auc_comparison_delong.csv", index=False)
print("\nPairwise DeLong AUC comparison:")
print(cmp_df.to_string(index=False))

# predictions.csv (per-sample test set)
pred_out = pd.DataFrame({"y_true": y_te})
for name in models:
    pred_out[f"proba_{name.split()[0].lower()}"] = proba_te[name]
pred_out.to_csv(TBL / "predictions.csv", index=False)

# ── Figures ────────────────────────────────────────────────────────────────────
# ROC
fig, ax = plt.subplots(figsize=(3.5, 3.5))
for name in models:
    fpr, tpr, _ = roc_curve(y_te, proba_te[name])
    auc, lo, hi, _ = delong_ci(y_te, proba_te[name])
    ax.plot(fpr, tpr, lw=1.5, label=f"{name.split('(')[0].strip()} (AUC {auc:.3f})")
ax.plot([0, 1], [0, 1], "k--", lw=0.8, alpha=0.6)
ax.set_xlabel("1 − Specificity")
ax.set_ylabel("Sensitivity")
ax.set_title("ROC — malignancy classification")
ax.legend(loc="lower right", fontsize=7, frameon=False)
fig.tight_layout()
fig.savefig(FIG / "roc_curve.pdf")
fig.savefig(FIG / "roc_curve.png", dpi=300)
plt.close(fig)

# Confusion matrices @0.5
fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.6))
for ax, name in zip(axes, models):
    pred = (proba_te[name] >= 0.5).astype(int)
    cm = confusion_matrix(y_te, pred, labels=[0, 1])
    im = ax.imshow(cm, cmap="Blues")
    for (r, c), v in np.ndenumerate(cm):
        ax.text(c, r, str(v), ha="center", va="center",
                color="white" if v > cm.max() / 2 else "black", fontsize=9)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Benign", "Malig"], fontsize=7)
    ax.set_yticks([0, 1]); ax.set_yticklabels(["Benign", "Malig"], fontsize=7)
    ax.set_xlabel("Predicted", fontsize=8); ax.set_ylabel("Actual", fontsize=8)
    ax.set_title(name.split("(")[0].strip(), fontsize=8)
fig.tight_layout()
fig.savefig(FIG / "confusion_matrices.pdf")
fig.savefig(FIG / "confusion_matrices.png", dpi=300)
plt.close(fig)

# ── Manifest ───────────────────────────────────────────────────────────────────
manifest = f"""# Analysis Outputs
Generated: 2026-06-07
Study type: Diagnostic accuracy (DTA / STARD), index tests vs histopathology reference

## Dataset
- Wisconsin Breast Cancer (sklearn.datasets.load_breast_cancer), N={N}, malignant={n_mal}, benign={N-n_mal}, {len(feature_cols)} FNA features.
- Stratified 70/30 train/test split, seed={SEED}. Test n={len(y_te)}.

## Tables
- `tables/table1_features_by_class.csv` -- Key features by reference-standard class (mean (SD), SMD, P)
- `tables/diagnostic_accuracy.csv` -- Sens/Spec/PPV/NPV/Acc (Wilson CIs) + AUC (DeLong CI) + Brier + Youden threshold
- `tables/auc_comparison_delong.csv` -- Pairwise DeLong AUC comparison
- `tables/predictions.csv` -- Per-sample test-set predicted probabilities + truth

## Figures
- `figures/roc_curve.pdf` / `.png` -- ROC curves (3 models, DeLong AUC in legend)
- `figures/confusion_matrices.pdf` / `.png` -- Confusion matrices at threshold 0.5

## Key results (test set, n={len(y_te)})
"""
for r in acc_rows:
    manifest += (f"- {r['Model']}: AUC {r['AUC']} ({r['AUC_lo']}-{r['AUC_hi']}), "
                 f"Sens {r['Thr0.5_Sens']}, Spec {r['Thr0.5_Spec']}, Brier {r['Brier']}\n")
(WORK / "analysis" / "_analysis_outputs.md").write_text(manifest, encoding="utf-8")
print("\nWrote _analysis_outputs.md")
print("DONE")
