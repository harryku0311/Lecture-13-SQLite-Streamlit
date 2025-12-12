# Taiwan Agricultural Weather Forecast Dashboard

A comprehensive weather data visualization system that fetches agricultural weather forecasts from Taiwan's Central Weather Administration (CWA) and presents them through both a Streamlit dashboard and an interactive map.

## Features

### 🌤️ Streamlit Dashboard
- **Location-based forecasts**: Select from 6 Taiwan regions
- **Detailed data tables**: View daily forecasts with max/min temperatures
- **Summary statistics**: Quick overview of forecast metrics
- **Responsive design**: Clean, modern UI

### 🗺️ Interactive Map
- **Taiwan map visualization**: See all forecast locations geographically
- **Color-coded markers**: Temperature-based color coding (red=hot, blue=cool)
- **Click interactions**: Click markers to view detailed temperature charts
- **Time-series charts**: Interactive Chart.js graphs showing temperature trends
- **Standalone version**: Can be opened directly in browser without server

## Project Structure

```
.
├── crawler.py              # Fetches weather data from CWA API
├── data_export.py          # Exports data to JSON for web visualization
├── dashboard.py            # Streamlit web dashboard
├── map.html                # Interactive map (requires server)
├── map_standalone.html     # Self-contained map (no server needed)
├── map.js                  # Map JavaScript logic
├── map_standalone.js       # Standalone version JavaScript
├── sqlitedata.db           # SQLite database (created by crawler)
├── weather_data.json       # Exported JSON data
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Installation

### Prerequisites
- Python 3.x
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Fetch Weather Data

Run the crawler to fetch latest data from CWA:

```bash
python crawler.py
```

This creates `sqlitedata.db` with weather forecasts for 6 Taiwan regions.

### Step 2: View in Streamlit Dashboard

```bash
streamlit run dashboard.py
```

Opens at `http://localhost:8501`

### Step 3: View Interactive Map

#### Option A: With HTTP Server

```bash
# Terminal 1: Start HTTP server
python -m http.server 8000

# Then open in browser:
# http://localhost:8000/map.html
```

#### Option B: Standalone (No Server)

1. Export data to JSON:
```bash
python data_export.py
```

2. Double-click `map_standalone.html` or open it in your browser

The standalone version has all data embedded and works without a server!

## Technologies Used

### Backend
- **Python 3**: Core language
- **SQLite**: Local database
- **Requests**: HTTP client for API calls
- **Pandas**: Data manipulation

### Frontend - Streamlit Dashboard
- **Streamlit**: Web dashboard framework
- **Pandas**: Data display

### Frontend - Interactive Map
- **HTML5 & JavaScript**: Web standards
- **Tailwind CSS**: Modern styling framework
- **Leaflet.js**: Interactive map library
- **Chart.js**: Temperature visualization charts

## Data Source

Weather data from **Taiwan Central Weather Administration (CWA) OpenData API**:
- Endpoint: Agricultural Weather Forecasts (F-A0010-001)
- Coverage: 6 Taiwan regions (North, Central, South, East, Northeast, Southeast)
- Update Frequency: As provided by CWA

## Features Breakdown

### Weather Data Collection (`crawler.py`)
- Fetches from CWA OpenData API
- Stores in two SQLite tables:
  - `weather_summary`: General weather profiles
  - `daily_forecasts`: Location-specific daily forecasts
- Automatic database initialization

### Streamlit Dashboard (`dashboard.py`)
- Location dropdown selector
- Sortable data tables
- Summary metrics (total days, avg temps)
- Error handling for missing data

### Interactive Map System
- **Data Export** (`data_export.py`): Converts SQLite → JSON with coordinates
- **Map Visualization**: Leaflet.js map centered on Taiwan
- **Marker System**: Color-coded circle markers by temperature
- **Charts**: Chart.js line graphs for temperature trends
- **Responsive**: Works on desktop and mobile

## Development Notes

### OpenSpec Workflow

This project uses OpenSpec for change management. See `openspec/` directory for:
- `project.md`: Project context and conventions
- `changes/`: Change proposals and implementation plans
- `specs/`: Feature specifications

### Bug Fixes

Several issues were resolved during development:
1. **CORS Error**: Fixed by creating standalone HTML with embedded data
2. **Map Click Issue**: Resolved with `map.invalidateSize()` timing fix
3. **Marker Interactions**: Simplified to use Leaflet circle markers

## License

Educational project for lecture demonstration.

## Author

Created for Lecture 13 - SQLite & Streamlit demonstration.

## Acknowledgments

- Taiwan Central Weather Administration for providing open weather data
- Streamlit team for the excellent dashboard framework
- Leaflet.js and Chart.js communities
