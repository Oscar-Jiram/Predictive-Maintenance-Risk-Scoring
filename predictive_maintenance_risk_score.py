# ============================================
# Predictive Maintenance – Risk Scoring Project
# ============================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------
# 1. Load dataset (local CSV)
# --------------------------------------------

DATA_PATH = "ai4i2020.csv"

df = pd.read_csv(DATA_PATH)

# --------------------------------------------
# 2. Basic cleaning
# --------------------------------------------

df = df.drop_duplicates().reset_index(drop=True)

# --------------------------------------------
# 3. Feature engineering (proxies)
# --------------------------------------------

# Temperature delta
df["delta_temp"] = df["Process temperature [K]"] - df["Air temperature [K]"]

# Power proxy (load indicator)
df["power_proxy"] = df["Torque [Nm]"] * df["Rotational speed [rpm]"]

df["wear_rate_proxy"] = df["Tool wear [min]"] / df["Rotational speed [rpm]"].replace(0, np.nan)
df["wear_rate_proxy"] = df["wear_rate_proxy"].fillna(0)

# Wear rate proxy
df["wear_rate_proxy"] = df["Tool wear [min]"] / df["Rotational speed [rpm]"]

# --------------------------------------------
# 4. Reliability KPIs
# --------------------------------------------

# Global failure rate
failure_rate = df["Machine failure"].mean()

# Failure rate by machine type
failure_rate_by_type = (
    df.groupby("Type")["Machine failure"]
      .mean()
      .sort_values(ascending=False)
)

# Failure modes distribution
failure_modes = ["TWF", "HDF", "PWF", "OSF", "RNF"]
mode_counts = df[failure_modes].sum().sort_values(ascending=False)
mode_pct = mode_counts / mode_counts.sum() * 100

# --------------------------------------------
# 5. Operating conditions by failure mode
# --------------------------------------------

operating_cols = [
    "delta_temp",
    "Torque [Nm]",
    "Rotational speed [rpm]",
    "Tool wear [min]"
]

HDF_OC = df.groupby("HDF")[operating_cols].mean()
OSF_OC = df.groupby("OSF")[operating_cols].mean()
PWF_OC = df.groupby("PWF")[operating_cols].mean()

# --------------------------------------------
# 6. Risk score construction
# --------------------------------------------

risk_features = ["Torque [Nm]", "Tool wear [min]", "power_proxy"]

for col in risk_features:
    df[col + "_norm"] = (
        (df[col] - df[col].min()) /
        (df[col].max() - df[col].min())
    )

df["risk_score"] = (
    0.4 * df["Torque [Nm]_norm"] +
    0.4 * df["Tool wear [min]_norm"] +
    0.2 * df["power_proxy_norm"]
)

# --------------------------------------------
# 7. Risk level segmentation (quantiles)
# --------------------------------------------

df["risk_level"] = pd.qcut(
    df["risk_score"],
    q=3,
    labels=["Low", "Medium", "High"]
)

# Failure rate by risk level
failure_by_risk = (
    df.groupby("risk_level", observed=False)["Machine failure"]
      .mean()
      * 100
)

# --------------------------------------------
# 8. Export business-ready dataset
# --------------------------------------------

os.makedirs("export", exist_ok=True)

final_cols = [
    "UDI", "Product ID", "Type",
    "Air temperature [K]", "Process temperature [K]",
    "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]",
    "delta_temp", "power_proxy",
    "Machine failure", "TWF", "HDF", "PWF", "OSF", "RNF",
    "risk_score", "risk_level"
]

df[final_cols].to_csv(
    "export/business_kpis.csv",
    index=False
)

# --------------------------------------------
# 9. Plots (saved to outputs/)
# --------------------------------------------

os.makedirs("outputs", exist_ok=True)

# Failure rate by risk level
failure_by_risk.plot(kind="bar")
plt.ylabel("Failure rate (%)")
plt.title("Failure Rate by Risk Level")
plt.tight_layout()
plt.savefig("outputs/failure_rate_by_risk_level.png", dpi=150)
plt.close()

# --------------------------------------------
# 7B. Risk score validation (business-ready)
# --------------------------------------------

# Baseline failure rate (%)
baseline_fail_pct = failure_rate * 100

# Segment sizes
risk_counts = df["risk_level"].value_counts().reindex(["Low", "Medium", "High"])

# Failure rate by segment (%)
risk_fail_pct = (
    df.groupby("risk_level", observed=False)["Machine failure"]
      .mean()
      .reindex(["Low", "Medium", "High"])
      * 100
)

# Lift vs baseline (how many times higher/lower than overall failure rate)
risk_lift_vs_baseline = risk_fail_pct / baseline_fail_pct

risk_summary = pd.DataFrame({
    "units": risk_counts,
    "failure_rate_pct": risk_fail_pct.round(2),
    "lift_vs_baseline": risk_lift_vs_baseline.round(2)
})

print("\n=== Risk Validation Summary ===")
print(risk_summary)

# Save summary for BI / reporting
os.makedirs("export", exist_ok=True)
risk_summary.to_csv("export/risk_summary.csv", index=True)



# Pareto of failure modes
mode_pct.plot(kind="bar")
plt.ylabel("Share of failures (%)")
plt.title("Pareto of Failure Modes")
plt.tight_layout()
plt.savefig("outputs/pareto_failure_modes.png", dpi=150)
plt.close()

# Failure rate by machine type
(failure_rate_by_type * 100).plot(kind="bar")
plt.ylabel("Failure rate (%)")
plt.title("Failure Rate by Product Type")
plt.tight_layout()
plt.savefig("outputs/failure_rate_by_type.png", dpi=150)
plt.close()

# --------------------------------------------
# 10. Console summary (sanity check)
# --------------------------------------------

print("Global failure rate:", round(failure_rate * 100, 2), "%")
print("\nFailure rate by risk level (%):")
print(failure_by_risk)

print("\nTop failure modes (%):")
print(mode_pct.round(2))
