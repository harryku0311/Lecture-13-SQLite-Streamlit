# Change: Add Interactive Taiwan Map with Temperature Time-Series

## Why
The current dashboard uses a simple dropdown selector, which doesn't provide a geographical context for the weather data. A standalone interactive web application with a Taiwan map would:
- Provide better user experience with modern web technologies
- Allow users to visualize where locations are in Taiwan
- Enable interactive selection by clicking on map locations
- Display temperature information directly on the map
- Work independently of the Streamlit dashboard
- Be more performant and shareable

## What Changes
- Create standalone HTML page with interactive Taiwan map
- Use JavaScript for dynamic map rendering and interactivity
- Style with Tailwind CSS for modern, responsive design
- Use Leaflet.js or similar library for map visualization
- Fetch weather data from SQLite database via API or JSON export
- Display temperature information on map markers
- Show time-series temperature charts when clicking locations
- Use Chart.js or similar for temperature visualization

**New Capability**: Standalone Map Visualization - Independent HTML/JS web application

## Impact
- **Affected specs**: 
  - `map-visualization` (NEW) - Standalone web application with interactive map
- **Affected code**:
  - New file: `map.html` - Main HTML page
  - New file: `map.js` - JavaScript for map logic and interactivity
  - New file: `data_export.py` - Export weather data to JSON for web consumption
  - Modified: `dashboard.py` - Optional link to map page
- **User Experience**: 
  - Standalone, shareable map visualization
  - Modern, responsive web interface
  - Direct temperature display on map
  - Interactive charts on location selection
  - Can be used independently or embedded in dashboard
