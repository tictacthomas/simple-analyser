"""
generate_data.py
Generates simulated offshore sensor data.
"""

import pandas as pd
import numpy as np


def generate_sensor_data() -> pd.DataFrame:
    np.random.seed(42)
    timestamps   = pd.date_range("2024-01-01", periods=432, freq="10min")
    pressure     = 300 + np.cumsum(np.random.randn(432) * 0.5)
    temperature  = 85  + np.cumsum(np.random.randn(432) * 0.2)
    flow_rate    = 50  + np.random.randn(432) * 2

    # Inject anomalies
    pressure[50]     = 340   # pressure spike
    pressure[150]    = 260   # pressure drop
    temperature[200] = 105   # temperature spike

    return pd.DataFrame({
        "timestamp":   timestamps,
        "pressure":    pressure.round(2),
        "temperature": temperature.round(2),
        "flow_rate":   flow_rate.round(2),
    })
