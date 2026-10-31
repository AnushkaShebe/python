# Real Time Weather Dashboard

**Student:** Anushka Shebe  
**Project ID:** CM25068  
**Technology:** Python, Streamlit, Pandas, Plotly

## Features
- Global city search and live current weather
- Temperature, feels-like temperature, humidity and wind speed
- UV index, sunrise, sunset and rain probability
- 24-hour temperature graph
- Five-day forecast table and chart
- Hourly data and search-history CSV downloads
- No API key required (Open-Meteo)

## Run locally in VS Code
Use Python 3.10 or newer. Open this folder in VS Code Terminal and run:

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install and run:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Visit https://share.streamlit.io/ and sign in with GitHub.
2. Select **Create app**.
3. Repository: `AnushkaShebe/python`
4. Branch: `main`
5. Main file path: `weather_dashboard/app.py`
6. Click **Deploy**. No API key or Secrets are required.

## Data source
Open-Meteo Geocoding API and Forecast API. Weather data is provided as forecasts/model-based data and availability may vary by location.

## Notes
- Search history is stored in the active session and is not a permanent database.
- The 24-hour chart uses the hourly forecast data returned by Open-Meteo.
