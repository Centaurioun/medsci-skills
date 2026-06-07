"""
Analysis: NHANES 2017-2018 analytic frame preparation (obesity <-> diabetes)
Date: 2026-06-07
Random seed: 42
Python: 3.14
Key packages: pandas==2.3.3
Reads raw SAS XPORT files, merges on SEQN, applies inclusion criteria,
and writes a single analytic CSV for downstream R survey analysis.
NO data is fabricated; every row originates from the CDC public XPT files.
"""
import os
import numpy as np
import pandas as pd

np.random.seed(42)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")


def read_xpt(name):
    path = os.path.join(DATA, f"{name}.xpt")
    df = pd.read_sas(path, format="xport")
    # SEQN comes in as float; keep as numeric key
    return df


# --- 1. Read raw files ---------------------------------------------------
demo = read_xpt("DEMO_J")[["SEQN", "RIDAGEYR", "RIAGENDR", "RIDRETH3",
                            "WTMEC2YR", "SDMVSTRA", "SDMVPSU"]]
bmx = read_xpt("BMX_J")[["SEQN", "BMXBMI"]]
diq = read_xpt("DIQ_J")[["SEQN", "DIQ010"]]
ghb = read_xpt("GHB_J")[["SEQN", "LBXGH"]]

print("Raw file row counts (records on disk):")
print(f"  DEMO_J: {len(demo)}")
print(f"  BMX_J : {len(bmx)}")
print(f"  DIQ_J : {len(diq)}")
print(f"  GHB_J : {len(ghb)}")

# --- 2. Merge on SEQN ----------------------------------------------------
df = demo.merge(bmx, on="SEQN", how="left") \
         .merge(diq, on="SEQN", how="left") \
         .merge(ghb, on="SEQN", how="left")
n_total = len(df)
print(f"\nMerged demographics frame (all DEMO_J participants): n = {n_total}")

# --- 3. Exclusion cascade (STROBE) --------------------------------------
cascade = []
cascade.append(("Total NHANES 2017-2018 participants (DEMO_J)", n_total))

# Step A: adults age >= 20
df_a = df[df["RIDAGEYR"] >= 20].copy()
cascade.append(("Excluded: age < 20 years", n_total - len(df_a)))
cascade.append(("Adults aged >= 20 years", len(df_a)))

# Step B: non-missing BMI
df_b = df_a[df_a["BMXBMI"].notna()].copy()
cascade.append(("Excluded: missing BMI (BMXBMI)", len(df_a) - len(df_b)))
cascade.append(("With measured BMI", len(df_b)))

# Step C: valid diabetes status (DIQ010 in {1,2}; exclude 7=refused, 9=don't know, missing, 3=borderline)
# DIQ010 codes: 1=Yes, 2=No, 3=Borderline, 7=Refused, 9=Don't know
df_c = df_b[df_b["DIQ010"].isin([1, 2])].copy()
cascade.append(("Excluded: diabetes status borderline/refused/unknown/missing (DIQ010 not in {1,2})",
                len(df_b) - len(df_c)))
cascade.append(("With valid self-reported diabetes status", len(df_c)))

# Step D: positive MEC exam weight
df_d = df_c[df_c["WTMEC2YR"] > 0].copy()
cascade.append(("Excluded: non-positive MEC exam weight (WTMEC2YR <= 0)", len(df_c) - len(df_d)))
cascade.append(("FINAL analytic sample", len(df_d)))

print("\n=== STROBE exclusion cascade ===")
for label, n in cascade:
    print(f"  {label}: {n}")

# --- 4. Derive analysis variables ---------------------------------------
analytic = df_d.copy()
analytic["obesity"] = (analytic["BMXBMI"] >= 30).astype(int)      # exposure: BMI>=30
analytic["diabetes"] = (analytic["DIQ010"] == 1).astype(int)       # outcome: self-report
analytic["female"] = (analytic["RIAGENDR"] == 2).astype(int)       # 1=Male, 2=Female
analytic["age"] = analytic["RIDAGEYR"].astype(float)
# RIDRETH3: 1 Mex-Am, 2 Other Hispanic, 3 NH White, 4 NH Black, 6 NH Asian, 7 Other/Multi
analytic["race"] = analytic["RIDRETH3"].astype(int)

# HbA1c sensitivity definition: LBXGH >= 6.5 (lab-confirmed diabetes among those with a value)
analytic["hba1c"] = analytic["LBXGH"]
analytic["dm_hba1c"] = np.where(analytic["LBXGH"].notna(),
                                (analytic["LBXGH"] >= 6.5).astype(float),
                                np.nan)

# --- 5. Keep modeling columns + design vars -----------------------------
keep = ["SEQN", "age", "female", "race", "BMXBMI", "obesity",
        "DIQ010", "diabetes", "hba1c", "dm_hba1c",
        "WTMEC2YR", "SDMVSTRA", "SDMVPSU"]
out = analytic[keep].copy()

out_path = os.path.join(DATA, "nhanes_analytic.csv")
out.to_csv(out_path, index=False)
print(f"\nWrote analytic frame: {out_path}  (n = {len(out)}, cols = {len(keep)})")

# Write the cascade as a CSV for reproducible downstream use
casc_df = pd.DataFrame(cascade, columns=["step", "n"])
casc_path = os.path.join(BASE, "analysis", "tables", "exclusion_cascade.csv")
casc_df.to_csv(casc_path, index=False)
print(f"Wrote exclusion cascade: {casc_path}")

# --- 6. Quick unweighted sanity counts ----------------------------------
print("\n=== Unweighted sanity counts (final sample) ===")
print(f"  N = {len(out)}")
print(f"  Obesity (BMI>=30): {out['obesity'].sum()} ({100*out['obesity'].mean():.1f}%)")
print(f"  Diabetes (self-report): {out['diabetes'].sum()} ({100*out['diabetes'].mean():.1f}%)")
print(f"  HbA1c available: {out['hba1c'].notna().sum()}")
print(f"  HbA1c>=6.5 (among available): "
      f"{int(np.nansum(out['dm_hba1c']))} / {out['dm_hba1c'].notna().sum()}")
print("\nDone.")
