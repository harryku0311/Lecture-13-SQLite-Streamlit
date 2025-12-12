# Change: Add Streamlit Web Dashboard

## Why
Currently, weather data is only accessible by querying the SQLite database directly, which is not user-friendly for non-technical users or for quick data visualization. A web-based dashboard would provide an accessible, interactive interface to view temperature forecasts across different locations.

## What Changes
- Add a Streamlit web application (`dashboard.py`) to visualize weather data
- Implement location dropdown selector to filter data by location
- Display temperature information (max/min) for selected location
- Add database query functions to retrieve weather data efficiently
- Update project dependencies to include Streamlit

**New Capability**: Weather Visualization - User interface for viewing weather forecasts

## Impact
- **Affected specs**: 
  - `weather-visualization` (NEW) - Web dashboard for weather data display
- **Affected code**:
  - New file: `dashboard.py` - Streamlit application
  - Modified: Project dependencies (requirements.txt or similar)
  - Existing: `sqlitedata.db` (read-only access)
- **User Experience**: 
  - Users can now view weather data through a web browser
  - Interactive location selection
  - Visual presentation of temperature data
