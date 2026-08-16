# Real-Time Weather Data Analytics Dashboard

**Student:** Anushka Shebe  
**Project ID:** CM25068  
**Technology:** Python

## Features
- Real-time weather data
- City search
- Temperature, humidity, wind, pressure and rainfall
- Historical data stored in CSV
- Statistical analysis
- Interactive Plotly charts
- Weather-condition distribution
- CSV download
- No API key required

## How to run

### Windows

Open the project folder in VS Code and run:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If `python` does not work, use `py`:

```powershell
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

The dashboard normally opens at:

http://localhost:8501

## Data source

The project uses Open-Meteo geocoding and forecast APIs. An API key is not required for this student project.

## Project structure

```text
Real_Time_Weather_Dashboard/
│
├── app.py
├── weather_api.py
├── data_analysis.py
├── requirements.txt
├── .gitignore
├── README.md
└── data/
    └── weather_history.csv  # created automatically
```
