import pandas as pd
import plotly.express as px

def temperature_chart(df):
    return px.line(
        df, x="timestamp", y="temperature_C",
        title="Temperature Trend", markers=True
    )

def parameter_chart(record_df):
    cols = ["temperature_C", "humidity_%", "wind_speed_kmh", "rainfall_mm", "pressure_hPa"]
    values = [{"Parameter": c, "Value": record_df[c].iloc[0]}
              for c in cols if c in record_df.columns]
    return px.bar(pd.DataFrame(values), x="Parameter", y="Value",
                  title="Current Weather Parameters")
