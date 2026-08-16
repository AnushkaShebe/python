import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from weather_api import get_weather
from data_analysis import (
    save_weather_data,
    load_weather_data,
    get_city_history,
    calculate_statistics,
    clear_history,
)

st.set_page_config(
    page_title="Real-Time Weather Analytics",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
.hero {
    padding: 1.5rem 1.8rem;
    border-radius: 18px;
    border: 1px solid rgba(128,128,128,.25);
    margin-bottom: 1.2rem;
}
.hero h1 {margin: 0; font-size: 2.2rem;}
.hero p {margin: .35rem 0 0; opacity: .75;}
.small-muted {opacity: .65; font-size: .85rem;}
</style>
""", unsafe_allow_html=True)

if "weather" not in st.session_state:
    st.session_state.weather = None
if "last_city" not in st.session_state:
    st.session_state.last_city = "Nagpur"

st.markdown("""
<div class="hero">
    <h1>🌤️ Real-Time Weather Data Analytics Dashboard</h1>
    <p>Python project • Real-time weather • Data storage • Analytics • Interactive charts</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🔎 Weather Search")
    city = st.text_input("Enter city", value=st.session_state.last_city, placeholder="e.g. Nagpur")

    col_a, col_b = st.columns(2)
    with col_a:
        fetch = st.button("Get Weather", type="primary", use_container_width=True)
    with col_b:
        refresh = st.button("Refresh", use_container_width=True)

    st.divider()
    st.subheader("Project")
    st.write("**Student:** Anushka Shebe")
    st.write("**Project ID:** CM25068")
    st.write("**Technology:** Python")
    st.write("**API:** Open-Meteo")
    st.caption("Open-Meteo is used so the project runs without an API key.")

    st.divider()
    if st.button("Clear Saved History", use_container_width=True):
        clear_history()
        st.success("History cleared.")
        st.rerun()

if fetch or refresh:
    if not city.strip():
        st.error("Please enter a city name.")
    else:
        with st.spinner("Fetching live weather data..."):
            result = get_weather(city.strip())

        if result["success"]:
            st.session_state.weather = result["data"]
            st.session_state.last_city = result["data"]["city"]
            save_weather_data(result["data"])
            st.success(
                f"Updated: {result['data']['city']}, "
                f"{result['data']['country']}"
            )
        else:
            st.error(result["error"])

weather = st.session_state.weather

if weather:
    st.subheader(f"📍 {weather['city']}, {weather['country']}")
    st.caption(
        f"Coordinates: {weather['latitude']:.4f}, {weather['longitude']:.4f} • "
        f"Last fetched: {weather['timestamp']}"
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡️ Temperature", f"{weather['temperature']:.1f} °C",
              f"Feels like {weather['feels_like']:.1f} °C")
    c2.metric("💧 Humidity", f"{weather['humidity']:.0f} %")
    c3.metric("💨 Wind Speed", f"{weather['wind_speed']:.1f} km/h")
    c4.metric("🌧️ Rain", f"{weather['rainfall']:.1f} mm")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("🔵 Pressure", f"{weather['pressure']:.0f} hPa")
    c6.metric("☁️ Condition", weather["weather"])
    c7.metric("🌡️ Min Temp", f"{weather['min_temperature']:.1f} °C")
    c8.metric("🌡️ Max Temp", f"{weather['max_temperature']:.1f} °C")

    st.divider()

    left, right = st.columns([1, 2])
    with left:
        st.subheader("Current Condition")
        st.markdown(f"### {weather['weather']}")
        st.write(weather["description"])
        st.write(f"**Wind direction:** {weather['wind_direction']:.0f}°")
        st.write(f"**Visibility:** {weather['visibility']:.1f} km")
    with right:
        st.subheader("Quick Summary")
        summary = (
            f"{weather['city']} is currently experiencing "
            f"{weather['weather'].lower()} conditions with a temperature of "
            f"{weather['temperature']:.1f} °C and humidity of "
            f"{weather['humidity']:.0f}%. "
            f"Wind speed is {weather['wind_speed']:.1f} km/h."
        )
        st.info(summary)
else:
    st.info("Enter a city in the sidebar and click **Get Weather** to start.")
    st.markdown("### Example cities")
    st.write("Nagpur • Mumbai • Pune • Delhi • Bengaluru • Hyderabad")

st.divider()
st.header("📊 Weather Data Analytics")

history = load_weather_data()

if history.empty:
    st.warning("No saved readings yet. Fetch weather data to build your analytics history.")
else:
    cities = sorted(history["City"].dropna().unique().tolist())
    selected_city = st.selectbox("Select city for analysis", cities)

    city_df = get_city_history(history, selected_city)
    stats = calculate_statistics(city_df)

    a1, a2, a3 = st.columns(3)
    a1.metric("Average Temperature", f"{stats['avg_temp']:.1f} °C")
    a2.metric("Maximum Temperature", f"{stats['max_temp']:.1f} °C")
    a3.metric("Minimum Temperature", f"{stats['min_temp']:.1f} °C")

    a4, a5, a6 = st.columns(3)
    a4.metric("Average Humidity", f"{stats['avg_humidity']:.1f} %")
    a5.metric("Maximum Wind", f"{stats['max_wind']:.1f} km/h")
    a6.metric("Total Rainfall", f"{stats['total_rain']:.1f} mm")

    st.subheader("🌡️ Temperature Trend")
    fig_temp = px.line(
        city_df, x="DateTime", y="Temperature",
        markers=True, title=f"Temperature — {selected_city}"
    )
    fig_temp.update_layout(
        xaxis_title="Time", yaxis_title="Temperature (°C)",
        hovermode="x unified"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.subheader("💧 Humidity Trend")
        fig_h = px.line(
            city_df, x="DateTime", y="Humidity",
            markers=True, title="Humidity over time"
        )
        fig_h.update_layout(xaxis_title="Time", yaxis_title="Humidity (%)")
        st.plotly_chart(fig_h, use_container_width=True)

    with right:
        st.subheader("💨 Wind Speed")
        fig_w = px.bar(
            city_df, x="DateTime", y="Wind Speed",
            title="Wind speed over time"
        )
        fig_w.update_layout(xaxis_title="Time", yaxis_title="Wind Speed (km/h)")
        st.plotly_chart(fig_w, use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.subheader("🌧️ Rainfall")
        fig_r = px.bar(
            city_df, x="DateTime", y="Rainfall",
            title="Rainfall over time"
        )
        fig_r.update_layout(xaxis_title="Time", yaxis_title="Rainfall (mm)")
        st.plotly_chart(fig_r, use_container_width=True)

    with right:
        st.subheader("☁️ Weather Conditions")
        counts = city_df["Weather"].value_counts().reset_index()
        counts.columns = ["Weather", "Count"]
        fig_pie = px.pie(
            counts, names="Weather", values="Count",
            title="Condition distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("📋 Stored Weather Records")
    display_df = city_df.copy()
    display_df["DateTime"] = display_df["DateTime"].dt.strftime("%d-%m-%Y %H:%M:%S")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download CSV",
        data=csv,
        file_name=f"{selected_city.lower().replace(' ', '_')}_weather_history.csv",
        mime="text/csv",
    )

st.divider()
st.caption(
    "CM25068 • Anushka Shebe • Real-Time Weather Data Analytics Dashboard"
)
