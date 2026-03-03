"""
analyzer.py
Analyzes and visualizes offshore sensor data.
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from generate_data import generate_sensor_data

# ── Load and clean data ────────────────────────────────────────────────────────
df = generate_sensor_data()
df = df.drop_duplicates(subset="timestamp").sort_values("timestamp")
df[["pressure", "temperature", "flow_rate"]] = df[["pressure", "temperature", "flow_rate"]].ffill()
print(f"Cleaned data: {len(df)} rows ready for analysis\n")

# ── Analyze ────────────────────────────────────────────────────────────────────
print("=== SENSOR REPORT ===")
for col in ["pressure", "temperature", "flow_rate"]:
    print(f"\n{col.upper()}")
    print(f"  mean: {df[col].mean():.2f}  min: {df[col].min():.2f}  max: {df[col].max():.2f}")

anomalies = df[(df["pressure"] > 330) | (df["pressure"] < 270) | (df["temperature"] > 100)].copy()
anomalies["reason"] = "High temperature"
anomalies.loc[df["pressure"] > 330, "reason"] = "High pressure"
anomalies.loc[df["pressure"] < 270, "reason"] = "Low pressure"
print(f"\n⚠ Anomalies found: {len(anomalies)}")
print(anomalies[["timestamp", "pressure", "temperature", "reason"]].to_string(index=False))

# ── Static graph ───────────────────────────────────────────────────────────────
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
for ax, col, color, limits in [
    (ax1, "pressure",    "steelblue", [330, 270]),
    (ax2, "temperature", "tomato",    [100]),
    (ax3, "flow_rate",   "seagreen",  []),
]:
    ax.plot(df["timestamp"], df[col], color=color, linewidth=0.8)
    for limit in limits:
        ax.axhline(limit, color="red", linestyle="--", linewidth=0.8)
    ax.scatter(anomalies["timestamp"], anomalies[col], color="red", zorder=5, s=30)
    ax.set_ylabel(col)
    ax.grid(True, alpha=0.3)

plt.suptitle("Offshore Sensor Monitor", fontweight="bold")
plt.tight_layout()
plt.savefig("sensor_report.png", dpi=150)
print("\nGraph saved → sensor_report.png")

# ── Interactive dashboard ──────────────────────────────────────────────────────
fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                    subplot_titles=("Pressure (bar)", "Temperature (°C)", "Flow Rate (m³/h)"))
for row, (col, color) in enumerate([("pressure", "steelblue"), ("temperature", "tomato"), ("flow_rate", "seagreen")], 1):
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df[col], name=col, line=dict(color=color)), row=row, col=1)

fig.add_trace(go.Scatter(x=anomalies["timestamp"], y=anomalies["pressure"],
    mode="markers", marker=dict(color="red", size=8, symbol="x"),
    name="Anomaly", hovertext=anomalies["reason"]), row=1, col=1)
fig.add_hline(y=330, line_dash="dash", line_color="red",    row=1, col=1)
fig.add_hline(y=270, line_dash="dash", line_color="orange", row=1, col=1)
fig.add_hline(y=100, line_dash="dash", line_color="red",    row=2, col=1)
fig.update_layout(title="Offshore Sensor Monitor – Interactive", height=800, template="plotly_white")
fig.write_html("sensor_dashboard.html", include_plotlyjs="cdn")
print("Dashboard saved → sensor_dashboard.html")
