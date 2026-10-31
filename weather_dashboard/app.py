import requests
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Real Time Weather Dashboard", page_icon="🌦️", layout="wide")

st.markdown("""
<style>
.stApp{background:#f4f8fc}
.block-container{padding-top:1.5rem}
.hero{padding:24px;border-radius:18px;color:white;background:linear-gradient(120deg,#102a43,#247ba0)}
.hero h1{color:white;margin:0}
div[data-testid="stMetric"]{background:white;padding:14px;border-radius:14px;border:1px solid #e5edf5}
</style>
<div class="hero"><h1>🌦️ Real Time Weather Dashboard</h1>
<p>Live weather analytics and forecast · Powered by Open-Meteo</p></div>
""", unsafe_allow_html=True)

GEO="https://geocoding-api.open-meteo.com/v1/search"
API="https://api.open-meteo.com/v1/forecast"

@st.cache_data(ttl=600)
def city_search(name):
    r=requests.get(GEO,params={"name":name,"count":5,"language":"en","format":"json"},timeout=15)
    r.raise_for_status()
    results=r.json().get("results",[])
    if not results: return None
    return next((x for x in results if x.get("name","").casefold()==name.casefold()),results[0])

@st.cache_data(ttl=600)
def weather_data(lat,lon,tz):
    params={
      "latitude":lat,"longitude":lon,"timezone":tz or "auto",
      "current":"temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
      "hourly":"temperature_2m,relative_humidity_2m,precipitation_probability",
      "daily":"weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_probability_max",
      "forecast_days":5
    }
    r=requests.get(API,params=params,timeout=20)
    r.raise_for_status()
    return r.json()

def describe(code):
    return {0:"Clear sky",1:"Mainly clear",2:"Partly cloudy",3:"Overcast",45:"Fog",48:"Rime fog",51:"Light drizzle",53:"Drizzle",55:"Heavy drizzle",61:"Light rain",63:"Moderate rain",65:"Heavy rain",71:"Light snow",73:"Snow",75:"Heavy snow",80:"Rain showers",81:"Moderate showers",82:"Heavy showers",95:"Thunderstorm",96:"Thunderstorm with hail",99:"Severe thunderstorm"}.get(int(code),"Weather conditions")

with st.sidebar:
    st.header("🔎 Search Location")
    city=st.text_input("Enter city name",placeholder="e.g. Nagpur")
    go=st.button("Get Live Weather",type="primary",use_container_width=True)
    st.caption("No API key required · Data by Open-Meteo")

if "history" not in st.session_state: st.session_state.history=[]
if "result" not in st.session_state: st.session_state.result=None

if go:
    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        try:
            with st.spinner("Fetching weather data..."):
                place=city_search(city.strip())
                if not place:
                    st.error("City not found. Check the spelling and try again.")
                else:
                    data=weather_data(place["latitude"],place["longitude"],place.get("timezone","auto"))
                    st.session_state.result={"place":place,"data":data}
                    st.session_state.history.insert(0,{"City":place["name"],"Country":place.get("country","")})
                    st.session_state.history=st.session_state.history[:20]
        except requests.RequestException as e:
            st.error(f"Unable to fetch weather data: {e}")

if st.session_state.result:
    place=st.session_state.result["place"]
    data=st.session_state.result["data"]
    cur=data["current"]; day=data["daily"]; hour=data["hourly"]
    st.subheader(f"📍 {place['name']}, {place.get('admin1',place.get('country',''))}")
    st.caption(f"Latitude: {place['latitude']} · Longitude: {place['longitude']} · Local time: {cur['time']}")
    st.markdown(f"### {describe(cur['weather_code'])}")
    a,b,c,d=st.columns(4)
    a.metric("🌡️ Temperature",f"{cur['temperature_2m']} °C")
    b.metric("🤗 Feels like",f"{cur['apparent_temperature']} °C")
    c.metric("💧 Humidity",f"{cur['relative_humidity_2m']} %")
    d.metric("💨 Wind speed",f"{cur['wind_speed_10m']} km/h")
    e,f,g,h=st.columns(4)
    e.metric("☀️ UV index (max today)",day["uv_index_max"][0])
    f.metric("🌧️ Rain probability",f"{day['precipitation_probability_max'][0]} %")
    g.metric("🌅 Sunrise",day["sunrise"][0].split("T")[-1])
    h.metric("🌇 Sunset",day["sunset"][0].split("T")[-1])

    st.subheader("📈 Next 24 hours — Temperature")
    hourly_df=pd.DataFrame({"Time":pd.to_datetime(hour["time"]),"Temperature (°C)":hour["temperature_2m"],"Humidity (%)":hour["relative_humidity_2m"],"Rain probability (%)":hour["precipitation_probability"]}).head(24)
    fig=px.line(hourly_df,x="Time",y="Temperature (°C)",markers=True,title="Hourly temperature forecast")
    fig.update_layout(height=350,margin=dict(l=10,r=10,t=50,b=10))
    st.plotly_chart(fig,use_container_width=True)

    st.subheader("🗓️ Five-day forecast")
    daily_df=pd.DataFrame({"Date":pd.to_datetime(day["time"]).date,"Condition":[describe(x) for x in day["weather_code"]],"Minimum (°C)":day["temperature_2m_min"],"Maximum (°C)":day["temperature_2m_max"],"UV index":day["uv_index_max"],"Rain probability (%)":day["precipitation_probability_max"]})
    st.dataframe(daily_df,use_container_width=True,hide_index=True)
    fig2=px.bar(daily_df,x="Date",y=["Minimum (°C)","Maximum (°C)"],barmode="group",title="Daily minimum and maximum temperature")
    st.plotly_chart(fig2,use_container_width=True)
    with st.expander("Hourly data and CSV download"):
        st.dataframe(hourly_df,use_container_width=True,hide_index=True)
        st.download_button("Download hourly CSV",hourly_df.to_csv(index=False).encode("utf-8"),"weather_hourly_data.csv","text/csv")
else:
    st.info("Enter a city name in the sidebar and click Get Live Weather.")
    x,y,z=st.columns(3)
    x.markdown("#### 🌍 Global city search\nSearch cities around the world.")
    y.markdown("#### 📊 Weather analytics\nTemperature, humidity, wind and UV.")
    z.markdown("#### 🗓️ Forecast\n24-hour trends and five-day forecast.")

st.divider()
st.subheader("🕘 Recent search history")
if st.session_state.history:
    hist=pd.DataFrame(st.session_state.history)
    st.dataframe(hist,use_container_width=True,hide_index=True)
    st.download_button("Download search history CSV",hist.to_csv(index=False).encode("utf-8"),"weather_search_history.csv","text/csv")
else:
    st.caption("Your recent searches will appear here during this session.")
st.caption("Student Project · Anushka Shebe · CM25068 · Python + Streamlit + Open-Meteo")
